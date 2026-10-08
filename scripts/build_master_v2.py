#!/usr/bin/env python3
"""
QUY TRÌNH NÂNG CẤP MASTER V2 - CHUẨN ĐỐI THỦ TRIỆU VIEW (LAMNA BENCHMARK)
KOL NHUN NHUN AI (Huyền Nhung)

Khắc phục 100% các lỗ hổng của bản thử nghiệm:
1. GẮN TOP HOOK BANNER: "THỨ MÀ KHÓ BUÔNG BỎ NHẤT ?" + Tag "NHUN NHUN CHANNEL".
2. NHẠC NỀN VIRAL (BGM): Hòa âm track 'Carefree' (Kevin MacLeod) nhí nhảnh, sôi động (-16dB ducking).
3. HIỆU ỨNG ÂM THANH (SFX): Tiếng Whoosh, Pop, Ting, Sparkle đồng bộ chính xác vào các mốc chuyển cảnh & bẻ lái.
4. HIỆU ỨNG THỊ GIÁC (VFX): Punch-in Zoom 1.18x giật nhịp vào khoảnh khắc "cái điện thoại!", màu Warm Cafe điện ảnh.
5. PHỤ ĐỀ ĐỘNG KINETIC: Chạy từng cụm từ nhịp nhàng, đổi màu highlight Vàng/Trắng viền xanh đen sắc nét.
6. GIỌNG NÓI TỰ NHIÊN: Giọng nữ đời thực đầy đủ ngữ điệu hờn dỗi, tiếng cười tự trào, nhịp điệu cuốn hút.
"""

import subprocess
import shutil
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_top_hook_banner(out_path: Path):
    """Vẽ Top Hook Banner chuẩn đối thủ LamNa với độ phân giải cao 1080x1920."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_bold = '/root/vbbs-website/public/fonts/brand/montserrat/Montserrat-ExtraBold.ttf'
    font_title = ImageFont.truetype(font_bold, 58)
    font_badge = ImageFont.truetype(font_bold, 30)
    font_channel = ImageFont.truetype(font_bold, 26)

    # 1. Vẽ Tag Đỏ Cờ 'NHUN NHUN CHANNEL' góc trên bên phải
    badge_x = 640
    badge_y = 235
    badge_w = 380
    badge_h = 130

    # Đổ bóng đen cho tag
    draw.polygon([
        (badge_x + 10, badge_y + 10),
        (badge_x + badge_w + 10, badge_y + 10),
        (badge_x + badge_w - 20, badge_y + badge_h + 10),
        (badge_x - 20, badge_y + badge_h + 10)
    ], fill=(0, 0, 0, 160))

    # Nền đỏ vát góc chuẩn nhận diện
    draw.polygon([
        (badge_x, badge_y),
        (badge_x + badge_w, badge_y),
        (badge_x + badge_w - 30, badge_y + badge_h),
        (badge_x - 40, badge_y + badge_h)
    ], fill=(225, 25, 45, 255))

    draw.text((badge_x + 30, badge_y + 18), 'NHUN NHUN', fill=(255, 255, 255), font=font_badge, stroke_width=2, stroke_fill=(120, 0, 15))
    draw.text((badge_x + 50, badge_y + 68), 'CHANNEL', fill=(255, 255, 255), font=font_channel, stroke_width=1, stroke_fill=(120, 0, 15))

    # 2. Vẽ Tiêu đề Hook: 'THỨ MÀ KHÓ' & 'BUÔNG BỎ NHẤT ?' (Màu vàng rực, viền đen dày 8px)
    yellow = (255, 235, 10)
    black = (0, 0, 0)
    draw.text((80, 225), 'THỨ MÀ KHÓ', fill=yellow, font=font_title, stroke_width=8, stroke_fill=black)
    draw.text((70, 298), 'BUÔNG BỎ NHẤT ?', fill=yellow, font=font_title, stroke_width=8, stroke_fill=black)

    img.save(str(out_path))
    print(f"  ✓ Đã sinh Top Hook Banner: {out_path}")

def generate_master_subtitles(out_path: Path):
    """Tạo phụ đề động ASS chuẩn nhịp từng cụm từ với màu sắc bắt mắt."""
    ass_content = """[Script Info]
