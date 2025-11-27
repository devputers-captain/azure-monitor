"""Application configuration using environment variables."""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Settings
    app_name: str = Field(default="azure-monitor-demo", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Azure Monitor Configuration
    applicationinsights_connection_string: str | None = Field(
        default=None, 
        alias="APPLICATIONINSIGHTS_CONNECTION_STRING"
    )
    applicationid: str | None = Field(
        default=None,
        description="Azure Application Insights Application ID"
    )
    
    # OpenTelemetry Configuration
    otel_service_name: str = Field(
        default="fastapi-otel-azure",
        description="OpenTelemetry service name"
    )
    
    # Logging Configuration
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields instead of raising errors
    )


# Global settings instance
settings = Settings()

