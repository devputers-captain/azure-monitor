# Azure Monitor Demo API

Python Observability with Azure Monitor using OpenTelemetry - A FastAPI application integrated with Azure Application Insights for comprehensive telemetry tracking.

## Project Structure

```
azure-monitor/
│
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application with endpoints
│   ├── config.py            # Application configuration with Pydantic
│   └── telemetry.py         # Azure Monitor OpenTelemetry configuration
│
├── tests/
│   └── test_main.py         # Unit tests for the application
│
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Features

- 🚀 FastAPI-based REST API
- 📊 **Azure Application Insights integration using OpenTelemetry** (Microsoft recommended)
- 📝 Automatic request/response tracking with FastAPI instrumentation
- ⚠️ Exception tracking and logging
- 🔍 Custom metrics and events
- 📈 Distributed tracing support
- 🧪 Comprehensive test suite
- 🔧 Environment-based configuration with Pydantic

## Telemetry Types Demonstrated

This demo showcases **ALL** Azure Monitor telemetry types:

| Type | Description | Demo Endpoint | Azure View |
|------|-------------|---------------|------------|
| **Traces** | Distributed tracing with custom spans | `/demo/trace` | Transaction search, Application map |
| **Logs (Info)** | Informational messages | `/demo/info` | Logs (severity 1) |
| **Logs (Warning)** | Warning-level messages | `/demo/warning` | Logs (severity 2) |
| **Logs (Error)** | Error-level messages | `/demo/error` | Logs (severity 3) |
| **Exceptions** | Exception tracking with stack traces | `/demo/exception` | Failures blade |
| **Metrics** | Custom counters, histograms, gauges | `/demo/metrics` | Metrics explorer |
| **Dependencies** | External API/service calls | `/demo/dependency` | Application map, Dependencies |
| **Performance** | Request duration and slow operations | `/demo/slow` | Performance blade |
| **Requests** | Automatic HTTP request tracking | All endpoints | Requests blade |

✨ **Try `/demo/all`** to generate all telemetry types in a single request!

## Prerequisites

- Python 3.8 or higher
- Azure subscription with Application Insights resource
- pip package manager

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/devputers-captain/azure-monitor.git
   cd azure-monitor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update the `APPLICATIONINSIGHTS_CONNECTION_STRING` with your Azure Application Insights connection string

## Getting Azure Application Insights Connection String

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to your Application Insights resource (or create a new one)
3. In the Overview section, copy the **Connection String**
4. Paste it in your `.env` file

## Running the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Basic Endpoints
| Method | Endpoint        | Description                          |
|--------|----------------|--------------------------------------|
| GET    | `/`            | Root endpoint with all available endpoints |
| GET    | `/health`      | Health check endpoint                |

### Demo Endpoints - Telemetry Showcase

| Method | Endpoint            | Description                                      | Telemetry Type       |
|--------|---------------------|--------------------------------------------------|---------------------|
| GET    | `/demo/info`        | Generate INFO level log                          | Logs (Info)         |
| GET    | `/demo/warning`     | Generate WARNING level log                       | Logs (Warning)      |
| GET    | `/demo/error`       | Generate ERROR level log                         | Logs (Error)        |
| GET    | `/demo/exception`   | Trigger exception with tracking (query: error_type) | Exceptions       |
| GET    | `/demo/metrics`     | Generate custom metrics (counter, histogram, gauge) | Metrics          |
| GET    | `/demo/trace`       | Create custom traces with nested spans           | Traces              |
| GET    | `/demo/dependency`  | Track external HTTP dependency                   | Dependencies        |
| GET    | `/demo/slow`        | Simulate slow operation for performance tracking | Performance         |
| GET    | `/demo/all`         | Generate ALL telemetry types in one request      | All Types           |

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running Tests

Execute the test suite using pytest:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```
