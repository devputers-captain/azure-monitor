import logging
import random
import time
from typing import Optional

import requests
from app.telemetry import setup_telemetry
from fastapi import FastAPI, HTTPException, Query
from opentelemetry import metrics, trace

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI + OpenTelemetry + Azure Monitor",
    description="Comprehensive demo showcasing all Azure Monitor telemetry types",
    version="1.0.0",
)

# Configure OpenTelemetry & Azure Monitor
setup_telemetry(app)

# Get tracer and meter for custom telemetry
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Create custom metrics
request_counter = meter.create_counter(
    name="demo.requests.total",
    description="Total number of demo requests",
    unit="1",
)

processing_time_histogram = meter.create_histogram(
    name="demo.processing.duration",
    description="Processing duration in milliseconds",
    unit="ms",
)

active_users_gauge = meter.create_up_down_counter(
    name="demo.active_users",
    description="Number of active users",
    unit="1",
)

error_counter = meter.create_counter(
    name="demo.errors.total",
    description="Total number of errors",
    unit="1",
)

# Logger
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    """Root endpoint with basic info logging."""
    logger.info("Root endpoint accessed", extra={"user_action": "view_home"})
    return {
        "message": "Hello from FastAPI with OpenTelemetry & Azure Monitor!",
        "endpoints": {
            "health": "/health",
            "info_log": "/demo/info",
            "warning_log": "/demo/warning",
            "error_log": "/demo/error",
            "exception": "/demo/exception",
            "metrics": "/demo/metrics",
            "custom_trace": "/demo/trace",
            "dependency": "/demo/dependency",
            "slow_operation": "/demo/slow",
            "all_telemetry": "/demo/all",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.debug("Health check performed")
    return {"status": "healthy", "timestamp": time.time()}


@app.get("/demo/info")
async def demo_info_log():
    """Demonstrate INFO level logging."""
    logger.info(
        "This is an informational message",
        extra={
            "event_type": "user_action",
            "action": "demo_info",
            "user_id": "user123",
        },
    )
    return {"message": "INFO log sent to Azure Monitor"}


@app.get("/demo/warning")
async def demo_warning_log():
    """Demonstrate WARNING level logging."""
    logger.warning(
        "This is a warning message - something unusual happened",
        extra={
            "warning_type": "unusual_behavior",
            "severity": "medium",
            "component": "demo_service",
        },
    )
    return {"message": "WARNING log sent to Azure Monitor"}


@app.get("/demo/error")
async def demo_error_log():
    """Demonstrate ERROR level logging without raising an exception."""
    error_counter.add(1, {"error_type": "logged_error", "endpoint": "/demo/error"})
    logger.error(
        "This is an error message - operation failed",
        extra={
            "error_code": "ERR_001",
            "operation": "data_processing",
            "retry_count": 3,
        },
    )
    return {"message": "ERROR log sent to Azure Monitor", "error_logged": True}


@app.get("/demo/exception")
async def demo_exception(
    error_type: Optional[str] = Query(default="runtime", description="Type of error to raise")
):
    """
    Demonstrate exception tracking.
    Query params: error_type = runtime | http | zero_division
    """
    error_counter.add(1, {"error_type": error_type, "endpoint": "/demo/exception"})

    try:
        if error_type == "runtime":
            raise RuntimeError("This is a simulated runtime error for testing")
        elif error_type == "http":
            raise HTTPException(
                status_code=503, detail="Service temporarily unavailable"
            )
        elif error_type == "zero_division":
            result = 1 / 0  # This will raise ZeroDivisionError
        else:
            raise ValueError(f"Unknown error type: {error_type}")
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.exception(
            f"Exception occurred: {type(e).__name__}",
            extra={"error_type": error_type, "exception_class": type(e).__name__},
        )
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/demo/metrics")
async def demo_metrics():
    """Demonstrate custom metrics (counters, histograms, gauges)."""
    # Counter
    request_counter.add(1, {"endpoint": "/demo/metrics", "method": "GET"})

    # Histogram - simulate processing time
    processing_time = random.uniform(10, 500)
    processing_time_histogram.record(processing_time, {"operation": "demo_metrics"})

    # Gauge - simulate active users
    user_change = random.choice([-1, 1, 2])
    active_users_gauge.add(user_change, {"region": "us-east"})

    logger.info(
        f"Custom metrics recorded: processing_time={processing_time:.2f}ms, user_change={user_change}"
    )

    return {
        "message": "Custom metrics sent to Azure Monitor",
        "metrics": {
            "request_count": "+1",
            "processing_time_ms": round(processing_time, 2),
            "active_users_change": user_change,
        },
    }


@app.get("/demo/trace")
async def demo_custom_trace():
    """Demonstrate custom traces with spans and span attributes."""
    with tracer.start_as_current_span("custom_operation") as span:
        span.set_attribute("operation.type", "demo")
        span.set_attribute("user.id", "user456")
        span.set_attribute("custom.property", "example_value")

        # Simulate some work
        time.sleep(0.1)

        # Create a child span
        with tracer.start_as_current_span("sub_operation") as child_span:
            child_span.set_attribute("sub_task", "data_processing")
            time.sleep(0.05)
            child_span.add_event("Processing started")

            # Simulate processing
            data_size = random.randint(100, 1000)
            child_span.set_attribute("data.size", data_size)
            child_span.add_event(
                "Processing completed", {"records_processed": data_size}
            )

        span.add_event("Operation completed successfully")
        logger.info("Custom trace with nested spans created")

    return {"message": "Custom trace with nested spans sent to Azure Monitor"}


@app.get("/demo/dependency")
async def demo_dependency_tracking():
    """Demonstrate external dependency tracking (HTTP calls)."""
    with tracer.start_as_current_span("external_api_call") as span:
        span.set_attribute("dependency.type", "http")
        span.set_attribute("dependency.target", "jsonplaceholder.typicode.com")

        try:
            # Make an external HTTP call (this will be auto-instrumented)
            response = requests.get(
                "https://jsonplaceholder.typicode.com/posts/1", timeout=5
            )
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("dependency.success", True)

            logger.info(
                "External API called successfully",
                extra={
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                },
            )

            return {
                "message": "Dependency tracking demonstrated",
                "external_api": "jsonplaceholder.typicode.com",
                "status_code": response.status_code,
                "data": response.json(),
            }
        except Exception as e:
            span.set_attribute("dependency.success", False)
            span.record_exception(e)
            logger.error(f"External API call failed: {str(e)}")
            raise HTTPException(
                status_code=502, detail=f"External service error: {str(e)}"
            )


@app.get("/demo/slow")
async def demo_slow_operation():
    """Demonstrate performance tracking of slow operations."""
    with tracer.start_as_current_span("slow_operation") as span:
        duration = random.uniform(1, 3)
        span.set_attribute("operation.duration_seconds", duration)

        logger.warning(
            f"Starting slow operation (will take {duration:.2f}s)",
            extra={"performance_warning": True, "expected_duration": duration},
        )

        # Simulate slow operation
        time.sleep(duration)

        processing_time_histogram.record(
            duration * 1000, {"operation": "slow_operation"}
        )

        logger.info(
            "Slow operation completed",
            extra={"actual_duration": duration, "performance_impact": "high"},
        )

        return {
            "message": "Slow operation completed",
            "duration_seconds": round(duration, 2),
            "note": "Check Azure Monitor for performance metrics",
        }


@app.get("/demo/all")
async def demo_all_telemetry():
    """
    Comprehensive demo: Generate all types of telemetry in a single request.
    This is great for testing the full Azure Monitor integration.
    """
    with tracer.start_as_current_span("comprehensive_demo") as span:
        span.set_attribute("demo.type", "comprehensive")
        results = []

        # 1. INFO Log
        logger.info("Comprehensive demo started", extra={"demo_id": "all_telemetry"})
        results.append("✓ INFO log")

        # 2. WARNING Log
        logger.warning(
            "This is part of the comprehensive demo",
            extra={"warning_level": "informational"},
        )
        results.append("✓ WARNING log")

        # 3. Metrics
        request_counter.add(1, {"endpoint": "/demo/all", "demo": "comprehensive"})
        processing_time_histogram.record(250, {"operation": "comprehensive_demo"})
        active_users_gauge.add(1, {"region": "demo"})
        results.append("✓ Custom metrics (counter, histogram, gauge)")

        # 4. Custom span with events
        with tracer.start_as_current_span("demo_sub_operation") as sub_span:
            sub_span.add_event("Sub-operation started")
            time.sleep(0.1)
            sub_span.set_attribute("records_processed", 42)
            sub_span.add_event("Sub-operation completed")
        results.append("✓ Custom nested trace")

        # 5. Dependency call
        try:
            response = requests.get(
                "https://jsonplaceholder.typicode.com/users/1", timeout=5
            )
            span.set_attribute("dependency.called", True)
            results.append(f"✓ Dependency tracking (status: {response.status_code})")
        except Exception as e:
            logger.error(f"Dependency call failed: {str(e)}")
            results.append("✗ Dependency tracking (failed)")

        # 6. ERROR Log (without exception)
        logger.error(
            "Simulated error for demo purposes",
            extra={"is_demo": True, "error_code": "DEMO_ERR"},
        )
        error_counter.add(1, {"error_type": "simulated", "endpoint": "/demo/all"})
        results.append("✓ ERROR log")

        # 7. Exception handling (caught)
        try:
            raise ValueError("This is a controlled exception for demo")
        except ValueError as e:
            logger.exception("Caught exception in comprehensive demo")
            span.record_exception(e)
            results.append("✓ Exception (caught and logged)")

        logger.info(
            "Comprehensive demo completed",
            extra={"telemetry_types_generated": len(results)},
        )

        return {
            "message": "All telemetry types generated successfully!",
            "telemetry_generated": results,
            "total_types": len(results),
            "note": "Check Azure Monitor Application Insights in 2-5 minutes",
        }


# Global exception handler to track unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(
        f"Unhandled exception on {request.url.path}",
        extra={"path": request.url.path, "method": request.method},
    )
    return {
        "error": "Internal server error",
        "detail": str(exc),
        "path": request.url.path,
    }
