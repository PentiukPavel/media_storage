from typing import Union

from pydantic import BaseModel


class BaseJsonLogSchema(BaseModel):
    """
    Схема основного тела лога в формате JSON.
    """

    thread: Union[int, str]
    level: int
    level_name: str
    message: str
    source: str
    duration: int
    exceptions: Union[list[str], str] = None
    trace_id: str = None
    span_id: str = None
    parent_id: str = None

    class ConfigDict:
        populate_by_name = True


class RequestJsonLogSchema(BaseModel):
    """
    Схема части запросов-ответов лога в формате JSON.
    """

    request_uri: str
    request_referer: str
    request_protocol: str
    request_method: str
    request_path: str
    request_host: str
    request_size: int
    request_content_type: str
    request_headers: str
    request_body: str
    request_direction: str
    remote_ip: str
    remote_port: int
    response_status_code: int
    response_size: int
    response_headers: str
    response_body: str
    duration: int
