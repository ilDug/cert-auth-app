from core.config import get_settings
from core.paths import get_settings as get_paths
from controllers.installer import Installer
from controllers.builder import IntermediateCABuilder, RootCABuilder
from controllers.cnf import ConfigController
from models.config_model import (
    RootCertificateConfigModel,
    IntermediateCertificateConfigModel,
)

def main():
    settings = get_settings()
    paths = get_paths()

    install_pki()

    config = ConfigController(settings, paths)
    config.compile_root_config(
        RootCertificateConfigModel(
            root_ca_dir=str(paths.ROOT_CA),
            country="IT",
            state="Lombardy",
            locality="Milan",
            organization="DagTech",
            organizational_unit="IT",
            common_name="DagCA",
        )
    )

    root_ca = RootCABuilder(settings, paths)
    root_ca.build()

    config = ConfigController(settings, paths)
    config.compile_intermediate_config(
        values=IntermediateCertificateConfigModel(
            intermediate_ca_dir=str(paths.INTERMEDIATE_CA),
            country="IT",
            state="Lombardy",
            locality="Milan",
            organization="DagTech",
            organizational_unit="IT",
            common_name="DagIntermediateCA",
        )
    )
    intermediate_ca = IntermediateCABuilder(settings, paths)
    intermediate_ca.build()


def install_pki():
    settings = get_settings()
    paths = get_paths()

    # Install the PKI infrastructure
    installer = Installer(settings, paths)
    installer.cleanup()
    installer.scaffolding()
    installer.db_files()


if __name__ == "__main__":
    main()
