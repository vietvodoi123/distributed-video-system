import asyncio
import logging

from apps.api.db.session import AsyncSessionLocal
from shared.orchestration.services.retry_service import (
    RetryService,
)

logger = logging.getLogger(__name__)

DEFAULT_INTERVAL_SECONDS = 60


async def retry_loop():
    """
    Background retry worker.

    This loop intentionally contains no business logic.

    Responsibilities:
        1. Recover expired task leases.
        2. Retry failed tasks.

    The RetryService owns all retry logic.
    This loop only executes it periodically.
    """

    while True:

        try:

            async with AsyncSessionLocal() as db:

                service = RetryService(
                    db
                )

                recovered = (
                    await service.recover_expired_leases()
                )

                retried = (
                    await service.retry_failed_tasks()
                )

                if recovered or retried:

                    logger.info(
                        "[RetryLoop] recovered=%s retried=%s",
                        recovered,
                        retried,
                    )

        except asyncio.CancelledError:
            logger.info(
                "[RetryLoop] stopped."
            )
            raise

        except Exception:

            logger.exception(
                "[RetryLoop] unexpected error."
            )

        await asyncio.sleep(
            DEFAULT_INTERVAL_SECONDS
        )