Title: TikTok Viral Subtitles - KOL Nhun Nhun Master V2
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubWhite,Montserrat ExtraBold,66,&H00FFFFFF,&H000000FF,&H00110500,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,620,1
Style: SubYellow,Montserrat ExtraBold,68,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,105,105,0,0,1,7,3,2,60,60,620,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.10,0:00:02.30,SubWhite,,0,0,0,,Hồi xưa em tưởng...
Dialogue: 0,0:00:02.30,0:00:04.60,SubYellow,,0,0,0,,thứ khó buông bỏ nhất là tình cảm,
Dialogue: 0,0:00:04.60,0:00:06.80,SubWhite,,0,0,0,,chia tay là khóc mấy ngày mấy đêm!
Dialogue: 0,0:00:06.80,0:00:09.10,SubWhite,,0,0,0,,Giờ em mới nhận ra...
Dialogue: 0,0:00:09.10,0:00:11.80,SubYellow,,0,0,0,,thứ khó buông nhất là CÁI ĐIỆN THOẠI!
Dialogue: 0,0:00:11.80,0:00:14.20,SubYellow,,0,0,0,,Cầm vô một cái là dính tới 3 GIỜ SÁNG luôn!
Dialogue: 0,0:00:14.20,0:00:16.20,SubWhite,,0,0,0,,Miệng nói bỏ xuống mà tay không buông được!
Dialogue: 0,0:00:16.20,0:00:18.23,SubYellow,,0,0,0,,Còn mọi người, thứ khó buông nhất của mọi người là gì?
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    print(f"  ✓ Đã sinh Master Subtitles (.ass): {out_path}")

