from core.paths import PkiPaths
from core.config import Settings
from pathlib import Path
from string import Template
from models import (
    RootCertificateConfigModel,
    IntermediateCertificateConfigModel,
    LeafCertificateConfigModel,
)


class Configurator:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths

    def compile_root_config(self, values: RootCertificateConfigModel) -> Path:
        template = self.paths.CONFIG_ROOT_TEMPLATE.read_text(encoding="utf-8")
        config = Template(template).substitute(values.model_dump())
        config_path = self.paths.ROOT_CONF
        config_path.write_text(config, encoding="utf-8")
        return config_path

    def compile_intermediate_config(
        self, values: IntermediateCertificateConfigModel
    ) -> Path:

        template = self.paths.CONFIG_INTERMEDIATE_TEMPLATE.read_text(encoding="utf-8")
        config = Template(template).substitute(values.model_dump())
        config_path = self.paths.INTERMEDIATE_CONF
        config_path.write_text(config, encoding="utf-8")
        return config_path

    def compile_leaf_config(
        self, values: LeafCertificateConfigModel, output_dir: Path
    ) -> Path:

        template = self.paths.CONFIG_LEAF_TEMPLATE.read_text(encoding="utf-8")
        config = Template(template).substitute(
            {
                "country": values.country,
                "state": values.state,
                "locality": values.locality,
                "organization": values.organization,
                "organizational_unit": values.organizational_unit,
                "common_name": values.common_name,
            }
        )
        config_path = output_dir / f"{values.common_name}.cnf"
        config_path.write_text(config, encoding="utf-8")
        return config_path

    def compile_server_extensions(
        self, values: LeafCertificateConfigModel, output_dir: Path
    ) -> Path:
        template = self.paths.EXT_SERVER_TEMPLATE.read_text(encoding="utf-8")
        san = ",".join(f"DNS:{name}" for name in values.alt_names)
        ext = Template(template).substitute({"san": san})
        ext_path = output_dir / f"{values.common_name}.ext"
        ext_path.write_text(ext, encoding="utf-8")
        return ext_path

    def compile_client_extensions(
        self, values: LeafCertificateConfigModel, output_dir: Path
    ) -> Path:
        template = self.paths.EXT_CLIENT_TEMPLATE.read_text(encoding="utf-8")
        san = ",".join(f"DNS:{name}" for name in values.alt_names)
        ext = Template(template).substitute({"san": san})
        ext_path = output_dir / f"{values.common_name}.ext"
        ext_path.write_text(ext, encoding="utf-8")
        return ext_path
