export type Palette = "meok" | "jjok" | "cheongja" | "songhwa" | "yeonji" | "jaju";
export type Theme = "dark" | "light" | "system";
export type ColorMode = "light" | "dark";
export type ColorRole =
  | "bg" | "bg-2" | "ink" | "ink-2" | "ink-3" | "line" | "paper"
  | "accent" | "accent-soft" | "on-accent" | "stain" | "ok" | "warn" | "err";

interface Token<T> { $type: string; $value: T; $description?: string }

export interface GyeolTokens {
  gyeol: {
    color: Record<Palette, { $description: string } & Record<ColorMode, Record<ColorRole, Token<string>>>>;
    font: Record<"display" | "body" | "mono", Token<string[]>>;
    type: Record<"display" | "h1" | "h2" | "h3" | "body" | "label", Token<{ fontFamily: string; fontSize: string; fontWeight: number; lineHeight: number }>>;
    space: Record<"pun-1" | "pun-2" | "pun-3" | "pun-4" | "pun-6" | "pun-8" | "pun-12" | "pun-16", Token<string>>;
    radius: Record<"r-1" | "r-2" | "r-3" | "r-4" | "pill", Token<string>>;
    duration: Record<"t-1" | "t-2" | "t-3", Token<string>>;
    easing: { bleed: Token<[number, number, number, number]> };
    material: Record<"hol" | "du" | "se", { thickness: Token<number>; blur: Token<string> }>;
  };
}

export declare const tokens: GyeolTokens;
export declare const palettes: Palette[];
export declare const themes: Theme[];
export declare function setPalette(palette: Palette, el?: HTMLElement): void;
export declare function setTheme(theme: Theme, el?: HTMLElement): void;
export declare function color(palette: Palette, theme: ColorMode, role: ColorRole): string;
export default tokens;
