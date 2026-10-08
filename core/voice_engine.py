#!/usr/bin/env python3
import subprocess
from pathlib import Path
from typing import Tuple

class VoiceEngine:
    """
    Tạo giọng đọc Gen Z tự nhiên cho KOL Nhun Nhun bằng Edge-TTS chất lượng cao.
    Mặc định: vi-VN-HoaiMyNeural, điều chỉnh tốc độ và cao độ trẻ trung.
    """
    def __init__(self, voice: str = "vi-VN-HoaiMyNeural", rate: str = "+10%", pitch: str = "+2Hz"):
        self.voice = voice
        self.rate = rate
        self.pitch = pitch

    def synthesize(self, text: str, output_mp3: Path, output_vtt: Path) -> Tuple[Path, Path]:
        output_mp3.parent.mkdir(parents=True, exist_ok=True)
        output_vtt.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "edge-tts",
            "--voice", self.voice,
            "--rate", self.rate,
            "--pitch", self.pitch,
            "--text", text.strip(),
            "--write-media", str(output_mp3),
            "--write-subtitles", str(output_vtt)
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Edge-TTS error: {res.stderr}")
            
        return output_mp3, output_vtt
