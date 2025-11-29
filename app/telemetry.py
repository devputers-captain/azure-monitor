import logging

from azure.monitor.opentelemetry import configure_azure_monitor
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorLogExporter,
    AzureMonitorMetricExporter,
    AzureMonitorTraceExporter,
)
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import settings


def setup_telemetry(app) -> None:
    """
    Configure OpenTelemetry tracing, metrics, and logging for FastAPI and Azure Monitor.
    """
    connection_string = settings.applicationinsights_connection_string
    service_name = settings.otel_service_name or settings.app_name

    if not connection_string:
        # Basic warning - still allow app to run without telemetry
        logging.warning(
            "APPLICATIONINSIGHTS_CONNECTION_STRING is not set. "
            "Telemetry will not be sent to Azure Monitor."
        )
        return

    # Resource describing this service
    resource = Resource(attributes={
        SERVICE_NAME: service_name,
        "service.version": settings.app_version,
        "deployment.environment": settings.environment,
    })

    # ========== TRACES ==========
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    trace_exporter = AzureMonitorTraceExporter.from_connection_string(
        connection_string
    )
    span_processor = BatchSpanProcessor(trace_exporter)
    tracer_provider.add_span_processor(span_processor)

    # ========== METRICS ==========
    metric_reader = PeriodicExportingMetricReader(
        AzureMonitorMetricExporter.from_connection_string(connection_string)
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Configure Azure Monitor for live metrics
    configure_azure_monitor(
        connection_string=connection_string,
        enable_live_metrics=True,
        logger_name="app.main",
    )

    # ========== LOGS ==========
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    log_exporter = AzureMonitorLogExporter.from_connection_string(connection_string)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    # Attach OTEL handler to root logger
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    # ========== INSTRUMENTATION ==========
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    # Instrument requests library for external HTTP calls
    RequestsInstrumentor().instrument()

    # Instrument logging so logs are correlated with traces
    LoggingInstrumentor().instrument(set_logging_format=True)

    logging.getLogger(__name__).info(
        f"OpenTelemetry with Azure Monitor configured for {service_name}"
    )
