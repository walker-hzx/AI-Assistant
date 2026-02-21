#!/usr/bin/env python3
"""
分析 Headless UI (v1/vue) 网站结构
"""

from playwright.sync_api import sync_playwright
from pathlib import Path

def analyze_website():
    url = "https://headlessui.com/v1/vue"
    print(f"🔍 正在分析网站: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            # 访问首页
            page.goto(url, wait_until="networkidle", timeout=30000)
            print(f"✓ 页面加载完成")

            # 提取组件列表
            print("\n📋 提取组件列表...")

            # Headless UI v1 的组件通常在侧边栏或主要内容区
            # 尝试多种选择器
            component_links = []

            # 方法1: 查找所有包含 /v1/vue/ 的链接
            try:
                all_links = page.locator('a[href*="/v1/vue/"]').all()
                print(f"  找到 {len(all_links)} 个候选链接")

                for link in all_links:
                    try:
                        href = link.get_attribute('href')
                        text = link.inner_text()
                        # 过滤有效的组件链接
                        if href and '/v1/vue/' in href:
                            # 排除首页和已知非组件页面
                            if href not in [url, '/v1/vue', '/v1/vue/']:
                                component_links.append({
                                    'name': text.strip() if text else href.split('/')[-1],
                                    'href': href
                                })
                    except:
                        continue
            except Exception as e:
                print(f"  链接查找失败: {e}")

            # 方法2: 如果还是没找到，尝试获取页面所有文本内容分析
            if not component_links:
                print("\n  尝试备用方案：提取页面文本...")
                try:
                    page_text = page.inner_text('body')
                    print(f"  页面文本长度: {len(page_text)} 字符")
                    # 保存页面内容供分析
                    Path('/tmp/headlessui_page.html').write_text(page.content())
                    print("  已保存页面内容到 /tmp/headlessui_page.html")
                except Exception as e:
                    print(f"  备用方案失败: {e}")

            # 去重
            seen = set()
            unique_components = []
            for comp in component_links:
                key = comp['href']
                if key not in seen and comp['name']:
                    seen.add(key)
                    unique_components.append(comp)

            print(f"✓ 发现 {len(unique_components)} 个组件")

            # 分析第一个组件页面结构
            if unique_components:
                first_comp = unique_components[0]
                print(f"\n🔍 分析组件页面结构: {first_comp['name']}")

                comp_url = first_comp['href']
                if not comp_url.startswith('http'):
                    comp_url = f"https://headlessui.com{comp_url}"

                page.goto(comp_url, wait_until="networkidle", timeout=30000)

                # 分析页面结构
                structure = {
                    'has_description': False,
                    'has_code_examples': False,
                    'has_props_table': False,
                    'has_events': False,
                }

                # 检查描述
                try:
                    desc = page.locator('main p').first
                    if desc and len(desc.inner_text()) > 20:
                        structure['has_description'] = True
                        print("  ✓ 有描述文本")
                except:
                    pass

                # 检查代码示例
                try:
                    code_blocks = page.locator('pre code').count()
                    if code_blocks > 0:
                        structure['has_code_examples'] = True
                        print(f"  ✓ 有 {code_blocks} 个代码示例")
                except:
                    pass

                # 检查 API 表格
                try:
                    tables = page.locator('table').count()
                    if tables > 0:
                        structure['has_props_table'] = True
                        print(f"  ✓ 有 {tables} 个表格")
                except:
                    pass

                # 检查事件
                try:
                    events_heading = page.locator('h2:has-text("Events"), h3:has-text("Events")').count()
                    if events_heading > 0:
                        structure['has_events'] = True
                        print("  ✓ 有 Events 章节")
                except:
                    pass

            browser.close()

            # 输出分析结果
            print("\n" + "="*50)
            print("📊 网站分析结果")
            print("="*50)
            print(f"网站: {url}")
            print(f"组件数量: {len(unique_components)}")
            print("\n组件列表:")
            for i, comp in enumerate(unique_components[:10], 1):  # 只显示前10个
                print(f"  {i}. {comp['name']} - {comp['href']}")

            if len(unique_components) > 10:
                print(f"  ... 还有 {len(unique_components) - 10} 个组件")

            print("\n页面结构:")
            for key, value in structure.items():
                status = "✓" if value else "✗"
                print(f"  {status} {key}")

            return {
                'components': unique_components,
                'structure': structure,
                'url': url
            }

        except Exception as e:
            print(f"\n✗ 分析失败: {e}")
            browser.close()
            return None

if __name__ == "__main__":
    result = analyze_website()
