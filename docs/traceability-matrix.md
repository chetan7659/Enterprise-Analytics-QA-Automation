# Traceability Matrix

This matrix maps core business and application requirements to the specific automated tests that validate them, ensuring 100% test coverage of critical functionality.

| Requirement ID | Requirement Description | Test Level | Automated Test Location | Status |
|---|---|---|---|---|
| **REQ-001** | Database holds valid sales records | Repository | `test_sales_repository.py::test_database_connection` | PASS |
| **REQ-002** | Query total company revenue | Repository | `test_sales_repository.py::test_sql_total_revenue` | PASS |
| **REQ-003** | API exposes total revenue endpoint | API | `test_api.py::test_total_revenue` | PASS |
| **REQ-004** | Revenue calculated accurately by Region | API | `test_api.py::test_revenue_by_region` | PASS |
| **REQ-005** | Dashboard UI loads and displays elements | UI Smoke | `tests/ui/test_dashboard.py::test_dashboard_loads` | PASS |
| **REQ-006** | ECharts visualizes revenue by region | UI Smoke | `tests/ui/test_dashboard.py::test_revenue_chart_is_visible` | PASS |
| **REQ-007** | ECharts legend and tooltips reflect accurate data | API/ECharts | `test_api.py::test_step45_simulate_tooltip_data_india` | PASS |
| **REQ-008** | Region dropdown filters dashboard data | E2E | `tests/ui/test_e2e_analytics.py::test_india_filter_updates_dashboard` | PASS |
| **REQ-009** | Resetting filter restores global dashboard data | E2E | `tests/ui/test_e2e_analytics.py::test_reset_filter_restores_data` | PASS |
| **REQ-010** | Chart type toggles (Bar/Pie/Line) | UI Smoke | `tests/ui/test_dashboard.py::test_chart_type_controls_visible` | PASS |
| **REQ-011** | Toggling chart type preserves filtered data state | E2E | `tests/ui/test_e2e_analytics.py::test_filter_and_chart_type_switch_preserves_data` | PASS |
| **REQ-012** | KPI syncs with Region filter state | API | `test_api.py::test_step46_kpi_syncs_with_filter` | PASS |
