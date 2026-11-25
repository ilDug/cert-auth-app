from core.config import Settings
from core.paths import PkiPaths
import core.openssl as cmds
from pathlib import Path
import subprocess


class CAController:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths

    def generate_private_key(
        self,
        destination: Path,
        passphrase: str,
        bits: int,
    ):
        cmd = (
            cmds.PRIVATEKEY.replace("<passphrase>", passphrase)
            .replace("<bits>", str(bits))
            .replace("<output>", str(destination))
            .split(" ")
        )
        subprocess.run(
            cmd,
            check=True,
        )

    def generate_passphrase(self, destination: Path, passphrase: str = None):
        # se la passprhase è menod di 24 caratteri , raise un errore
        if passphrase is not None and len(passphrase) < 24:
            raise ValueError("Passphrase must be at least 24 characters long.")

        if passphrase is not None:
            destination.write_text(passphrase)

        else:
            cmd = cmds.PASSPHRASE.split(" ")
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                encoding="ascii",
            )
            phrase = (
                result.stdout.strip()
                .replace("/", "_")
                .replace(".", "_")
                .replace("+", "_")
                .replace("=", "_")
            )

            destination.write_text(phrase)

        # destination.chmod(0o600)


####################################################################################
class RootController(CAController):

    def __init__(self, cnf: Settings, paths: PkiPaths):
        super().__init__(cnf, paths)

    def passphrase(self, passphrase: str = None):
        self.generate_passphrase(self.paths.ROOT_PASS, passphrase)

    def private_key(self):
        self.generate_private_key(
            destination=self.paths.ROOT_KEY,
            passphrase=self.paths.ROOT_PASS.read_text(),
            bits=4096,
        )

    


####################################################################################
class IntermediateController(CAController):

    def __init__(self, cnf: Settings, paths: PkiPaths):
        super().__init__(cnf, paths)

    def passphrase(self, passphrase: str = None):
        self.generate_passphrase(self.paths.INTERMEDIATE_PASS, passphrase)

    def private_key(self):
        self.generate_private_key(
            destination=self.paths.INTERMEDIATE_KEY,
            passphrase=self.paths.INTERMEDIATE_PASS.read_text(),
            bits=3072,
        )
