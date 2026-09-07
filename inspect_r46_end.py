import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
regions = tree.findall('.//{http://schemas.mathsoft.com/worksheet30}region')

for i in range(45, len(regions)):
    r = regions[i]
    math_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    text_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}text')
    if text_el is not None:
        p_texts = [p.text for p in text_el.findall('.//{http://schemas.mathsoft.com/worksheet30}p') if p.text]
        print(f"R{i+1:02d} [TEXT]: {' '.join(p_texts)}")
    elif math_el is not None:
        err = math_el.attrib.get('error', '')
        # print xml snippet
        raw = ET.tostring(math_el, encoding='unicode')
        print(f"R{i+1:02d} [MATH] err='{err}':")
        # print non-empty text nodes
        tokens = [t.strip() for t in math_el.itertext() if t.strip()]
        print("   Tokens:", " ".join(tokens))
        res = math_el.find('.//{http://schemas.mathsoft.com/math30}result')
        if res is not None:
            print("   Result:", " ".join([t.strip() for t in res.itertext() if t.strip()]))
