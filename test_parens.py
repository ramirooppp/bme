import xml.etree.ElementTree as ET
import win32com.client
import os

template_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Prueba_Final_Renderizada.xmcd'
test_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_parens.xmcd'
rendered_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_parens_rendered.xmcd'

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

# Test k1(T) with parens around the polynomial:
xml_test = """<root xmlns:ws="http://schemas.mathsoft.com/worksheet30" xmlns:ml="http://schemas.mathsoft.com/math30">
    <ws:region region-id="1" left="50" top="30" width="400" height="30" align-x="50" align-y="30" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:function>
                    <ml:id xml:space="preserve">k1</ml:id>
                    <ml:boundVars><ml:id xml:space="preserve">T</ml:id></ml:boundVars>
                </ml:function>
                <ml:apply>
                    <ml:mult/>
                    <ml:parens>
                        <ml:apply>
                            <ml:plus/>
                            <ml:apply>
                                <ml:plus/>
                                <ml:real>0.1496</ml:real>
                                <ml:apply><ml:mult/><ml:real>-0.00003938</ml:real><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
                            </ml:apply>
                            <ml:apply><ml:mult/><ml:real>-0.00000019208</ml:real><ml:apply><ml:pow/><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply><ml:real>2</ml:real></ml:apply></ml:apply>
                        </ml:apply>
                    </ml:parens>
                    <ml:apply><ml:div/><ml:id xml:space="preserve">watt</ml:id><ml:apply><ml:mult/><ml:id xml:space="preserve">m</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
                </ml:apply>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="2" left="50" top="80" width="200" height="30" align-x="50" align-y="80" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:eval placeholderMultiplicationStyle="default">
                <ml:apply><ml:id xml:space="preserve">k1</ml:id><ml:apply><ml:mult/><ml:real>298.15</ml:real><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
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
    print('Recalculated with parens!')
finally:
    mc.Quit(2)

tree_res = ET.parse(rendered_path)
for i, r in enumerate(tree_res.findall('.//{http://schemas.mathsoft.com/worksheet30}region')):
    math = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    print(f"Region {i+1}: error={math.attrib.get('error', 'OK')}")
    res = math.find('.//{http://schemas.mathsoft.com/math30}result')
    if res is not None:
        print(f"Result: {ET.tostring(res, encoding='unicode')}")
