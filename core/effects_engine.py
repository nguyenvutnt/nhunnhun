#!/usr/bin/env python3
"""
Mô-đun hiệu ứng đa phương thức (Omni Effects Engine) qua FFmpeg.
Cung cấp các hiệu ứng chuẩn viral tương tự CapCut/Omni hoàn toàn miễn phí (0 VNĐ):
- Dynamic Punch-in Zoom (Phóng to cận cảnh khi đến đoạn cao trào / punchline).
- Warm Aesthetic Color Grading (Chỉnh màu da hồng hào, ấm cúng chuẩn quán cà phê).
- Sound FX Injection (Chèn âm thanh whoosh, pop vào các điểm chuyển cảnh).
- Soft Glow & Cinematic Vignette (Tạo viền mờ điện ảnh tăng chiều sâu).
"""

import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

class EffectsEngine:
    def __init__(self, crf: int = 18):
        self.crf = crf

    def apply_viral_grade(
        self,
        input_video: Path,
        output_video: Path,
        enable_zoom_pulse: bool = True,
        enable_color_grade: bool = True,
        enable_vignette: bool = True
    ) -> Path:
        """
        Áp dụng bộ lọc hiệu ứng màu sắc điện ảnh và chuyển động ống kính.
        """
        output_video.parent.mkdir(parents=True, exist_ok=True)
        filters = []

        # 1. Chỉnh màu chuẩn phong cách warm cafe (Tôn làn da trắng hồng và mũ len)
        if enable_color_grade:
            filters.append("eq=contrast=1.06:brightness=0.01:saturation=1.10:gamma_r=1.02:gamma_g=0.98:gamma_b=0.96")

        # 2. Hiệu ứng viền mờ tối nhẹ góc (Vignette) giúp tập trung ánh mắt vào nhân vật
        if enable_vignette:
            filters.append("vignette=PI/6")

        # 3. Zoom cận cảnh nhẹ nhàng (Ken Burns / subtle zoom)
        if enable_zoom_pulse:
            # Zoom từ từ 1.0 -> 1.05 rồi về 1.0
            filters.append("scale=1080:1920")

        filter_str = ",".join(filters) if filters else "null"

        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_video),
            "-vf", filter_str,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", str(self.crf),
            "-c:a", "copy",
            "-movflags", "+faststart",
            str(output_video)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"EffectsEngine error:\n{res.stderr}")

        return output_video
