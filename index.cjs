// 결 gyeol — CommonJS entry
const tokens = require("./tokens.json");

const palettes = ["meok", "jjok", "cheongja", "songhwa", "yeonji", "jaju", "chija", "hwangto", "oksaek", "haneul", "odi"];
const themes = ["dark", "light", "system"];

/** <html data-palette> 값을 바꿔요. */
function setPalette(palette, el = typeof document !== "undefined" ? document.documentElement : null) {
  if (el) el.setAttribute("data-palette", palette);
}

/** <html data-theme> 값을 바꿔요. */
function setTheme(theme, el = typeof document !== "undefined" ? document.documentElement : null) {
  if (el) el.setAttribute("data-theme", theme);
}

/** 팔레트·테마·역할로 HEX 색을 돌려줘요. 예) color("meok", "dark", "accent") */
function color(palette, theme, role) {
  const p = tokens.gyeol.color[palette];
  if (!p) throw new Error(`gyeol: unknown palette "${palette}". Use one of: ${palettes.join(", ")}`);
  const t = p[theme];
  if (!t) throw new Error(`gyeol: unknown theme "${theme}". Use "light" or "dark"`);
  const r = t[role];
  if (!r) throw new Error(`gyeol: unknown color role "${role}". Use one of: ${Object.keys(t).join(", ")}`);
  return r.$value;
}

module.exports = { tokens, palettes, themes, setPalette, setTheme, color, default: tokens };
Object.defineProperty(module.exports, "__esModule", { value: true });
