"""결 gyeol 빌드: 팔레트 표 하나에서 tokens.json, index.mjs/cjs 목록, gyeol.min.css, 소개 사이트(index.html)를 만든다.

    python scripts/build.py [../gyeol.html]

팔레트를 추가할 때는 아래 PALETTES와 gyeol.css의 [data-palette] 규칙을 같이 고친다.
명도 대비(WCAG AA 4.5:1)를 못 넘는 조합이 있으면 멈춘다.
"""
import json, math, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# key: (이름, 바탕 색상각 h, 바탕 채도 c, 물감 색상각 ah, 물감 채도 ac, 물감 명도 보정 ad)
PALETTES = {
    "meok":     ("먹",   255, .012, 265, .14,  0),
    "jjok":     ("쪽빛", 265, .14,  265, .14,  0),
    "cheongja": ("청자", 178, .08,  178, .08,  .04),
    "songhwa":  ("송화",  98, .12,   98, .12,  0),
    "yeonji":   ("연지",  16, .16,   16, .16,  0),
    "jaju":     ("자주", 330, .13,  330, .13,  0),
    "chija":    ("치자",  70, .14,   70, .14,  0),
    "hwangto":  ("황토",  48, .065,  48, .065, 0),
    "oksaek":   ("옥색", 195, .10,  195, .10, -.05),
    "haneul":   ("하늘", 235, .14,  235, .14, -.05),
    "odi":      ("오디", 300, .15,  300, .15, -.05),
    "ssuk":     ("쑥",   135, .11,  135, .11,  0),
    "hongsi":   ("홍시",  42, .15,   42, .15,  .04),
}


def oklch_hex(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + .3963377774 * a + .2158037573 * b) ** 3
    m = (L - .1055613458 * a - .0638541728 * b) ** 3
    s = (L - .0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + .2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s,
           -.0041960863 * l - .7034186147 * m + 1.7076147010 * s)
    def gamma(x):
        x = min(1, max(0, x))
        return 12.92 * x if x <= .0031308 else 1.055 * x ** (1 / 2.4) - .055
    return "#" + "".join("%02x" % round(gamma(v) * 255) for v in rgb)


def contrast(x, y):
    def lum(h):
        v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        v = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in v]
        return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]
    a, b = sorted((lum(x), lum(y)))
    return (b + .05) / (a + .05)


def roles(h, c, ah, ac, ad, dark):
    """gyeol.css의 oklch 식과 같은 값."""
    if dark:
        return {"bg": (.17, c * .22, h), "bg-2": (.21, c * .3, h), "ink": (.95, c * .08, h),
                "ink-2": (.79, c * .15, h), "ink-3": (.70, c * .15, h), "line": (.33, c * .25, h),
                "paper": (.29, c * .25, h), "accent": (.76 + ad, ac, ah), "accent-soft": (.33, ac * .55, ah),
                "on-accent": (.18, .03, ah), "stain": (.48, c * .9 + .03, h + 70),
                "ok": (.74, .14, 150), "warn": (.80, .13, 75), "err": (.72, .16, 25)}
    return {"bg": (.965, c * .12, h), "bg-2": (.925, c * .22, h), "ink": (.23, c * .35, h),
            "ink-2": (.43, c * .25, h), "ink-3": (.50, c * .18, h), "line": (.84, c * .22, h),
            "paper": (.992, c * .05, h), "accent": (.49 + ad, ac, ah), "accent-soft": (.90, ac * .45, ah),
            "on-accent": (.99, 0, 0), "stain": (.80, c * .9 + .03, h + 70),
            "ok": (.50, .13, 150), "warn": (.54, .13, 65), "err": (.52, .19, 25)}


