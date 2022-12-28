from fastapi import APIRouter, Body, BackgroundTasks
from fastapi.responses import PlainTextResponse, FileResponse
from controllers import Installer, PKIController
from core.install import install


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
