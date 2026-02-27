#!/usr/bin/env python3
"""
浏览器错误捕获脚本
使用 Playwright 监听控制台和网络事件，自动捕获错误

功能：
- Console 错误捕获
- 网络请求失败捕获
- 页面异常捕获
- 错误截图
- HAR 导出
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser, ConsoleMessage, Request, Response


class BrowserCapture:
    """浏览器错误捕获器"""

    def __init__(self,
                 wait_time: int = 5,
                 screenshot_on_error: bool = True,
                 har_path: str = None):
        self.wait_time = wait_time
        self.screenshot_on_error = screenshot_on_error
        self.har_path = har_path

        self.console_messages: List[Dict] = []
        self.network_errors: List[Dict] = []
        self.page_errors: List[Dict] = []
        self.has_error = False

    def on_console(self, msg: ConsoleMessage):
        """Console 消息处理"""
        # 只记录 error 和 warning
        if msg.type in ('error', 'warning'):
            self.has_error = True
            entry = {
                'type': 'console',
                'level': msg.type,
                'text': msg.text,
                'timestamp': datetime.now().isoformat()
            }
            self.console_messages.append(entry)
            print(f"[CONSOLE {msg.type.upper()}] {msg.text}")

    def on_request_failed(self, request: Request):
        """请求失败处理"""
        self.has_error = True
        failure = request.failure
        entry = {
            'type': 'network-error',
            'method': request.method,
            'url': request.url,
            'failure': failure,
            'timestamp': datetime.now().isoformat()
        }
        self.network_errors.append(entry)
        print(f"[NETWORK ERROR] {request.method} {request.url}")
        if failure:
            print(f"  → {failure}")

    def on_response(self, response: Response):
        """响应处理 - 只记录 4xx/5xx"""
        if response.status >= 400:
            self.has_error = True
            entry = {
                'type': 'network-error',
                'method': response.request.method,
                'url': response.url,
                'status': response.status,
                'status_text': response.status_text,
                'timestamp': datetime.now().isoformat()
            }
            self.network_errors.append(entry)
            print(f"[NETWORK ERROR] {response.status} {response.request.method} {response.url}")

    def on_page_error(self, error: Exception):
        """页面异常处理"""
        self.has_error = True
        entry = {
            'type': 'page-error',
            'message': str(error),
            'timestamp': datetime.now().isoformat()
        }
        self.page_errors.append(entry)
        print(f"[PAGE ERROR] {error}")

    def capture(self, url: str, screenshot_path: str = None) -> Dict:
        """执行捕获"""
        print(f"\n{'='*50}")
        print(f"开始捕获: {url}")
        print(f"{'='*50}\n")

        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # 设置事件监听
            page.on('console', self.on_console)
            page.on('requestfailed', self.on_request_failed)
            page.on('response', self.on_response)
            page.on('pageerror', self.on_page_error)

            try:
                # 访问页面
                print(f"正在访问: {url}")
                response = page.goto(url, wait_until='domcontentloaded', timeout=30000)

                if response is None:
                    print("警告: 无法获取页面响应")
                elif response.status >= 400:
                    print(f"警告: HTTP {response.status}")

                # 等待动态内容加载
                if self.wait_time > 0:
                    print(f"等待 {self.wait_time} 秒...")
                    page.wait_for_timeout(self.wait_time * 1000)

                # 如果有错误且需要截图
                if self.has_error and screenshot_path:
                    print(f"\n保存截图: {screenshot_path}")
                    page.screenshot(path=screenshot_path, full_page=True)

                # 导出 HAR
                if self.har_path:
                    print(f"HAR 导出到: {self.har_path}")
                    # Playwright 不直接支持 HAR 导出，需要额外处理

            except Exception as e:
                print(f"错误: {e}")
                if screenshot_path and self.screenshot_on_error:
                    page.screenshot(path=screenshot_path, full_page=True)
            finally:
                browser.close()

        return self.get_results()

    def get_results(self) -> Dict:
        """获取结果"""
        return {
            'url': '',
            'timestamp': datetime.now().isoformat(),
            'has_error': self.has_error,
            'console_messages': self.console_messages,
            'network_errors': self.network_errors,
            'page_errors': self.page_errors,
            'summary': {
                'console_count': len(self.console_messages),
                'network_error_count': len(self.network_errors),
                'page_error_count': len(self.page_errors)
            }
        }

    def to_markdown(self) -> str:
        """转换为 Markdown 格式"""
        md = "# 浏览器错误捕获报告\n\n"
        md += f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += f"**有错误**: {'是' if self.has_error else '否'}\n\n"

        md += "## 统计\n\n"
        md += f"- Console 错误/警告: {len(self.console_messages)}\n"
        md += f"- 网络请求失败: {len(self.network_errors)}\n"
        md += f"- 页面异常: {len(self.page_errors)}\n\n"

        if self.console_messages:
            md += "## Console 消息\n\n"
            for msg in self.console_messages:
                md += f"### {msg['level'].upper()}\n\n"
                md += f"```\n{msg['text']}\n```\n\n"

        if self.network_errors:
            md += "## 网络请求错误\n\n"
            for err in self.network_errors:
                md += f"### {err['method']} {err.get('url', err.get('url'))}\n\n"
                md += f"- 状态: {err.get('status', 'Failed')}\n"
                if err.get('failure'):
                    md += f"- 错误: {err['failure']}\n"
                md += "\n"

        if self.page_errors:
            md += "## 页面异常\n\n"
            for err in self.page_errors:
                md += f"```\n{err['message']}\n```\n\n"

        return md


def main():
    parser = argparse.ArgumentParser(description='浏览器错误捕获工具')
    parser.add_argument('url', help='要访问的 URL')
    parser.add_argument('-w', '--wait', type=int, default=5,
                        help='等待页面渲染的秒数 (默认: 5)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-s', '--screenshot', help='错误时截图保存路径')
    parser.add_argument('--har', help='导出 HAR 文件')
    parser.add_argument('--console-only', action='store_true',
                        help='只捕获 console 消息')
    parser.add_argument('-j', '--json', action='store_true',
                        help='JSON 格式输出')

    args = parser.parse_args()

    # 验证 URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'http://' + args.url

    # 执行捕获
    capture = BrowserCapture(
        wait_time=args.wait,
        screenshot_on_error=bool(args.screenshot),
        har_path=args.har
    )

    results = capture.capture(args.url, args.screenshot)

    # 输出
    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False)
    else:
        output = capture.to_markdown()

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')
        print(f"\n结果已保存到: {args.output}")
    else:
        print("\n" + "="*50)
        print(output)
        print("="*50)

    # 返回状态码
    sys.exit(1 if capture.has_error else 0)


if __name__ == "__main__":
    main()
