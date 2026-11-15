import subprocess

from core.config import Settings
from core.openssl_commands import (
    CERT_GEN,
    CERT_PRINT,
    CERT_VERIFY,
    PRIV_KEY_GEN,
    PRIV_KEY_PRINT,
    REQ_GEN,
    REQ_PRINT,
)
from fastapi import HTTPException


class Generator:

    def __init__(self, cnf: Settings):
        self.cnf = cnf

    def priv_key(self, subject: str):
        """genera la chiave privata a 2048 bits con il nome file passato come argomento"""

        key = self.cnf.KEYS_PATH / f"{subject}.key"

        cmd = PRIV_KEY_GEN.substitute(bits=2048, keypath=key)
        subprocess.run(cmd, shell=True, check=True)

        print("chiave privata generata")
        cmd = PRIV_KEY_PRINT.substitute(keypath=key)
        subprocess.run(cmd, shell=True, check=True)

    def request(self, subject: str, alt_names: list[str]):
        """genera il Certificate Signing Request. Il nome deve essere lo stesso della chiave privata generata in preventivamente."""

        # crea la configurazione
        self.create_config(subject, alt_names)

        key = self.cnf.KEYS_PATH / f"{subject}.key"
        config = self.cnf.CONFIGS_PATH / f"{subject}.cnf"
        csr = self.cnf.REQS_PATH / f"{subject}.csr"

        if not key.exists() or not config.exists():
            raise HTTPException(
                500, "la chiave privata o la configurazione non esistono"
            )

        cmd = REQ_GEN.substitute(configpath=config, keypath=key, csrpath=csr)
        subprocess.run(cmd, shell=True, check=True)

        print("Certificate Signing Request generata")
        cmd = REQ_PRINT.substitute(csrpath=csr)
        subprocess.run(cmd, shell=True, check=True)

    def create_config(self, subject: str, alt_names: list[str]):
        """Crea la configurazione per la creazione del CSR."""

        config = self.cnf.CONFIGS_PATH / f"{subject}.cnf"
        extensions = [
            "subjectAltName = @alt_names\n",
            "[alt_names]\n",
            "DNS." + str(len(alt_names) + 1) + " = " + subject + "\n",
        ]

        print(alt_names)
        for i in range(len(alt_names)):
            s = "DNS." + str(i + 1) + " = " + alt_names[i] + "\n"
            extensions.append(s)

        with open(self.cnf.CNF_BASE_DEFAULT, "r") as old, open(config, "w") as new:
            new.writelines(line.replace("__subject__", subject) for line in old)
            if len(alt_names) > 0:
                new.writelines(extensions)

    def certificate(self, subject: str, alt_names: list[str], days: int = 1825):
        """crea il certificato, deve esistere la chiave privata el la richiesta CSR"""
        # key = self.cnf.KEYS_PATH / f"{subject}.key"
        ext = self.cnf.CONFIGS_PATH / f"{subject}.cnf"
        csr = self.cnf.REQS_PATH / f"{subject}.csr"
        crt = self.cnf.CERTS_PATH / f"{subject}.crt"

        cmd = CERT_GEN.substitute(
            confpath=self.cnf.CONFIG_FILE,
            days=days,
            extpath=ext,
            passphrsepath=self.cnf.PASSPRHASE_PATH,
            csrpath=csr,
            crtpath=crt,
        )
        subprocess.run(cmd, shell=True, check=True)

        print("Certificato generato")
        cmd = CERT_PRINT.substitute(crtpath=crt)
        subprocess.run(cmd, shell=True, check=True)

        print("Verifica certificato")
        cmd = CERT_VERIFY.substitute(capath=self.cnf.CA_CRT_PATH, crtpath=crt)
        subcmd = cmd.split(" ")
        return subprocess.run(subcmd, capture_output=True, text=True, check=True).stdout
