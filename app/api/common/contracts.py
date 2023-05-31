from typing import Optional

from caseconverter import camelcase  # noqa: PyPI package name differs from actual
from pydantic import BaseModel


class JSONContract(BaseModel):
    """Base class for handling camelCase json naming format."""

    class Config:  # noqa
        alias_generator = camelcase
        allow_population_by_field_name = True


class HealthCheckResponse(JSONContract):
    """Response for health check endpoint."""

    api_title: str
    api_version: str
    api_description: str
    ram_total: int
    ram_available: int
    ram_usage: float
    cpu_count: Optional[int]
    cpu_freq_current: Optional[float]
    cpu_freq_min: Optional[float]
    cpu_freq_max: Optional[float]
    cpu_usage: float
    disk_total: int
    disk_used: int
    disk_usage: float
    net_bytes_out: int
    net_bytes_in: int
    net_packets_out: int
    net_packets_in: int
    net_errors_out: int
    net_errors_in: int
    net_dropped_out: int
    net_dropped_in: int
