# Defect Logs

This document tracks representative defects discovered and resolved during the QA and deployment phases of the Enterprise Analytics project. This illustrates the defect management lifecycle (Detection -> Analysis -> Fix -> Retest).

---

## DEF-001: Localhost Hardcoding in Production Build
**Status**: Closed / Fixed
**Severity**: High
**Environment**: Production (Render)

**Description**:
After successful deployment of the FastAPI application to Render, the frontend dashboard loaded but the charts displayed no data. The API endpoints themselves returned HTTP 200 when accessed directly.

**Expected Behavior**:
The frontend ECharts dashboard should dynamically fetch data from the production API URL and render the charts correctly.

**Actual Behavior**:
The dashboard rendered visually, but network requests failed. The browser attempted to fetch data from `http://localhost:8000/analytics/revenue-by-region` instead of the relative production URL.

**Root Cause**:
In `frontend/app.js`, the `baseUrl` for fetch requests was hardcoded to `http://localhost:8000`. This worked in the local development environment but failed when served over the public internet, as the client's browser could not resolve `localhost` to the Render server.

**Resolution**:
Updated `frontend/app.js` to use relative routing (e.g., `/analytics/revenue-by-region`). The HTTP origin is now dynamically resolved by the browser.

---

## DEF-002: Region Filter Ignored on Empty Selection
**Status**: Closed / Fixed
**Severity**: Medium
**Environment**: Local / UI Automation

**Description**:
During E2E testing of the interactive Region filter, selecting a specific region correctly filtered the dashboard. However, resetting the filter to "All Regions" (value="") did not successfully restore the global dataset.

**Expected Behavior**:
Selecting "All Regions" (empty value string) should trigger an API fetch to `/analytics/revenue-by-region` (with no query parameters) and ECharts should render data for all regions.

**Actual Behavior**:
The ECharts visualization remained locked onto the previously selected region (e.g., India).

**Root Cause**:
The `app.js` frontend script constructed the URL using URLSearchParams, but the backend FastAPI route did not properly handle empty query parameters or the frontend failed to omit the parameter, leading to stale caching in `cachedData`.

**Resolution**:
Refactored `fetchRevenueByRegion` in `app.js` to only append `?region=X` if a truthy region value was provided. Modified `handleRegionFilter` to actively invalidate `cachedData = null` whenever the dropdown changes, forcing a fresh fetch.
