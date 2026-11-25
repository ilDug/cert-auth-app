from pydantic import BaseModel, ConfigDict, field_validator


class CertificateConfigModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    country: str
    state: str
    locality: str
    organization: str
    organizational_unit: str
    common_name: str

    @field_validator("*")
    @classmethod
    def validate_config_value(cls, value: str) -> str:
        if not value or any(ord(char) < 32 or ord(char) == 127 for char in value):
            raise ValueError("must be non-empty and contain no control characters")
        return value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$")


class LeafCertificateConfigModel(CertificateConfigModel):
    pass


class IntermediateCertificateConfigModel(CertificateConfigModel):
    intermediate_ca_dir: str


class RootCertificateConfigModel(CertificateConfigModel):
    root_ca_dir: str
