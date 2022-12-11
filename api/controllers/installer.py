import shutil
import os
from pathlib import Path
import subprocess
from core.openssl_commands import CA_CRT_GEN, CA_KEY_GEN, CA_PUB_KEY_GEN, PASSPHRASE_GEN
from core.settings import (
    CA_CRT_PATH,
    CA_KEY_PATH,
    CA_PUB_PATH,
    CNF_BASE_OPENSSL,
    CONFIG_FILE,
    CONFIGS_PATH,
    PASSPRHASE_PATH,
    PKI_PATH,
)


class Installer:
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
        if PKI_PATH.exists():
            shutil.rmtree(str(PKI_PATH), ignore_errors=True)

    ######################################################################################

    def scaffolding(self):
        PKI_PATH.mkdir(770, exist_ok=True)

        for p in [PKI_PATH / d for d in self.dirs]:
            p.mkdir(770, exist_ok=True)

        Path(PKI_PATH / "index.txt").write_text("")
        Path(PKI_PATH / "serial").write_text("1000")
        Path(PKI_PATH / "crlnumber").write_text("1000")

        # compila i file di opzioni
        with open(CNF_BASE_OPENSSL) as base_conf_file:
            with open(CONFIG_FILE, "w") as cnf:
                for line in base_conf_file:
                    cnf.write(line.replace("__pki_dir__", str(PKI_PATH.as_posix())))

    ######################################################################################

    def generate_passphrase(length: int = 24):
        cmd = PASSPHRASE_GEN.substitute(
            passphrasepath=PASSPRHASE_PATH.as_posix(), length=24
        )
        print(cmd)

        os.system(cmd)
        PASSPRHASE_PATH.chmod(400)

    ######################################################################################

    def create_ca_key(self):
        cmd = CA_KEY_GEN.substitute(
            passphrasepath=PASSPRHASE_PATH, cakeypath=CA_KEY_PATH
        )
        os.system(cmd)
        CA_KEY_PATH.chmod(400)

    ######################################################################################

    def create_ca_crt(self):
        cmd = CA_CRT_GEN.substitute(
            configpath=CONFIG_FILE,
            passphrasepath=PASSPRHASE_PATH,
            cakeypath=CA_KEY_PATH,
            cacrtpath=CA_CRT_PATH,
            days=3650,
        )
        os.system(cmd)
        CA_CRT_PATH.chmod(444)

    ######################################################################################

    def generate_public_key(self):
        cmd = CA_PUB_KEY_GEN.substitute(cacrtpath=CA_CRT_PATH, pubkeypath=CA_PUB_PATH)
        os.system(cmd)
        print(CA_PUB_PATH)

    ######################################################################################

    def verify_ca_crt(self):
        os.system(f"openssl x509 -noout -text -in {CA_CRT_PATH}")
        os.system(
            f"openssl rsa -check -in {CA_KEY_PATH}  -noout -text -passin file:{PASSPRHASE_PATH}"
        )
