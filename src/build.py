"""Builds index.html (the portfolio) in the repository root from src/portfolio-src.html.
Usage: python src/build.py"""
import base64, pathlib

# Address of the CV site, used by the "CV" buttons.
CV_URL = "https://cv-rayvanalifarlo.netlify.app/"

R = pathlib.Path(__file__).parent
b64 = lambda p: base64.b64encode((R / p).read_bytes()).decode()
def font(name, fam, w, st='normal'):
    return f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(data:font/woff2;base64,{b64("assets/fonts/" + name + ".woff2")}) format("woff2")}}'
fonts = font('space-grotesk-latin-wght-normal', 'Space Grotesk Variable', '300 700') + font('archivo-latin-wght-normal', 'Archivo Variable', '100 900')
h = (R / 'portfolio-src.html').read_text(encoding='utf-8').replace('/*{{FONTS}}*/', fonts)
h = h.replace('{{CV_URL}}', CV_URL)
h = h.replace('/*{{PHOTO}}*/', 'data:image/webp;base64,' + b64('assets/img/me.webp'))
for p in (R / 'assets/logos').glob('*.webp'):
    h = h.replace('/*{{LOGO_' + p.stem.upper() + '}}*/', 'data:image/webp;base64,' + b64('assets/logos/' + p.name))
h = h.replace('/*{{ENGINE_CSS}}*/', (R / 'engine/scrollcraft.css').read_text(encoding='utf-8'))
h = h.replace('/*{{ENGINE_JS}}*/', (R / 'engine/scrollcraft.js').read_text(encoding='utf-8').replace('</script', '<\\/script'))
(R.parent / 'index.html').write_text(h, encoding='utf-8')
print('index.html', len(h) // 1024, 'KB, placeholders left:', h.count('{{'))
