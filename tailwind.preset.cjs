// 결 gyeol — Tailwind CSS preset (v3 / v4 config 호환)
// 1) gyeol.css를 먼저 불러와 CSS 변수를 정의하세요.
// 2) tailwind.config.js: module.exports = { presets: [require('gyeol/tailwind')] }
// 색은 CSS 변수를 그대로 참조하므로 data-palette / data-theme을 바꾸면 Tailwind 클래스도 함께 바뀌어요.
const plugin = require('tailwindcss/plugin');

module.exports = {
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        'bg-2': 'var(--bg-2)',
        paper: 'var(--paper)',
        ink: { DEFAULT: 'var(--ink)', 2: 'var(--ink-2)', 3: 'var(--ink-3)' },
        line: 'var(--line)',
        accent: { DEFAULT: 'var(--accent)', soft: 'var(--accent-soft)', on: 'var(--on-accent)' },
        stain: 'var(--stain)',
        ok: 'var(--ok)',
        warn: 'var(--warn)',
        err: 'var(--err)',
      },
      fontFamily: {
        display: ['Hahmlet', 'Nanum Myeongjo', 'serif'],
        body: ['IBM Plex Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', 'sans-serif'],
        mono: ['IBM Plex Mono', 'Consolas', 'monospace'],
      },
      fontSize: {
        display: ['72px', { lineHeight: '0.92', fontWeight: '800' }],
        h1: ['40px', { lineHeight: '1.1', fontWeight: '700' }],
        h2: ['28px', { lineHeight: '1.2', fontWeight: '700' }],
        h3: ['20px', { lineHeight: '1.3', fontWeight: '600' }],
        body: ['16px', { lineHeight: '1.65' }],
        label: ['12px', { lineHeight: '1', letterSpacing: '.12em' }],
      },
      spacing: {
        'pun-1': '4px', 'pun-2': '8px', 'pun-3': '12px', 'pun-4': '16px',
        'pun-6': '24px', 'pun-8': '32px', 'pun-12': '48px', 'pun-16': '64px',
      },
      borderRadius: { 'r-1': '6px', 'r-2': '12px', 'r-3': '20px', 'r-4': '28px' },
      transitionTimingFunction: { bleed: 'cubic-bezier(.2,.7,.2,1)' },
      transitionDuration: { 't-1': '120ms', 't-2': '220ms', 't-3': '420ms' },
      boxShadow: { paper: 'var(--shadow)' },
    },
  },
  plugins: [
    // 겹 소재: class="gyeop gyeop-du"
    plugin(({ addComponents }) => {
      addComponents({
        '.gyeop': {
          position: 'relative', isolation: 'isolate',
          background: 'color-mix(in oklch, var(--paper) var(--thick, 74%), transparent)',
          backdropFilter: 'blur(var(--blur, 14px)) saturate(1.2)',
          border: '1px solid color-mix(in oklch, var(--paper) 50%, var(--line))',
          borderRadius: '20px', boxShadow: 'var(--shadow)',
        },
        '.gyeop::before': {
          content: '""', position: 'absolute', inset: '0', borderRadius: 'inherit',
          backgroundImage: 'var(--grain)', opacity: 'var(--grain-o)', pointerEvents: 'none', zIndex: '-1',
        },
        '.gyeop-hol': { '--thick': '46%', '--blur': '6px' },
        '.gyeop-du': { '--thick': '72%', '--blur': '14px' },
        '.gyeop-se': { '--thick': '90%', '--blur': '24px' },
      });
    }),
  ],
};
