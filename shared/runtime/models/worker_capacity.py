from dataclasses import dataclass


@dataclass
class WorkerCapacity:

    cpu: float

    ram: float

    gpu: float

    network: float

    disk_io: float

    queue_pressure: float = 0

    @classmethod
    def from_dict(cls, data):

        return cls(**(data or {}))

    def total_cost(self):

        return (

            self.cpu * 4 +

            self.ram * 1 +

            self.gpu * 3 +

            self.network * 1 +

            self.disk_io * 1

            -

            self.queue_pressure
        )