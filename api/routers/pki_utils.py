from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse
from controllers import Installer
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
def export_pki():
    """genera tutta l'infrastruttira della PKI importando la chiave ed il certificato root. Eventuali strutture esistenti verranno cancellate"""
    pass