from fastapi import APIRouter
from . import api
from . import privacy

router = APIRouter()

from fastapi.security import HTTPBasic
security = HTTPBasic()

router.include_router(api.api_router, prefix="/api")
router.include_router(privacy.router)
