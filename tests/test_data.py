import pandas as pd
import pytest

from src.data import filter_data, load_data


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Elevation": [2000, 2500, 3000, 3500],
            "Cover_Type": [1, 2, 1, 3],
            "Wilderness_Area1": [1, 0, 0, 1],
            "Wilderness_Area2": [0, 1, 0, 0],
            "Wilderness_Area3": [0, 0, 1, 0],
            "Wilderness_Area4": [0, 0, 0, 0],
        }
    )


def test_load_data_reads_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("Elevation,Cover_Type\n2000,1\n2500,2\n")

    df = load_data(str(csv_path))

    assert list(df.columns) == ["Elevation", "Cover_Type"]
    assert len(df) == 2


def test_load_data_missing_file_raises(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_data(str(missing_path))


def test_filter_data_no_filters_returns_all_rows(sample_df):
    result = filter_data(sample_df)

    assert len(result) == len(sample_df)


def test_filter_data_by_wilderness_area(sample_df):
    result = filter_data(sample_df, wilderness_areas=[1])

    assert set(result.index) == {0, 3}


def test_filter_data_by_cover_type(sample_df):
    result = filter_data(sample_df, cover_types=[1])

    assert set(result["Cover_Type"]) == {1}
    assert len(result) == 2


def test_filter_data_by_elevation_range(sample_df):
    result = filter_data(sample_df, elevation_range=(2200, 3200))

    assert set(result["Elevation"]) == {2500, 3000}


def test_filter_data_combines_filters(sample_df):
    result = filter_data(
        sample_df,
        wilderness_areas=[1, 2],
        cover_types=[1, 2],
        elevation_range=(2000, 2600),
    )

    assert set(result.index) == {0, 1}
