from core.paths import PkiPaths
from core.config import Settings
from pathlib import Path
from string import Template

class ConfigController:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths

    def compile_root_config(
        self,
        *,
        country: str,
        state: str,
        locality: str,
        organization: str,
        organizational_unit: str,
        common_name: str,
    ) -> Path:
        values = {
            "root_ca_dir": str(self.paths.ROOT_CA),
            "country": country,
            "state": state,
            "locality": locality,
            "organization": organization,
            "organizational_unit": organizational_unit,
            "common_name": common_name,
        }
        # sanitize input values to prevent control characters and escape special characters for the template
        for name, value in values.items():
            if not value or any(ord(char) < 32 or ord(char) == 127 for char in value):
                raise ValueError(
                    f"{name} must be non-empty and contain no control characters"
                )
            values[name] = (
                value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$")
            )

        template = self.paths.CONFIG_ROOT_TEMPLATE.read_text(encoding="utf-8")
        config = Template(template).substitute(values)
        config_path = self.paths.ROOT_CONF
        config_path.write_text(config, encoding="utf-8")
        return config_path
