from pathlib import Path
import aiofiles
from .installer import Installer
import zipfile
from config.conf import PKI_PATH, CA_CRT_PATH, CA_KEY_PATH, PASSPRHASE_PATH
from fastapi import HTTPException, UploadFile
from core.utils.remove_tmp_file import remove_tmp_file


class Importer(Installer):
    def __init__(self) -> None:
        super().__init__()

    async def extract_pki(self, archive: UploadFile):
        try:
            temp_path = Path("/tmp/imported_pki.zip")
            async with aiofiles.open(temp_path, "wb") as out_file:
                while content := await archive.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk

            with zipfile.ZipFile(temp_path, mode="r") as zip_file:
                for file in zip_file.namelist():
                    zip_file.extract(file, PKI_PATH)

            remove_tmp_file(temp_path)

            return True
        except Exception as e :
            raise HTTPException(500, f"impossibile estrare archivio: {str(e)}")

    async def import_root(self, crt: UploadFile, key: UploadFile, passphrase: str):
        try:
            async with aiofiles.open(CA_CRT_PATH, "wb") as out_crt:
                while content := await crt.read(1024):  # async read chunk
                    await out_crt.write(content)  # async write chunk

            async with aiofiles.open(CA_KEY_PATH, "wb") as out_key:
                while content := await key.read(1024):  # async read chunk
                    await out_key.write(content)  # async write chunk

            PASSPRHASE_PATH.write_text(passphrase)
            PASSPRHASE_PATH.chmod(400)
            CA_KEY_PATH.chmod(400)
            CA_CRT_PATH.chmod(444)
            return True
        except Exception:
            HTTPException(500, "Errori durante il salvataggio dei files")
