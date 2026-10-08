#!/usr/bin/env python3
"""
Bộ xuất bản CDN công khai (CDN Publisher) cho kênh Nhun Nhun.
Đẩy video lên thư mục phục vụ tĩnh của Caddy server và tạo URL truy cập ngay lập tức.
"""

import shutil
from pathlib import Path
from typing import Optional

class CdnPublisher:
    DEFAULT_CDN_DIR = Path('/srv/school-ai/var/video-cong-khai/nhunnhun')
    BASE_URL = "https://bot.eyc.asia/v-c0e8efc0d44cce2e3794ff0fff190b87/nhunnhun"

    def __init__(self, cdn_dir: Optional[Path] = None):
        self.cdn_dir = cdn_dir or self.DEFAULT_CDN_DIR
        self.cdn_dir.mkdir(parents=True, exist_ok=True)

    def publish(self, local_video: Path, cdn_filename: Optional[str] = None) -> str:
        filename = cdn_filename or local_video.name
        dest = self.cdn_dir / filename
        shutil.copy2(local_video, dest)
        public_url = f"{self.BASE_URL}/{filename}"
        return public_url
