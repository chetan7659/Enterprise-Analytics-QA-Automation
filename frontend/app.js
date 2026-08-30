/**
 * Step 44: Interactive ECharts Filters
 * Extends Step 43 with a Region filter dropdown that propagates
 * from the UI → API → Database → ECharts.
 *
 * Filter Pipeline:
 *   User selects region
 *     → selectedRegion state updated
 *     → cachedData invalidated
 *     → fetchRevenueByRegion(selectedRegion) called
 *     → ?region=<value> appended to API URL (omitted when "All")
 *     → API returns filtered result
 *     → ECharts re-renders
 */

// ============================================================================
// APPLICATION STATE
// ============================================================================

let chartInstance = null;
let cachedData = null;
let currentChartType = 'bar';

// Step 44: Filter state
// "" → All Regions (no ?region= param sent)
// "India" / "USA" → filtered request
let selectedRegion = "";

// ============================================================================
// PART 4: Initialize ECharts
// ============================================================================

function initChart() {
    const chartElement = document.getElementById('revenue-chart');

    if (!chartElement) {
        console.error('Chart container not found!');
        return null;
    }

    // Initialize ECharts instance with dark theme
    const chart = echarts.init(chartElement, 'dark');
    console.log('✅ ECharts initialized with dark theme');
    window.revenueChart = chart; // Expose to Playwright for E2E testing

    return chart;
}

// ============================================================================
// PART 5: Connect to Existing API (with Region Filter)
// ============================================================================

/**
 * Fetch revenue data from the API.
 *
 * @param {string} region - "" for All Regions, or a specific region name.
 *
 * Filter → URL mapping:
 *   ""      → /analytics/revenue-by-region          (no param)
 *   "India" → /analytics/revenue-by-region?region=India
 *   "USA"   → /analytics/revenue-by-region?region=USA
 */
async function fetchRevenueByRegion(region = "") {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error-message');
    const noDataEl = document.getElementById('no-data-message');

    try {
        loadingEl.classList.add('active');
        errorEl.classList.remove('active');
        noDataEl.classList.remove('active');

        // Build URL — only add ?region= when a specific region is selected
        const params = new URLSearchParams();
        if (region) {
            params.set("region", region);
        }

        const baseUrl = '/analytics/revenue-by-region';
        const url = region ? `${baseUrl}?${params.toString()}` : baseUrl;

        console.log(`🔍 Fetching: ${url}`);

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`API returned status ${response.status}`);
        }

        const data = await response.json();
        console.log('✅ API response received:', data);

        loadingEl.classList.remove('active');
        return data;

    } catch (error) {
        console.error('❌ Error fetching from API:', error);
        errorEl.textContent = `Error: ${error.message}. Make sure the backend is running.`;
        errorEl.classList.add('active');
        loadingEl.classList.remove('active');
        return null;
    }
}

// ============================================================================
// PART 6: Transform API Data
// ============================================================================

function transformData(apiResponse) {
    if (!apiResponse || !apiResponse.data) {
        console.error('Invalid API response structure');
        return null;
    }

    const regions = [];
    const revenues = [];

    // Extract dimensions and measures
    for (const item of apiResponse.data) {
        regions.push(item.region);      // X-axis: dimension
        revenues.push(item.revenue);    // Y-axis: measure
    }

    console.log('✅ Data transformed');
    console.log('  Regions:', regions);
    console.log('  Revenues:', revenues);

    return {
        regions,
        revenues
    };
}

// ============================================================================
// PART 7: Create ECharts Option
// ============================================================================

function createChartOption(transformedData, chartType) {
    if (!transformedData) {
        return null;
    }

    // Set background color to transparent to match container styling
    const baseOption = {
        backgroundColor: 'transparent',
        title: {
            text: 'Revenue by Region',
            left: 'center',
            top: 10,
            textStyle: {
                fontSize: 16,
                fontWeight: 'bold',
                color: '#ffffff'
            }
        },

        legend: {
            show: true,
            top: 'bottom',
            textStyle: {
                color: '#94a3b8'
            }
        },

        tooltip: {
            trigger: chartType === 'pie' ? 'item' : 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: (params) => {
                const dataPoint = Array.isArray(params) ? params[0] : params;
                if (dataPoint) {
                    const value = dataPoint.value;
                    const numValue = typeof value === 'object' ? value.value : value;
                    const formatted = new Intl.NumberFormat('en-US').format(numValue);
                    if (chartType === 'pie') {
                        return `${dataPoint.name}: $${formatted} (${dataPoint.percent}%)`;
                    }
                    return `${dataPoint.name}: $${formatted}`;
                }
                return '';
            }
        },

        grid: chartType === 'pie' ? undefined : {
            left: '12%',
            right: '12%',
            top: 70,
            bottom: '15%',
            containLabel: true
        }
    };

    if (chartType === 'pie') {
        const pieData = transformedData.regions.map((region, index) => ({
            name: region,
            value: transformedData.revenues[index]
        }));

        return {
            ...baseOption,
            series: [
                {
                    name: 'Revenue',
                    type: 'pie',
                    radius: '55%',
                    center: ['50%', '60%'],
                    data: pieData,
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    label: {
                        show: true,
                        formatter: '{b}: ${c}'
                    }
                }
            ]
        };
    } else {
        return {
            ...baseOption,
            xAxis: {
                type: 'category',
                data: transformedData.regions,
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    fontSize: 12,
                    color: '#94a3b8'
                },
                axisLine: {
                    lineStyle: {
                        color: '#475569'
                    }
                }
            },

            yAxis: {
                type: 'value',
                name: 'Revenue ($)',
                nameTextStyle: {
                    color: '#94a3b8'
                },
                axisLabel: {
                    fontSize: 12,
                    color: '#94a3b8',
                    formatter: (value) => {
                        if (value >= 1000) {
                            return '$' + (value / 1000).toFixed(0) + 'k';
                        }
                        return '$' + value;
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: '#334155'
                    }
                }
            },

            series: [
                {
                    name: 'Revenue',
                    type: chartType,
                    data: transformedData.revenues,
                    itemStyle: {
                        color: chartType === 'bar' ? '#3b82f6' : '#10b981'
                    },
                    emphasis: {
                        itemStyle: {
                            color: chartType === 'bar' ? '#2563eb' : '#059669'
                        }
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: (params) => {
                            return '$' + (params.value / 1000).toFixed(0) + 'k';
                        },
                        fontSize: 12,
                        color: '#ffffff'
                    }
                }
            ]
        };
    }
}

