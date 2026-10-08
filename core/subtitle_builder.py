#!/usr/bin/env python3
import re
from pathlib import Path

class SubtitleBuilder:
    """
    Chuyển đổi phụ đề VTT thành định dạng ASS phong cách viral TikTok/Reels:
    - Font to, rõ, viền đen dày, bóng đổ sâu chống chìm nền.
    - Màu sắc luân phiên Vàng / Trắng bắt mắt.
    - Căn chỉnh vị trí an toàn cho giao diện điện thoại (MarginV=380px).
    """

    ASS_HEADER = """[Script Info]
Title: TikTok Viral Subtitles - KOL Nhun Nhun
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTokYellow,Liberation Sans,68,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,50,50,380,1
Style: TikTokWhite,Liberation Sans,68,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,50,50,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    @staticmethod
    def _format_time(t_str: str) -> str:
        t_str = t_str.replace(',', '.')
        parts = t_str.split(':')
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
        return f"{h}:{m:02d}:{s:05.2f}"

    def vtt_to_ass(self, vtt_path: Path, ass_path: Path) -> Path:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = re.findall(
            r'(\d\d:\d\d:\d\d[,\.]\d\d\d)\s*-->\s*(\d\d:\d\d:\d\d[,\.]\d\d\d)\n(.*?)(?=\n\n|\Z)',
            content,
            re.DOTALL
        )

        events = []
        for idx, (st, et, text) in enumerate(blocks):
            clean_text = ' '.join(text.strip().split())
            start_fmt = self._format_time(st)
            end_fmt = self._format_time(et)

            words = clean_text.split()
            if len(words) > 7:
                mid = len(words) // 2
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:])
                dialogue_text = f"{line1}\\N{line2}"
            else:
                dialogue_text = clean_text

            style = "TikTokYellow" if idx % 2 == 0 else "TikTokWhite"
            events.append(f"Dialogue: 0,{start_fmt},{end_fmt},{style},,0,0,0,,{dialogue_text}")

        ass_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ass_path, 'w', encoding='utf-8') as f:
            f.write(self.ASS_HEADER + "\n".join(events) + "\n")

        return ass_path
