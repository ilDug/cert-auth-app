from pathlib import Path
from fastapi import APIRouter, Body, BackgroundTasks, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from controllers import Installer, PKIController, Importer
from core.install import install
import aiofiles

router = APIRouter(tags=["import"])


@router.get("/pki/reset")
async def reset_pki():
    pki = Installer()
    pki.clean_structure()
    print("PKI directory creation...")
    install()
    return True


@router.get("/pki/export")
async def export_pki(background_tasks: BackgroundTasks):
    pki = PKIController()
    pathfile = pki.export()
    filename = pathfile.name
    background_tasks.add_task(pki.remove_zip_after_download, pathfile)
    return FileResponse(pathfile, media_type="application/zip", filename=filename)

    # """genera tutta l'infrastruttira della PKI importando la chiave ed il certificato root. Eventuali strutture esistenti verranno cancellate"""


@router.post("/pki/import/archive")
async def import_pki_zip(archive: UploadFile):
    if archive.content_type != "application/zip":
        raise HTTPException(400, "il file deve essere un archivio zip")

    importer = Importer()
    importer.clean_structure()

    temp_path = Path("/tmp/imported_pki.zip")
    async with aiofiles.open(temp_path, "wb") as out_file:
        while content := await archive.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    return importer.extract_pki(temp_path)

    
