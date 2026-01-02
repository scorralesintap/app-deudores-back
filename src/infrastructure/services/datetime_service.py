from datetime import datetime, timezone, timedelta
from src.infrastructure.config.settings import settings

class DatetimeService:
    TZ = timezone(timedelta(hours=settings.TIMEZONE_OFFSET))
    DEFAULT_FORMAT = "%d/%m/%Y %H:%M:%I"

    @staticmethod
    def to_local(dt: datetime) -> datetime:
        if dt is None:
            return None
        return dt.astimezone(DatetimeService.TZ)

    @staticmethod
    def format_datetime(dt: datetime, format: str | None = None) -> str:
        if dt is None:
            return ""
        local_dt = DatetimeService.to_local(dt)
        return local_dt.strftime(format or DatetimeService.DEFAULT_FORMAT)

    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def now_local() -> datetime:
        return datetime.now(DatetimeService.TZ)