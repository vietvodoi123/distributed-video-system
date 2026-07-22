from datetime import datetime

from sqlalchemy import select

from apps.api.models.worker import Worker


class WorkerService:

    def __init__(
        self,
        db,
    ):
        self.db = db

    async def heartbeat(
        self,
        *,
        worker_id: str,
        worker_type: str,
        capabilities: list[str],
        resource_capacity: dict | None = None,
        battery: int | None = None,
        temperature: int | None = None,
        is_charging: bool | None = None,
        tailscale_ip: str | None = None,
    ) -> Worker:

        worker = await self.db.scalar(
            select(Worker).where(
                Worker.worker_id == worker_id
            )
        )

        if worker is None:

            worker = Worker(

                worker_id=worker_id,

                worker_type=worker_type,

                capabilities=capabilities,

                free_slots=0,

                max_concurrency=0,

                battery=battery,

                temperature=temperature,

                is_charging=is_charging,

                tailscale_ip=tailscale_ip,

                status="online",

                resource_capacity=resource_capacity or {},

                last_heartbeat=datetime.utcnow(),
            )

            self.db.add(worker)

        else:

            worker.worker_type = worker_type

            worker.capabilities = capabilities

            worker.resource_capacity = (
                resource_capacity or {}
            )

            worker.battery = battery

            worker.temperature = temperature

            worker.is_charging = is_charging

            worker.tailscale_ip = tailscale_ip

            worker.status = "online"

            worker.last_heartbeat = datetime.utcnow()

        await self.db.flush()

        return worker