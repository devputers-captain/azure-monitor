# HTTP Error Tracking in Azure Monitor

## Quick Start

### Generate Test Errors
```bash
docker-compose up -d

curl http://localhost:8000/demo/http-errors/400  # Bad Request
curl http://localhost:8000/demo/http-errors/404  # Not Found
curl http://localhost:8000/demo/http-errors/500  # Server Error
```

### Run Test Script
```bash
python tests/test_http_errors.py
```

---

## Available Error Endpoints

| Code | Endpoint | Type |
|------|----------|------|
| 400 | `/demo/http-errors/400` | Client Error |
| 401 | `/demo/http-errors/401` | Client Error |
| 403 | `/demo/http-errors/403` | Client Error |
| 404 | `/demo/http-errors/404` | Client Error |
| 429 | `/demo/http-errors/429` | Client Error |
| 500 | `/demo/http-errors/500` | Server Error |
| 503 | `/demo/http-errors/503` | Server Error |

---

## View Errors in Azure Portal

### Method 1: Failures Blade (Visual)
1. Go to **Application Insights** → **Failures**
2. See failure rate, errors by status code
3. Click any status code to drill down

### Method 2: KQL Queries
Click **Logs** and run these queries

---

## Essential KQL Queries

### 1. All Failed Requests
```kusto
requests
| where timestamp > ago(1h)
| where success == false
| project timestamp, name, resultCode, duration
| order by timestamp desc
```

### 2. Count Errors by Status Code
```kusto
requests
| where timestamp > ago(24h)
| where success == false
| summarize ErrorCount = count() by resultCode
| order by ErrorCount desc
```

### 3. Client (4xx) vs Server (5xx) Errors
```kusto
requests
| where timestamp > ago(24h)
| where success == false
| extend resultCodeInt = toint(resultCode)
| extend ErrorType = case(
    resultCodeInt >= 400 and resultCodeInt < 500, "4xx Client Error",
    resultCodeInt >= 500, "5xx Server Error",
    "Other"
)
| summarize Count = count() by ErrorType
| render piechart
```

### 4. Error Rate Over Time
```kusto
requests
| where timestamp > ago(24h)
| summarize 
    Total = count(),
    Failed = countif(success == false)
    by bin(timestamp, 1h)
| extend ErrorRate = (Failed * 100.0) / Total
| render timechart
```

### 5. Top Failing Endpoints
```kusto
requests
| where timestamp > ago(24h)
| where success == false
| summarize FailureCount = count() by name, resultCode
| top 10 by FailureCount desc
```

### 6. Specific Error Code (e.g., 500)
```kusto
requests
| where timestamp > ago(1h)
| extend resultCodeInt = toint(resultCode)
| where resultCodeInt == 500
| project timestamp, name, url, duration
| order by timestamp desc
```

### 7. Error Spike Detection
```kusto
requests
| where timestamp > ago(24h)
| where success == false
| summarize ErrorCount = count() by bin(timestamp, 5m)
| where ErrorCount > 10
| order by timestamp desc
```

### 8. Errors with User Context
```kusto
requests
| where timestamp > ago(1h)
| where success == false
| extend user_id = tostring(customDimensions.user_id)
| project timestamp, name, resultCode, user_id
| order by timestamp desc
```

---

## Set Up Alerts

### Alert 1: High Error Count
**Condition:**
```kusto
requests
| where timestamp > ago(5m)
| where success == false
| summarize ErrorCount = count()
| where ErrorCount > 10
```

### Alert 2: 500 Errors
**Condition:**
```kusto
requests
| where timestamp > ago(5m)
| extend resultCodeInt = toint(resultCode)
| where resultCodeInt == 500
| summarize Count = count()
| where Count > 5
```

### Alert 3: Error Rate Threshold
**Condition:**
```kusto
requests
| where timestamp > ago(15m)
| summarize 
    Total = count(),
    Failed = countif(success == false)
| extend ErrorRate = (Failed * 100.0) / Total
| where ErrorRate > 10
```

---

## Quick Reference

| Need | Query |
|------|-------|
| All errors | `requests \| where success == false` |
| Count by code | `requests \| where success == false \| summarize count() by resultCode` |
| Error rate | `requests \| summarize Total = count(), Failed = countif(success == false) \| extend ErrorRate = (Failed * 100.0) / Total` |
| Specific code | `requests \| extend resultCodeInt = toint(resultCode) \| where resultCodeInt == 500` |

---

## Key Points

✅ Use `toint(resultCode)` for numeric comparisons  
✅ Use `tostring(customDimensions.field)` for custom fields  
✅ Wait 2-5 minutes for data ingestion  
✅ Use **Failures** blade for visual analysis  
✅ Use **Logs** for custom KQL queries  

---

## Test Checklist

- [ ] Errors appear in Azure Portal (wait 2-5 minutes)
- [ ] Can see errors in Failures blade
- [ ] KQL queries return data
- [ ] Can filter by status code
- [ ] Can see error trends over time
