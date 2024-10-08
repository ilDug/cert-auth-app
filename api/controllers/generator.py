import subprocess
from fastapi import HTTPException
from core.config import (
    PKI_PATH,
    KEYS_PATH,
    CONFIGS_PATH,
    REQS_PATH,
    CNF_BASE_DEFAULT,
    CONFIG_FILE,
    PASSPRHASE_PATH,
    CERTS_PATH,
    CA_CRT_PATH,
)
from core.openssl_commands import (
    PRIV_KEY_GEN,
    REQ_GEN,
    REQ_PRINT,
    CERT_GEN,
    CERT_PRINT,
    CERT_VERIFY,
    PRIV_KEY_PRINT,
)
import os


class Generator:
    def priv_key(self, subject: str):
        """genera la chiave privata a 2048 bits con il nome file passato come argomento"""

        key = KEYS_PATH / f"{subject}.key"

        cmd = PRIV_KEY_GEN.substitute(bits=2048, keypath=key)
        os.system(cmd)

        print("chiave privata generata")
        cmd = PRIV_KEY_PRINT.substitute(keypath=key)
        os.system(cmd)

    def request(self, subject: str, alt_names: list[str]):
        """genera il Certificate Signing Request. Il nome deve essere lo stesso della chiave privata generata in preventivamente."""

        # crea la configurazione
        self.create_config(subject, alt_names)

        key = KEYS_PATH / f"{subject}.key"
        config = CONFIGS_PATH / f"{subject}.cnf"
        csr = REQS_PATH / f"{subject}.csr"

        if not key.exists() or not config.exists():
            raise HTTPException(
                500, "la chiave privata o la configurazione non esistono"
            )

        cmd = REQ_GEN.substitute(configpath=config, keypath=key, csrpath=csr)
        os.system(cmd)

        print("Certificate Signing Request generata")
        cmd = REQ_PRINT.substitute(csrpath=csr)
        os.system(cmd)

    def create_config(self, subject: str, alt_names: list[str]):
        """Crea la configurazione per la creazione del CSR."""

        config = CONFIGS_PATH / f"{subject}.cnf"
        extensions = [
            "subjectAltName = @alt_names\n",
            "[alt_names]\n",
            "DNS." + str(len(alt_names) + 1) + " = " + subject + "\n",
        ]

        print(alt_names)
        for i in range(len(alt_names)):
            s = "DNS." + str(i + 1) + " = " + alt_names[i] + "\n"
            extensions.append(s)

        with open(CNF_BASE_DEFAULT, "r") as old:
            with open(config, "w") as new:
                for line in old:
                    new.write(line.replace("__subject__", subject))
                if len(alt_names) > 0:
                    new.writelines(extensions)

    def certificate(self, subject: str, alt_names: list[str], days: int = 1825):
        """crea il certificato, deve esistere la chiave privata el la richiesta CSR"""
        key = KEYS_PATH / f"{subject}.key"
        ext = CONFIGS_PATH / f"{subject}.cnf"
        csr = REQS_PATH / f"{subject}.csr"
        crt = CERTS_PATH / f"{subject}.crt"

        cmd = CERT_GEN.substitute(
            confpath=CONFIG_FILE,
            days=days,
            extpath=ext,
            passphrsepath=PASSPRHASE_PATH,
            csrpath=csr,
            crtpath=crt,
        )
        os.system(cmd)

        print("Certificato generato")
        cmd = CERT_PRINT.substitute(crtpath=crt)
        os.system(cmd)

        print("Verifica certificato")
        cmd = CERT_VERIFY.substitute(capath=CA_CRT_PATH, crtpath=crt)
        subcmd = cmd.split(" ")
        return subprocess.run(subcmd, capture_output=True, text=True).stdout