// ============================================================================
// PART 8: Render & Update Chart
// ============================================================================

/**
 * Show / hide the "Filtered" badge next to the dropdown.
 * Badge is visible whenever a specific region is selected.
 */
function updateFilterBadge(region) {
    const badge = document.getElementById('filter-badge');
    if (!badge) return;
    if (region) {
        badge.textContent = `Filtered: ${region}`;
        badge.classList.add('visible');
    } else {
        badge.classList.remove('visible');
    }
}

/**
 * Show / hide the "No data" message and the chart container.
 * Called when the API returns an empty data array (e.g. unknown region).
 */
function showNoData(isEmpty) {
    const noDataEl = document.getElementById('no-data-message');
    const chartEl = document.getElementById('revenue-chart');
    if (isEmpty) {
        noDataEl.classList.add('active');
        chartEl.style.display = 'none';
    } else {
        noDataEl.classList.remove('active');
        chartEl.style.display = '';
    }
}

async function updateChart(type) {
    currentChartType = type;
    console.log(`🚀 Rendering chart type: ${type} | region: "${selectedRegion || 'All'}"...`);

    // Ensure chart is initialized
    if (!chartInstance) {
        chartInstance = initChart();
    }
    if (!chartInstance) return;

    // Step 44: always fetch fresh data when cachedData is null (cache is
    // invalidated on every filter change via handleRegionFilter).
    if (!cachedData) {
        const apiResponse = await fetchRevenueByRegion(selectedRegion);
        if (!apiResponse) return;

        // Handle empty data (e.g. unknown region)
        if (!apiResponse.data || apiResponse.data.length === 0) {
            showNoData(true);
            console.log(`ℹ️ No data returned for region: "${selectedRegion || 'All'}"`);
            return;
        }

        showNoData(false);
        cachedData = transformData(apiResponse);
    }
    if (!cachedData) return;

    // Generate configuration option
    const option = createChartOption(cachedData, currentChartType);
    if (!option) return;

    // Render chart (use notMerge=true to prevent merging axis configs on pie switch)
    chartInstance.setOption(option, true);
    console.log(`✅ Chart updated to ${type} successfully!`);
}

// ============================================================================
// STEP 44: Region Filter Handler
// ============================================================================

/**
 * Called when the Region dropdown value changes.
 *
 * Filter Pipeline:
 *   change event
 *     → selectedRegion updated
 *     → cachedData invalidated (force fresh API call)
 *     → filter badge updated
 *     → updateChart() called with current chart type
 *
 * Filter state is preserved independently of chart type — switching Bar → Line
 * while "India" is selected keeps the India filter active.
 */
function handleRegionFilter(e) {
    selectedRegion = e.target.value;

    // Invalidate cache — filter changed, stale data must not be reused
    cachedData = null;

    console.log(`🔽 Region filter changed → "${selectedRegion || 'All Regions'}"`);

    // Update the visual badge
    updateFilterBadge(selectedRegion);

    // Re-render with the current chart type (filter state preserved)
    updateChart(currentChartType);
    
    // Step 46: Sync KPI
    updateKPI();
}

// ============================================================================
// STEP 46: KPI Dashboard Integration
// ============================================================================

async function updateKPI() {
    try {
        const params = new URLSearchParams();
        if (selectedRegion) {
            params.set("region", selectedRegion);
        }
        const baseUrl = '/analytics/revenue';
        const url = selectedRegion ? `${baseUrl}?${params.toString()}` : baseUrl;

        const response = await fetch(url);
        if (!response.ok) throw new Error(`KPI API returned status ${response.status}`);
        
        const data = await response.json();
        
        const formattedValue = new Intl.NumberFormat('en-US').format(data.value || 0);
        document.getElementById('kpi-revenue').textContent = `$${formattedValue}`;
    } catch (error) {
        console.error('❌ Error fetching KPI:', error);
        document.getElementById('kpi-revenue').textContent = 'Error';
    }
}

// ============================================================================
// INITIALISATION
// ============================================================================

function initApp() {
    // Set up click listeners for the chart-type selector buttons
    const buttons = document.querySelectorAll('.btn-tab');
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const selectedType = e.target.getAttribute('data-type');

            // Update active states
            buttons.forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');

            // Step 44: switching chart type does NOT reset the region filter.
            // selectedRegion and cachedData remain unchanged.
            updateChart(selectedType);
        });
    });

    // Step 44: wire the region filter dropdown
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter) {
        regionFilter.addEventListener('change', handleRegionFilter);
        console.log('✅ Region filter wired');
    }

    // Initial render (All Regions, Bar chart)
    updateChart('bar');
    updateKPI();

    // Handle window resize
    window.addEventListener('resize', () => {
        if (chartInstance) {
            chartInstance.resize();
        }
    });
}

// Start application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
