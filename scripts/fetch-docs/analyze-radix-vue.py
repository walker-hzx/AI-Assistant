#!/usr/bin/env python3
"""
分析 Radix Vue 网站结构
https://www.radix-vue.com/
"""

from playwright.sync_api import sync_playwright
from pathlib import Path


def analyze_website():
    url = "https://www.radix-vue.com/overview/getting-started.html"
    print(f"🔍 正在分析网站: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            # 访问首页
            print("  加载页面...")
            page.goto(url, wait_until="networkidle", timeout=30000)
            print(f"  ✓ 页面加载完成")

            # 等待内容加载 - Radix Vue 使用动态渲染
            print("  等待内容渲染...")
            page.wait_for_selector("nav, .sidebar, aside", timeout=10000)

            # 提取组件列表
            print("\n📋 提取组件列表...")
            component_links = []

            # 方法1: 查找导航菜单中的组件链接
            try:
                # Radix Vue 的导航通常在侧边栏
                links = page.locator(
                    'nav a[href*="/components/"], aside a[href*="/components/"], .sidebar a[href*="/components/"]'
                ).all()
                print(f"  找到 {len(links)} 个候选链接")

                for link in links:
                    try:
                        href = link.get_attribute("href")
                        text = link.inner_text()
                        if href and "/components/" in href:
                            # 清理文本
                            name = text.strip() if text else href.split("/")[-1]
                            # 去重
                            if not any(c["href"] == href for c in component_links):
                                component_links.append({"name": name, "href": href})
                    except:
                        continue
            except Exception as e:
                print(f"  导航查找失败: {e}")

            # 方法2: 直接访问组件页面获取列表
            if not component_links:
                print("  尝试访问组件概览页面...")
                try:
                    page.goto(
                        "https://www.radix-vue.com/components/accordion.html",
                        wait_until="networkidle",
                    )
                    page.wait_for_timeout(2000)

                    # 提取所有链接
                    all_links = page.locator('a[href*="/components/"]').all()
                    for link in all_links:
                        try:
                            href = link.get_attribute("href")
                            text = link.inner_text()
                            if href and "/components/" in href:
                                name = text.strip() if text else href.split("/")[-1]
                                if not any(c["href"] == href for c in component_links):
                                    component_links.append({"name": name, "href": href})
                        except:
                            continue
                except Exception as e:
                    print(f"  备选方案失败: {e}")

            print(f"✓ 发现 {len(component_links)} 个组件")

            # 分析第一个组件页面
            if component_links:
                first_comp = component_links[0]
                print(f"\n🔍 分析组件页面结构: {first_comp['name']}")

                comp_url = first_comp["href"]
                if not comp_url.startswith("http"):
                    comp_url = f"https://www.radix-vue.com{comp_url}"

                page.goto(comp_url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(2000)  # 额外等待动态内容

                structure = {
                    "has_description": False,
                    "has_code_examples": False,
                    "has_props_table": False,
                    "has_events": False,
                    "has_usage": False,
                }

                # 检查描述
                try:
                    paragraphs = page.locator("main p, article p").all()
                    for p in paragraphs[:3]:
                        text = p.inner_text()
                        if text and len(text) > 20:
                            structure["has_description"] = True
                            print(f"  ✓ 有描述文本: {text[:50]}...")
                            break
                except:
                    pass

                # 检查代码示例
                try:
                    code_blocks = page.locator("pre code, pre[class*='language']").count()
                    if code_blocks > 0:
                        structure["has_code_examples"] = True
                        print(f"  ✓ 有 {code_blocks} 个代码示例")
                except:
                    pass

                # 检查 API 表格
                try:
                    tables = page.locator("table").count()
                    if tables > 0:
                        structure["has_props_table"] = True
                        print(f"  ✓ 有 {tables} 个表格")
                except:
                    pass

                # 检查 Usage 章节
                try:
                    usage_heading = page.locator(
                        "h2:has-text('Usage'), h3:has-text('Usage'), h2:has-text('用法'), h3:has-text('用法')"
                    ).count()
                    if usage_heading > 0:
                        structure["has_usage"] = True
                        print("  ✓ 有 Usage 章节")
                except:
                    pass

                # 保存页面源码供分析
                try:
                    html_content = page.content()
                    Path("/tmp/radix-vue-component.html").write_text(html_content)
                    print("  ✓ 已保存页面源码到 /tmp/radix-vue-component.html")
                except:
                    pass

            browser.close()

            # 输出分析结果
            print("\n" + "=" * 50)
            print("📊 网站分析结果")
            print("=" * 50)
            print(f"网站: {url}")
            print(f"组件数量: {len(component_links)}")
            print("\n组件列表 (前10个):")
            for i, comp in enumerate(component_links[:10], 1):
                print(f"  {i}. {comp['name']} - {comp['href']}")

            if len(component_links) > 10:
                print(f"  ... 还有 {len(component_links) - 10} 个组件")

            print("\n页面结构:")
            for key, value in structure.items():
                status = "✓" if value else "✗"
                print(f"  {status} {key}")

            return {
                "components": component_links,
                "structure": structure,
                "url": url,
            }

        except Exception as e:
            print(f"\n✗ 分析失败: {e}")
            import traceback

            traceback.print_exc()
            browser.close()
            return None


if __name__ == "__main__":
    result = analyze_website()
