from fastapi import APIRouter
from app.routes import v1 as v1
from app.routes import v2 as v2
from app.routes import v3 as v3
from app.routes import v4 as v4
from app.routes import health as health
from app.routes import privacy as privacy


router = APIRouter()

router.include_router(v1.router, prefix="/v1")
router.include_router(v2.router, prefix="/v2")
router.include_router(v3.router, prefix="/v3")
router.include_router(v4.router, prefix="/v4")
router.include_router(health.router)
router.include_router(privacy.router)
