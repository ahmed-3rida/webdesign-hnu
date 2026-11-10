"""Generates the color-palette CSS and the palette list used by the picker,
and writes them into src/index.html between the PALETTES markers.

Usage: python3 tools/palettes.py
Edit PALETTES below to add or tweak a palette, then run it again.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.html"

# Each palette has a light and a dark set. Missing tokens are derived in fill().
# b1 = main button (yellow in Arcade), b2 = secondary button / level badge, b3 = third button.
PALETTES = {
    "arcade": {
        "name": "Arcade",
        "light": dict(bg="#f5f4f0", panel="#ffffff", panel2="#f1efe9", line="#d8d5ca", pxsh="#0b0d12", ink="#0b0d12", muted="#5d6474",
                      hl="#a35f00", acc="#4b55e8", acc2="#d97a08",
                      b1="#ffd23f", b1d="#c99a00", b1l="#fff3b0", b1t="#0b0d12",
                      b2="#7c88ff", b2d="#4b55e8", b2l="#b9c0ff", b2t="#05070d",
                      b3="#ffb547", b3d="#d97a08", b3l="#ffe0b0", b3t="#0b0d12",
                      hero="#1b2160", herosh="#b9c0ff", herospan="#e08a00", herospansh="#0b0d12",
                      star1="#c9c5b8", star2="#e6e3da", grid="#4b55e833", canvas="#ece9e1",
                      defbg="#eef0ff", deftx="#1d2350", tipbg="#fff8de", pickbg="#fff3c4", glow="rgba(75,85,232,.35)"),
        "dark": dict(bg="#05070d", panel="#0d111c", panel2="#151b2c", line="#262d45", pxsh="#262d45", ink="#eef1f8", muted="#8a93a8",
                     hl="#ffd23f", acc="#7c88ff", acc2="#ffb547",
                     b1="#ffd23f", b1d="#c99a00", b1l="#fff3b0", b1t="#0b0d12",
                     b2="#7c88ff", b2d="#4b55e8", b2l="#b9c0ff", b2t="#05070d",
                     b3="#ffb547", b3d="#d97a08", b3l="#ffe0b0", b3t="#0b0d12",
                     hero="#dfe3ff", herosh="#4b55e8", herospan="#ffd23f", herospansh="#a86f00",
                     star1="#8a93a8", star2="#262d45", grid="#7c88ff55", canvas="#0a0d16",
                     defbg="#0a0d16", deftx="#d6dbff", tipbg="#1a1708", pickbg="#2e2810", glow="rgba(124,136,255,.45)"),
    },
    "matcha": {
        "name": "Matcha",
        "light": dict(bg="#f1f5ef", panel="#ffffff", panel2="#e7eee4", line="#cbd9c6", pxsh="#10231a", ink="#10231a", muted="#52665a",
                      hl="#1d7148", acc="#1f8f5f", acc2="#b85a1f",
                      b1="#3ddc97", b1d="#1f9e66", b1l="#c2f7df", b1t="#0b1f15",
                      b2="#1f8f5f", b2d="#14623f", b2l="#7fd3ab", b2t="#ffffff",
                      b3="#ffb36b", b3d="#d97a2b", b3l="#ffe1c2", b3t="#2a1608",
                      hero="#123d29", herosh="#a8e6c9", herospan="#1f9e66", herospansh="#10231a",
                      defbg="#e3f3ea", tipbg="#eef7e6", pickbg="#dcf5e8"),
        "dark": dict(bg="#06100b", panel="#0d1b14", panel2="#13261c", line="#21412f", pxsh="#21412f", ink="#e8f5ee", muted="#8fb1a0",
                     hl="#6ff2b5", acc="#3ddc97", acc2="#ffb36b",
                     b1="#3ddc97", b1d="#1f9e66", b1l="#c2f7df", b1t="#06100b",
                     b2="#a3e635", b2d="#6b9a1c", b2l="#e4f9b8", b2t="#0f1a04",
                     b3="#ffb36b", b3d="#d97a2b", b3l="#ffe1c2", b3t="#2a1608",
                     hero="#d9fbe9", herosh="#1f9e66", herospan="#6ff2b5", herospansh="#0b5a3a",
                     defbg="#0a1711", tipbg="#0f1f12", pickbg="#123020"),
    },
    "ocean": {
        "name": "Ocean",
        "light": dict(bg="#eef5f9", panel="#ffffff", panel2="#e2edf4", line="#c6d9e5", pxsh="#0b2233", ink="#0b2233", muted="#4f6b7d",
                      hl="#0a64a0", acc="#0277b8", acc2="#0f8a7e",
                      b1="#38bdf8", b1d="#0284c7", b1l="#c7ecfd", b1t="#062033",
                      b2="#0f766e", b2d="#0a524d", b2l="#7fd8cc", b2t="#ffffff",
                      b3="#fbbf24", b3d="#c98a00", b3l="#fde9a8", b3t="#2a1d00",
                      hero="#0b3554", herosh="#9fd8f5", herospan="#0284c7", herospansh="#0b2233",
                      defbg="#e3f2fb", tipbg="#e8f6f4", pickbg="#d9effb"),
        "dark": dict(bg="#040b13", panel="#0a1622", panel2="#0f2030", line="#1b3347", pxsh="#1b3347", ink="#e6f3fb", muted="#8aa7ba",
                     hl="#7dd3fc", acc="#38bdf8", acc2="#2dd4bf",
                     b1="#38bdf8", b1d="#0284c7", b1l="#c7ecfd", b1t="#04121d",
                     b2="#2dd4bf", b2d="#0f9a88", b2l="#b4f3ea", b2t="#04121d",
                     b3="#fbbf24", b3d="#c98a00", b3l="#fde9a8", b3t="#2a1d00",
                     hero="#e0f2fe", herosh="#0369a1", herospan="#7dd3fc", herospansh="#0b3554",
                     defbg="#071521", tipbg="#08191c", pickbg="#0b2236"),
    },
    "sunset": {
        "name": "Sunset",
        "light": dict(bg="#fbf3ee", panel="#ffffff", panel2="#f6e8df", line="#ead2c4", pxsh="#2a1320", ink="#2a1320", muted="#7a5c66",
                      hl="#b8400c", acc="#c92a62", acc2="#6d3ad6",
                      b1="#ff8a5b", b1d="#d9592c", b1l="#ffd5c3", b1t="#2a1320",
                      b2="#d6336c", b2d="#9e1f4c", b2l="#ffaccb", b2t="#ffffff",
                      b3="#a78bfa", b3d="#7c3aed", b3l="#e2d8ff", b3t="#1e0f3a",
                      hero="#4a1530", herosh="#ffbfa8", herospan="#e8572a", herospansh="#2a1320",
                      defbg="#fdebe4", tipbg="#fff0e6", pickbg="#ffe3d6"),
        "dark": dict(bg="#110910", panel="#1c1017", panel2="#271621", line="#3e2433", pxsh="#3e2433", ink="#fbeef2", muted="#b8949f",
                     hl="#ffb38a", acc="#ff6b9a", acc2="#b69cff",
                     b1="#ff8a5b", b1d="#d9592c", b1l="#ffd5c3", b1t="#1c0b06",
                     b2="#ff6b9a", b2d="#c23a68", b2l="#ffc2d6", b2t="#1c0610",
                     b3="#b69cff", b3d="#7c3aed", b3l="#e6ddff", b3t="#160a30",
                     hero="#ffe3d6", herosh="#b8400c", herospan="#ffb38a", herospansh="#7a1e3a",
                     defbg="#180c14", tipbg="#1f1009", pickbg="#2c1520"),
    },
    "sakura": {
        "name": "Sakura",
        "light": dict(bg="#fbf4f7", panel="#ffffff", panel2="#f5e7ee", line="#ebd0dc", pxsh="#2b1420", ink="#2b1420", muted="#7b5a69",
                      hl="#a8285f", acc="#c81f6c", acc2="#6a4fe0",
                      b1="#f9a8d4", b1d="#db2777", b1l="#fde2f0", b1t="#2b1420",
                      b2="#a78bfa", b2d="#7c3aed", b2l="#e4dcff", b2t="#1e0f3a",
                      b3="#fcd34d", b3d="#d4a017", b3l="#fff0b3", b3t="#2a1d00",
                      hero="#5a1a3a", herosh="#f9c4dd", herospan="#db2777", herospansh="#2b1420",
                      defbg="#fbe7f1", tipbg="#fff6dc", pickbg="#fde2f0"),
        "dark": dict(bg="#10080d", panel="#1b0f16", panel2="#26141f", line="#3c2232", pxsh="#3c2232", ink="#fbeaf2", muted="#b893a5",
                     hl="#f9a8d4", acc="#f472b6", acc2="#a78bfa",
                     b1="#f9a8d4", b1d="#db2777", b1l="#fde2f0", b1t="#2b1420",
                     b2="#a78bfa", b2d="#7c3aed", b2l="#e4dcff", b2t="#1e0f3a",
                     b3="#fcd34d", b3d="#d4a017", b3l="#fff0b3", b3t="#2a1d00",
                     hero="#ffe4f1", herosh="#9d174d", herospan="#f9a8d4", herospansh="#6b1239",
                     defbg="#170a12", tipbg="#1d1508", pickbg="#2a1220"),
    },
    "mono": {
        "name": "Mono",
        "light": dict(bg="#f4f4f4", panel="#ffffff", panel2="#ebebeb", line="#d2d2d2", pxsh="#111111", ink="#111111", muted="#5c5c5c",
                      hl="#c01540", acc="#111111", acc2="#c01540",
                      b1="#111111", b1d="#000000", b1l="#4a4a4a", b1t="#ffffff",
                      b2="#ffffff", b2d="#bdbdbd", b2l="#ffffff", b2t="#111111",
                      b3="#e11d48", b3d="#9f1239", b3l="#fb7185", b3t="#ffffff",
                      hero="#111111", herosh="#cfcfcf", herospan="#e11d48", herospansh="#111111",
                      grid="#11111122", defbg="#efefef", tipbg="#fbeef1", pickbg="#ececec", glow="rgba(0,0,0,.25)"),
        "dark": dict(bg="#0a0a0a", panel="#141414", panel2="#1c1c1c", line="#2f2f2f", pxsh="#2f2f2f", ink="#f2f2f2", muted="#9a9a9a",
                     hl="#fb7185", acc="#f2f2f2", acc2="#fb7185",
                     b1="#f2f2f2", b1d="#9a9a9a", b1l="#ffffff", b1t="#0a0a0a",
                     b2="#2f2f2f", b2d="#000000", b2l="#555555", b2t="#ffffff",
                     b3="#fb7185", b3d="#be123c", b3l="#fecdd3", b3t="#1a0509",
                     hero="#ffffff", herosh="#3a3a3a", herospan="#fb7185", herospansh="#000000",
                     grid="#ffffff22", defbg="#111111", tipbg="#1a0f11", pickbg="#222222", glow="rgba(255,255,255,.2)"),
    },
}

SEMANTIC = {
    "light": dict(rose="#d6304f", ok="#12804a", okbg="#e3f5ea", badbg="#fde8ec", ground="#0b0d12", scheme="light"),
    "dark": dict(rose="#ff4d6d", ok="#3ddc97", okbg="#0f3a2c", badbg="#3a1220", ground="#ffffff", scheme="dark"),
}


def fill(t, mode):
    t = dict(t)
    t.setdefault("star1", t["muted"])
    t.setdefault("star2", t["line"])
    t.setdefault("grid", t["acc"] + ("44" if mode == "dark" else "33"))
    t.setdefault("canvas", t["panel2"])
    t.setdefault("defbg", t["panel2"])
    t.setdefault("deftx", t["ink"])
    t.setdefault("tipbg", t["panel2"])
    t.setdefault("pickbg", t["panel2"])
    t.setdefault("glow", t["acc"] + "66")
    s = {**SEMANTIC[mode]}
    scheme = s.pop("scheme")
    t.update(s)
    return t, scheme


def block(sel, t, scheme):
    body = "".join(f"--{k}:{v};" for k, v in t.items())
    return f"{sel}{{{body}color-scheme:{scheme}}}"


def css():
    out = []
    for key, p in PALETTES.items():
        lt, ls = fill(p["light"], "light")
        dk, ds = fill(p["dark"], "dark")
        base = ':root' if key == "arcade" else f':root[data-pal="{key}"]'
        # light: default (or explicit light)
        out.append(block(base + ("" if key == "arcade" else ""), lt, ls))
        # dark from system, unless light chosen
        sys_sel = (':root:not([data-theme="light"])' if key == "arcade" else f':root[data-pal="{key}"]:not([data-theme="light"])')
        out.append("@media (prefers-color-scheme: dark){" + block(sys_sel, dk, ds) + "}")
        exp = (':root[data-theme="dark"]' if key == "arcade" else f':root[data-pal="{key}"][data-theme="dark"]')
        out.append(block(exp, dk, ds))
        if key == "arcade":
            # explicit light must also win over a non-arcade palette's system dark: handled by palette selectors' :not()
            pass
    return "\n".join(out)


def js():
    lst = []
    for key, p in PALETTES.items():
        lt, _ = fill(p["light"], "light")
        dk, _ = fill(p["dark"], "dark")
        lst.append({"k": key, "n": p["name"],
                    "l": [lt["bg"], lt["b1"], lt["b2"], lt["b3"]],
                    "d": [dk["bg"], dk["b1"], dk["b2"], dk["b3"]]})
    return "const PALS=" + json.dumps(lst) + ";"


def main():
    s = SRC.read_text(encoding="utf8")
    s = re.sub(r"/\*PALETTES-CSS\*/[\s\S]*?/\*END-PALETTES-CSS\*/",
               lambda m: "/*PALETTES-CSS*/\n" + css() + "\n/*END-PALETTES-CSS*/", s)
    s = re.sub(r"/\*PALETTES-JS\*/[\s\S]*?/\*END-PALETTES-JS\*/",
               lambda m: "/*PALETTES-JS*/" + js() + "/*END-PALETTES-JS*/", s)
    SRC.write_text(s, encoding="utf8")
    print("palettes:", ", ".join(PALETTES))


if __name__ == "__main__":
    main()