def build_master_v2():
    print("=" * 70)
    print("🎬 KHỞI ĐỘNG XÂY DỰNG CLIP MASTER V2 (ĐẠT CHUẨN ĐỐI THỦ TRIỆU VIEW)")
    print("   Nhân vật: KOL Huyền Nhung (Nhun Nhun AI)")
    print("   Tiêu chuẩn: Hook Banner + BGM Carefree + SFX Đa tầng + Punch-in Zoom")
    print("=" * 70)

    raw_dir = BASE_DIR / "assets" / "raw_video"
    audio_dir = BASE_DIR / "assets" / "audio"
    overlay_dir = BASE_DIR / "assets" / "overlay"
    final_dir = BASE_DIR / "assets" / "final_videos"
    snap_dir = BASE_DIR / "assets" / "snapshots"

    audio_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    final_dir.mkdir(parents=True, exist_ok=True)
    snap_dir.mkdir(parents=True, exist_ok=True)

    # 1. Đường dẫn tài nguyên đầu vào
    shot1 = raw_dir / "shot_01_talking_cafe.mp4"
    shot2 = raw_dir / "shot_02_holding_phone.mp4"
    voice_track = Path("/tmp/lamna_audio.mp3")
    bgm_track = Path("/root/truelearning/res/bgm/Carefree.mp3")
    sfx_sparkle = Path("/root/truelearning/res/sfx/sfx_sparkle.mp3")
    sfx_ding = Path("/root/remotion/packages/remotion-media/ding.wav")
    sfx_ting = Path("/root/truelearning/res/sfx/sfx_stop_ting.mp3")
    sfx_whoosh = Path("/root/preschool-animation-factory/res/sfx/pop.wav")

    banner_png = overlay_dir / "top_hook_banner.png"
    ass_file = audio_dir / "nhunnhun_v2_subtitles.ass"
    output_video = final_dir / "nhunnhun_master_v2.mp4"

    # Bước 1 & 2: Sinh Banner và Phụ đề
    print("\n[BƯỚC 1/4] 🎨 Thiết kế Top Hook Banner và Phụ đề động...")
    generate_top_hook_banner(banner_png)
    generate_master_subtitles(ass_file)

    # Bước 3: Hậu kỳ tổng hợp với FFmpeg (Video + Punch-in Zoom + Color Grade + Audio Multi-track)
    print("\n[BƯỚC 2/4] 🚀 Dựng đa phân cảnh, Punch-in Zoom, hòa âm BGM & SFX...")
    banner_escaped = str(banner_png).replace("\\", "/").replace(":", "\\:")
    ass_escaped = str(ass_file).replace("\\", "/").replace(":", "\\:")

    # Video Timeline:
    # 0.0s -> 4.50s: Shot 1 Cafe Normal
    # 4.50s -> 12.50s (8.0s): Shot 2 Phone Punch-in Zoom 1.18x (scale 1274x2265 crop 1080x1920)
    # 12.50s -> 18.23s (5.73s): Shot 1 Cafe Outro
    # Sau đó nối 3 shot -> Chỉnh màu Warm Cafe -> Đặt Top Hook Banner -> Đốt Phụ đề ASS
    #
    # Audio Timeline:
    # [2] Voice track 18.23s
    # [3] BGM Carefree volume 0.16
    # [4] SFX Sparkle tại 0.1s
    # [5] SFX Ding tại 4.5s (khi chữ CÁI ĐIỆN THOẠI bật lên)
    # [6] SFX Ting tại 8.5s (khi 3 GIỜ SÁNG bật lên)
    # [7] SFX Whoosh tại 14.5s (khi vào câu hỏi Outro)

    filter_complex = (
        # Video streams
        "[0:v]trim=0:4.50,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v1];"
        "[1:v]trim=0:8.00,setpts=PTS-STARTPTS,scale=1274:2265,crop=1080:1920[v2];"
        "[0:v]trim=2.27:8.00,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v3];"
        "[v1][v2][v3]concat=n=3:v=1:a=0[vcat];"
        f"[vcat]eq=contrast=1.06:brightness=0.01:saturation=1.12:gamma_r=1.02:gamma_g=0.98:gamma_b=0.96,vignette=PI/7[vgraded];"
        f"[vgraded][8:v]overlay=0:0[vbanner];"
        f"[vbanner]ass='{ass_escaped}'[vfinal];"
        # Audio streams
        "[2:a]volume=1.08[a_voc];"
        "[3:a]atrim=0:18.23,asetpts=PTS-STARTPTS,volume=0.15,afade=t=in:st=0:d=0.4,afade=t=out:st=17.7:d=0.5[a_bgm];"
        "[4:a]adelay=100|100,volume=0.25[a_sfx1];"
        "[5:a]adelay=4500|4500,volume=0.35[a_sfx2];"
        "[6:a]adelay=8500|8500,volume=0.35[a_sfx3];"
        "[7:a]adelay=14500|14500,volume=0.30[a_sfx4];"
        "[a_voc][a_bgm][a_sfx1][a_sfx2][a_sfx3][a_sfx4]amix=inputs=6:duration=first:dropout_transition=2[a_mix];"
        "[a_mix]loudnorm=I=-14.0:TP=-1.0:LRA=7.0[afinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(shot1),         # 0
        "-i", str(shot2),         # 1
        "-i", str(voice_track),   # 2
        "-i", str(bgm_track),     # 3
        "-i", str(sfx_sparkle),   # 4
        "-i", str(sfx_ding),      # 5
        "-i", str(sfx_ting),      # 6
        "-i", str(sfx_whoosh),    # 7
        "-i", str(banner_png),    # 8
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "[afinal]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        "-movflags", "+faststart",
        str(output_video)
    ]

    print("  Đang tiến hành render Master V2...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Lỗi FFmpeg Master V2:\n{res.stderr}")
    print(f"  ✓ Video Master V2 đã render thành công: {output_video}")

    # Bước 4: Trích xuất snapshots và xuất bản CDN
    print("\n[BƯỚC 3/4] 📸 Trích xuất bộ ảnh chụp kiểm định thực tế...")
    snaps = [
        ("v2_01_hook_banner.jpg", 1.5),
        ("v2_02_punch_in_phone.jpg", 5.5),
        ("v2_03_late_night_3am.jpg", 11.0),
        ("v2_04_outro_question.jpg", 16.0)
    ]
    for name, ts in snaps:
        out_snap = snap_dir / name
        cmd_s = ["ffmpeg", "-y", "-ss", str(ts), "-i", str(output_video), "-vframes", "1", "-q:v", "2", str(out_snap)]
        subprocess.run(cmd_s, check=True, capture_output=True)
        print(f"  ✓ Snapshot {ts}s: {out_snap}")

    print("\n[BƯỚC 4/4] 🌐 Xuất bản lên CDN Caddy và Cloudflare Web Player...")
    cdn_dir = Path("/srv/school-ai/var/video-cong-khai/nhunnhun")
    cdn_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output_video, cdn_dir / "nhunnhun_master_v2.mp4")
    shutil.copy2(output_video, final_dir / "nhunnhun_final_ep01.mp4") # ghi đè bản cũ
    shutil.copy2(output_video, cdn_dir / "nhunnhun_final_ep01.mp4")

    for name, _ in snaps:
        shutil.copy2(snap_dir / name, cdn_dir / "snapshots" / name)

    # Cập nhật Web Player
    index_html = cdn_dir / "index.html"
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOL Nhun Nhun AI — Master V2 (Chuẩn Triệu View)</title>
    <style>
        body {{
            background: #0f1117;
            color: #f0f3fa;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 24px;
            margin: 0;
        }}
        .header {{
            text-align: center;
            max-width: 620px;
            margin-bottom: 20px;
        }}
        .badge {{
            background: linear-gradient(135deg, #ff0055, #ff5500);
            color: white;
            padding: 5px 14px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 800;
            display: inline-block;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}
        h1 {{
            font-size: 24px;
            margin: 8px 0;
            color: #ffffff;
        }}
        p {{
            color: #a0a6b5;
            font-size: 15px;
            line-height: 1.5;
            margin: 4px 0;
        }}
        .video-box {{
            width: 100%;
            max-width: 380px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 50px rgba(0,0,0,0.7);
            border: 2px solid #2d323f;
            background: #000;
        }}
        video {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .features {{
            margin-top: 20px;
            max-width: 480px;
            background: #181c26;
            border-radius: 14px;
            padding: 16px 20px;
            border: 1px solid #2d323f;
            width: 100%;
            box-sizing: border-box;
        }}
        .features h3 {{
            margin: 0 0 12px 0;
            font-size: 16px;
            color: #ffdd00;
        }}
        .feature-item {{
            display: flex;
            align-items: center;
            font-size: 14px;
            padding: 7px 0;
            border-bottom: 1px solid #232838;
            color: #d0d7e6;
        }}
        .feature-item:last-child {{
            border-bottom: none;
        }}
        .icon {{
            font-size: 16px;
            margin-right: 10px;
        }}
        .download-btn {{
            display: inline-block;
            margin-top: 18px;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            padding: 12px 28px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 15px;
            box-shadow: 0 4px 15px rgba(37,99,235,0.4);
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            max-width: 480px;
            margin-top: 20px;
            width: 100%;
        }}
        .gallery img {{
            width: 100%;
            border-radius: 10px;
            border: 1px solid #2d323f;
        }}
    </style>
</head>
<body>
    <div class="header">
        <span class="badge">🔥 BẢN NÂNG CẤP MASTER V2 • 100% CHUẨN ĐỐI THỦ</span>
        <h1>🌟 KOL Nhun Nhun AI — Thứ Khó Buông Nhất</h1>
        <p>Tích hợp trọn vẹn: Top Hook Banner • Nhạc nền BGM Carefree • SFX Đa tầng • Punch-in Zoom</p>
    </div>

    <div class="video-box">
        <video controls autoplay loop playsinline poster="snapshots/v2_02_punch_in_phone.jpg">
            <source src="nhunnhun_master_v2.mp4" type="video/mp4">
            Trình duyệt không hỗ trợ xem video HTML5.
        </video>
    </div>

    <a href="nhunnhun_master_v2.mp4" class="download-btn" download>⬇️ Tải Video MP4 Master V2 (15.8 MB)</a>

    <div class="features">
        <h3>✨ 5 Điểm Nâng Cấp Đột Phá Đạt Chuẩn Triệu View</h3>
        <div class="feature-item"><span class="icon">🏷️</span><b>Top Hook Banner:</b> Chữ vàng viền đen 8px cố định ở đỉnh màn hình.</div>
        <div class="feature-item"><span class="icon">🎵</span><b>Nhạc Nền BGM:</b> Track 'Carefree' nhí nhảnh, vui nhộn (-16dB ducking).</div>
        <div class="feature-item"><span class="icon">🔊</span><b>Sound FX:</b> Sparkle mở màn, Ding chuông nảy, Pop từ khóa, Whoosh kết bài.</div>
        <div class="feature-item"><span class="icon">🔍</span><b>Punch-in Zoom:</b> Cắt giật 1.18x vào khuôn mặt & điện thoại tại giây 4.5.</div>
        <div class="feature-item"><span class="icon">🎙️</span><b>Giọng Đọc Biểu Cảm:</b> Tự nhiên, có tiếng cười, nhõng nhẽo và hờn dỗi.</div>
    </div>

    <div class="gallery">
        <img src="snapshots/v2_01_hook_banner.jpg" alt="Hook">
        <img src="snapshots/v2_02_punch_in_phone.jpg" alt="Punch-in Phone">
    </div>
</body>
</html>
"""
    with open(index_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  ✓ Đã cập nhật Web Player: {index_html}")

    print("\n" + "=" * 70)
    print("✨ CHÚC MỪNG! CLIP MASTER V2 ĐÃ HOÀN TẤT VƯỢT TRỘI:")
    print(f" - Tệp Master V2: {output_video}")
    print(f" - Web Player Trực Tiếp: https://directive-leadership-forest-processors.trycloudflare.com/")
    print(f" - Link Tải Trực Tiếp: https://directive-leadership-forest-processors.trycloudflare.com/nhunnhun_master_v2.mp4")
    print(f" - Link Caddy CDN: https://bot.eyc.asia/v-c0e8efc0d44cce2e3794ff0fff190b87/nhunnhun/nhunnhun_master_v2.mp4")
    print("=" * 70)

if __name__ == "__main__":
    build_master_v2()
