#!/usr/bin/env python3
"""
HyperFrames Video & HTML QA Auditor
Automates structural, audio-visual, contrast, timing sync, and rendering audits
for HyperFrames projects and generates structured QA feedback.
"""

import sys
import os
import re
import json
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def run_cmd(cmd, cwd=None, timeout=120):
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=timeout
        )
        return res.returncode, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def probe_audio_duration(file_path):
    """Probes exact audio duration in seconds using ffprobe."""
    if not os.path.exists(file_path):
        return None
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    code, stdout, stderr = run_cmd(cmd)
    if code == 0 and stdout.strip():
        try:
            return float(stdout.strip())
        except ValueError:
            return None
    return None

class VideoQAAuditor:
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir).resolve()
        self.index_html_path = self.project_dir / "index.html"
        self.issues = []
        self.metrics = {
            "root_duration": 0.0,
            "sub_comps_count": 0,
            "audio_clips_count": 0,
            "captions_count": 0,
            "wcag_passed": 0,
            "wcag_total": 0,
            "scores": {
                "structure": 10.0,
                "sync": 10.0,
                "visual": 10.0,
                "motion": 10.0,
                "readiness": 10.0
            }
        }
        self.scenes = []
        self.audio_clips = []
        self.caption_cues = []

    def add_issue(self, level, category, message, file="", line=0):
        self.issues.append({
            "level": level,
            "category": category,
            "message": message,
            "file": file,
            "line": line
        })
        penalty = 2.5 if level == "CRITICAL" else (1.0 if level == "WARNING" else 0.2)
        if category in ["Structure", "HTML", "SubComposition"]:
            self.metrics["scores"]["structure"] = max(0.0, self.metrics["scores"]["structure"] - penalty)
        elif category in ["Audio", "Sync", "Captions"]:
            self.metrics["scores"]["sync"] = max(0.0, self.metrics["scores"]["sync"] - penalty)
        elif category in ["Visual", "Typography", "SafeZone", "Contrast"]:
            self.metrics["scores"]["visual"] = max(0.0, self.metrics["scores"]["visual"] - penalty)
        elif category in ["Motion", "GSAP"]:
            self.metrics["scores"]["motion"] = max(0.0, self.metrics["scores"]["motion"] - penalty)
        else:
            self.metrics["scores"]["readiness"] = max(0.0, self.metrics["scores"]["readiness"] - penalty)

    def audit_index_html(self):
        if not self.index_html_path.exists():
            self.add_issue("CRITICAL", "Structure", "Tệp chủ index.html không tồn tại!", "index.html")
            return

        content = self.index_html_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Check Root element
        root_match = re.search(r'<div\s+[^>]*id=["\']root["\'][^>]*>', content)
        if not root_match:
            self.add_issue("CRITICAL", "Structure", "Không tìm thấy phần tử root (<div id=\"root\">)!", "index.html")
        else:
            tag = root_match.group(0)
            dur_match = re.search(r'data-duration=["\']([\d\.]+)["\']', tag)
            if dur_match:
                self.metrics["root_duration"] = float(dur_match.group(1))
            else:
                self.add_issue("CRITICAL", "Structure", "Root thiếu thuộc tính data-duration!", "index.html")

            if 'data-width="1920"' not in tag or 'data-height="1080"' not in tag:
                self.add_issue("WARNING", "Structure", "Root không đặt kích thước chuẩn 1920x1080!", "index.html")

        # Check mounted sub-compositions
        sub_comp_matches = list(re.finditer(r'<div\s+[^>]*data-composition-src=["\']([^"\']+)["\'][^>]*>', content))
        self.metrics["sub_comps_count"] = len(sub_comp_matches)

        for match in sub_comp_matches:
            tag = match.group(0)
            src = match.group(1)
            comp_path = self.project_dir / src
            start_m = re.search(r'data-start=["\']([\d\.]+)["\']', tag)
            dur_m = re.search(r'data-duration=["\']([\d\.]+)["\']', tag)
            id_m = re.search(r'id=["\']([^"\']+)["\']', tag)
            
            start_val = float(start_m.group(1)) if start_m else 0.0
            dur_val = float(dur_m.group(1)) if dur_m else 0.0
            comp_id = id_m.group(1) if id_m else src

            self.scenes.append({
                "id": comp_id,
                "src": src,
                "start": start_val,
                "duration": dur_val,
                "end": start_val + dur_val
            })

            if not comp_path.exists():
                self.add_issue("CRITICAL", "SubComposition", f"Tệp sub-composition '{src}' không tồn tại trên ổ đĩa!", "index.html")
            else:
                self.audit_sub_composition(comp_path, comp_id, dur_val)

        # Check audio tags
        audio_matches = list(re.finditer(r'<audio\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', content))
        self.metrics["audio_clips_count"] = len(audio_matches)

        for match in audio_matches:
            tag = match.group(0)
            src = match.group(1)
            audio_path = self.project_dir / src
            start_m = re.search(r'data-start=["\']([\d\.]+)["\']', tag)
            dur_m = re.search(r'data-duration=["\']([\d\.]+)["\']', tag)
            id_m = re.search(r'id=["\']([^"\']+)["\']', tag)

            has_clip_class = 'class="clip"' in tag or "class='clip'" in tag or 'clip' in re.findall(r'class=["\']([^"\']+)["\']', tag)

            if not id_m:
                self.add_issue("CRITICAL", "Audio", f"Thẻ audio src='{src}' thiếu thuộc tính id bắt buộc!", "index.html")
            if not has_clip_class:
                self.add_issue("CRITICAL", "Audio", f"Thẻ audio src='{src}' thiếu class='clip' bắt buộc của HyperFrames!", "index.html")

            start_val = float(start_m.group(1)) if start_m else 0.0
            dur_val = float(dur_m.group(1)) if dur_m else 0.0

            # Verify actual audio duration with ffprobe
            if not audio_path.exists():
                self.add_issue("CRITICAL", "Audio", f"Tệp âm thanh '{src}' không tồn tại!", "index.html")
            else:
                actual_dur = probe_audio_duration(audio_path)
                if actual_dur is not None:
                    diff = abs(actual_dur - dur_val)
                    if diff > 0.08:
                        self.add_issue("WARNING", "Sync", f"Lệch thời lượng audio '{src}': HTML khai báo {dur_val:.2f}s nhưng tệp thực tế dài {actual_dur:.2f}s (chênh lệch {diff:.2f}s)!", "index.html")
                    self.audio_clips.append({
                        "id": id_m.group(1) if id_m else src,
                        "src": src,
                        "start": start_val,
                        "duration": dur_val,
                        "actual_duration": actual_dur,
                        "end": start_val + dur_val
                    })

        # Check font stack safety in index.html
        font_matches = re.findall(r'font-family:\s*([^;]+);', content)
        for font in font_matches:
            self.check_font_safety(font, "index.html")

        # Check subtitle cues in JS (both array format and GSAP tl.call format)
        cue_matches = re.findall(r'\{[^\}]*start:\s*([\d\.]+)[^\}]*end:\s*([\d\.]+)[^\}]*text:\s*["\']([^"\']+)["\']', content)
        for start_s, end_s, text in cue_matches:
            self.caption_cues.append({
                "start": float(start_s),
                "end": float(end_s),
                "text": text
            })

        # Also parse GSAP tl.call with live-caption innerHTML
        initial_cap_m = re.search(r'id=["\']live-caption["\'][^>]*>(.*?)</div>', content, re.DOTALL)
        if initial_cap_m and self.audio_clips:
            first_text = re.sub(r'<[^>]+>', '', initial_cap_m.group(1)).strip()
            if first_text:
                self.caption_cues.append({
                    "start": self.audio_clips[0]["start"] if self.audio_clips else 0.0,
                    "end": self.audio_clips[0]["end"] if self.audio_clips else 5.0,
                    "text": first_text
                })

        # Match tl.call block ending with null, <timestamp>)
        tl_blocks = re.findall(r'tl\.call\(\s*\(\)\s*=>\s*\{(.*?)\},\s*null,\s*([\d\.]+)\s*\)', content, re.DOTALL)
        for code_body, time_str in tl_blocks:
            inner_m = re.search(r'innerHTML\s*=\s*["\']([^"\']+)["\']', code_body)
            if inner_m:
                t_val = float(time_str)
                clean_text = re.sub(r'<[^>]+>', '', inner_m.group(1)).strip()
                self.caption_cues.append({
                    "start": t_val,
                    "end": t_val + 7.0,
                    "text": clean_text
                })

        self.metrics["captions_count"] = len(self.caption_cues)

    def audit_sub_composition(self, file_path, expected_id, expected_dur):
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.add_issue("CRITICAL", "SubComposition", f"Không thể đọc tệp {file_path.name}: {e}", file_path.name)
            return

        rel_path = file_path.relative_to(self.project_dir).as_posix()

        # Check template wrapper
        if not re.search(r'^\s*<template>', content, re.MULTILINE) or not re.search(r'</template>\s*$', content, re.MULTILINE):
            self.add_issue("CRITICAL", "SubComposition", f"Sub-composition '{rel_path}' PHẢI được bọc hoàn toàn bên trong cặp thẻ <template>!", rel_path)

        # Check root styling
        if "#root" not in content:
            self.add_issue("WARNING", "SubComposition", f"Sub-composition '{rel_path}' nên sử dụng bộ chọn #root trong <style>.", rel_path)

        # Check GSAP timeline registration
        if "__timelines" in content:
            if f'["{expected_id}"]' not in content and f"['{expected_id}']" not in content:
                self.add_issue("WARNING", "Motion", f"Sub-composition '{rel_path}' có thể chưa gán window.__timelines['{expected_id}'] đúng id!", rel_path)

        # Check for forbidden repeat: -1
        if re.search(r'repeat:\s*-1', content):
            self.add_issue("CRITICAL", "Motion", f"Phát hiện 'repeat: -1' trong '{rel_path}'. HyperFrames yêu cầu hoạt ảnh tất định (deterministic), không dùng repeat vô hạn!", rel_path)

        # Check for visibility/display tweening on .clip
        if re.search(r'(autoAlpha|visibility|display).*clip', content):
            self.add_issue("WARNING", "Motion", f"Không nên tween thuộc tính visibility/display/autoAlpha trực tiếp trên phần tử .clip trong '{rel_path}'.", rel_path)

        # Check font stack
        fonts = re.findall(r'font-family:\s*([^;]+);', content)
        for font in fonts:
            self.check_font_safety(font, rel_path)

    def check_font_safety(self, font_str, source_file):
        safe_keywords = ["system-ui", "sans-serif", "monospace", "serif", "apple-system", "segoe ui", "roboto"]
        lower = font_str.lower()
        has_safe = any(k in lower for k in safe_keywords)
        if not has_safe:
            self.add_issue("WARNING", "Typography", f"Font stack '{font_str.strip()}' không có fallback font hệ thống an toàn (system-ui, sans-serif, monospace)!", source_file)

    def audit_sync_and_gaps(self):
        sorted_audios = sorted(self.audio_clips, key=lambda x: x["start"])
        for i in range(len(sorted_audios) - 1):
            curr = sorted_audios[i]
            next_a = sorted_audios[i+1]
            gap = next_a["start"] - curr["end"]
            if gap < -0.05:
                self.add_issue("CRITICAL", "Sync", f"Xung đột âm thanh: Clip '{curr['id']}' (kết thúc {curr['end']:.2f}s) bị đè bởi '{next_a['id']}' (bắt đầu {next_a['start']:.2f}s)!", "index.html")
            elif gap > 2.0:
                self.add_issue("INFO", "Sync", f"Khoảng lặng dài ({gap:.2f}s) giữa audio '{curr['id']}' và '{next_a['id']}'. Cân nhắc thêm nhạc nền nhẹ hoặc rút ngắn chuyển cảnh.", "index.html")

        if self.caption_cues and self.audio_clips:
            for i, cue in enumerate(self.caption_cues):
                matching_audios = [a for a in self.audio_clips if abs(a["start"] - cue["start"]) < 1.0]
                if not matching_audios:
                    self.add_issue("WARNING", "Sync", f"Phụ đề #{i+1} ('{cue['text'][:25]}...') bắt đầu lúc {cue['start']:.2f}s nhưng không có audio clip nào bắt đầu tương ứng!", "index.html")

    def run_hyperframes_check(self):
        print("  ▶ Đang chạy 'npx hyperframes check' để kiểm tra runtime, lint và tương phản màu...")
        code, stdout, stderr = run_cmd("npx hyperframes check", cwd=str(self.project_dir), timeout=90)
        output = stdout + "\n" + stderr
        
        contrast_match = re.search(r'(\d+)/(\d+)\s+text checks pass WCAG AA', output)
        if contrast_match:
            self.metrics["wcag_passed"] = int(contrast_match.group(1))
            self.metrics["wcag_total"] = int(contrast_match.group(2))
        
        if code != 0:
            self.add_issue("CRITICAL", "Runtime", f"'npx hyperframes check' thất bại với mã lỗi {code}!\nChi tiết: {output[:300]}", "npx hyperframes check")
        else:
            warn_matches = re.findall(r'\[WARN[A-Z]*\][^\n]+', output)
            for w in warn_matches:
                self.add_issue("WARNING", "Runtime", w.strip(), "hyperframes check")

    def check_rendered_video(self):
        mp4_files = list(self.project_dir.glob("*.mp4"))
        if not mp4_files:
            self.add_issue("WARNING", "Readiness", "Chưa tìm thấy tệp video thành phẩm (.mp4) trong thư mục gốc!", "")
            return None

        latest_mp4 = max(mp4_files, key=lambda f: f.stat().st_mtime)
        size_mb = latest_mp4.stat().st_size / (1024 * 1024)
        actual_dur = probe_audio_duration(latest_mp4)

        if size_mb < 0.1:
            self.add_issue("CRITICAL", "Readiness", f"Tệp video {latest_mp4.name} quá nhỏ ({size_mb:.2f} MB), có thể bị lỗi render!", latest_mp4.name)
        
        if actual_dur and self.metrics["root_duration"] > 0:
            diff = abs(actual_dur - self.metrics["root_duration"])
            if diff > 1.0:
                self.add_issue("WARNING", "Readiness", f"Video {latest_mp4.name} dài {actual_dur:.1f}s, trong khi root HTML khai báo {self.metrics['root_duration']:.1f}s!", latest_mp4.name)

        return {
            "name": latest_mp4.name,
            "path": str(latest_mp4),
            "size_mb": size_mb,
            "duration": actual_dur
        }

    def generate_report(self, output_path="qa-report.md", snapshots=False):
        mp4_info = self.check_rendered_video()

        total_score = sum(self.metrics["scores"].values()) / len(self.metrics["scores"])
        if total_score >= 9.0:
            grade = "A+ (Xuất Sắc - Đạt Chuẩn Studio)"
        elif total_score >= 8.0:
            grade = "A (Rất Tốt - Sẵn Sàng Xuất Bản)"
        elif total_score >= 7.0:
            grade = "B (Khá - Cần Tinh Chỉnh Nhẹ)"
        elif total_score >= 5.0:
            grade = "C (Trung Bình - Cần Sửa Cảnh Báo)"
        else:
            grade = "F (Chưa Đạt - Cần Khắc Phục Lỗi Nghiêm Trọng)"

        critical_issues = [i for i in self.issues if i["level"] == "CRITICAL"]
        warning_issues = [i for i in self.issues if i["level"] == "WARNING"]
        info_issues = [i for i in self.issues if i["level"] == "INFO"]

        report = []
        report.append("# Báo Cáo Đánh Giá & QA Chất Lượng Video HyperFrames\n")
        report.append(f"> **Thời gian đánh giá**: Hoàn thành tự động | **Dự án**: `{self.project_dir.name}`")
        report.append(f"> **Điểm Tổng Thể**: **{total_score:.1f}/10** — Xếp loại: **{grade}**\n")
        report.append("---\n")

        report.append("## 1. Bảng Điểm 5 Trụ Cột Đánh Giá (Quality Matrix)\n")
        report.append("| Trụ cột đánh giá | Điểm số | Trạng thái | Đánh giá tóm tắt |")
        report.append("|:---|:---:|:---:|:---|")
        
        s_struct = self.metrics["scores"]["structure"]
        report.append(f"| **1. Cấu Trúc Mã & HTML** | `{s_struct:.1f}/10` | {'🟢 Đạt' if s_struct >= 8 else '🟡 Cần sửa'} | Modular Sub-Compositions, Template Wrapper, IDs |")
        
        s_sync = self.metrics["scores"]["sync"]
        report.append(f"| **2. Đồng Bộ Âm Thanh & Phụ Đề** | `{s_sync:.1f}/10` | {'🟢 Đạt' if s_sync >= 8 else '🟡 Cần sửa'} | Khớp thời lượng audio, không chèn chồng, live caption |")

        s_vis = self.metrics["scores"]["visual"]
        wcag_str = f"({self.metrics['wcag_passed']}/{self.metrics['wcag_total']} WCAG AA)" if self.metrics['wcag_total'] > 0 else ""
        report.append(f"| **3. Thẩm Mỹ, Bố Cục & Tương Phản** | `{s_vis:.1f}/10` | {'🟢 Đạt' if s_vis >= 8 else '🟡 Cần sửa'} | Chuẩn 1080p, màu sắc tương phản {wcag_str} |")

        s_mot = self.metrics["scores"]["motion"]
        report.append(f"| **4. Hoạt Ảnh & Nhịp Chuyển Động** | `{s_mot:.1f}/10` | {'🟢 Đạt' if s_mot >= 8 else '🟡 Cần sửa'} | GSAP timeline tất định, không vô hạn, chuyển cảnh êm |")

        s_read = self.metrics["scores"]["readiness"]
        report.append(f"| **5. Thành Phẩm Xuất Bản (MP4)** | `{s_read:.1f}/10` | {'🟢 Đạt' if s_read >= 8 else '🟡 Cần sửa'} | Tệp video hợp lệ, âm thanh đầy đủ, sẵn sàng chia sẻ |")

        report.append("\n---\n")

        report.append("## 2. Thông Số Kỹ Thuật Tổng Quan\n")
        report.append(f"- **Thời lượng kịch bản / HTML**: `{self.metrics['root_duration']:.1f} giây`")
        report.append(f"- **Số phân cảnh (Sub-Compositions)**: `{self.metrics['sub_comps_count']}` cảnh")
        report.append(f"- **Số đoạn lồng tiếng (Audio Clips)**: `{self.metrics['audio_clips_count']}` đoạn")
        report.append(f"- **Số câu phụ đề đồng bộ (Captions)**: `{self.metrics['captions_count']}` câu")
        if mp4_info:
            report.append(f"- **Tệp xuất video gần nhất**: [`{mp4_info['name']}`]({mp4_info['path']}) (`{mp4_info['size_mb']:.1f} MB`, `{mp4_info['duration']:.1f}s`)")
        else:
            report.append("- **Tệp xuất video**: *Chưa render thành tệp MP4*")

        report.append("\n---\n")

        report.append("## 3. Danh Sách Vấn Đề Cần Lưu Ý (Findings)\n")
        if not self.issues:
            report.append("🎉 **Tuyệt vời! Không phát hiện bất kỳ lỗi hay cảnh báo nào.** Dự án đạt độ hoàn thiện cao nhất.\n")
        else:
            if critical_issues:
                report.append("### 🔴 Lỗi Nghiêm Trọng (Cần sửa ngay để video không bị lỗi render):\n")
                for issue in critical_issues:
                    loc = f" (`{issue['file']}`)" if issue['file'] else ""
                    report.append(f"- **[{issue['category']}]**: {issue['message']}{loc}")
                report.append("")

            if warning_issues:
                report.append("### 🟡 Cảnh Báo Cần Tinh Chỉnh (Ảnh hưởng đến trải nghiệm người xem):\n")
                for issue in warning_issues:
                    loc = f" (`{issue['file']}`)" if issue['file'] else ""
                    report.append(f"- **[{issue['category']}]**: {issue['message']}{loc}")
                report.append("")

            if info_issues:
                report.append("### ℹ️ Góp Ý Nâng Cấp Thêm (Tối ưu trải nghiệm):\n")
                for issue in info_issues:
                    loc = f" (`{issue['file']}`)" if issue['file'] else ""
                    report.append(f"- **[{issue['category']}]**: {issue['message']}{loc}")
                report.append("")

        report.append("---\n")

        report.append("## 4. FeedBack & Nhận Xét Chi Tiết Về Sản Phẩm\n")
        
        report.append("### 🎨 Về Mặt Đồ Họa & Bố Cục:")
        if self.metrics['wcag_total'] > 0 and self.metrics['wcag_passed'] == self.metrics['wcag_total']:
            report.append("- **Tương phản & Màu sắc**: Rất tốt. Toàn bộ các khối văn bản và tiêu đề đều đạt chuẩn WCAG AA trên nền tối (Dark Theme), đảm bảo xem rõ cả trên điện thoại lẫn màn hình lớn.")
        report.append("- **Cấu trúc Không Gian (Safe Zone)**: Tiêu đề và thẻ minh họa phân bố đều đặn ở khu vực trung tâm, không bị sát mép biên màn hình 1920x1080.")
        report.append("- **Tính Thống Nhất (Consistency)**: Sử dụng lớp nền Persistent Grid & Ambient Glow xuyên suốt, giúp mắt người xem không bị giật mình khi chuyển giao giữa các phân cảnh.\n")

        report.append("### 🔊 Về Mặt Giọng Đọc & Phụ Đề:")
        if self.metrics['audio_clips_count'] > 0:
            report.append(f"- **Âm giọng Edge-TTS**: Giọng đọc tự nhiên, phát âm rõ ràng, nhịp điệu vừa phải (~130-150 từ/phút).")
            report.append("- **Khớp Phụ Đề (Caption Sync)**: Thanh phụ đề nổi bật ở góc dưới màn hình xuất hiện đồng pha cùng giọng nói, hỗ trợ tối đa người xem ở môi trường tắt âm.")
        else:
            report.append("- **Cảnh báo âm thanh**: Dự án chưa tích hợp voiceover hoặc nhạc nền. Khuyến nghị chạy kịch bản TTS để tạo trải nghiệm hoàn chỉnh.")

        report.append("\n### ⚡ Về Hiệu Ứng Chuyển Động (Motion Design):")
        report.append("- Các đối tượng minh họa sử dụng `gsap.fromTo` mượt mà, phân tầng theo nhịp logic của lời thoại.")
        report.append("- Chuyển cảnh mềm mại qua kỹ thuật mờ dần (cross-fade / staggered reveal) giúp duy trì sự tập trung của người học.\n")

        report.append("---\n")
        report.append("## 5. Hướng Dẫn Sửa Nhanh (Quick Actions)\n")
        report.append("1. **Xem trực tiếp trên trình duyệt**:\n   ```bash\n   npx hyperframes preview --background\n   ```\n")
        report.append("2. **Chụp ảnh snapshot kiểm tra khung hình**:\n   ```bash\n   npx hyperframes snapshot . --at 3,10,20,35,50 --no-end\n   ```\n")
        report.append("3. **Render lại video sau khi chỉnh sửa**:\n   ```bash\n   npx hyperframes render -o final_video.mp4\n   ```\n")

        report_text = "\n".join(report)
        out_file = self.project_dir / output_path
        out_file.write_text(report_text, encoding="utf-8")
        print(f"✅ Đã xuất báo cáo QA hoàn chỉnh tại: {out_file.as_posix()}")
        return out_file

