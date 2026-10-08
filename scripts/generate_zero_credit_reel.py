#!/usr/bin/env python3
"""
NHÀ MÁY SẢN XUẤT VIDEO 0 CREDIT (ZERO-CREDIT PIPELINE).
Tạo video triệu view hoàn toàn không tốn credit Google Flow (0 Credit, 0 VNĐ):
- Tận dụng kho cảnh quay chuẩn (Raw Assets) đã sinh từ Veo 3.1.
- Sinh giọng đọc mới chuẩn Gen Z qua Edge-TTS (0 VNĐ).
- Sinh phụ đề động TikTok Vàng/Trắng qua SubtitleBuilder (0 VNĐ).
- Tự động cắt đảo góc quay, phóng to Punch-in và chỉnh màu qua EffectsEngine (0 VNĐ).
- Xuất bản lên CDN công khai (0 VNĐ).
"""

import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.voice_engine import VoiceEngine
from core.subtitle_builder import SubtitleBuilder
from core.video_composer import VideoComposer
from core.effects_engine import EffectsEngine
from core.cdn_publisher import CdnPublisher
from scripts.batch_content_planner import TOPICS

def make_zero_credit_reel(topic_idx: int = 1):
    topic = TOPICS[topic_idx]
    print("=" * 65)
    print(f" SẢN XUẤT VIDEO 0 CREDIT: [{topic['id']}] {topic['title']}")
    print("=" * 65)

    audio_dir = BASE_DIR / "assets" / "audio"
    raw_dir = BASE_DIR / "assets" / "raw_video"
    out_dir = BASE_DIR / "assets" / "final_videos"

    topic_slug = topic["id"].lower()
    mp3_file = audio_dir / f"{topic_slug}_voice.mp3"
    vtt_file = audio_dir / f"{topic_slug}_voice.vtt"
    ass_file = audio_dir / f"{topic_slug}_subtitles.ass"
    composite_video = out_dir / f"{topic_slug}_composite.mp4"
    final_graded_video = out_dir / f"{topic_slug}_zero_credit_final.mp4"

    # 1. Thu âm giọng đọc mới (0 VNĐ)
    print(f"[1/4] Tạo giọng nói cho kịch bản: '{topic['title']}'...")
    voice_engine = VoiceEngine(rate="+11%", pitch="+2Hz")
    voice_engine.synthesize(topic["script"], mp3_file, vtt_file)

    # 2. Tạo phụ đề động (0 VNĐ)
    print("[2/4] Chuyển đổi phụ đề động ASS chuẩn viral...")
    sub_builder = SubtitleBuilder()
    sub_builder.vtt_to_ass(vtt_file, ass_file)

    # 3. Ghép nối đa cảnh từ kho video Veo 3.1 có sẵn (0 CREDIT!)
    print("[3/4] Cắt ghép đảo phân cảnh đa góc quay (0 Credit)...")
    shot1 = raw_dir / "shot_01_talking_cafe.mp4"
    shot2 = raw_dir / "shot_02_holding_phone.mp4"

    composer = VideoComposer(1080, 1920, 24)
    # Timeline đa phân cảnh luân phiên 3 shot
    timeline = [
        {"video": shot1, "start": 0.5, "end": 5.2},
        {"video": shot2, "start": 0.2, "end": 7.8},
        {"video": shot1, "start": 3.8, "end": 8.0}
    ]
    composer.compose_multi_shot(timeline, mp3_file, ass_file, composite_video)

    # 4. Áp dụng hiệu ứng màu điện ảnh & Vignette (0 VNĐ)
    print("[4/4] Áp dụng bộ lọc màu da ấm & Vignette điện ảnh...")
    effects = EffectsEngine()
    effects.apply_viral_grade(composite_video, final_graded_video)

    # Xuất bản CDN
    publisher = CdnPublisher()
    cdn_url = publisher.publish(final_graded_video, f"nhunnhun_{topic_slug}.mp4")

    print("\n" + "=" * 65)
    print(" XUẤT BẢN THÀNH CÔNG (TIÊU TỐN: 0 CREDIT FLOW, 0 VNĐ)!")
    print(f" Video thành phẩm: {final_graded_video}")
    print(f" Link xem trực tiếp: {cdn_url}")
    print("=" * 65)
    return cdn_url

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=int, default=1, help="Index chủ đề (1: Giảm cân, 2: Ngủ nướng, 3: Eyeliner)")
    args = parser.parse_args()
    make_zero_credit_reel(args.topic)
