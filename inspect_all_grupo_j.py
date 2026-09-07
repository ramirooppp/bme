import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30', 'ml': 'http://schemas.mathsoft.com/math30'}

regions = root.findall('.//ws:region', ns)
print(f'Total regions: {len(regions)}')

for i, r in enumerate(regions):
    rid = r.attrib.get('region-id')
    top = r.attrib.get('top')
    left = r.attrib.get('left')
    m = r.find('ws:math', ns)
    t = r.find('ws:text', ns)
    p = r.find('ws:plot', ns)
    if t is not None:
        p_txt = ' '.join([x.text for x in t.findall('.//ws:p', ns) if x.text])
        print(f'R{i+1:02d} (id={rid}, top={top}) [TEXT]: {p_txt}')
    elif p is not None:
        print(f'R{i+1:02d} (id={rid}, top={top}) [PLOT]: item-idref={p.attrib.get("item-idref")}')
    elif m is not None:
        tokens = ' '.join([x.strip() for x in m.itertext() if x.strip()])
        err = m.attrib.get('error', '')
        # check if it is define or eval
        define = m.find('.//ml:define', ns)
        eval_el = m.find('.//ml:eval', ns)
        kind = "DEF" if define is not None else ("EVAL" if eval_el is not None else "EQ")
        print(f'R{i+1:02d} (id={rid}, top={top}) [MATH-{kind}] (err={err}): {tokens[:120]}')
