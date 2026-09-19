"""Data loading and filtering helpers for the Forest Cover Type dataset."""
from pathlib import Path

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Load the Forest Cover Type dataset from a CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"No dataset found at {csv_path}")
    return pd.read_csv(csv_path)


def filter_data(
    df: pd.DataFrame,
    wilderness_areas: list[int] | None = None,
    cover_types: list[int] | None = None,
    elevation_range: tuple[int, int] | None = None,
) -> pd.DataFrame:
    """Filter the dataset by wilderness area, cover type, and/or elevation range.

    wilderness_areas: which of the 4 wilderness areas (1-4) to keep, based on
        the one-hot Wilderness_AreaX columns. None keeps all rows.
    cover_types: which Cover_Type values (1-7) to keep. None keeps all rows.
    elevation_range: (min, max) elevation, inclusive, to keep. None keeps all rows.
    """
    filtered = df

    if wilderness_areas:
        area_columns = [f"Wilderness_Area{area}" for area in wilderness_areas]
        filtered = filtered[filtered[area_columns].eq(1).any(axis=1)]

    if cover_types:
        filtered = filtered[filtered["Cover_Type"].isin(cover_types)]

    if elevation_range:
        low, high = elevation_range
        filtered = filtered[filtered["Elevation"].between(low, high)]

    return filtered.copy()
