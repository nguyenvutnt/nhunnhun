#!/usr/bin/env python3
"""
Bộ xử lý hậu kỳ video tự động (Video Composer) qua FFmpeg.
Hỗ trợ:
- Cắt và ghép nối nhiều góc quay (multi-shot sequencing).
- Đồng bộ hóa khẩu hình và nhịp điệu với tệp âm thanh chính.
- Nạp và đốt phụ đề động định dạng ASS chuẩn phong cách viral TikTok/Reels.
- Xuất bản độ phân giải Full HD 1080x1920 (9:16 portrait) tốc độ cao.
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

class VideoComposer:
    def __init__(self, output_width: int = 1080, output_height: int = 1920, fps: int = 24):
        self.width = output_width
        self.height = output_height
        self.fps = fps

    def compose_multi_shot(
        self,
        timeline: List[Dict[str, Any]],
        audio_path: Path,
        ass_subtitle_path: Path,
        output_path: Path,
        crf: int = 19
    ) -> Path:
        """
        timeline: Danh sách các phân cảnh dạng:
        [
            {"video": Path("..."), "start": 0.0, "end": 4.93},
            {"video": Path("..."), "start": 0.0, "end": 8.13},
            {"video": Path("..."), "start": 4.0, "end": 8.05}
        ]
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Xây dựng danh sách input files và filter_complex
        inputs = []
        filter_parts = []
        concat_labels = []

        video_index_map = {}
        curr_idx = 0

        for item in timeline:
            v_path = str(item["video"])
            if v_path not in video_index_map:
                video_index_map[v_path] = curr_idx
                inputs.extend(["-i", v_path])
                curr_idx += 1

        # Input audio
        audio_idx = curr_idx
        inputs.extend(["-i", str(audio_path)])

        for i, item in enumerate(timeline):
            v_idx = video_index_map[str(item["video"])]
            s = item["start"]
            e = item["end"]
            lbl = f"v{i}"
            filter_parts.append(
                f"[{v_idx}:v]trim={s}:{e},setpts=PTS-STARTPTS,"
                f"scale={self.width}:{self.height}:force_original_aspect_ratio=increase,"
                f"crop={self.width}:{self.height}[{lbl}];"
            )
            concat_labels.append(f"[{lbl}]")

        concat_clause = "".join(concat_labels) + f"concat=n={len(timeline)}:v=1:a=0[vcat];"
        filter_parts.append(concat_clause)

        # Đốt phụ đề ASS
        ass_str = str(ass_subtitle_path).replace("\\", "/").replace(":", "\\:")
        filter_parts.append(f"[vcat]ass='{ass_str}'[vfinal]")

        full_filter = "".join(filter_parts)

        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", full_filter,
            "-map", "[vfinal]",
            "-map", f"{audio_idx}:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", str(crf),
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(output_path)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg composite failed:\n{res.stderr}")

        return output_path
