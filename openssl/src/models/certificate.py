from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CertificateInputModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    country: str
    state: str = "*"
    locality: str = "*"
    organization: str
    organizational_unit: str = "Information and Technology"
    common_name: str

    @field_validator("*")
    @classmethod
    def validate_config_value(
        cls, value: str | int | bool | list[str]
    ) -> str | int | bool | list[str]:

        if not isinstance(value, str):
            return value

        # Ensure the value is a non-empty string without control characters (like newline, tab, etc.)
        if isinstance(value, str) and any(
            ord(char) < 32 or ord(char) == 127 for char in value
        ):
            raise ValueError("must contain no control characters")

        return (
            value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").strip()
        )


class LeafCertificateInputModel(CertificateInputModel):
    days: int = 365
    wildcard: bool = False
    alt_names: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def compile_alt_names(self) -> Self:
        """Ensure the common_name is included in the alt_names list."""
        if self.common_name not in self.alt_names:
            self.alt_names.append(self.common_name)
        return self

    @model_validator(mode="after")
    def validate_alt_names(self) -> Self:
        """Validate and update alt_names for wildcard certificates. If wildcard is True and no alt_name starts with '*.', add a wildcard entry for the common_name."""
        if self.wildcard and not any(name.startswith("*.") for name in self.alt_names):
            self.alt_names.append(f"*.{self.common_name}")
        return self


class IntermediateCertificateInputModel(CertificateInputModel):
    intermediate_ca_dir: str


class RootCertificateInputModel(CertificateInputModel):
    root_ca_dir: str
