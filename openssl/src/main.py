from core.config import get_settings
from core.paths import get_settings as get_paths
from controllers.installer import Installer
from controllers.builder import IntermediateCABuilder, RootCABuilder
from controllers.cnf import ConfigController
from models.config_model import (
    RootCertificateConfigModel,
    IntermediateCertificateConfigModel,
    LeafCertificateConfigModel,
)
from controllers.issuer import CertificateAuthority

def main():
    settings = get_settings()
    paths = get_paths()

    cert_config = LeafCertificateConfigModel(
        common_name="dag.com",
        country="IT",
        state="Lombardy",
        locality="Milan",
        organization="DagTech",
        organizational_unit="IT",
        days=20,
        wildcard=True,
        alt_names=["dag.com", "www.dag.com"],
    )
    ca = CertificateAuthority(settings, paths)
    ca.issue_certificate(cert_config)

    # install_pki(settings, paths)
    # build_root_ca(settings, paths)
    # build_intermediate_ca(settings, paths)


###############################################################################
def build_intermediate_ca(settings, paths):
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


def build_root_ca(settings, paths):
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


def install_pki(settings, paths):
    # Install the PKI infrastructure
    installer = Installer(settings, paths)
    installer.cleanup()
    installer.scaffolding()
    installer.db_files()


if __name__ == "__main__":
    main()
