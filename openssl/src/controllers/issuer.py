from typing import Literal
from pathlib import Path
from controllers import cnf
from core.config import Settings
from core.paths import PkiPaths
from models import LeafCertificateInputModel
from controllers.cnf import Configurator
import core.openssl as cmds
import subprocess


class CertificateAuthority:
    def __init__(
        self,
        cnf: Settings,
        paths: PkiPaths,
        type: Literal["SERVER", "CLIENT"] = "SERVER",
    ):
        self.settings = cnf
        self.paths = paths
        self.type = type
        self.configurator = Configurator(cnf, paths)

    def issue_certificate(self, cnf: LeafCertificateInputModel):
        # 0 - Creazione della working directory per il certificato
        wd = self._mk_working_dir(cnf)
        # 1 - generare la configurazione a partire dal template
        cnf_path = self._compile_config(self.configurator, cnf, wd)
        # 2 - generare extensioni per il certificato (alt_names, ecc.)
        ext_path = self._compile_extensions(self.configurator, cnf, wd)
        # 3 - generare la chiave privata per il certificato (senza passphrase)
        key_path = self._generate_private_key(wd, cnf.common_name)
        # 4 - generare la richiesta di firma del certificato (CSR)
        csr_path = self._issue_csr(wd, cnf.common_name, cnf_path, key_path)
        # 5 - firmare la richiesta con l'autorità di certificazione appropriata ed emettere il certificato
        crt_path = self._sign_certificate(wd, cnf.common_name, csr_path, ext_path)
        # 6 - emettere il la chain del certificato assieme ai certificati intermedi
        chain_path = self._chain_certificate(wd, cnf.common_name, crt_path)

    def _mk_working_dir(self, model: LeafCertificateInputModel) -> Path:
        wd = (
            self.paths.SERVERS if self.type == "SERVER" else self.paths.CLIENTS
        ) / model.common_name

        wd.mkdir(parents=True, exist_ok=True)
        return wd

    def _compile_config(
        self, compiler: Configurator, model: LeafCertificateInputModel, wd: Path
    ) -> Path:
        return compiler.compile_leaf_config(model, output_dir=wd)

    def _compile_extensions(
        self, compiler: Configurator, model: LeafCertificateInputModel, wd: Path
    ) -> Path:
        if self.type == "SERVER":
            return compiler.compile_server_extensions(model, output_dir=wd)
        else:
            return compiler.compile_client_extensions(model, output_dir=wd)

    def _generate_private_key(self, wd: Path, name: str, bits: int = 2048) -> Path:
        key_path = wd / f"{name}.key"
        values = {"bits": bits, "output": key_path}
        cmd = cmds.parse_cmd(cmds.KEY_GEN, values)
        subprocess.run(cmd, check=True)
        return key_path

    def _issue_csr(self, wd: Path, name: str, cnf_path: Path, key_path: Path) -> Path:
        csr_path = wd / f"{name}.csr"
        values = {"configpath": cnf_path, "keypath": key_path, "csrpath": csr_path}

        cmd = cmds.parse_cmd(cmds.CSR_GEN, values)
        subprocess.run(cmd, check=True)

        cmd = cmds.parse_cmd(cmds.CSR_VERIFY, {"csrpath": csr_path})
        subprocess.run(cmd, check=True)
        return csr_path

    def _sign_certificate(
        self,
        wd: Path,
        name: str,
        csr_path: Path,
        ext_path: Path,
        days: int | None = None,
    ) -> Path:
        output_path: Path = wd / f"{name}.crt"
        values = {
            "csrpath": csr_path,
            "extpath": ext_path,
            "output": output_path,
            "intermediateconfigpath": self.paths.INTERMEDIATE_CONF,
            "intermediatepassphrasepath": self.paths.INTERMEDIATE_PASS,
        }
        if days is not None:
            values["days"] = days

        if self.type == "SERVER":
            cmd = cmds.parse_cmd(cmds.CRT_SIGN_SERVER, values)
        elif self.type == "CLIENT":
            cmd = cmds.parse_cmd(cmds.CRT_SIGN_CLIENT, values)
        else:
            raise ValueError(f"Unsupported certificate type: {self.type}")
        subprocess.run(cmd, check=True)
        return output_path

    def _chain_certificate(self, wd: Path, name: str, crt_path: Path) -> Path:
        chain_path = wd / f"{name}.fullchain.crt"
        with open(chain_path, "wb") as chain_file:
            with open(crt_path, "rb") as crt_file:
                chain_file.write(crt_file.read())
            with open(self.paths.INTERMEDIATE_CRT, "rb") as inter_file:
                chain_file.write(inter_file.read())
        return chain_path
