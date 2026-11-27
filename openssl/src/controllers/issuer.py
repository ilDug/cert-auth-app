from typing import Literal
from pathlib import Path
from controllers import cnf
from core.config import Settings
from core.paths import PkiPaths
from models.config_model import LeafCertificateConfigModel
from controllers.cnf import ConfigController
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
        self.config_ctrl = ConfigController(cnf, paths)

    def issue_certificate(self, cnf: LeafCertificateConfigModel):
        # 0 - Creazione della working directory per il certificato
        self.wd = self._mk_working_dir(cnf)
        # 1 - generare la configurazione a partire dal template
        self.cnf_path = self._compile_config(cnf, self.wd)
        # 2 - generare extensioni per il certificato (alt_names, ecc.)
        self.ext_path = self._compile_extensions(cnf, self.wd)
        # 3 - generare la chiave privata per il certificato (senza passphrase)
        self.key_path = self._generate_private_key(cnf.common_name)
        # 4 - generare la richiesta di firma del certificato (CSR)
        self.csr_path = self._issue_csr(cnf, self.cnf_path, self.key_path)
        # 5 - firmare la richiesta con l'autorità di certificazione appropriata ed emettere il certificato
        self.crt_path = self._sign_certificate(cnf, self.csr_path, self.ext_path)
        # 6 - emettere il la chain del certificato assieme ai certificati intermedi
        self.chain_path = self._chain_certificate(self.crt_path, cnf)

    def _mk_working_dir(self, model: LeafCertificateConfigModel) -> Path:
        wd = (
            self.paths.SERVERS if self.type == "SERVER" else self.paths.CLIENTS
        ) / model.common_name

        wd.mkdir(parents=True, exist_ok=True)
        return wd

    def _compile_config(self, model: LeafCertificateConfigModel, wd: Path) -> Path:
        return self.config_ctrl.compile_leaf_config(model, output_dir=wd)

    def _compile_extensions(self, model: LeafCertificateConfigModel, wd: Path) -> Path:
        if self.type == "SERVER":
            return self.config_ctrl.compile_server_extensions(model, output_dir=wd)
        else:
            return self.config_ctrl.compile_client_extensions(model, output_dir=wd)

    def _generate_private_key(self, name: str, bits: int = 2048) -> Path:
        key_path = self.wd / f"{name}.key"
        values = {"bits": bits, "output": key_path}
        cmd = cmds.parse_cmd(cmds.KEY_GEN, values)
        subprocess.run(cmd, check=True)
        return key_path

    def _issue_csr(
        self, cnf: LeafCertificateConfigModel, cnf_path: Path, key_path: Path
    ) -> Path:
        csr_path = self.wd / f"{cnf.common_name}.csr"
        values = {"configpath": cnf_path, "keypath": key_path, "csrpath": csr_path}

        cmd = cmds.parse_cmd(cmds.CSR_GEN, values)
        subprocess.run(cmd, check=True)

        cmd = cmds.parse_cmd(cmds.CSR_VERIFY, {"csrpath": csr_path})
        subprocess.run(cmd, check=True)
        return csr_path

    def _sign_certificate(
        self,
        cnf: LeafCertificateConfigModel,
        csr_path: Path,
        ext_path: Path,
    ) -> Path:
        output_path: Path = self.wd / f"{cnf.common_name}.crt"
        values = {
            "csrpath": csr_path,
            "extpath": ext_path,
            "output": output_path,
            "days": cnf.days,
            "intermediateconfigpath": self.paths.INTERMEDIATE_CONF,
            "intermediatepassphrasepath": self.paths.INTERMEDIATE_PASS,
        }
        if self.type == "SERVER":
            cmd = cmds.parse_cmd(cmds.CRT_SIGN_SERVER, values)
        elif self.type == "CLIENT":
            cmd = cmds.parse_cmd(cmds.CRT_SIGN_CLIENT, values)
        subprocess.run(cmd, check=True)
        return output_path

    def _chain_certificate(
        self, crt_path: Path, cnf: LeafCertificateConfigModel
    ) -> Path:
        chain_path = self.wd / f"{cnf.common_name}.fullchain.crt"
        with open(chain_path, "wb") as chain_file:
            with open(crt_path, "rb") as crt_file:
                chain_file.write(crt_file.read())
            with open(self.paths.INTERMEDIATE_CRT, "rb") as inter_file:
                chain_file.write(inter_file.read())
        return chain_path
