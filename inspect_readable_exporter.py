import xml.etree.ElementTree as ET

sys_stdout = open(r'c:\Users\nahue\Desktop\segundo cuatrimestre\inspect_readable.txt', 'w', encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
regions = tree.findall('.//{http://schemas.mathsoft.com/worksheet30}region')

for i, r in enumerate(regions):
    math_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    text_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}text')
    plot_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}plot')
    if text_el is not None:
        p_texts = [p.text for p in text_el.findall('.//{http://schemas.mathsoft.com/worksheet30}p') if p.text]
        sys_stdout.write(f'--- R{i+1:02d} TEXT ---\n{" ".join(p_texts)}\n\n')
    elif math_el is not None:
        err = math_el.attrib.get('error', '')
        raw = ET.tostring(math_el, encoding='unicode')
        sys_stdout.write(f'--- R{i+1:02d} MATH (error: {err}) ---\n{raw}\n\n')
    elif plot_el is not None:
        sys_stdout.write(f'--- R{i+1:02d} PLOT ---\n\n')

sys_stdout.close()
print("Done writing inspect_readable.txt")
