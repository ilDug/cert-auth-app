from icecream import ic
from core.config import Settings
from core.paths import PkiPaths
import core.openssl as cmds
from pathlib import Path
import subprocess


class CABuilder:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths

    def generate_private_key(
        self,
        destination: Path,
        passphrase: str,
        bits: int,
    ):
        values = {
            "passphrase": passphrase,
            "bits": str(bits),
            "output": str(destination),
        }
        cmd = cmds.parse_cmd(cmds.PRIVATEKEY_GEN, values)
        subprocess.run(cmd, check=True)

    def set_passphrase(self, destination: Path, passphrase: str = None):
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

    # def display_privatekey_details(self, keypath: Path, passphrasepath: Path) -> str:
    #     cmd = cmds.parse_cmd(
    #         cmds.PRIVATEKEY_SHOW,
    #         {"keypath": keypath, "passphrasepath": passphrasepath},
    #     )
    #     result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    #     ic(result.stdout)
    #     return result.stdout

    # def show_publickey(self, crtpath: Path) -> str:
    #     cmd = cmds.parse_cmd(cmds.PUBLICKEY_FROM_CRT_SHOW, {"crtpath": crtpath})
    #     result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    #     ic(result.stdout)
    #     return result.stdout

    # def show_certificate(self, crtpath: Path, pem: bool = False) -> str:
    # if pem:
    #     crt = crtpath.read_text()
    #     print(crt)
    #     return crt

    # cmd = cmds.parse_cmd(cmds.CRT_SHOW, {"crtpath": crtpath})
    # crt = subprocess.run(cmd, check=True, capture_output=True, text=True)
    # ic(crt.stdout)
    # return crt.stdout


####################################################################################
class RootCABuilder(CABuilder):

    def __init__(self, cnf: Settings, paths: PkiPaths):
        super().__init__(cnf, paths)

    def build(self):
        self.set_passphrase()
        self.generate_private_key()
        self.issue_selfsigned_root_certificate()

    def set_passphrase(self, passphrase: str = None):
        super().set_passphrase(self.paths.ROOT_PASS, passphrase)

    def generate_private_key(self):
        super().generate_private_key(
            destination=self.paths.ROOT_KEY,
            passphrase=self.paths.ROOT_PASS.read_text(),
            bits=4096,
        )

    def issue_selfsigned_root_certificate(
        self,
        passphrasepath: Path | None = None,
        cakeypath: Path | None = None,
        cacrtpath: Path | None = None,
    ):
        if passphrasepath is None:
            passphrasepath = self.paths.ROOT_PASS
        if cakeypath is None:
            cakeypath = self.paths.ROOT_KEY
        if cacrtpath is None:
            cacrtpath = self.paths.ROOT_CRT

        values = {
            "configpath": self.paths.ROOT_CONF,
            "passphrasepath": passphrasepath,
            "cakeypath": cakeypath,
            "cacrtpath": cacrtpath,
        }
        cmd = cmds.parse_cmd(cmds.ROOT_CRT_GEN, values)

        subprocess.run(cmd, check=True)

    # def show_certificate(self, pem: bool = False):
    #     return super().show_certificate(self.paths.ROOT_CRT, pem=pem)

    # def display_privatekey_details(self):
    #     return super().display_privatekey_details(
    #         self.paths.ROOT_KEY, self.paths.ROOT_PASS
    #     )

    # def show_publickey(self) -> str:
    #     return super().show_publickey(self.paths.ROOT_CRT)


####################################################################################
class IntermediateCABuilder(CABuilder):

    def __init__(self, cnf: Settings, paths: PkiPaths):
        super().__init__(cnf, paths)

    def build(self):
        self.set_passphrase()
        self.generate_private_key()
        self.issue_intermediate_csr()
        self.issue_intermediate_certificate()
        self.verify_intermediate_certificate()

    def set_passphrase(self, passphrase: str = None):
        super().set_passphrase(self.paths.INTERMEDIATE_PASS, passphrase)

    def generate_private_key(self):
        super().generate_private_key(
            destination=self.paths.INTERMEDIATE_KEY,
            passphrase=self.paths.INTERMEDIATE_PASS.read_text(),
            bits=3072,
        )

    def issue_intermediate_csr(self):
        ic("Issuing intermediate CSR")
        values = {
            "intermediateconfigpath": self.paths.INTERMEDIATE_CONF,
            "passphrasepath": self.paths.INTERMEDIATE_PASS,
            "intermediatekeypath": self.paths.INTERMEDIATE_KEY,
            "csrpath": self.paths.INTERMEDIATE_CSR,
        }
        # genera la richiesta di certificato intermedio (CSR)
        cmd = cmds.parse_cmd(cmds.INTERMEDIATE_CSR_GEN, values)
        subprocess.run(cmd, check=True)
        # verifica la richiesta di certificato intermedio (CSR)
        cmd = cmds.parse_cmd(
            cmds.INTERMEDIATE_CSR_VERIFY, {"csrpath": self.paths.INTERMEDIATE_CSR}
        )
        subprocess.run(cmd, check=True)

    def issue_intermediate_certificate(self):
        values = {
            "rootconfigpath": self.paths.ROOT_CONF,
            "csrpath": self.paths.INTERMEDIATE_CSR,
            "output": self.paths.INTERMEDIATE_CRT,
            "passphrasepath": self.paths.ROOT_PASS,
        }
        cmd = cmds.parse_cmd(cmds.ROOT_SIGN_INTERMEDIATE_CRT, values)
        subprocess.run(cmd, check=True)

    def verify_intermediate_certificate(self):
        ic("Verifying intermediate certificate")
        values = {
            "crtpath": self.paths.INTERMEDIATE_CRT,
            "CAcrtpath": self.paths.ROOT_CRT,
        }
        cmd = cmds.parse_cmd(cmds.CRT_VERIFY, values)
        subprocess.run(cmd, check=True)

    # def display_privatekey_details(self):
    #     return super().display_privatekey_details(
    #         self.paths.INTERMEDIATE_KEY, self.paths.INTERMEDIATE_PASS
    #     )

    # def show_publickey(self) -> str:
    #     return super().show_publickey(self.paths.INTERMEDIATE_CRT)

    # def show_certificate(self, pem: bool = False):
    #     return super().show_certificate(self.paths.INTERMEDIATE_CRT, pem=pem)
