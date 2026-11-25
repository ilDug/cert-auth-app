import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from controllers.cnf import ConfigController
from core.config import Settings
from core.paths import PkiPaths
from models.config_model import RootCertificateConfigModel


class RootConfigTests(unittest.TestCase):
    def test_compiled_config_creates_root_with_literal_subject(self):
        template = Path(__file__).resolve().parents[1] / "configs" / "root-ca.cnf"
        original = template.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'root $dir "test"'
            root.mkdir()
            paths = PkiPaths(
                MODE="development",
                ROOT_CA=root,
                ROOT_CONF=root / "root-ca.cnf",
                CONFIG_ROOT_TEMPLATE=template,
            )
            controller = ConfigController(Settings(MODE="development"), paths)
            name = 'Example $name # "Root" \\ CA'
            config = controller.compile_root_config(RootCertificateConfigModel(
                root_ca_dir=str(root),
                country="US",
                state="Test State",
                locality="Test City",
                organization="Example",
                organizational_unit="PKI",
                common_name=name,
            ))
            self.assertEqual(config, paths.ROOT_CONF)
            self.assertEqual(original, template.read_text(encoding="utf-8"))
            compiled = config.read_text(encoding="utf-8")
            self.assertNotIn("${ENV::", compiled)
            self.assertIn("certs             = $dir/certs", compiled)
            self.assertIn('countryName             = "US"', compiled)

            key = root / "key.pem"
            cert = root / "cert.pem"
            subprocess.run(
                ["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt",
                 "rsa_keygen_bits:2048", "-out", str(key)],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["openssl", "req", "-new", "-x509", "-config", str(config),
                 "-key", str(key), "-out", str(cert), "-days", "1"],
                check=True, capture_output=True,
            )
            subject = subprocess.run(
                ["openssl", "x509", "-in", str(cert), "-noout",
                 "-subject", "-nameopt", "multiline"],
                check=True, capture_output=True, text=True,
            ).stdout
            self.assertIn(name.replace("\\", "\\\\"), subject)
            for directory in ("certs", "private", "newcerts"):
                (root / directory).mkdir()
            shutil.copyfile(key, root / "private" / "root.key")
            shutil.copyfile(cert, root / "certs" / "root.crt")
            (root / "index.txt").touch()
            (root / "serial").write_text("1000\n", encoding="ascii")
            csr = root / "intermediate.csr"
            subprocess.run(
                ["openssl", "req", "-new", "-key", str(key),
                 "-subj", "/C=US/O=Example/CN=Intermediate", "-out", str(csr)],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["openssl", "ca", "-batch", "-config", str(config),
                 "-extensions", "v3_intermediate_ca", "-in", str(csr),
                 "-out", str(root / "intermediate.crt"), "-days", "1"],
                check=True, capture_output=True,
            )

    def test_rejects_configuration_injection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = PkiPaths(MODE="development", ROOT_CA=root, ROOT_CONF=root / "root.cnf")
            controller = ConfigController(Settings(MODE="development"), paths)
            with self.assertRaises(ValueError):
                controller.compile_root_config(RootCertificateConfigModel(
                    root_ca_dir=str(root),
                    country="US",
                    state="Test",
                    locality="Test",
                    organization="Example\nkeyUsage = anything",
                    organizational_unit="PKI",
                    common_name="Root",
                ))
            self.assertFalse(paths.ROOT_CONF.exists())


if __name__ == "__main__":
    unittest.main()
