from core.config import Settings
from core.paths import PkiPaths
import shutil


class Installer:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths

    def scaffolding(self):
        """Create the necessary directory structure for the CA and issued certificates."""

        for dir in ["certs", "private", "crl", "newcerts", "conf"]:
            (self.paths.ROOT_CA / dir).mkdir(parents=True, exist_ok=True)

        for dir in ["certs", "private", "csr", "crl", "newcerts", "conf"]:
            (self.paths.INTERMEDIATE_CA / dir).mkdir(parents=True, exist_ok=True)

        # create issued directories for clients and servers
        for dir in [self.paths.CLIENTS, self.paths.SERVERS]:
            dir.mkdir(
                parents=True,
                exist_ok=True,
            )

    def cleanup(self):
        """Remove the directory structure for the CA and issued certificates."""

        if self.paths.PKI.exists():
            shutil.rmtree(self.paths.PKI, ignore_errors=True)

    def db_files(self):
        """Initialize the database files for the CA directories."""
        for ca_dir in [self.paths.ROOT_CA, self.paths.INTERMEDIATE_CA]:
            (ca_dir / "index.txt").touch(exist_ok=True)
            (ca_dir / "serial").write_text("1000", encoding="utf-8")
            (ca_dir / "crlnumber").write_text("1000", encoding="utf-8")
