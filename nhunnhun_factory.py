#!/usr/bin/env python3
"""
NHÀ MÁY SẢN XUẤT NỘI DUNG KOL AI TỰ ĐỘNG - KÊNH NHUN NHUN
Tác giả: Vũ Nguyễn (@nguyenvutnt)

Tính năng:
1. Kết nối Google Flow (Veo 3.1) để sinh các cảnh quay điện ảnh 9:16 có độ nhất quán cao.
2. Sinh giọng đọc Gen Z tự nhiên qua Edge-TTS (0 VNĐ).
3. Tự động biên dịch phụ đề động chuẩn viral TikTok/Reels (.ass).
4. Hậu kỳ ghép cảnh đa luồng qua FFmpeg.
5. Tự động xuất bản lên CDN công khai tốc độ cao.
"""

import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.voice_engine import VoiceEngine
from core.subtitle_builder import SubtitleBuilder
from core.video_composer import VideoComposer
from core.cdn_publisher import CdnPublisher
from scripts.batch_content_planner import TOPICS

def build_pilot():
    print("=" * 60)
    print(" BẮT ĐẦU SẢN XUẤT VIDEO PILOT: TẬP 1 - THỨ KHÓ BUÔNG NHẤT")
    print("=" * 60)

    audio_dir = BASE_DIR / "assets" / "audio"
    raw_dir = BASE_DIR / "assets" / "raw_video"
    out_dir = BASE_DIR / "assets" / "final_videos"

    mp3_file = audio_dir / "kol_monologue_01.mp3"
    vtt_file = audio_dir / "kol_monologue_01.vtt"
    ass_file = audio_dir / "kol_monologue_01.ass"
    final_video = out_dir / "nhunnhun_pilot_reel_01.mp4"

    # 1. Giọng nói
    print("[1/4] Tạo giọng nói truyền cảm Gen Z...")
    voice_engine = VoiceEngine(rate="+10%", pitch="+2Hz")
    script = TOPICS[0]["script"]
    voice_engine.synthesize(script, mp3_file, vtt_file)

    # 2. Phụ đề
    print("[2/4] Chuyển đổi phụ đề động ASS...")
    sub_builder = SubtitleBuilder()
    sub_builder.vtt_to_ass(vtt_file, ass_file)

    # 3. Ghép video đa cảnh
    print("[3/4] Hậu kỳ ghép video đa góc quay với FFmpeg...")
    shot1 = raw_dir / "shot_01_talking_cafe.mp4"
    shot2 = raw_dir / "shot_02_holding_phone.mp4"

    if not shot1.exists() or not shot2.exists():
        print(f"Lỗi: Thiếu tài nguyên video gốc tại {raw_dir}")
        return

    composer = VideoComposer(1080, 1920, 24)
    timeline = [
        {"video": shot1, "start": 0.0, "end": 4.93},
        {"video": shot2, "start": 0.0, "end": 8.13},
        {"video": shot1, "start": 4.0, "end": 8.05}
    ]
    composer.compose_multi_shot(timeline, mp3_file, ass_file, final_video)

    # 4. Xuất bản CDN
    print("[4/4] Đẩy video lên CDN công khai...")
    publisher = CdnPublisher()
    cdn_url = publisher.publish(final_video, "nhunnhun_pilot_01.mp4")

    print("\n" + "=" * 60)
    print(" XUẤT BẢN THÀNH CÔNG!")
    print(f" Video cục bộ: {final_video}")
    print(f" Đường dẫn trực tiếp: {cdn_url}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Nhà máy nội dung KOL ảo Nhun Nhun")
    parser.add_argument("--pilot", action="store_true", help="Dựng và xuất bản video Pilot")
    parser.add_argument("--list-topics", action="store_true", help="Hiển thị danh sách các chủ đề viral")
    args = parser.parse_args()

    if args.list_topics:
        for t in TOPICS:
            print(f"[{t['id']}] {t['title']} ({t['category']})")
            print(f"  Script: {t['script']}\n")
    else:
        build_pilot()

if __name__ == '__main__':
    main()
