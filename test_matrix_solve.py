import xml.etree.ElementTree as ET
import win32com.client
import os

template_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Prueba_Final_Renderizada.xmcd'
test_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_matrix_solve.xmcd'
rendered_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_matrix_solve_rendered.xmcd'

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

# Col 1: 1, 3.316215, 1.040048
# Col 2: 1, 3.893618, 1.160466
# Col 3: 1, 5.877123, 1.452842
xml_test = """<root xmlns:ws="http://schemas.mathsoft.com/worksheet30" xmlns:ml="http://schemas.mathsoft.com/math30">
    <ws:region region-id="1" left="50" top="30" width="100" height="20" align-x="50" align-y="30" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:id xml:space="preserve">ORIGIN</ml:id>
                <ml:real>1</ml:real>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="2" left="50" top="60" width="200" height="60" align-x="50" align-y="60" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:id xml:space="preserve">M</ml:id>
                <ml:matrix rows="3" cols="3">
                    <ml:real>1</ml:real><ml:real>3.316215</ml:real><ml:real>1.040048</ml:real>
                    <ml:real>1</ml:real><ml:real>3.893618</ml:real><ml:real>1.160466</ml:real>
                    <ml:real>1</ml:real><ml:real>5.877123</ml:real><ml:real>1.452842</ml:real>
                </ml:matrix>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="3" left="300" top="60" width="100" height="60" align-x="300" align-y="60" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:id xml:space="preserve">b</ml:id>
                <ml:matrix rows="3" cols="1">
                    <ml:real>1</ml:real>
                    <ml:real>4.053</ml:real>
                    <ml:real>1.167</ml:real>
                </ml:matrix>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="4" left="50" top="150" width="150" height="30" align-x="50" align-y="150" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:id xml:space="preserve">x</ml:id>
                <ml:apply>
                    <ml:mult/>
                    <ml:apply>
                        <ml:pow/>
                        <ml:id xml:space="preserve">M</ml:id>
                        <ml:real>-1</ml:real>
                    </ml:apply>
                    <ml:id xml:space="preserve">b</ml:id>
                </ml:apply>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="5" left="50" top="200" width="150" height="60" align-x="50" align-y="200" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:eval placeholderMultiplicationStyle="default">
                <ml:id xml:space="preserve">x</ml:id>
            </ml:eval>
        </ws:math>
    </ws:region>
</root>"""

temp = ET.fromstring(xml_test)
for r in list(temp):
    regions.append(r)

tree.write(test_path, encoding='utf-8', xml_declaration=True)

mc = win32com.client.Dispatch('Mathcad.Application')
try:
    ws = mc.Worksheets.Open(os.path.abspath(test_path))
    ws.Recalculate()
    ws.SaveAs(os.path.abspath(rendered_path))
    ws.Close(2)
    print('Matrix solve recalculated successfully!')
finally:
    mc.Quit(2)

tree_res = ET.parse(rendered_path)
for i, r in enumerate(tree_res.findall('.//{http://schemas.mathsoft.com/worksheet30}region')):
    math = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    if math is not None:
        res = math.find('.//{http://schemas.mathsoft.com/math30}result')
        if res is not None:
            print(f"Region {i+1} result: {ET.tostring(res, encoding='unicode')}")
