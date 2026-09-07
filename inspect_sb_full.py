"""
Analyze and fix clase24.8.26.xmcd
"""
import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\clase24.8.26.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30', 'ml': 'http://schemas.mathsoft.com/math30'}

# Let's inspect all regions inside the solve block (from Given to Find)
given_found = False
for i, r in enumerate(root.findall('.//ws:region', ns)):
    m = r.find('ws:math', ns)
    t = r.find('ws:text', ns)
    rid = r.attrib.get('region-id')
    top = r.attrib.get('top')
    
    if m is not None:
        raw = ET.tostring(m, encoding='unicode')
        tokens = ' '.join([x.strip() for x in m.itertext() if x.strip()])
        if 'Given' in tokens:
            given_found = True
        if given_found:
            err = m.attrib.get('error', '')
            print(f"R{i+1:02d} (id={rid}, top={top}) [MATH] err='{err}': {tokens}")
            if 'Find' in tokens:
                break
    elif t is not None:
        p_texts = [p.text for p in t.findall('.//ws:p', ns) if p.text]
        if given_found:
            print(f"R{i+1:02d} (id={rid}, top={top}) [TEXT]: {' '.join(p_texts)}")
