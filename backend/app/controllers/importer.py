from pathlib import Path
import aiofiles
from .installer import Installer
import zipfile
from core.config import Settings
from fastapi import HTTPException, UploadFile

class Importer(Installer):

    def __init__(self, cnf: Settings) -> None:
        super().__init__(cnf)

    async def extract_pki(self, archive: UploadFile):
        temp_path = Path("/tmp/imported_pki.zip")
        try:
            async with aiofiles.open(temp_path, "wb") as out_file:
                while content := await archive.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk

            with zipfile.ZipFile(temp_path, mode="r") as zip_file:
                for file in zip_file.namelist():
                    zip_file.extract(file, self.cnf.PKI)

            return True
        except Exception as e:
            raise HTTPException(500, f"impossibile estrare archivio: {str(e)}")
        finally:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

    async def import_root(self, crt: str, key: str, passphrase: str):
        try:
            # async with aiofiles.open(CA_CRT_PATH, "wb") as out_crt:
            #     while content := await crt.read(1024):  # async read chunk
            #         await out_crt.write(content)  # async write chunk

            # async with aiofiles.open(CA_KEY_PATH, "wb") as out_key:
            #     while content := await key.read(1024):  # async read chunk
            #         await out_key.write(content)  # async write chunk

            self.cnf.CA_CRT_PATH.write_text(crt)
            self.cnf.CA_KEY_PATH.write_text(key)
            self.cnf.PASSPRHASE_PATH.write_text(passphrase)
            self.cnf.CA_CRT_PATH.chmod(444)
            self.cnf.CA_KEY_PATH.chmod(400)
            self.cnf.PASSPRHASE_PATH.chmod(400)

            return True
        except Exception:
            raise HTTPException(500, "Errori durante il salvataggio dei files")
