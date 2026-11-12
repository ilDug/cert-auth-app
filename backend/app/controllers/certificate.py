import subprocess
from fastapi import HTTPException
import core.openssl_commands as cmds
from core.config import Settings

class CertificateController:

    def __init__(self, cnf: Settings):
        self.cnf = cnf

    def list_certificates(self):
        certs = [c.name for c in self.cnf.CERTS_PATH.iterdir() if c.is_file()]
        certs = [c.split(".")[:-1] for c in certs]
        certs = [".".join(c) for c in certs]
        return certs

    def pub_key(self, subject: str):
        crt = self.cnf.CERTS_PATH / f"{subject}.crt"
        pub = self.cnf.PUBLIC_PATH / f"{subject}.pub.pem"
        key = self.cnf.KEYS_PATH / f"{subject}.key"

        if not pub.exists():
            cmd = cmds.PUB_KEY_GEN.substitute(crtpath=crt, pubkeypath=pub)
            subprocess.run(cmd, shell=True, check=True)

            cmd = cmds.PUB_KEY_PRINT.substitute(keypath=key)
            subcmd = cmd.split(" ")
            return subprocess.run(subcmd, capture_output=True, text=True).stdout
        else:
            return pub.read_text()

    def priv_key(self, subject: str, pem: bool = False):
        key = self.cnf.KEYS_PATH / f"{subject}.key"

        if not key.exists():
            raise HTTPException(404, "la chiave privata non esiste")

        if pem:
            return key.read_text()

        cmd = cmds.PRIV_KEY_PRINT.substitute(keypath=key)
        print(cmd)
        output = subprocess.getoutput(cmd)
        print(output)
        return output

    def cert(self, subject: str, pem: bool = False):
        crt = self.cnf.CERTS_PATH / f"{subject}.crt"

        if not crt.exists():
            raise HTTPException(404, "certificato inesistente")

        if pem:
            _crt = crt.read_text()
            return _crt

        cmd = cmds.CERT_PRINT.substitute(crtpath=crt)
        subcmd = cmd.split(" ")
        return subprocess.run(subcmd, capture_output=True, text=True).stdout

    def verify(self, subject: str):
        crt = self.cnf.CERTS_PATH / f"{subject}.crt"

        if not crt.exists():
            raise HTTPException(404, "certificato inesistente")

        cmd = cmds.CERT_VERIFY.substitute(capath=self.cnf.CA_CRT_PATH, crtpath=crt)
        subcmd = cmd.split(" ")
        return subprocess.run(subcmd, capture_output=True, text=True).stdout
