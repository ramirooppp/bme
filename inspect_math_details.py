import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)

regions = tree.findall('.//{http://schemas.mathsoft.com/worksheet30}region')

for i, r in enumerate(regions):
    text_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}text')
    math_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    plot_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}plot')
    if text_el is not None:
        p_texts = [p.text for p in text_el.findall('.//{http://schemas.mathsoft.com/worksheet30}p') if p.text]
        print(f'R{i+1:02d} [TEXT]: {" ".join(p_texts)}')
    elif math_el is not None:
        err = math_el.attrib.get('error', '')
        # print string representation of math
        xml_str = ET.tostring(math_el, encoding='unicode')
        # clean xml tags roughly to see math
        print(f'R{i+1:02d} [MATH] err={err}:')
        print(xml_str)
    elif plot_el is not None:
        print(f'R{i+1:02d} [PLOT]')
