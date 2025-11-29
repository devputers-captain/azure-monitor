# Azure Monitor Demo API

FastAPI application with Azure Application Insights - demonstrating telemetry tracking, HTTP error monitoring, and user context logging.

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/devputers-captain/azure-monitor.git
cd azure-monitor

# Configure (add your Azure connection string)
cp .env.example .env

# Run
docker-compose up -d

# Test
curl http://localhost:8000/health
```

**API:** http://localhost:8000  
**Docs:** http://localhost:8000/docs

---

## 🔑 Azure Setup

1. Go to [Azure Portal](https://portal.azure.com/)
2. Create **Application Insights** resource
3. Copy **Connection String**
4. Add to `.env`:
   ```
   APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
   ```

---

## 📊 Demo Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Generate telemetry
curl http://localhost:8000/demo/all

# Test HTTP errors
curl http://localhost:8000/demo/http-errors/500

# User context logging
curl "http://localhost:8000/demo/user-context?user_id=john&action=purchase"
```

---

## 🧪 Testing

```bash
# Test all HTTP error codes
python tests/test_http_errors.py

# Generate random load
python tests/load_testing.py

# Unit tests
pytest -v
```

---

## 📚 Documentation

All detailed guides are in separate files:

| Guide | Purpose |
|-------|---------|
| **[HTTP_ERROR_TRACKING_GUIDE.md](HTTP_ERROR_TRACKING_GUIDE.md)** | Track & query HTTP errors (400-503) |
| **[USER_CONTEXT_QUERIES.md](USER_CONTEXT_QUERIES.md)** | Filter logs by user_id, session, etc. |
| **[AZURE_MONITOR_GUIDE.md](AZURE_MONITOR_GUIDE.md)** | Complete Azure Portal guide |
| **[tests/README.md](tests/README.md)** | Testing scripts documentation |

---

## 🐳 Docker Commands

```bash
# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

## 💻 Local Development

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔗 Resources

- [Azure Monitor Docs](https://docs.microsoft.com/azure/azure-monitor/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

**For detailed Azure queries and examples, see the guide files above.**
