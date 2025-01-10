from fastapi import APIRouter
from app.utils.helpers import select_reverse_exponential_items, select_random_item
import pandas as pd
import os

DATAPATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "v1")
df = pd.read_csv(os.path.join(DATAPATH, "data.csv"))

router = APIRouter()

@router.get(
    "/generate",
    description="Generates a random isekai scenario based on optional query parameters.",
)
async def v1(k: int = 3, p_zero: float = 0.4):
    expanential_columns = [
        "Навык / способность",
        "Уникальный предмет",
        "Баф от бога(ов)",
        "Главная слабость",
    ]
    stats = {}
    for column in df.columns:
        if column in expanential_columns:
            stats[column] = ", ".join(
                select_reverse_exponential_items(df[column], k=k, p_zero=p_zero).values
            )
        else:
            stats[column] = ", ".join(select_random_item(df[column], k=k).values)

    return stats
