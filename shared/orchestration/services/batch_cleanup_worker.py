import asyncio

from apps.api.db.session import (
    AsyncSessionLocal
)

from shared.orchestration.services.batch_cleanup_service import (
    BatchCleanupService
)


async def batch_cleanup_loop():

    print(
        "[BatchCleanupWorker] Started"
    )

    while True:

        try:

            async with AsyncSessionLocal() as db:

                service = BatchCleanupService(
                    db
                )

                await service.cleanup()


        except Exception as e:

            print(
                "[BatchCleanupWorker ERROR]",
                repr(e)
            )


        await asyncio.sleep(
            60
        )