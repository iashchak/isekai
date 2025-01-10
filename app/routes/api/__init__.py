import secrets
from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from . import v1
from . import v2
from . import v3
from . import v4
from . import v5
from . import health

def verify_credentials(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    correct_username = secrets.compare_digest(credentials.username, "isekai_lover")
    correct_password = secrets.compare_digest(credentials.password, "isekai_lover")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

router = APIRouter()

router.include_router(router=v1.router, prefix="/v1", dependencies=[Depends(verify_credentials)])
router.include_router(router=v2.router, prefix="/v2", dependencies=[Depends(verify_credentials)])
router.include_router(router=v3.router, prefix="/v3", dependencies=[Depends(verify_credentials)])
router.include_router(router=v4.router, prefix="/v4", dependencies=[Depends(verify_credentials)])
router.include_router(router=v5.router, prefix="/v5", dependencies=[Depends(verify_credentials)])

router.include_router(router=health.router)
