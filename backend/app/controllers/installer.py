import shutil
import subprocess
from pathlib import Path
from core.openssl_commands import CA_CRT_GEN, CA_KEY_GEN, CA_PUB_KEY_GEN, PASSPHRASE_GEN
from core.config import Settings

class Installer:

    def __init__(self, cnf: Settings) -> None:
        self.cnf = cnf

    dirs = [
        "certs",
        "crl",
        "newcerts",
        "private",
        "reqs",
        "configs",
        "public",
        "workshop",
    ]

    ######################################################################################

    def clean_structure(self):
        """pulisce la cartella della PKI"""
        if self.cnf.PKI.exists():
            shutil.rmtree(str(self.cnf.PKI), ignore_errors=True)

    ######################################################################################

    def scaffolding(self):
        self.cnf.PKI.mkdir(0o777, exist_ok=True)

        for p in [self.cnf.PKI / d for d in self.dirs]:
            p.mkdir(0o777, exist_ok=True)
            p.chmod(0o777)

        Path(self.cnf.PKI / "index.txt").write_text("")
        Path(self.cnf.PKI / "serial").write_text("1000")
        Path(self.cnf.PKI / "crlnumber").write_text("1000")

        # compila i file di opzioni
        with open(self.cnf.CNF_BASE_OPENSSL) as base_conf_file:
            with open(self.cnf.CONFIG_FILE, "w") as cnf:
                for line in base_conf_file:
                    cnf.write(line.replace("__pki_dir__", str(self.cnf.PKI.as_posix())))

    ######################################################################################

    def generate_passphrase(self, length: int = 24):
        cmd = PASSPHRASE_GEN.substitute(
            passphrasepath=self.cnf.PASSPRHASE_PATH.as_posix(), length=24
        )
        print(cmd)

        subprocess.run(cmd, shell=True, check=True)
        self.cnf.PASSPRHASE_PATH.chmod(400)

    ######################################################################################

    def create_ca_key(self):
        cmd = CA_KEY_GEN.substitute(
            passphrasepath=self.cnf.PASSPRHASE_PATH.as_posix(),
            cakeypath=self.cnf.CA_KEY_PATH.as_posix(),
        )
        subprocess.run(cmd, shell=True, check=True)
        self.cnf.CA_KEY_PATH.chmod(400)

    ######################################################################################

    def create_ca_crt(self):
        cmd = CA_CRT_GEN.substitute(
            configpath=self.cnf.CONFIG_FILE,
            passphrasepath=self.cnf.PASSPRHASE_PATH.as_posix(),
            cakeypath=self.cnf.CA_KEY_PATH.as_posix(),
            cacrtpath=self.cnf.CA_CRT_PATH.as_posix(),
            days=self.cnf.CA_DURATION,
        )
        print(cmd)
        subprocess.run(cmd, shell=True, check=True)
        self.cnf.CA_CRT_PATH.chmod(444)

    ######################################################################################

    def generate_public_key(self):
        cmd = CA_PUB_KEY_GEN.substitute(
            cacrtpath=self.cnf.CA_CRT_PATH.as_posix(),
            pubkeypath=self.cnf.CA_PUB_PATH.as_posix(),
        )
        subprocess.run(cmd, shell=True, check=True)
        print(self.cnf.CA_PUB_PATH.as_posix())

    ######################################################################################

    def verify_ca_crt(self):
        subprocess.run(
            f"openssl x509 -noout -text -in {self.cnf.CA_CRT_PATH.as_posix()}",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"openssl rsa -check -in {self.cnf.CA_KEY_PATH.as_posix()}  -noout -text -passin file:{self.cnf.PASSPRHASE_PATH.as_posix()}",
            shell=True,
            check=True,
        )
