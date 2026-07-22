from __future__ import annotations

import os
from apps.api.models.task import Task

from shared.contracts.capabilities.capabilities import (
    ANDROID_LINE_TASK,
)

from shared.contracts.enums.task_types import (
    LINE_TASK,
    MERGE_TTS_SEGMENTS,
)

from shared.orchestration.expansion.base_expander import (
    BaseTaskExpander,
)

from shared.orchestration.models.expansion_result import (
    ExpansionResult,
)

from shared.orchestration.models.spawn_task_definition import (
    SpawnTaskDefinition,
)


class TtsSegmentExpander(
    BaseTaskExpander,
):

    async def expand(
            self,
            *,
            scheduler,
            expansion_task: Task,
    ) -> ExpansionResult:

        result = (
                expansion_task.result
                or {}
        )

        # 1. Lấy chuỗi văn bản đã dịch từ kết quả của translate task
        translate_text = result.get("translated_text")

        if not translate_text:
            raise RuntimeError(
                f"Translate task {expansion_task.id} completed "
                f"but 'translate_text' is empty or missing!"
            )

        # 2. Cắt văn bản dịch theo từng dòng và loại bỏ khoảng trắng dư thừa
        raw_lines = translate_text.split("\n")
        lines = [line.strip() for line in raw_lines if line.strip()]

        definitions: list[
            SpawnTaskDefinition
        ] = []

        # Lấy thông tin voice cấu hình chung (nếu có trong payload gốc của translate task)
        # hoặc sử dụng một giọng đọc mặc định.
        voice = expansion_task.payload.get("voice", "vi-vn-x-vie-local") if expansion_task.payload else "vi-VN-Wavenet-A"

        # 3. Duyệt qua từng dòng và tạo định nghĩa SpawnTaskDefinition cho LINE_TASK
        for index, line_text in enumerate(lines):
            # Tự động tính toán output_path cho từng dòng con dựa trên batch/chapter
            # Ví dụ: "audio_line_0.mp3"
            output_path = f"batches/{expansion_task.batch_id}/chapters/{expansion_task.chapter_number}/tts/audio/audio_line_{index}.mp3"

            definitions.append(
                SpawnTaskDefinition(
                    task_type=LINE_TASK,
                    task_stage="tts",
                    required_capabilities=[
                        ANDROID_LINE_TASK,
                    ],
                    payload={
                        "line_index": index,
                        "line_text": line_text,
                        "voice": voice,
                        "output_path": output_path,
                    },
                )
            )

        return ExpansionResult(
            dynamic_tasks=definitions,
            downstream_task_types=[
                MERGE_TTS_SEGMENTS,
            ],
        )