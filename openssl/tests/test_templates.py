import subprocess
import tempfile
import unittest
from pathlib import Path
from string import Template


class TemplateTests(unittest.TestCase):
    def test_intermediate_and_leaf_templates_with_openssl(self):
        templates = Path(__file__).resolve().parents[1] / "configs"
        subject = {
            "country": "US",
            "state": "Test",
            "locality": "Test",
            "organization": "Example",
            "organizational_unit": "PKI",
            "common_name": "Example",
            "email": "ca@example.test",
        }
        with tempfile.TemporaryDirectory() as temporary:
            ca = Path(temporary) / "intermediate"
            for name in ("certs", "private", "newcerts"):
                (ca / name).mkdir(parents=True, exist_ok=True)
            (ca / "index.txt").touch()
            (ca / "serial").write_text("1000\n", encoding="ascii")

            def render(filename, values):
                result = Template((templates / filename).read_text(encoding="utf-8"))
                path = Path(temporary) / filename
                path.write_text(result.substitute(values), encoding="utf-8")
                return path

            def openssl(*args):
                return subprocess.run(
                    ["openssl", *map(str, args)],
                    check=True, capture_output=True, text=True,
                )

            intermediate = render(
                "intermediate-ca.cnf", subject | {"intermediate_ca_dir": str(ca)}
            )
            key = ca / "private" / "intermediate-ca.key"
            certificate = ca / "certs" / "intermediate-ca.crt"
            openssl("genpkey", "-algorithm", "RSA", "-pkeyopt",
                    "rsa_keygen_bits:2048", "-out", key)
            openssl("req", "-new", "-x509", "-config", intermediate,
                    "-extensions", "v3_intermediate_req", "-key", key,
                    "-out", certificate, "-days", "1")

            leaf = render("leaf-certificate.cnf", subject)
            leaf_key = Path(temporary) / "leaf.key"
            csr = Path(temporary) / "leaf.csr"
            openssl("genpkey", "-algorithm", "RSA", "-pkeyopt",
                    "rsa_keygen_bits:2048", "-out", leaf_key)
            openssl("req", "-new", "-config", leaf, "-key", leaf_key, "-out", csr)

            for role, san, expected in (
                ("server", "DNS:api.example.test,IP:192.0.2.10", "TLS Web Server Authentication"),
                ("client", "URI:spiffe://example.test/client", "TLS Web Client Authentication"),
            ):
                with self.subTest(role=role):
                    extensions = render(f"{role}.ext", {"san": san})
                    issued = Path(temporary) / f"{role}.crt"
                    openssl("ca", "-batch", "-config", intermediate, "-extfile",
                            extensions, "-extensions", f"{role}_cert", "-in", csr,
                            "-out", issued, "-days", "1", "-notext")
                    text = openssl("x509", "-in", issued, "-noout", "-text").stdout
                    self.assertIn(expected, text)
                    self.assertIn(san.split(",", 1)[0], text)
                    openssl("verify", "-CAfile", certificate, "-purpose",
                            f"ssl{role}", issued)


if __name__ == "__main__":
    unittest.main()
