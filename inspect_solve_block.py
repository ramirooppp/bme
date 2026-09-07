import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\clase24.8.26.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30', 'ml': 'http://schemas.mathsoft.com/math30'}

regions = root.findall('.//ws:region', ns)

for i in range(50, len(regions)):
    r = regions[i]
    rid = r.attrib.get('region-id')
    top = r.attrib.get('top')
    left = r.attrib.get('left')
    math_el = r.find('ws:math', ns)
    text_el = r.find('ws:text', ns)
    if text_el is not None:
        p_texts = [p.text for p in text_el.findall('.//ws:p', ns) if p.text]
        print(f"--- R{i+1:02d} (id={rid}, top={top}, left={left}) TEXT: {' '.join(p_texts)}")
    elif math_el is not None:
        err = math_el.attrib.get('error', '')
        print(f"--- R{i+1:02d} (id={rid}, top={top}, left={left}) MATH err='{err}':")
        print(ET.tostring(math_el, encoding='unicode'))
