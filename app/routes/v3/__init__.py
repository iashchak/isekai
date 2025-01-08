from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.routes.v3.hero_generator import HeroGenerator
from app.utils.helpers import verify_credentials
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("transitions").setLevel(logging.INFO)

router = APIRouter()

hero = HeroGenerator()

security = HTTPBasic()


@router.get("/generate", description="Generates a random hero with all attributes.")
async def generate_hero(random_seed: int = None, credentials: HTTPBasicCredentials = Depends(security)):
    """Generate a random hero."""
    verify_credentials(credentials)
    hero_data = hero.generate_hero(random_seed=random_seed)
    return hero_data
