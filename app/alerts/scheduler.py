import asyncio
from app.alerts.manager import AlertManager


async def continuous_check():
    while True:
        await AlertManager.check_sections()
        await asyncio.sleep(60)
