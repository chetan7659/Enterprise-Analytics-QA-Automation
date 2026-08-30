# Analytics QA Test Strategy

## 1. Objective
Validate the data accuracy, business logic, API behavior, visualization integrity, and end-to-end dashboard workflows of the Enterprise Analytics Platform. This ensures that executive dashboards display mathematically proven data across all chart types and interactive states.

## 2. Scope
### In Scope
- Database schema validation and SQL extraction.
- REST API contract validation and business logic calculations.
- UI Smoke testing (layout, components, rendering).
- Frontend ECharts state management.
- End-to-End user journeys (Filters, Chart toggles).
- CI/CD Deployment validation.

### Out of Scope
- Performance and load testing (DDoS, concurrency scaling).
- Security penetration testing (SQL injection, XSS).
- Mobile device compatibility testing (specifically targeting desktop chromium for E2E).

## 3. Test Levels
1. **Repository/Database**: Validate SQLite extraction and raw SQL data correctness.
2. **API (Integration)**: Validate FastAPI routes return mathematically verified JSON identical to the SQL Oracle.
3. **UI (Smoke)**: Fast, non-stateful DOM checks to ensure elements load and basic Javascript executes.
4. **End-to-End**: Playwright interacting with a Live Uvicorn Server, mimicking true user paths and cross-referencing UI state against the SQL Oracle.

## 4. Test Types
- **Data Validation Tests**: Confirm aggregates (`SUM`, averages) map correctly.
- **Contract Tests**: Validate API JSON schemas and types.
- **Invariant Tests**: Ensure changing visual representations (Bar -> Pie) does not alter underlying numeric data.
- **State Transition Tests**: Test dynamic filters (e.g., India -> USA -> All Regions).

## 5. Test Data Strategy
Tests utilize an isolated SQLite test database populated with explicitly controlled, deterministic seed data. This enables the creation of an **Independent SQL Oracle**, where expected values are dynamically queried during tests rather than hardcoded.

## 6. Automation Strategy
- **Framework**: `pytest` as the core execution engine.
- **Browser Automation**: `playwright` (Chromium) for synchronous E2E UI verification.
- **State Introspection**: Programmatic extraction of ECharts internal Javascript state via `page.evaluate()` rather than relying solely on brittle image comparison.

## 7. Environment
- **Local Development**: Windows, Python 3.14.
- **CI Environment**: Ubuntu latest, GitHub Actions, Headless Chromium.
- **CD Environment**: Render Platform (Python Web Service).

## 8. CI/CD Integration
- GitHub Actions runs the entire test suite (`pytest`) automatically on every `push` and `pull_request` to `main`.
- The pipeline acts as a deployment quality gate: no broken code is deployed to Render.
- Test artifacts (HTML reports) are generated and uploaded for transparency.

## 9. Risks
- **Data Desync**: ECharts asynchronous rendering animations causing race conditions with Playwright assertions (Mitigated via `page.wait_for_function`).
- **Dependency Drift**: Environment mismatch between Local and CI (Mitigated via strictly pinned `requirements.txt`).

## 10. Exit Criteria
- 100% pass rate across all 90+ tests in the automated suite.
- Zero open critical or high-severity defects.
- Successful generation and archiving of the `pytest-html` report in the CI pipeline.
- Successful deployment rollout to the live Render environment.
