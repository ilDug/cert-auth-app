import os
import subprocess

from fastapi import HTTPException
from core.openssl_commands import (
    PUB_KEY_GEN,
    PRIV_KEY_PRINT,
    CERT_PRINT,
    CERT_VERIFY,
    PUB_KEY_PRINT,
)
from config import CERTS_PATH, KEYS_PATH, PUBLIC_PATH, CA_CRT_PATH


class Certificate:
    def list_certificates(self):
        certs = [c.name for c in CERTS_PATH.iterdir() if c.is_file()]
        certs = [ c.split(".")[:-1] for c in certs]
        certs = [ ".".join(c) for c in certs]
        return certs

    def pub_key(self, subject: str):
        crt = CERTS_PATH / f"{subject}.crt"
        pub = PUBLIC_PATH / f"{subject}.pub.pem"
        key = KEYS_PATH / f"{subject}.key"

        if not pub.exists():
            cmd = PUB_KEY_GEN.substitute(crtpath=crt, pubkeypath=pub)
            os.system(cmd)

            cmd = PUB_KEY_PRINT.substitute(keypath=key)
            subcmd = cmd.split(" ")
            return subprocess.run(subcmd, capture_output=True, text=True).stdout
        else:
            return pub.read_text()

    def priv_key(self, subject: str, pem: bool = False):
        key = KEYS_PATH / f"{subject}.key"

        if not key.exists():
            raise HTTPException(404, "la chiave privata non esiste")

        if pem:
            return key.read_text()

        cmd = PRIV_KEY_PRINT.substitute(keypath=key)
        print(cmd)
        output = subprocess.getoutput(cmd)
        print(output)
        return output

    def cert(self, subject: str, pem: bool = False):
        crt = CERTS_PATH / f"{subject}.crt"

        if not crt.exists():
            raise HTTPException(404, "certificato inesistente")

        if pem:
            _crt = crt.read_text()
            return _crt

        cmd = CERT_PRINT.substitute(crtpath=crt)
        subcmd = cmd.split(" ")

        # os.system(cmd)
        # result = subprocess.run(subcmd, stdout=subprocess.PIPE)
        # return result.stdout.decode("utf-8")
        return subprocess.run(subcmd, capture_output=True, text=True).stdout

    def verify(self, subject: str):
        crt = CERTS_PATH / f"{subject}.crt"

        if not crt.exists():
            raise HTTPException(404, "certificato inesistente")

        cmd = CERT_VERIFY.substitute(capath=CA_CRT_PATH, crtpath=crt)
        subcmd = cmd.split(" ")
        return subprocess.run(subcmd, capture_output=True, text=True).stdout
