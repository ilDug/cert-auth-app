from datetime import datetime
from pathlib import Path
import shutil
from core.config import Settings
from models import Certificate
import zipfile
from datetime import datetime


class PKIController:

    def __init__(self, cnf: Settings):
        self.cnf = cnf

    def list_keys(self):
        keys = [c.name for c in self.cnf.KEYS_PATH.iterdir() if c.is_file()]
        if "_passphrase" in keys:
            keys.remove("_passphrase")
        keys = [c.split(".")[:-1] for c in keys]
        keys = [".".join(c) for c in keys]
        if "ca" in keys:
            keys.remove("ca")
        return keys

    def list_certificates(self):
        with self.cnf.PKI_DB.open("r") as db:
            lines = [line.rstrip() for line in db]
            items = [line.split("\t") for line in lines]
            certificates = [
                Certificate(
                    status=i[0],
                    exp_date=self.__convert_date(i[1]),
                    revoke_date=self.__convert_date(i[2]),
                    serial=i[3],
                    filename_unknown=i[4],
                    common_name=i[5].replace("/CN=", ""),
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
        zipname = f"pki-{datetime.now().strftime('%Y%d%m-%H%M%S')}.zip"
        zippath = Path("/tmp") / zipname
        pki = self.cnf.PKI

        with zipfile.ZipFile(
            zippath, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for file_path in pki.rglob("*"):
                archive.write(file_path, arcname=file_path.relative_to(pki))
        return zippath

    def download_ca_root(self):
        zipname = f"ca-root.zip"
        zippath = Path("/tmp") / zipname

        with zipfile.ZipFile(zippath, mode="w") as archive:
            for f in [
                self.cnf.CA_KEY_PATH,
                self.cnf.CA_CRT_PATH,
                self.cnf.PASSPRHASE_PATH,
            ]:
                archive.write(f, arcname=f.name)

        with zipfile.ZipFile(zippath, mode="r") as archive:
            archive.printdir()
        return zippath
