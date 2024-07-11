import asyncio

from app.alerts.manager import AlertManager
from app.utils.logger import get_logger
from app.utils.constants import WATCHLIST_CHECK_INTERVAL

logger = get_logger(__name__)


# Async task to check sections on watchlist every specified interval
async def continuous_check():
    while True:
        try:
            await AlertManager.check_sections()
            await asyncio.sleep(WATCHLIST_CHECK_INTERVAL)
        except asyncio.CancelledError:
            # Suppress error when server is manually stopped
            break
        except Exception as e:
            logger.error(f"Continuous check error: {e}")
            await asyncio.sleep(WATCHLIST_CHECK_INTERVAL)
