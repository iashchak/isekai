from fastapi import APIRouter
from app.utils.helpers import select_reverse_exponential_items, select_random_item
import pandas as pd
import os
import yaml

DATAPATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..","data", "v2")

dfs = [
    pd.read_csv(os.path.join(DATAPATH, f)) for f in os.listdir(DATAPATH) if f.endswith(".csv")
]

metadata = yaml.safe_load(open(os.path.join(DATAPATH, "metadata.yaml"), "r")) 

router = APIRouter()

@router.get(
    "/generate",
    description="Generates a random isekai scenario based on optional query parameters.",
)
async def v2(k: int = 1, n: int = 1, p_zero: float = 0.4):
    stats = {}
    for df in dfs:
        for column in df.columns:
            metadata_column = next((x for x in metadata if x["name"] == column), None)
            is_spreading = metadata_column and metadata_column.get("speading") or False
            key = metadata_column and (metadata_column.get("harem") or metadata_column.get("name")) or column
            koef = metadata_column and metadata_column.get("K") or 1
            koef = koef * 1.0 * k
            if key in stats:
                continue
            if is_spreading: 
                stats[key] = ", ".join([string.strip() for string in select_reverse_exponential_items(df[column], k=koef, p_zero=p_zero).values])
            else:
                stats[key] = ", ".join([string.strip() for string in select_random_item(df[column], k=n).values])
    
    # remove empty values
    stats_without_empty = {}
    for key, value in stats.items():
        if value:
            metadata_column = next((x for x in metadata if x["name"] == key), None)
            alias = metadata_column and metadata_column.get("alias") or key
            stats_without_empty[alias] = value

    return stats_without_empty