def build_colors():
    out, worst = {}, 99
    for key, (name, *v) in PALETTES.items():
        out[key] = {"$description": name}
        for theme in ("light", "dark"):
            hexes = {r: oklch_hex(*x) for r, x in roles(*v, theme == "dark").items()}
            out[key][theme] = {r: {"$type": "color", "$value": x} for r, x in hexes.items()}
            pairs = [("accent", "on-accent"), ("accent", "bg"), ("accent", "paper"),
                     ("ink-2", "paper"), ("ink-3", "bg")]
            for a, b in pairs:
                r = contrast(hexes[a], hexes[b])
                worst = min(worst, r)
                if r < 4.5:
                    sys.exit(f"대비 부족: {key} {theme} {a}/{b} = {r:.2f}")
    print(f"팔레트 {len(PALETTES)}종 x 2테마, 최소 대비 {worst:.2f}")
    return out


def minify_css(css):
    # 문자열(data URI 등)은 건드리지 않고, 주석과 공백만 줄인다. /*! 머리말은 남긴다.
    parts = re.split(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', css)
    for i in range(0, len(parts), 2):
        p = re.sub(r"/\*(?!!).*?\*/", "", parts[i], flags=re.S)
        p = re.sub(r"\s+", " ", p)
        p = re.sub(r"\s*([{};,>])\s*", r"\1", p)   # 앞뒤 공백 제거 (calc의 +,-와 선택자 앞 ':'은 그대로)
        p = re.sub(r":\s+", ":", p)
        p = p.replace(";}", "}")
        parts[i] = p
    return "".join(parts).strip() + "\n"


SITE_HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="한지를 겹겹이 올리는 디자인 시스템. CSS, Tailwind preset, DTCG 디자인 토큰.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#17191f">
<meta property="og:title" content="결 gyeol">
<meta property="og:description" content="한지를 겹겹이 올리는 디자인 시스템">
<meta property="og:image" content="https://minjaek111.github.io/gyeol/icon-512.png">
"""


def build_site(src):
    html = src.read_text(encoding="utf-8")
    html = html.replace('data-f="gyeol/', 'data-f="')
    html = re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + minify_css(m.group(1)) + "</style>", html, count=1, flags=re.S)
    html = html.replace("</style>\n", "</style>\n</head>\n<body>\n", 1)
    return SITE_HEAD + html + "\n</body>\n</html>\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    tokens_path = ROOT / "tokens.json"
    tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
    tokens["gyeol"]["color"] = build_colors()
    text = json.dumps(tokens, ensure_ascii=False, indent=2) + "\n"
    tokens_path.write_text(text, encoding="utf-8")

    keys = json.dumps(list(PALETTES), ensure_ascii=False).replace('","', '", "')
    mjs = (ROOT / "index.mjs").read_text(encoding="utf-8")
    body = mjs[mjs.index("\nexport const palettes"):]
    body = re.sub(r"export const palettes = \[.*?\];", f"export const palettes = {keys};", body)
    (ROOT / "index.mjs").write_text("// 결 gyeol — generated from tokens.json\nconst tokens = " + text.rstrip() + ";\n" + body, encoding="utf-8")

    cjs = (ROOT / "index.cjs").read_text(encoding="utf-8")
    (ROOT / "index.cjs").write_text(re.sub(r"const palettes = \[.*?\];", f"const palettes = {keys};", cjs), encoding="utf-8")

    css = (ROOT / "gyeol.css").read_text(encoding="utf-8")
    for k in PALETTES:
        if f'[data-palette="{k}"]' not in css:
            sys.exit(f"gyeol.css에 {k} 팔레트 규칙이 없어요")
    mini = minify_css(css)
    (ROOT / "gyeol.min.css").write_text(mini, encoding="utf-8")
    print(f"gyeol.css {len(css.encode()):,}B -> gyeol.min.css {len(mini.encode()):,}B")

    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "gyeol.html"
    if src.exists():
        site = build_site(src)
        (ROOT / "index.html").write_text(site, encoding="utf-8")
        print(f"index.html {len(site.encode()):,}B")


if __name__ == "__main__":
    main()
