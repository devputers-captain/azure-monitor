# User Context Filtering in Azure Monitor

## Quick Start

### Log with User Context
```python
logger.info("User action", extra={
    "user_id": "john_doe",
    "action": "purchase",
    "country": "US"
})
```

### Test It
```bash
curl "http://localhost:8000/demo/user-context?user_id=john_doe&action=purchase"
```

---

## Essential Azure Queries

Go to **Application Insights → Logs**

### 1. Filter by Specific User
```kusto
traces
| where timestamp > ago(1h)
| where tostring(customDimensions.user_id) == "john_doe"
| project timestamp, message, 
    user_id = tostring(customDimensions.user_id),
    action = tostring(customDimensions.action)
| order by timestamp desc
```

### 2. Count Actions by User
```kusto
traces
| where timestamp > ago(24h)
| where customDimensions.user_id != ""
| summarize Actions = count() by 
    User = tostring(customDimensions.user_id),
    Action = tostring(customDimensions.action)
| order by Actions desc
```

### 3. Find Users with Errors
```kusto
traces
| where timestamp > ago(1h)
| where severityLevel >= 3
| where customDimensions.user_id != ""
| project timestamp, 
    user_id = tostring(customDimensions.user_id),
    message
| order by timestamp desc
```

### 4. Top Active Users
```kusto
traces
| where timestamp > ago(24h)
| summarize ActivityCount = count() 
    by User = tostring(customDimensions.user_id)
| top 10 by ActivityCount desc
```

### 5. User Activity Timeline
```kusto
traces
| where timestamp > ago(1h)
| where tostring(customDimensions.user_id) == "john_doe"
| project timestamp, 
    action = tostring(customDimensions.action),
    message
| order by timestamp asc
```

---

## Common Custom Dimensions

```python
extra={
    "user_id": "user123",        # Filter by user
    "session_id": "sess_456",    # Track sessions
    "action": "purchase",         # User action
    "country": "US",              # Geography
    "device": "mobile"            # Device type
}
```

---

## Quick Reference

| Need | Query |
|------|-------|
| One user's logs | `traces \| where tostring(customDimensions.user_id) == "USER_ID"` |
| User's errors | `traces \| where tostring(customDimensions.user_id) == "USER_ID" and severityLevel >= 3` |
| Count by user | `traces \| summarize count() by tostring(customDimensions.user_id)` |
| Top users | `traces \| summarize count() by tostring(customDimensions.user_id) \| top 10 by count_` |

---

## That's It!

1. Log with `extra={"user_id": "..."}`
2. Wait 2-5 minutes
3. Query: `traces | where tostring(customDimensions.user_id) == "your_user"`