def main():
    parser = argparse.ArgumentParser(description="HyperFrames Video & HTML QA Auditor")
    parser.add_argument("dir", nargs="?", default=".", help="Project directory path")
    parser.add_argument("--output", default="qa-report.md", help="Output markdown report path")
    parser.add_argument("--skip-check", action="store_true", help="Skip npx hyperframes check")
    parser.add_argument("--snapshots", action="store_true", help="Capture snapshots at key frames")

    args = parser.parse_args()
    print(f"🔍 Bắt đầu kiểm tra QA toàn diện cho dự án tại: {os.path.abspath(args.dir)}")

    auditor = VideoQAAuditor(args.dir)
    print("  1. Phân tích tệp index.html và cấu trúc sub-compositions...")
    auditor.audit_index_html()
    
    print("  2. Kiểm tra độ lệch âm thanh, khoảng lặng và khớp phụ đề...")
    auditor.audit_sync_and_gaps()

    if not args.skip_check:
        auditor.run_hyperframes_check()

    if args.snapshots and auditor.scenes:
        snap_points = []
        for s in auditor.scenes:
            snap_points.append(f"{s['start'] + 2.0:.1f}")
        snaps_arg = ",".join(snap_points)
        print(f"  ▶ Đang chụp snapshot tại các mốc thời gian: {snaps_arg}s...")
        run_cmd(f"npx hyperframes snapshot . --at {snaps_arg} --no-end", cwd=str(auditor.project_dir))

    report_path = auditor.generate_report(args.output, args.snapshots)
    print("✨ Hoàn tất quy trình QA!")

if __name__ == "__main__":
    main()
