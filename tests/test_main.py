from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    """Test root endpoint returns message and endpoints list."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health():
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_demo_info_log():
    """Test INFO log demo endpoint."""
    response = client.get("/demo/info")
    assert response.status_code == 200
    assert "INFO log" in response.json()["message"]


def test_demo_warning_log():
    """Test WARNING log demo endpoint."""
    response = client.get("/demo/warning")
    assert response.status_code == 200
    assert "WARNING log" in response.json()["message"]


def test_demo_error_log():
    """Test ERROR log demo endpoint."""
    response = client.get("/demo/error")
    assert response.status_code == 200
    data = response.json()
    assert "ERROR log" in data["message"]
    assert data["error_logged"] is True


def test_demo_exception_runtime():
    """Test exception endpoint with runtime error."""
    response = client.get("/demo/exception?error_type=runtime")
    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower()


def test_demo_exception_http():
    """Test exception endpoint with HTTP error."""
    response = client.get("/demo/exception?error_type=http")
    assert response.status_code == 503


def test_demo_exception_zero_division():
    """Test exception endpoint with zero division error."""
    response = client.get("/demo/exception?error_type=zero_division")
    assert response.status_code == 500


def test_demo_metrics():
    """Test custom metrics endpoint."""
    response = client.get("/demo/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "request_count" in data["metrics"]
    assert "processing_time_ms" in data["metrics"]


def test_demo_custom_trace():
    """Test custom trace endpoint."""
    response = client.get("/demo/trace")
    assert response.status_code == 200
    assert "Custom trace" in response.json()["message"]


def test_demo_dependency_tracking():
    """Test dependency tracking endpoint."""
    response = client.get("/demo/dependency")
    # External API might fail, so we accept both 200 and 502
    assert response.status_code in [200, 502]
    if response.status_code == 200:
        data = response.json()
        assert "external_api" in data
        assert data["external_api"] == "jsonplaceholder.typicode.com"


def test_demo_slow_operation():
    """Test slow operation endpoint."""
    response = client.get("/demo/slow")
    assert response.status_code == 200
    data = response.json()
    assert "duration_seconds" in data
    assert data["duration_seconds"] > 0


def test_demo_all_telemetry():
    """Test comprehensive demo endpoint that generates all telemetry types."""
    response = client.get("/demo/all")
    # External API in /demo/all might fail, but endpoint should still return 200
    assert response.status_code == 200
    data = response.json()
    assert "telemetry_generated" in data
    assert "total_types" in data
    assert len(data["telemetry_generated"]) > 0
