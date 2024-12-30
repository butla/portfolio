from urllib.parse import urlencode

from sample_backend.main import app


def get_endpoint_url(
    endpoint_name: str, path_parameters: dict | None = None, query_parameters: dict | None = None
) -> str:
    """
    Get an endpoint URL.

    Args:
        endpoint_name: e.g. sample_backend.interface.routers.notes.get_all_notes.__name__
    """
    _path_parameters: dict = path_parameters or {}
    _query_parameters: dict = query_parameters or {}

    base_url = app.url_path_for(endpoint_name, **_path_parameters)
    return f"{base_url}?{urlencode(_query_parameters)}" if _query_parameters else base_url
