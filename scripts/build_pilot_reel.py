#!/usr/bin/env python3
"""
Tự động dựng lại video Pilot (Tập 1 - Thứ khó buông bỏ nhất) từ assets có sẵn.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.video_composer import VideoComposer
from core.cdn_publisher import CdnPublisher

def main():
    raw_dir = BASE_DIR / 'assets' / 'raw_video'
    audio_dir = BASE_DIR / 'assets' / 'audio'
    out_dir = BASE_DIR / 'assets' / 'final_videos'

    shot1 = raw_dir / 'shot_01_talking_cafe.mp4'
    shot2 = raw_dir / 'shot_02_holding_phone.mp4'
    audio = audio_dir / 'kol_monologue_01.mp3'
    ass = audio_dir / 'kol_monologue_01.ass'
    final_output = out_dir / 'nhunnhun_pilot_reel_01.mp4'

    print("Bắt đầu xử lý hậu kỳ đa phân cảnh...")
    composer = VideoComposer(1080, 1920, 24)
    timeline = [
        {"video": shot1, "start": 0.0, "end": 4.93},
        {"video": shot2, "start": 0.0, "end": 8.13},
        {"video": shot1, "start": 4.0, "end": 8.05}
    ]

    composer.compose_multi_shot(timeline, audio, ass, final_output)
    print(f"Video hoàn tất tại: {final_output}")

    publisher = CdnPublisher()
    url = publisher.publish(final_output, "nhunnhun_pilot_01.mp4")
    print(f"Đã xuất bản lên CDN công khai: {url}")

if __name__ == '__main__':
    main()
