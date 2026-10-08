# 결 gyeol

한지를 겹겹이 올리듯 화면을 쌓는 디자인 시스템이에요. 다른 프로젝트나 도구에서 쓸 수 있게 세 가지 형식으로 나눠 두었어요.

```bash
npm install gyeol
```

소개 사이트: https://minjaek111.github.io/gyeol/

| 파일 | 쓰는 곳 |
| --- | --- |
| `gyeol.css` | 아무 웹 프로젝트(HTML, React, Vue, Svelte 등). 토큰, 팔레트, 테마, 겹 소재, 컴포넌트 클래스가 모두 들어 있어요. |
| `tailwind.preset.cjs` | Tailwind CSS 프로젝트. `gyeol.css`의 CSS 변수를 Tailwind 클래스로 연결해요. |
| `tokens.json` | 디자인 토큰 표준(DTCG) 형식. Figma Tokens Studio, Style Dictionary, iOS·Android 변환에 써요. |

## 1. 웹 (CSS)

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@300;500;700;800&family=IBM+Plex+Sans+KR:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gyeol@0.1.0/gyeol.css">

<html data-palette="meok" data-theme="dark">
<body class="gy">
  <div class="gy-gyeop gy-du">
    <button class="gy-btn">저장하기</button>
    <button class="gy-btn gy-btn--paper">취소</button>
  </div>
</body>
```

번들러(Vite, Next.js 등)를 쓰면 CSS를 이렇게 불러와요.

```js
import 'gyeol/gyeol.css';
import { setPalette, setTheme, color, tokens } from 'gyeol';

setPalette('cheongja');
setTheme('light');
color('meok', 'dark', 'accent'); // '#85aeff'
```

- `data-palette`: `meok`(기본) · `jjok` · `cheongja` · `songhwa` · `yeonji` · `jaju`
- `data-theme`: `dark`(기본) · `light` · `system`
- 컴포넌트 클래스는 모두 `gy-` 접두사를 써서 기존 CSS와 겹치지 않아요.

| 컴포넌트 | 클래스 |
| --- | --- |
| 겹 소재 | `gy-gyeop` + `gy-hol` / `gy-du` / `gy-se` |
| 버튼 | `gy-btn` + `--ink` / `--paper` / `--ghost` / `--danger` / `--sm` |
| 스위치 | `<button class="gy-switch" role="switch" aria-checked="true">` |
| 세그먼트 | `gy-seg` 안에 `aria-pressed` 버튼 |
| 칩 | `gy-chip` + `aria-pressed` |
| 입력 필드 | `gy-field` (오류는 `gy-field--error`) |
| 체크박스 | `<label class="gy-check"><input type="checkbox"> 텍스트</label>` |
| 배지 | `gy-badge` + `--ok` / `--warn` / `--err` |
| 진행 막대 | `<div class="gy-progress" style="--p:60%"><i></i></div>` |
| 토스트·툴팁 | `gy-toast`(겹과 함께), `gy-tooltip` |

## 2. Tailwind

```js
// tailwind.config.js
module.exports = {
  presets: [require('gyeol/tailwind')],
};
```

`gyeol.css`를 함께 불러와야 색이 정의돼요. 그다음 `bg-paper`, `text-ink-2`, `bg-accent`, `p-pun-4`, `rounded-r-3`, `font-display`, `gyeop gyeop-du`처럼 써요.

## 3. 디자인 토큰 JSON (Figma, iOS, Android)

`tokens.json`은 [DTCG](https://tr.designtokens.org/format/) 형식이고, 색은 팔레트·테마별로 계산된 HEX 값이에요.

```
gyeol.color.<팔레트>.<light|dark>.<역할>   예) gyeol.color.meok.dark.accent = #85aeff
gyeol.space.pun-4 = 16px
gyeol.radius.r-3 = 20px
gyeol.material.du.thickness = 0.72
```

- **JS에서 바로**: `import tokens from 'gyeol'` 또는 `import tokens from 'gyeol/tokens.json'`
- **Figma**: Tokens Studio 플러그인에서 `tokens.json`을 불러오세요.
- **iOS / Android**: Style Dictionary로 `tokens.json`을 Swift, Kotlin, XML 리소스로 변환하세요.

HEX 값은 화면용 sRGB로 변환한 근사치예요. 웹에서는 `gyeol.css`의 oklch 원본을 쓰는 게 더 정확해요.

## 패키지 경로

| 경로 | 내용 |
| --- | --- |
| `gyeol` | 토큰 객체와 `setPalette`, `setTheme`, `color` 함수 (ESM·CommonJS·TypeScript 타입 포함) |
| `gyeol/gyeol.css` (또는 `gyeol/css`) | 전체 CSS |
| `gyeol/tailwind` | Tailwind 프리셋 |
| `gyeol/tokens.json` | DTCG 토큰 원본 |

## 라이선스

MIT
