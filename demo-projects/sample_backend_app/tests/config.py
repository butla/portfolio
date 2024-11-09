from sample_backend.config import AppConfig


class AppTestsConfig(AppConfig):
    """Config for values only used in tests."""

    api_port: int = 8080
