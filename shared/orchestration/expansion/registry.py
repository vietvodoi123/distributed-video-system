from __future__ import annotations

from typing import Type

from .base_expander import BaseTaskExpander


class ExpansionRegistry:

    def __init__(self):

        self._expanders: dict[
            Type[BaseTaskExpander],
            BaseTaskExpander
        ] = {}

    def register(
        self,
        expander_cls: Type[BaseTaskExpander],
    ) -> None:

        if expander_cls in self._expanders:
            return

        self._expanders[
            expander_cls
        ] = expander_cls()

    def unregister(
        self,
        expander_cls: Type[BaseTaskExpander],
    ) -> None:

        self._expanders.pop(
            expander_cls,
            None
        )

    def get(
        self,
        expander_cls: Type[BaseTaskExpander],
    ) -> BaseTaskExpander:

        try:

            return self._expanders[
                expander_cls
            ]

        except KeyError:

            raise RuntimeError(
                f"Expander not registered: "
                f"{expander_cls.__name__}"
            )

    async def expand(
            self,
            *,
            scheduler,
            expansion_task,
            expander_cls,
    ):

        expander = self.get(
            expander_cls
        )

        return await expander.expand(
            scheduler=scheduler,
            expansion_task=expansion_task,
        )