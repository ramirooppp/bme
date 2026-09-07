import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
regions = tree.findall('.//{http://schemas.mathsoft.com/worksheet30}region')

print(f'Total regions: {len(regions)}')
for i, r in enumerate(regions):
    math_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    text_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}text')
    plot_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}plot')
    if text_el is not None:
        p_texts = [p.text for p in text_el.findall('.//{http://schemas.mathsoft.com/worksheet30}p') if p.text]
        txt = " ".join(p_texts)
        print(f'R{i+1:02d} [TEXT]: {txt}')
    elif math_el is not None:
        err = math_el.attrib.get('error', '')
        raw = ET.tostring(math_el, encoding='unicode').replace('\n', ' ')
        raw = ' '.join(raw.split())
        print(f'R{i+1:02d} [MATH] (err: {err}): {raw[:180]}...')
    elif plot_el is not None:
        print(f'R{i+1:02d} [PLOT]')
