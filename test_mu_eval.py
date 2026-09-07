import xml.etree.ElementTree as ET
import win32com.client
import os

template_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Prueba_Final_Renderizada.xmcd'
test_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_mu_plot.xmcd'
rendered_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\test_mu_plot_rendered.xmcd'

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

xml_test = """<root xmlns:ws="http://schemas.mathsoft.com/worksheet30" xmlns:ml="http://schemas.mathsoft.com/math30">
    <ws:region region-id="1" left="50" top="30" width="120" height="30" align-x="50" align-y="30" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:id xml:space="preserve">cP</ml:id>
                <ml:apply><ml:mult/><ml:real>0.01</ml:real><ml:id xml:space="preserve">poise</ml:id></ml:apply>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="2" left="50" top="70" width="400" height="40" align-x="50" align-y="70" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:function>
                    <ml:id xml:space="preserve">mu1_noparens</ml:id>
                    <ml:boundVars><ml:id xml:space="preserve">T</ml:id></ml:boundVars>
                </ml:function>
                <ml:apply>
                    <ml:mult/>
                    <ml:apply>
                        <ml:pow/>
                        <ml:real>10</ml:real>
                        <ml:apply>
                            <ml:plus/>
                            <ml:apply>
                                <ml:plus/>
                                <ml:apply>
                                    <ml:plus/>
                                    <ml:real>-5.0263</ml:real>
                                    <ml:apply><ml:div/><ml:real>1034.3</ml:real><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
                                </ml:apply>
                                <ml:apply><ml:mult/><ml:real>0.0087</ml:real><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
                            </ml:apply>
                            <ml:apply><ml:mult/><ml:real>-0.000008276</ml:real><ml:apply><ml:pow/><ml:parens><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:parens><ml:real>2</ml:real></ml:apply></ml:apply>
                        </ml:apply>
                    </ml:apply>
                    <ml:id xml:space="preserve">cP</ml:id>
                </ml:apply>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="3" left="50" top="120" width="400" height="40" align-x="50" align-y="120" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:define>
                <ml:function>
                    <ml:id xml:space="preserve">mu1_withparens</ml:id>
                    <ml:boundVars><ml:id xml:space="preserve">T</ml:id></ml:boundVars>
                </ml:function>
                <ml:apply>
                    <ml:mult/>
                    <ml:apply>
                        <ml:pow/>
                        <ml:real>10</ml:real>
                        <ml:parens>
                            <ml:apply>
                                <ml:plus/>
                                <ml:apply>
                                    <ml:plus/>
                                    <ml:apply>
                                        <ml:plus/>
                                        <ml:real>-5.0263</ml:real>
                                        <ml:apply><ml:div/><ml:real>1034.3</ml:real><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
                                    </ml:apply>
                                    <ml:apply><ml:mult/><ml:real>0.0087</ml:real><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply>
                                </ml:apply>
                                <ml:apply><ml:mult/><ml:real>-0.000008276</ml:real><ml:apply><ml:pow/><ml:parens><ml:apply><ml:div/><ml:id xml:space="preserve">T</ml:id><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:parens><ml:real>2</ml:real></ml:apply></ml:apply>
                            </ml:apply>
                        </ml:parens>
                    </ml:apply>
                    <ml:id xml:space="preserve">cP</ml:id>
                </ml:apply>
            </ml:define>
        </ws:math>
    </ws:region>
    <ws:region region-id="4" left="50" top="170" width="200" height="30" align-x="50" align-y="170" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:eval placeholderMultiplicationStyle="default">
                <ml:apply><ml:div/><ml:apply><ml:id xml:space="preserve">mu1_noparens</ml:id><ml:apply><ml:mult/><ml:real>273</ml:real><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply><ml:id xml:space="preserve">cP</ml:id></ml:apply>
            </ml:eval>
        </ws:math>
    </ws:region>
    <ws:region region-id="5" left="50" top="210" width="200" height="30" align-x="50" align-y="210" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
        <ws:math optimize="false" disable-calc="false">
            <ml:eval placeholderMultiplicationStyle="default">
                <ml:apply><ml:div/><ml:apply><ml:id xml:space="preserve">mu1_withparens</ml:id><ml:apply><ml:mult/><ml:real>273</ml:real><ml:id xml:space="preserve">K</ml:id></ml:apply></ml:apply><ml:id xml:space="preserve">cP</ml:id></ml:apply>
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
finally:
    mc.Quit(2)

tree_res = ET.parse(rendered_path)
for i, r in enumerate(tree_res.findall('.//{http://schemas.mathsoft.com/worksheet30}region')):
    math = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    if math is not None:
        res = math.find('.//{http://schemas.mathsoft.com/math30}result')
        if res is not None:
            real = res.find('.//{http://schemas.mathsoft.com/math30}real')
            print(f"Region {i+1}: {real.text if real is not None else ''}")
