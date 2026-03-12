#!/usr/bin/env python3
"""
DOM 样式检查器

获取元素的 computed styles、CSS 变量、DOM 结构等信息，
用于排查前端样式问题。

用法：
    python dom-inspector.py <url> --selector ".button" --styles
    python dom-inspector.py <url> --selector "#header" --css-vars
    python dom-inspector.py <url> --selector ".card" --all --screenshot output.png
"""

import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def get_computed_styles(page, selector: str) -> dict:
    """获取元素的 computed style"""
    result = page.evaluate(f"""
        () => {{
            const el = document.querySelector('{selector}');
            if (!el) return null;

            const computed = window.getComputedStyle(el);
            const styles = {{}};

            // 关键样式属性
            const props = [
                'display', 'position', 'top', 'right', 'bottom', 'left',
                'width', 'height', 'margin', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
                'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
                'border', 'border-width', 'border-style', 'border-color',
                'background', 'background-color', 'background-image',
                'color', 'font', 'font-size', 'font-weight', 'font-family',
                'line-height', 'text-align', 'vertical-align',
                'flex', 'flex-direction', 'flex-wrap', 'justify-content', 'align-items', 'align-content',
                'grid', 'grid-template-columns', 'grid-template-rows',
                'overflow', 'overflow-x', 'overflow-y',
                'z-index', 'opacity', 'visibility',
                'transform', 'transition', 'animation'
            ];

            for (const prop of props) {{
                styles[prop] = computed.getPropertyValue(prop).trim();
            }}

            // 盒子模型
            styles['box-model'] = {{
                'margin': computed.margin,
                'border': computed.border,
                'padding': computed.padding,
                'width': computed.width,
                'height': computed.height,
                'innerWidth': el.clientWidth,
                'innerHeight': el.clientHeight,
                'outerWidth': el.offsetWidth,
                'outerHeight': el.offsetHeight
            }};

            return styles;
        }}
    """)
    return result


def get_css_variables(page, selector: str) -> dict:
    """获取元素上的 CSS 变量值"""
    result = page.evaluate(f"""
        () => {{
            const el = document.querySelector('{selector}');
            if (!el) return null;

            const vars = {{}};
            const computed = window.getComputedStyle(el);

            // 获取所有 CSS 变量
            for (let i = 0; i < computed.length; i++) {{
                const prop = computed[i];
                if (prop.startsWith('--')) {{
                    vars[prop] = computed.getPropertyValue(prop).trim();
                }}
            }}

            // 同时检查父级链上的变量继承
            let parent = el.parentElement;
            let level = 1;
            while (parent && level <= 5) {{
                const parentComputed = window.getComputedStyle(parent);
                for (let i = 0; i < parentComputed.length; i++) {{
                    const prop = parentComputed[i];
                    if (prop.startsWith('--') && !vars[prop]) {{
                        vars[prop + ` (继承, 父级 level ${level})`] = parentComputed.getPropertyValue(prop).trim();
                    }}
                }}
                parent = parent.parentElement;
                level++;
            }}

            return vars;
        }}
    """)
    return result


def get_element_info(page, selector: str) -> dict:
    """获取元素的完整信息"""
    result = page.evaluate(f"""
        () => {{
            const el = document.querySelector('{selector}');
            if (!el) return null;

            return {{
                'tag': el.tagName.toLowerCase(),
                'id': el.id || null,
                'class': el.className || null,
                'classes': el.classList ? Array.from(el.classList) : [],
                'inlineStyles': el.style.cssText || null,
                'attributes': Array.from(el.attributes).reduce((acc, attr) => {{
                    acc[attr.name] = attr.value;
                    return acc;
                }}, {{}}),
                'parent': el.parentElement ? el.parentElement.tagName.toLowerCase() : null,
                'childrenCount': el.children.length,
                'visible': el.offsetParent !== null,
                'bounds': el.getBoundingClientRect().toJSON()
            }};
        }}
    """)
    return result


def get_selector_specificity(page, selector: str) -> dict:
    """分析选择器的特异性"""
    result = page.evaluate(f"""
        () => {{
            const el = document.querySelector('{selector}');
            if (!el) return null;

            // 简单的特异性计算
            let specificity = {{ ids: 0, classes: 0, tags: 0 }};

            // 检查当前元素匹配哪些规则
            const sheets = document.styleSheets;
            let matchingRules = [];

            try {{
                for (const sheet of sheets) {{
                    try {{
                        const rules = sheet.cssRules || sheet.rules;
                        for (const rule of rules) {{
                            try {{
                                if (el.matches(rule.selectorText)) {{
                                    matchingRules.push({{
                                        selector: rule.selectorText,
                                        cssText: rule.cssText.substring(0, 200)
                                    }});
                                }}
                            }} catch(e) {{}}
                        }}
                    }} catch(e) {{}}
                }}
            }} catch(e) {{}}

            return {{
                'element': {{
                    id: el.id || null,
                    classes: Array.from(el.classList),
                    tag: el.tagName.toLowerCase()
                }},
                'matchingRulesCount': matchingRules.length,
                'topMatchingRules': matchingRules.slice(0, 10)
            }};
        }}
    """)
    return result


def capture_screenshot(page, selector: str, output: str) -> str:
    """截取元素所在区域的截图"""
    bounds = page.evaluate(f"""
        () => {{
            const el = document.querySelector('{selector}');
            if (!el) return null;
            const rect = el.getBoundingClientRect();
            return {{
                x: Math.max(0, rect.x - 50),
                y: Math.max(0, rect.y - 50),
                width: rect.width + 100,
                height: rect.height + 100
            }};
        }}
    """)

    if bounds:
        page.screenshot(path=output, clip=bounds)
        return output
    return None


def main():
    parser = argparse.ArgumentParser(description='DOM 样式检查器')
    parser.add_argument('url', help='要检查的 URL')
    parser.add_argument('--selector', '-s', required=True, help='CSS 选择器')
    parser.add_argument('--styles', '-st', action='store_true', help='获取 computed styles')
    parser.add_argument('--css-vars', '-cv', action='store_true', help='获取 CSS 变量')
    parser.add_argument('--info', '-i', action='store_true', help='获取元素基本信息')
    parser.add_argument('--specificity', '-sp', action='store_true', help='分析选择器特异性')
    parser.add_argument('--all', '-a', action='store_true', help='获取所有信息')
    parser.add_argument('--screenshot', '-sh', help='截图输出路径')
    parser.add_argument('--output', '-o', help='JSON 输出文件')
    parser.add_argument('--wait', '-w', type=int, default=3, help='等待秒数')

    args = parser.parse_args()

    result = {
        'url': args.url,
        'selector': args.selector,
        'data': {}
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(args.url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(args.wait * 1000)

        # 检查元素是否存在
        exists = page.evaluate(f"""
            () => document.querySelector('{args.selector}') !== null
        """)

        if not exists:
            print(f"错误: 未找到匹配 '{args.selector}' 的元素")
            browser.close()
            sys.exit(1)

        # 获取各项信息
        if args.all or args.styles:
            result['data']['computed_styles'] = get_computed_styles(page, args.selector)

        if args.all or args.css_vars:
            result['data']['css_variables'] = get_css_variables(page, args.selector)

        if args.all or args.info:
            result['data']['element_info'] = get_element_info(page, args.selector)

        if args.all or args.specificity:
            result['data']['selector_specificity'] = get_selector_specificity(page, args.selector)

        # 截图
        if args.screenshot:
            result['data']['screenshot'] = capture_screenshot(page, args.selector, args.screenshot)

        browser.close()

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
