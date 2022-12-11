import os
from core.openssl_commands import (
    PUB_KEY_GEN,
    PRIV_KEY_PRINT,
    CERT_PRINT,
    CERT_VERIFY,
    PUB_KEY_PRINT,
)
from core.settings import CERTS_PATH, KEYS_PATH, PUBLIC_PATH, CA_CRT_PATH
import typer


class Certificate:
    def pub_key(self, subject: str):
        crt = CERTS_PATH / f"{subject}.crt"
        pub = PUBLIC_PATH / f"{subject}.pub.pem"
        key = KEYS_PATH / f"{subject}.key"

        if not pub.exists():
            cmd = PUB_KEY_GEN.substitute(crtpath=crt, pubkeypath=pub)
            os.system(cmd)

        cmd = PUB_KEY_PRINT.substitute(keypath=key)
        os.system(cmd)

    def priv_key(self, subject: str, pem: bool = False):
        key = KEYS_PATH / f"{subject}.key"

        if not key.exists():
            raise typer.Exit(
                typer.secho("chiave inesistente", fg=typer.colors.BRIGHT_RED)
            )

        if pem:
            print(key.read_text())
            return

        cmd = PRIV_KEY_PRINT.substitute(keypath=key)
        os.system(cmd)

    def cert(self, subject: str, pem: bool = False):
        crt = CERTS_PATH / f"{subject}.crt"

        if not crt.exists():
            raise typer.Exit(
                typer.secho("certificato inesistente", fg=typer.colors.BRIGHT_RED)
            )

        if pem:
            print(crt.read_text())
            return

        cmd = CERT_PRINT.substitute(crtpath=crt)
        os.system(cmd)

    def verify(self, subject: str):
        crt = CERTS_PATH / f"{subject}.crt"

        if not crt.exists():
            raise typer.Exit(
                typer.secho("certificato inesistente", fg=typer.colors.BRIGHT_RED)
            )

        cmd = CERT_VERIFY.substitute(capath=CA_CRT_PATH, crtpath=crt)
        os.system(cmd)
