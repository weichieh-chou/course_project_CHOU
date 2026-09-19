# Forest Cover Type Explorer

A Streamlit dashboard for exploring and filtering the Kaggle [Forest Cover
Type Prediction](https://www.kaggle.com/c/forest-cover-type-prediction)
dataset, containerized with Docker. Built for the HEC "Tooling for Data
Science" course.

This project reuses the dataset from an earlier project,
[aezacero/Forest-Cover-Type](https://github.com/aezacero/Forest-Cover-Type),
simplified down to a single data-exploration app (no model
training/prediction) to keep the project easy to build, test, and reproduce
end to end.

## What it does

The dataset has 15,120 forest patches described by 54 features (elevation,
aspect, slope, distances to hydrology/roads/fire points, hillshade, 4
one-hot wilderness areas, 40 one-hot soil types) and a `Cover_Type` label
(1-7). The app lets you filter the data by wilderness area, cover type, and
elevation range, and shows the filtered table plus two summary charts.

## Project structure

```
.
├── app.py                  # Streamlit app
├── src/data.py              # load_data() / filter_data() — the tested logic
├── tests/test_data.py       # unit tests for src/data.py
├── data/train.csv           # dataset
├── Dockerfile
├── requirements.txt
└── .github/workflows/ci.yml # runs pytest on every push/PR
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (defaults to http://localhost:8501).

## Run tests

```bash
pip install -r requirements.txt
pytest
```

Tests cover `load_data` and `filter_data` in [src/data.py](src/data.py),
using small synthetic fixtures so they run fast and don't depend on the
full dataset.

## Run with Docker

```bash
docker build -t forest-cover-explorer .
docker run -p 8501:8501 forest-cover-explorer
```

Then open http://localhost:8501.

## Continuous integration

Every push/PR to `main` runs the test suite via GitHub Actions
([.github/workflows/ci.yml](.github/workflows/ci.yml)), so the app's core
data logic is verified automatically.

## Reproducibility

- Pinned entry point (`requirements.txt`) installs the same top-level
  dependencies for local runs, CI, and the Docker image.
- The dataset is committed directly to the repo (`data/train.csv`, ~1.7MB),
  so no external download step is needed to run the app.
- The Dockerfile builds a self-contained image from `python:3.11-slim` with
  no host-specific configuration.
