# Enterprise Analytics QA Automation

A professional-grade Quality Assurance and Test Automation repository for an Enterprise Analytics Platform.

This project demonstrates a comprehensive QA strategy, featuring a complete testing pyramid that spans from raw SQL database validation to end-to-end browser automation, managed through a continuous CI/CD deployment pipeline.

## 🌟 Overview

The application under test is a data-driven FastAPI backend serving an interactive Apache ECharts frontend dashboard. 

The core mission of this QA project is to mathematically prove that the interactive visual dashboard accurately reflects the raw database state. It enforces the core invariant: **`SQL Expected == API Actual == UI Representation`**.

### Tech Stack
- **Testing Framework**: `pytest`
- **Browser Automation**: `Playwright`
- **Application Backend**: `FastAPI` (Python)
- **Application Frontend**: Vanilla JS + `Apache ECharts`
- **Database**: `SQLite3`
- **CI/CD**: `GitHub Actions` & `Render`

---

## 🏗️ QA Architecture & Test Pyramid

The repository boasts **90+ automated tests** logically separated across the testing pyramid. 

1. **Repository/Database Tests** (`@pytest.mark.repository`): Extracts baseline truth directly from the database using SQL queries, completely isolated from application logic.
2. **API Tests** (`@pytest.mark.api`): Asserts that the FastAPI routes serve the correct JSON structures and aggregates matching the database.
3. **UI Smoke Tests** (`@pytest.mark.ui`): Light, rapid DOM-level validations asserting the application mounts cleanly without relying on brittle timing states.
4. **End-to-End Tests** (`@pytest.mark.e2e`): Playwright orchestrates the headless Chromium browser through full user journeys (e.g. toggling Region filters, swapping chart types) while dynamically verifying the Javascript ECharts state against the SQL backend.

---

## 🚀 CI/CD Pipeline

This project employs a zero-tolerance deployment quality gate using **GitHub Actions**.

On every `push` or `pull_request` to `main`, the CI pipeline automatically:
1. Provisions a clean Ubuntu environment.
2. Installs Python and the frozen `requirements.txt`.
3. Installs Chromium via Playwright.
4. Executes the full 90+ test suite (`pytest -v`).
5. Generates a standalone HTML Test Report.
6. Blocks deployment if *any* test fails. 

Once the CI gate passes, the application is deployed automatically to **Render**.

---

## 🧪 Running Tests Locally

### Prerequisites
- Python 3.10+
- Playwright browsers installed (`playwright install chromium`)

### Quick Start
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

Run the entire test suite:
```bash
pytest
```

Generate the HTML test report:
```bash
pytest --html=docs/reports/test-report.html --self-contained-html
```

### Selective Execution via Markers
Run only the API integration tests:
```bash
pytest -m api
```

Run only End-to-End Playwright tests:
```bash
pytest -m e2e
```

---

## 📚 QA Documentation
- [Test Strategy](docs/test-strategy.md)
- [Requirements Traceability Matrix](docs/traceability-matrix.md)
- [Defect Logs](docs/defects.md)

---

## 🌎 Live Demo
The application is continuously deployed to Render after passing the CI quality gate.
*Note: Depending on the host's free-tier spin-up time, the API may take ~30s to respond on the first load.*
