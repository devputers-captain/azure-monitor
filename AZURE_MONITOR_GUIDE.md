
## Monitoring in Azure - Complete Guide

### Step-by-Step: Viewing Telemetry in Azure Portal

Once your application is running and generating telemetry, follow these steps to view different telemetry types:

### 1. Access Application Insights

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to your **Application Insights** resource
3. Wait 2-5 minutes after generating telemetry (there's a slight ingestion delay)

---

### 2. View Live Metrics (Real-Time)

**Best for: Real-time monitoring of requests, failures, and performance**

1. In Application Insights, click **Live Metrics** (left menu under "Investigate")
2. Make requests to your API endpoints
3. Watch real-time:
   - Incoming requests per second
   - Failed requests
   - Server response time
   - CPU/Memory usage

📝 **Try**: Hit `/demo/all` endpoint and watch metrics appear in real-time!

---

### 3. View Traces (Distributed Tracing)

**Best for: Understanding request flow and custom spans**

1. Click **Transaction search** or **Logs** (left menu)
2. Run this KQL query:

```kusto
traces
| where timestamp > ago(1h)
| project timestamp, message, severityLevel, customDimensions
| order by timestamp desc
```

**To see custom traces from `/demo/trace`:**
```kusto
traces
| where operation_Name == "GET /demo/trace"
| order by timestamp desc
```

📝 **Try**: Call `/demo/trace` endpoint, then search for "custom_operation" spans

---

### 4. View Logs by Severity Level

**Best for: Debugging and monitoring application behavior**

#### View INFO Logs
```kusto
traces
| where severityLevel == 1  // Info = 1
| where timestamp > ago(1h)
| project timestamp, message, customDimensions
| order by timestamp desc
```

#### View WARNING Logs
```kusto
traces
| where severityLevel == 2  // Warning = 2
| where timestamp > ago(1h)
| project timestamp, message, customDimensions
| order by timestamp desc
```

#### View ERROR Logs
```kusto
traces
| where severityLevel == 3  // Error = 3
| where timestamp > ago(1h)
| project timestamp, message, customDimensions
| order by timestamp desc
```

📝 **Try**: 
- Call `/demo/info` → Check severity level 1
- Call `/demo/warning` → Check severity level 2
- Call `/demo/error` → Check severity level 3

---

### 5. View Exceptions

**Best for: Tracking application errors and exceptions**

#### Option 1: Failures Blade (Visual)
1. Click **Failures** (left menu under "Investigate")
2. View exception counts, types, and trends
3. Click on any exception to see:
   - Full stack trace
   - Request details
   - Custom properties

#### Option 2: Using KQL Queries
```kusto
exceptions
| where timestamp > ago(1h)
| project timestamp, type, outerMessage, innermostMessage, problemId
| order by timestamp desc
```

**View exceptions with custom properties:**
```kusto
exceptions
| where timestamp > ago(1h)
| extend error_type = tostring(customDimensions.error_type)
| project timestamp, type, outerMessage, error_type, customDimensions
| order by timestamp desc
```

📝 **Try**: 
- Call `/demo/exception?error_type=runtime`
- Call `/demo/exception?error_type=zero_division`

---

### 6. View Custom Metrics

**Best for: Tracking business metrics and performance indicators**

#### Option 1: Metrics Explorer (Visual)
1. Click **Metrics** (left menu under "Monitoring")
2. Click "+ New chart"
3. Select metric namespace: **azure.applicationinsights**
4. Select metrics:
   - `demo.requests.total` (counter)
   - `demo.processing.duration` (histogram)
   - `demo.active_users` (gauge)
   - `demo.errors.total` (counter)
5. Add filters and splits as needed

#### Option 2: Using KQL Queries
```kusto
customMetrics
| where name in ("demo.requests.total", "demo.processing.duration", "demo.active_users", "demo.errors.total")
| where timestamp > ago(1h)
| project timestamp, name, value, customDimensions
| order by timestamp desc
```

**Analyze metric trends:**
```kusto
customMetrics
| where name == "demo.processing.duration"
| where timestamp > ago(1h)
| summarize avg(value), min(value), max(value), percentile(value, 95) by bin(timestamp, 5m)
| render timechart
```

📝 **Try**: Call `/demo/metrics` multiple times and watch metrics accumulate

---

### 7. View Dependencies (External Calls)

**Best for: Monitoring external API calls, databases, and services**

#### Option 1: Application Map
1. Click **Application map** (left menu under "Investigate")
2. See visual representation of your service and its dependencies
3. Click on dependency nodes to see:
   - Call counts
   - Success/failure rates
   - Average duration

#### Option 2: Dependencies Blade
1. Click **Performance** → **Dependencies** tab
2. View all external dependencies
3. Sort by duration or failure rate

#### Option 3: Using KQL Queries
```kusto
dependencies
| where timestamp > ago(1h)
| project timestamp, name, target, duration, success, resultCode
| order by timestamp desc
```

**View failed dependencies:**
```kusto
dependencies
| where success == false
| where timestamp > ago(1h)
| project timestamp, name, target, duration, resultCode, customDimensions
| order by timestamp desc
```

📝 **Try**: Call `/demo/dependency` to see external HTTP call to jsonplaceholder.typicode.com

---

### 8. View Performance Metrics

**Best for: Identifying slow operations and bottlenecks**

1. Click **Performance** (left menu under "Investigate")
2. View:
   - Request duration distribution
   - Operation timeline
   - Slowest operations

**KQL Query for slow operations:**
```kusto
requests
| where timestamp > ago(1h)
| where duration > 1000  // Slower than 1 second
| project timestamp, name, duration, success, resultCode
| order by duration desc
```

📝 **Try**: Call `/demo/slow` to generate slow operation telemetry

---

### 9. Comprehensive Query - View Everything

**See all telemetry types for a specific time window:**

```kusto
union traces, exceptions, requests, dependencies, customMetrics
| where timestamp > ago(30m)
| project timestamp, itemType, 
          name = coalesce(name, message, type),
          details = coalesce(outerMessage, message),
          customDimensions
| order by timestamp desc
```

**View all telemetry for the comprehensive demo:**
```kusto
union traces, exceptions, requests, dependencies, customMetrics
| where timestamp > ago(30m)
| where operation_Name == "GET /demo/all" or 
        cloud_RoleName == "fastapi-otel-azure"
| project timestamp, itemType, name, severityLevel, customDimensions
| order by timestamp desc
```

📝 **Try**: Call `/demo/all` and run this query to see ALL telemetry types!

---

### 10. Create Custom Workbooks

**Best for: Creating custom dashboards and reports**

1. Click **Workbooks** (left menu under "Monitoring")
2. Click **+ New**
3. Add visualizations:
   - Text (Markdown)
   - Metrics
   - Query-based charts
   - Filters
4. Save your workbook

**Example: Create a dashboard showing:**
- Total requests (counter)
- Error rate (chart)
- Exception list (table)
- Performance trends (timechart)

---

### 11. Set Up Alerts

**Best for: Proactive monitoring and incident response**

1. Click **Alerts** (left menu under "Monitoring")
2. Click **+ Create** → **Alert rule**
3. Configure:
   - **Scope**: Your Application Insights resource
   - **Condition**: 
     - Exception count > threshold
     - Response time > 1000ms
     - Custom metric threshold
   - **Actions**: Email, SMS, webhook
   - **Details**: Name and severity

---

### Quick Test Checklist

To verify your Azure Monitor integration is working, test each telemetry type:

- **Traces**: Call `/demo/trace` → Check Transaction search
- **Info Logs**: Call `/demo/info` → Check Logs (severity 1)
- **Warning Logs**: Call `/demo/warning` → Check Logs (severity 2)
- **Error Logs**: Call `/demo/error` → Check Logs (severity 3)
- **Exceptions**: Call `/demo/exception` → Check Failures blade
- **Metrics**: Call `/demo/metrics` → Check Metrics explorer
- **Dependencies**: Call `/demo/dependency` → Check Application map
- **Performance**: Call `/demo/slow` → Check Performance blade
- **All Types**: Call `/demo/all` → Check comprehensive query

---

### Common KQL Queries Reference

```sql
// Recent errors and exceptions
union traces, exceptions
| where severityLevel >= 3 or itemType == "exception"
| where timestamp > ago(1h)
| order by timestamp desc

// Request success rate
requests
| where timestamp > ago(1h)
| summarize total = count(), failures = countif(success == false)
| extend success_rate = 100.0 * (total - failures) / total

// Top slowest operations
requests
| where timestamp > ago(1h)
| summarize avg(duration), max(duration), count() by name
| order by avg_duration desc

// Dependency failure rate
dependencies
| where timestamp > ago(1h)
| summarize total = count(), failures = countif(success == false) by target
| extend failure_rate = 100.0 * failures / total
| order by failure_rate desc
```

## Telemetry Features

### Automatic Tracking (via OpenTelemetry)
- ✅ **HTTP requests** with duration and status codes (FastAPI auto-instrumentation)
- ✅ **Distributed tracing** across services
- ✅ **Exceptions** with full stack traces
- ✅ **Application logs** sent to Azure Monitor
- ✅ **Performance metrics** and dependencies

### Custom Tracking
The `telemetry.py` module provides functions for custom tracking:

```python
from app.telemetry import track_metric, track_event, get_tracer

# Track custom metric
track_metric("order_value", 99.99, {"currency": "USD", "region": "US"})

# Track custom event
track_event("user_signup", {"plan": "premium", "user_id": "12345"})

# Create custom spans for distributed tracing
tracer = get_tracer()
with tracer.start_as_current_span("process_order") as span:
    span.set_attribute("order.id", "ORDER-123")
    span.set_attribute("order.total", 99.99)
    # Your business logic here
```

## Troubleshooting

### Telemetry not appearing in Azure

1. **Check connection string**:
   ```bash
   # Verify environment variable is set
   echo $APPLICATIONINSIGHTS_CONNECTION_STRING  # Linux/Mac
   echo %APPLICATIONINSIGHTS_CONNECTION_STRING%  # Windows CMD
   $env:APPLICATIONINSIGHTS_CONNECTION_STRING   # Windows PowerShell
   ```

2. **Check application logs**:
   ```bash
   # Look for this message in console
   "OpenTelemetry with Azure Monitor configured"
   ```

3. **Wait longer**: Azure ingestion can take 2-5 minutes

4. **Check Azure resource**: Ensure Application Insights resource is not disabled

### Tests failing

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

3. **Check for errors**:
   ```bash
   # Look at application logs for errors
   uvicorn app.main:app --reload --log-level debug
   ```

---

## Advanced: Load Testing

Generate significant telemetry volume:

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/demo/all

# Using curl in a loop
for i in {1..100}; do
  curl -s http://localhost:8000/demo/all > /dev/null
  echo "Request $i completed"
done
```

**Then check in Azure:**
- **Live Metrics**: Watch real-time incoming telemetry
- **Performance**: See aggregated metrics
- **Application map**: View service topology

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure Monitor OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=python)
- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/instrumentation/python/)
- [Azure Application Insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [OpenTelemetry Python API](https://opentelemetry-python.readthedocs.io/)