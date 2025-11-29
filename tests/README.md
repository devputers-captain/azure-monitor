# Testing Scripts

## Available Scripts

### 1. `test_http_errors.py` - HTTP Error Code Testing
**Purpose:** Test all HTTP error codes systematically

**Features:**
- ✅ Tests all error codes (400, 401, 403, 404, 429, 500, 503)
- ✅ Tests success cases (200)
- ✅ Colored output showing pass/fail
- ✅ Shows Azure Portal KQL queries
- ✅ Comprehensive test report

**Usage:**
```bash
python tests/test_http_errors.py
```

**Output:**
- Tests each error code endpoint
- Shows expected vs actual status
- Displays test summary
- Provides Azure Portal queries

---

### 2. `load_testing.py` - Load Testing
**Purpose:** Generate traffic for telemetry testing

**Features:**
- ✅ Random endpoint selection
- ✅ Mix of success and error responses
- ✅ Configurable iterations
- ✅ Quick results summary

**Usage:**
```bash
# Default: 20 requests
python tests/load_testing.py

# Custom: 50 requests
python tests/load_testing.py 50
```

**Output:**
- Real-time request status
- Success/error counts
- Error rate percentage

---

## Quick Comparison

| Feature | test_http_errors.py | load_testing.py |
|---------|---------------------|-----------------|
| **Purpose** | Validate error codes | Generate traffic |
| **Requests** | ~10 specific tests | 20+ random requests |
| **Output** | Detailed test report | Quick summary |
| **Use Case** | Testing/debugging | Load generation |
| **Azure Queries** | ✅ Included | ❌ Not included |

---

## Typical Workflow

1. **Start the application:**
   ```bash
   docker-compose up -d
   ```

2. **Test error codes:**
   ```bash
   python tests/test_http_errors.py
   ```

3. **Generate load (optional):**
   ```bash
   python tests/load_testing.py 50
   ```

4. **View in Azure Portal:**
   - Wait 2-5 minutes
   - Go to Application Insights → Failures
   - Or run KQL queries in Logs

---

## Requirements

Install dependencies:
```bash
pip install requests
```

Or install all project dependencies:
```bash
pip install -r requirements.txt
```

