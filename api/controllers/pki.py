from datetime import datetime
import shutil
from config.conf import CERTS_PATH, PKI_DB, KEYS_PATH, PKI_PATH
from core.models import Certificate


class PKIController:
    def list_keys(self):
        keys = [c.name for c in KEYS_PATH.iterdir() if c.is_file()]
        keys.remove("_passphrase")
        keys = [c.split(".")[:-1] for c in keys]
        keys = [".".join(c) for c in keys]
        keys.remove("ca")
        return keys

    def list_certificates(self):
        with PKI_DB.open("r") as db:
            lines = [line.rstrip() for line in db]
            items = [line.split("\t") for line in lines]
            certificates = [
                Certificate(
                    status=i[0],
                    exp_date=self.__convert_date(i[1]),
                    revoke_date=self.__convert_date(i[2]),
                    serial=i[3],
                    filename_unknown=i[4],
                    common_name=i[5].replace("/CN=", "")
                )
                for i in items
            ]
            return certificates

    def __convert_date(self, raw: str):
        try:
            return datetime.strptime(raw, "%y%m%d%H%M%SZ")
        except (ValueError, TypeError):
            return None

    def export(self):
        if pki := PKI_PATH.exists():
            pass