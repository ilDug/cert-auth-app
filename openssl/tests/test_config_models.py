import subprocess
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from controllers.configs import ConfigController
from core.config import Settings
from core.paths import PkiPaths
from models.config_model import (
    IntermediateCertificateConfigModel,
    LeafCertificateConfigModel,
    RootCertificateConfigModel,
)

SUBJECT = {
    "country": "US",
    "state": "Test",
    "locality": "Test",
    "organization": "Example",
    "organizational_unit": "PKI",
    "common_name": 'Example $name "CA" \\ test',
}


class ConfigModelTests(unittest.TestCase):
    def test_leaf_alt_names_include_common_name(self):
        model = LeafCertificateConfigModel(**SUBJECT)
        self.assertEqual(model.alt_names, [model.common_name])

        model = LeafCertificateConfigModel(
            **(SUBJECT | {"alt_names": ["DNS:example.test", "DNS:www.example.test"]})
        )
        self.assertEqual(
            model.alt_names,
            ["DNS:example.test", "DNS:www.example.test", model.common_name],
        )

        model = LeafCertificateConfigModel(
            **(SUBJECT | {"alt_names": [SUBJECT["common_name"]]})
        )
        self.assertEqual(model.alt_names, [model.common_name])

        model.alt_names = ["DNS:new.example.test"]
        self.assertIn(model.common_name, model.alt_names)

    def test_all_models_validate_and_escape_fields(self):
        cases = (
            (RootCertificateConfigModel, {"root_ca_dir": "/tmp/root"}),
            (IntermediateCertificateConfigModel, {"intermediate_ca_dir": "/tmp/ca"}),
            (LeafCertificateConfigModel, {}),
        )
        for model_type, extra in cases:
            with self.subTest(model=model_type.__name__):
                model = model_type(**(SUBJECT | extra))
                self.assertEqual(
                    model.common_name, 'Example \\$name \\"CA\\" \\\\ test'
                )
                for bad_value in ("", "bad\nvalue", "bad\x7fvalue"):
                    with self.assertRaises(ValidationError):
                        model_type(**(SUBJECT | extra | {"common_name": bad_value}))
                with self.assertRaises(ValidationError):
                    model.common_name = "bad\nvalue"

        with self.assertRaises(ValidationError):
            RootCertificateConfigModel(**(SUBJECT | {"root_ca_dir": "/tmp/\nroot"}))
        with self.assertRaises(ValidationError):
            IntermediateCertificateConfigModel(
                **(SUBJECT | {"intermediate_ca_dir": ""})
            )

    def test_controllers_render_validated_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / 'root $test "ca"'
            intermediate = base / 'intermediate $test "ca"'
            root.mkdir()
            intermediate.mkdir()
            paths = PkiPaths(
                MODE="development",
                ROOT_CA=root,
                ROOT_CONF=root / "root.cnf",
                INTERMEDIATE_CA=intermediate,
                INTERMEDIATE_CONF=intermediate / "intermediate.cnf",
                LEAF_CONF=base / "leaf.cnf",
            )
            controller = ConfigController(Settings(MODE="development"), paths)
            root_model = RootCertificateConfigModel(
                **(SUBJECT | {"root_ca_dir": str(root)})
            )
            compiled = (
                controller.compile_root_config(root_model),
                controller.compile_intermediate_config(**SUBJECT),
                controller.compile_leaf_config(**SUBJECT),
            )
            for path in compiled:
                text = path.read_text(encoding="utf-8")
                self.assertIn(
                    'commonName              = "Example \\$name \\"CA\\" \\\\ test"',
                    text,
                )
            self.assertIn("certs             = $dir/certs", compiled[0].read_text())
            self.assertIn("certs             = $dir/certs", compiled[1].read_text())

            key = base / "root.key"
            cert = base / "root.crt"
            subprocess.run(
                [
                    "openssl",
                    "genpkey",
                    "-algorithm",
                    "RSA",
                    "-pkeyopt",
                    "rsa_keygen_bits:2048",
                    "-out",
                    str(key),
                ],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "openssl",
                    "req",
                    "-new",
                    "-x509",
                    "-config",
                    str(compiled[0]),
                    "-subj",
                    "/CN=Test",
                    "-key",
                    str(key),
                    "-out",
                    str(cert),
                    "-days",
                    "1",
                ],
                check=True,
                capture_output=True,
            )


if __name__ == "__main__":
    unittest.main()
