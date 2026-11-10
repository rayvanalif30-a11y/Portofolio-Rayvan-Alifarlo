"""Rakit portfolio-src.html dan cv-src.html menjadi dua file HTML siap buka.
Pakai: python build.py   ->  menghasilkan portfolio.html dan cv.html di folder ini."""
import base64, pathlib
R = pathlib.Path(__file__).parent
b64 = lambda p: base64.b64encode((R / p).read_bytes()).decode()
def font(name, fam, w, st='normal'):
    return f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(data:font/woff2;base64,{b64("assets/fonts/" + name + ".woff2")}) format("woff2")}}'
FONTS = {
    'portfolio': font('space-grotesk-latin-wght-normal', 'Space Grotesk Variable', '300 700') + font('archivo-latin-wght-normal', 'Archivo Variable', '100 900'),
    'cv': font('libre-bodoni-latin-wght-normal', 'Libre Bodoni Variable', '400 700') + font('libre-bodoni-latin-wght-italic', 'Libre Bodoni Variable', '400 700', 'italic') + font('public-sans-latin-wght-normal', 'Public Sans Variable', '100 900'),
}
css = (R / 'engine/scrollcraft.css').read_text(encoding='utf-8')
js = (R / 'engine/scrollcraft.js').read_text(encoding='utf-8').replace('</script', '<\\/script')
for name in ['portfolio', 'cv']:
    h = (R / f'{name}-src.html').read_text(encoding='utf-8').replace('/*{{FONTS}}*/', FONTS[name])
    h = h.replace('/*{{PHOTO}}*/', 'data:image/webp;base64,' + b64('assets/img/me.webp'))
    for p in (R / 'assets/logos').glob('*.webp'):
        h = h.replace('/*{{LOGO_' + p.stem.upper() + '}}*/', 'data:image/webp;base64,' + b64('assets/logos/' + p.name))
    h = h.replace('/*{{ENGINE_CSS}}*/', css).replace('/*{{ENGINE_JS}}*/', js)
    left = h.count('{{')
    (R.parent / ("index.html" if name == "portfolio" else "cv.html")).write_text(h, encoding='utf-8')
    print(name + '.html', len(h) // 1024, 'KB', '(placeholder tersisa: %d)' % left)
