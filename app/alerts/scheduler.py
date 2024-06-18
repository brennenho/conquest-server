import asyncio
from app.alerts.manager import AlertManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


# async task to check watchlist every minute
async def continuous_check():
    while True:
        try:
            await AlertManager.check_sections()
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in continuous check: {e}")
            await asyncio.sleep(60)
