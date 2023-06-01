import psutil
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, FastAPI, Request, status

from .contracts import HealthCheckResponse
from .dependencies import Container
from .settings import FastAPISettings

router = APIRouter()


@inject
def bootstrap(
    app: FastAPI,
    fastapi_settings: FastAPISettings = Provide[Container.fastapi_settings],
) -> FastAPI:
    """Initialize common FastAPI endpoints.

    Args:
        app (FastAPI): to bootstrap with common endpoints.

    Returns:
        FastAPI: bootstrapped with common endpoints.
    """
    if fastapi_settings.USE_DEFAULT_PING:
        router.add_api_route(
            methods=["GET"],
            path="/ping",
            endpoint=get_ping,
            description="Check if server is up and running",
            status_code=status.HTTP_204_NO_CONTENT,
        )

    if fastapi_settings.USE_DEFAULT_HEALTH:
        router.add_api_route(
            methods=["GET"],
            path="/health",
            endpoint=get_health,
            description="Check API health",
            status_code=status.HTTP_200_OK,
            response_model=HealthCheckResponse,
        )

    app.include_router(router, tags=["Common"])

    return app


def get_ping() -> None:  # noqa
    return


# TODO discus if this endpoint is actually needed there, or can be placed in some
# internal common library
def get_health(request: Request) -> HealthCheckResponse:  # noqa
    try:
        cpu_stats = psutil.cpu_freq()
    except FileNotFoundError:
        # this error occurs on MacOS M1/M1 Pro/M2 processors
        # see https://github.com/giampaolo/psutil/issues/1892
        cpu_stats = None
    ram_stats = psutil.virtual_memory()
    disk_stats = psutil.disk_usage("/")
    net_stats = psutil.net_io_counters()

    return HealthCheckResponse(
        # API info
        api_title=request.app.title,
        api_version=request.app.version,
        api_description=request.app.description,
        # CPU stats
        cpu_count=psutil.cpu_count(),
        cpu_freq_min=cpu_stats.min if cpu_stats else 0.0,
        cpu_freq_max=cpu_stats.max if cpu_stats else 0.0,
        cpu_freq_current=cpu_stats.current if cpu_stats else 0.0,
        cpu_usage=psutil.cpu_percent(),
        # RAM stats
        ram_total=ram_stats.total,
        ram_available=ram_stats.available,
        ram_usage=ram_stats.percent,
        # Disk stats
        disk_total=disk_stats.total,
        disk_used=disk_stats.used,
        disk_usage=disk_stats.percent,
        # Network stats
        net_bytes_out=net_stats.bytes_sent,
        net_bytes_in=net_stats.bytes_recv,
        net_packets_out=net_stats.packets_sent,
        net_packets_in=net_stats.packets_recv,
        net_errors_out=net_stats.errout,
        net_errors_in=net_stats.errin,
        net_dropped_out=net_stats.dropout,
        net_dropped_in=net_stats.dropin,
    )
