"""Shared fixtures for M1-B2 tests."""
from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Même chemin que celui servi par l'API via lifespan (cf. app/main.py).
MODEL_PATH = Path(__file__).parent.parent / "models" / "pyrenex_risk_v2.joblib"


@pytest.fixture(scope="module")
def client() -> TestClient:
    """TestClient avec lifespan déclenché (modèle chargé).

    Skip propre de toute la suite API tant que le modèle n'est pas présent —
    copie ton .joblib produit en M1-B1 dans ``models/`` pour activer ces tests.
    """
    if not MODEL_PATH.exists():
        pytest.skip(
            f"Modèle absent : {MODEL_PATH}. Copie d'abord ton .joblib produit "
            "en M1-B1 dans le dossier models/."
        )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def valid_payload() -> dict:
    """Valid loan application payload."""
    return {
        "loan_amnt": 10_000,
        "term": "36 months",
        "int_rate": 12.5,
        "annual_inc": 60000,
        "purpose": "debt_consolidation",
        "installment": 320.75,
        "dti": 15.0,
        "delinq_2yrs": 0,
        "fico_range_low": 700,
        "revol_util": 45.0,
        "grade": "B",
        "emp_length": "5 years",
        "home_ownership": "MORTGAGE",
        "verification_status": "Verified",
    }
