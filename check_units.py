import xml.etree.ElementTree as ET
import win32com.client
import os

template_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Prueba_Final_Renderizada.xmcd'
test_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_unit_names.xmcd'
rendered_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_unit_names_rendered.xmcd'

NS = {
    'ws': 'http://schemas.mathsoft.com/worksheet30',
    'ml': 'http://schemas.mathsoft.com/math30',
    'p': 'http://schemas.mathsoft.com/provenance10',
    'u': 'http://schemas.mathsoft.com/units10'
}
ET.register_namespace('', NS['ws'])
ET.register_namespace('ml', NS['ml'])
ET.register_namespace('p', NS['p'])
ET.register_namespace('u', NS['u'])

tree = ET.parse(template_path)
root = tree.getroot()
regions = root.find('.//{http://schemas.mathsoft.com/worksheet30}regions')
for r in list(regions):
    regions.remove(r)

units = ['K', 'kelvin', 'Pa', 's', 'sec', 'kg', 'm', 'joule', 'watt', 'poise', 'cP', 'g', 'cm', 'mole', 'mol']
xml_regions = []
for i, u in enumerate(units):
    top_val = 50 + i * 30
    xml_regions.append(f"""<ws:region region-id="{i+1}" left="50" top="{top_val}" width="100" height="20" align-x="50" align-y="50" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:eval placeholderMultiplicationStyle="default">
                <ml:id xml:space="preserve">{u}</ml:id>
            </ml:eval>
        </ws:math>
    </ws:region>""")

xml_content = f"""<root xmlns:ws="http://schemas.mathsoft.com/worksheet30" xmlns:ml="http://schemas.mathsoft.com/math30">
{''.join(xml_regions)}
</root>"""

temp = ET.fromstring(xml_content)
for r in list(temp):
    regions.append(r)

tree.write(test_path, encoding='utf-8', xml_declaration=True)

mc = win32com.client.Dispatch('Mathcad.Application')
try:
    ws = mc.Worksheets.Open(os.path.abspath(test_path))
    ws.Recalculate()
    ws.SaveAs(os.path.abspath(rendered_path))
    ws.Close(2)
finally:
    mc.Quit(2)

tree_res = ET.parse(rendered_path)
for i, r in enumerate(tree_res.findall('.//{http://schemas.mathsoft.com/worksheet30}region')):
    math = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    print(f"Unit {units[i]}: {math.attrib.get('error', 'OK')}")
