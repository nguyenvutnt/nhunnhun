#!/usr/bin/env python3
"""
Google Flow (Veo 3.1) Automation Client via Chrome DevTools Protocol (CDP).
Hỗ trợ tạo video điện ảnh 9:16 cho KOL ảo Nhun Nhun.
"""

import sys
import os
import time
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# Nạp module CDP dùng sẵn trên máy chủ
sys.path.insert(0, '/srv/school-ai/scripts/flow')
try:
    from cdp import Chrome
except ImportError:
    Chrome = None


class FlowVeoClient:
    def __init__(self, port: int = 9223, downloads_dir: Optional[Path] = None):
        if Chrome is None:
            raise RuntimeError("Module CDP chưa được cài đặt hoặc thiếu môi trường!")
        self.port = port
        self.downloads_dir = downloads_dir or Path('/root/Downloads')
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.chrome = Chrome(self.port)

    def find_project_tab(self) -> Optional[str]:
        """Tìm tab Google Flow đang mở trên Chrome"""
        for tab in self.chrome.danh_sách_tab():
            url = tab.get('url', '')
            if 'flow.google.com/project/' in url:
                return tab.get('id')
        return None

    def get_or_create_session(self) -> str:
        """Kết nối tới tab Flow hiện tại hoặc mở tab mới"""
        target_id = self.find_project_tab()
        if not target_id:
            for tab in self.chrome.danh_sách_tab():
                if 'flow.google.com' in tab.get('url', ''):
                    target_id = tab.get('id')
                    break

        if not target_id:
            sid = self.chrome.tab_mới("https://flow.google.com/")
            time.sleep(6)
            return sid

        sid = self.chrome.lệnh('Target.attachToTarget', {'targetId': target_id, 'flatten': True})['sessionId']
        self.chrome.lệnh('Runtime.enable', session=sid)
        self.chrome.lệnh('Browser.setDownloadBehavior', {
            'behavior': 'allow',
            'downloadPath': str(self.downloads_dir)
        }, session=sid)
        return sid

    def configure_generation_settings(self, sid: str, aspect_ratio: str = "9:16", model: str = "Veo 3.1 - Quality"):
        """Cấu hình model và tỉ lệ khung hình (mặc định 9:16 portrait)"""
        # Đảm bảo bật Settings trigger nếu có
        self.chrome.js('''(() => {
            const btn = document.querySelector('button[aria-label="Settings trigger"]');
            if (btn) btn.click();
        })()''', sid)
        time.sleep(1)

        # Chọn tab Video
        self.chrome.js('''(() => {
            const btn = [...document.querySelectorAll('button')].find(e => (e.innerText||'').includes('Video'));
            if (btn) btn.click();
        })()''', sid)
        time.sleep(0.5)

        # Chọn tỉ lệ
        self.chrome.js(f'''(() => {{
            const btn = [...document.querySelectorAll('button')].find(e => (e.innerText||'').includes('{aspect_ratio}'));
            if (btn) btn.click();
        }})()''', sid)
        time.sleep(0.5)

        # Chọn model family
        self.chrome.js('''(() => {
            const dd = document.querySelector('button[aria-label="Select model family"]');
            if (dd) dd.click();
        })()''', sid)
        time.sleep(1)

        self.chrome.js(f'''(() => {{
            const item = [...document.querySelectorAll('button, [role=menuitem]')].find(e => (e.innerText||'').includes('{model}'));
            if (item) item.click();
        }})()''', sid)
        time.sleep(1)

    def trigger_generation(self, prompt: str, output_dest: Path, timeout_seconds: int = 600) -> Path:
        """
        Nhập prompt, phát lệnh render trên Google Flow, theo dõi % và tải video về đích.
        """
        sid = self.get_or_create_session()
        self.configure_generation_settings(sid)

        # Snapshot thư mục tải
        pre_files = set(self.downloads_dir.glob('*'))

        # Nhập text vào ProseMirror
        self.chrome.js(f'''(() => {{
            const el = document.querySelector('.ProseMirror[contenteditable=true]');
            if (el) {{
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, {json.dumps(prompt)});
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'a', bubbles: true }}));
                el.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'a', bubbles: true }}));
            }}
        }})()''', sid)
        time.sleep(1.5)

        # Bấm Start generation
        res = self.chrome.js('''(() => {
            const btn = document.querySelector('button[aria-label="Start generation"]');
            if (btn && !btn.disabled) {
                btn.click();
                return true;
            }
            return false;
        })()''', sid)

        if not res:
            raise RuntimeError("Không thể bấm nút 'Start generation' (nút bị vô hiệu hoặc không tìm thấy).")

        print("Đã phát lệnh sinh video trên hạ tầng Veo 3.1...")
        start_t = time.time()
        last_pct = None

        while time.time() - start_t < timeout_seconds:
            time.sleep(5)
            status = self.chrome.js('''(() => {
                const text = document.body.innerText;
                const match = text.match(/(\\d{1,3})%/);
                const dls = Array.from(document.querySelectorAll('button[aria-label="Download batch"]'));
                return {
                    pct: match ? match[1] : null,
                    has_ready_dl: dls.length > 0 && !dls[0].disabled
                };
            })()''', sid)

            pct = status.get('pct')
            if pct and pct != last_pct:
                print(f"Tiến độ render Veo: {pct}%")
                last_pct = pct

            if status.get('has_ready_dl') and (pct == '100' or pct is None):
                print("Render video hoàn tất! Đang bấm tải xuống...")
                break

        # Bấm Download batch đầu tiên
        self.chrome.js('''(() => {
            const dls = document.querySelectorAll('button[aria-label="Download batch"]');
            if (dls.length > 0) dls[0].click();
        })()''', sid)

        # Chờ file tải về
        downloaded_zip = None
        for _ in range(30):
            time.sleep(2)
            current = set(self.downloads_dir.glob('*'))
            diff = current - pre_files
            non_cr = [f for f in diff if not f.name.endswith('.crdownload')]
            if non_cr:
                downloaded_zip = non_cr[0]
                break

        if not downloaded_zip:
            raise TimeoutError("Quá thời gian chờ tải video từ Flow!")

        output_dest.parent.mkdir(parents=True, exist_ok=True)
        if downloaded_zip.suffix == '.zip':
            temp_extract = self.downloads_dir / f"extract_{int(time.time())}"
            temp_extract.mkdir(parents=True, exist_ok=True)
            subprocess.run(['unzip', '-o', str(downloaded_zip), '-d', str(temp_extract)], check=True)
            mp4s = list(temp_extract.glob('*.mp4'))
            if not mp4s:
                raise RuntimeError("Không tìm thấy tệp MP4 trong gói tải về!")
            shutil.move(str(mp4s[0]), str(output_dest))
            shutil.rmtree(temp_extract, ignore_errors=True)
            downloaded_zip.unlink(missing_ok=True)
        else:
            shutil.move(str(downloaded_zip), str(output_dest))

        print(f"Tệp video sẵn sàng: {output_dest}")
        return output_dest
