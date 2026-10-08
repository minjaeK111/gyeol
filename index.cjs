// 결 gyeol — CommonJS entry
const tokens = require("./tokens.json");

const palettes = ["meok", "jjok", "cheongja", "songhwa", "yeonji", "jaju"];
const themes = ["dark", "light", "system"];

/** <html data-palette> 값을 바꿔요. */
function setPalette(palette, el = document.documentElement) {
  el.setAttribute("data-palette", palette);
}

/** <html data-theme> 값을 바꿔요. */
function setTheme(theme, el = document.documentElement) {
  el.setAttribute("data-theme", theme);
}

/** 팔레트·테마·역할로 HEX 색을 돌려줘요. 예) color("meok", "dark", "accent") */
function color(palette, theme, role) {
  return tokens.gyeol.color[palette][theme][role].$value;
}

module.exports = { tokens, palettes, themes, setPalette, setTheme, color, default: tokens };
