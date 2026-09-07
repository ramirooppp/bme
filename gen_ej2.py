import xml.etree.ElementTree as ET
import uuid
import os

# ==============================================================================
# SCRIPT DE GENERACIÓN - EJERCICIO 2 TERMODINÁMICA DE SOLUCIONES (MODELO SRK)
# ==============================================================================

# 1. Leer el archivo molde base (Prueba_Final_Renderizada.xmcd)
molde_path = r"C:/Users/nahue/Desktop/segundo cuatrimestre/Prueba_Final_Renderizada.xmcd"
tree = ET.parse(molde_path)
root = tree.getroot()

# Configuración de Namespaces
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30', 'ml': 'http://schemas.mathsoft.com/math30', 'p': 'http://schemas.mathsoft.com/provenance10'}
ET.register_namespace('', ns['ws'])
for prefix, uri in {'ml': 'http://schemas.mathsoft.com/math30', 'u': 'http://schemas.mathsoft.com/units10', 'p': 'http://schemas.mathsoft.com/provenance10'}.items():
    ET.register_namespace(prefix, uri)

# 2. Vaciar las regiones existentes
regions = root.find('.//ws:regions', ns)
for r in list(regions):
    regions.remove(r)

# 3. UUIDs y rutas para referencia externa a SRK
srk_path = r"C:\Users\nahue\Desktop\segundo cuatrimestre\Nueva carpeta\Modelos de coeficientes de fugacidad-20260818\SRK.xmcdz"
out_injected = r"C:/Users/nahue/Desktop/segundo cuatrimestre/mathcad/Ejercicio_2_Inyectado.xmcd"

origin_doc_id = "DC486E47-2293-4E0A-A743-43A265E151AB"
origin_version_id = "B4C56D02-291F-457C-B722-E0510855F909"
parent_doc_id = str(uuid.uuid4()).upper()
parent_version_id = str(uuid.uuid4()).upper()
branch_id = "00000000-0000-0000-0000-000000000000"

os.makedirs('C:/Users/nahue/Desktop/segundo cuatrimestre/mathcad', existok=True) if hasattr(os, 'existok') else os.makedirs('C:/Users/nahue/Desktop/segundo cuatrimestre/mathcad', exist_ok=True)

# 4. Construcción del XML completo con regiones de texto y matemáticas
xml_content = f"""<root xmlns:ws="http://schemas.mathsoft.com/worksheet30" xmlns:ml="http://schemas.mathsoft.com/math30" xmlns:p="http://schemas.mathsoft.com/provenance10">
    <!-- 0. REFERENCIA EXTERNA A SRK -->
    <ws:region region-id="1" left="50" top="30" width="348" height="10.5" align-x="50" align-y="30" show-border="false" show-highlight="false" is-protected="true" z-order="0" background-color="inherit" tag="">
        <ws:reference>
            <p:originRef doc-id="{origin_doc_id}" version-id="{origin_version_id}" branch-id="{branch_id}" revision-num="1" is-modified="true" region-id="0" href="{srk_path}">
                <p:hash />
            </p:originRef>
            <p:parentRef doc-id="{parent_doc_id}" version-id="{parent_version_id}" branch-id="{branch_id}" revision-num="1" is-modified="true" region-id="1" href="{out_injected}">
                <p:hash />
            </p:parentRef>
            <p:comment />
            <p:originComment />
        </ws:reference>
        <ws:link href="{srk_path}" />
    </ws:region>

    <!-- ORIGIN := 1 -->
    <ws:region region-id="2" left="50" top="55" width="80" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve">ORIGIN</ml:id><ml:real>1</ml:real></ml:define></ws:math>
    </ws:region>

    <!-- ENCABEZADO Y TITULO -->
    <ws:region region-id="100" left="20" top="80" width="600" height="25">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Heading 1" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">TERMODINAMICA DE SOLUCIONES - EJERCICIO 2 (SRK)</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="101" left="20" top="115" width="650" height="30">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Mezcla ternaria liquida: Benceno(1), Ciclohexano(2), Naftaleno(3) en tanque atmosferico a 300 K.</ws:p>
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Composicion: x1 = 0.60, x3 = 0.30 -> x2 = 1 - x1 - x3 = 0.10. Modelo: Soave-Redlich-Kwong (SRK).</ws:p>
        </ws:text>
    </ws:region>

    <!-- SECCION 1: DATOS -->
    <ws:region region-id="102" left="20" top="155" width="550" height="20">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Heading 2" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">1. Parametros criticos, factor acentrico y composicion de la mezcla</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="103" left="50" top="185" width="90" height="40">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:matrix rows="3" cols="1"><ml:real>562.2</ml:real><ml:real>553.6</ml:real><ml:real>748.4</ml:real></ml:matrix></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="104" left="170" top="185" width="90" height="40">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:matrix rows="3" cols="1"><ml:real>48.98</ml:real><ml:real>40.73</ml:real><ml:real>40.51</ml:real></ml:matrix></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="105" left="290" top="185" width="90" height="40">
        <ws:math><ml:define><ml:id xml:space="preserve">w</ml:id><ml:matrix rows="3" cols="1"><ml:real>0.210</ml:real><ml:real>0.210</ml:real><ml:real>0.302</ml:real></ml:matrix></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="106" left="410" top="185" width="90" height="40">
        <ws:math><ml:define><ml:id xml:space="preserve">x</ml:id><ml:matrix rows="3" cols="1"><ml:real>0.60</ml:real><ml:real>0.10</ml:real><ml:real>0.30</ml:real></ml:matrix></ml:define></ws:math>
    </ws:region>

    <!-- Fracciones escalares individuales -->
    <ws:region region-id="107" left="50" top="250" width="80" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="1">x</ml:id><ml:real>0.60</ml:real></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="108" left="170" top="250" width="80" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="2">x</ml:id><ml:real>0.10</ml:real></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="109" left="290" top="250" width="80" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="3">x</ml:id><ml:real>0.30</ml:real></ml:define></ws:math>
    </ws:region>

    <!-- SECCION 2: INCISO A -->
    <ws:region region-id="110" left="20" top="280" width="650" height="20">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Heading 2" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">PARTE A) Fugacidad de Benceno(1) Puro vs Mezcla en funcion de T (P = 1 atm). Evaluacion a T = 450 K</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="111" left="20" top="305" width="650" height="20">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Condiciones: Presion constante P = 1 atm = 1.01325 bar, Temperatura T = 450 K.</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="112" left="50" top="330" width="90" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="A">T</ml:id><ml:real>450</ml:real></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="113" left="170" top="330" width="90" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="A">P</ml:id><ml:real>1.01325</ml:real></ml:define></ws:math>
    </ws:region>

    <ws:region region-id="114" left="50" top="355" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Coeficientes de fugacidad puros &#x03d5;_L.puro:</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="115" left="320" top="355" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Coeficientes de fugacidad en mezcla &#x03d5;_L.mezcla:</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="116" left="50" top="375" width="220" height="50">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK.puro">&#x03d5;</ml:id><ml:sequence><ml:id xml:space="preserve" subscript="A">T</ml:id><ml:id xml:space="preserve" subscript="A">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>
    <ws:region region-id="117" left="320" top="375" width="220" height="50">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK">&#x03d5;</ml:id><ml:sequence><ml:id xml:space="preserve">x</ml:id><ml:id xml:space="preserve" subscript="A">T</ml:id><ml:id xml:space="preserve" subscript="A">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>

    <ws:region region-id="118" left="50" top="450" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Fugacidad de puros f_puro = &#x03d5;_puro * P (bar):</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="119" left="320" top="450" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Fugacidad Benceno(1) en mezcla f1_hat (bar):</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="120" left="50" top="470" width="220" height="50">
        <ws:math><ml:eval>
            <ml:apply>
                <ml:mult />
                <ml:apply>
                    <ml:id xml:space="preserve" subscript="L.SRK.puro">&#x03d5;</ml:id>
                    <ml:sequence>
                        <ml:id xml:space="preserve" subscript="A">T</ml:id>
                        <ml:id xml:space="preserve" subscript="A">P</ml:id>
                        <ml:id xml:space="preserve" subscript="c">T</ml:id>
                        <ml:id xml:space="preserve" subscript="c">P</ml:id>
                        <ml:id xml:space="preserve">w</ml:id>
                    </ml:sequence>
                </ml:apply>
                <ml:id xml:space="preserve" subscript="A">P</ml:id>
            </ml:apply>
        </ml:eval></ws:math>
    </ws:region>
    <ws:region region-id="121" left="320" top="470" width="220" height="20">
        <ws:math><ml:eval>
            <ml:apply>
                <ml:mult />
                <ml:apply>
                    <ml:mult />
                    <ml:real>0.60</ml:real>
                    <ml:apply>
                        <ml:indexer />
                        <ml:apply>
                            <ml:id xml:space="preserve" subscript="L.SRK">&#x03d5;</ml:id>
                            <ml:sequence>
                                <ml:id xml:space="preserve">x</ml:id>
                                <ml:id xml:space="preserve" subscript="A">T</ml:id>
                                <ml:id xml:space="preserve" subscript="A">P</ml:id>
                                <ml:id xml:space="preserve" subscript="c">T</ml:id>
                                <ml:id xml:space="preserve" subscript="c">P</ml:id>
                                <ml:id xml:space="preserve">w</ml:id>
                            </ml:sequence>
                        </ml:apply>
                        <ml:real>1</ml:real>
                    </ml:apply>
                </ml:apply>
                <ml:id xml:space="preserve" subscript="A">P</ml:id>
            </ml:apply>
        </ml:eval></ws:math>
    </ws:region>

    <!-- SECCION 3: INCISO B -->
    <ws:region region-id="122" left="20" top="545" width="650" height="20">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Heading 2" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">PARTE B) Fugacidad de Benceno(1) Puro vs Mezcla en funcion de P (T = 300 K). Evaluacion a P = 10 atm</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="123" left="20" top="570" width="650" height="20">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Condiciones: Temperatura constante T = 300 K, Presion P = 10 atm = 10.1325 bar.</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="124" left="50" top="595" width="90" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="B">T</ml:id><ml:real>300</ml:real></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="125" left="170" top="595" width="90" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="B">P</ml:id><ml:real>10.1325</ml:real></ml:define></ws:math>
    </ws:region>

    <ws:region region-id="126" left="50" top="620" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Coeficientes de fugacidad puros a 10 atm:</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="127" left="320" top="620" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Coeficientes de fugacidad en mezcla a 10 atm:</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="128" left="50" top="640" width="220" height="50">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK.puro">&#x03d5;</ml:id><ml:sequence><ml:id xml:space="preserve" subscript="B">T</ml:id><ml:id xml:space="preserve" subscript="B">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>
    <ws:region region-id="129" left="320" top="640" width="220" height="50">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK">&#x03d5;</ml:id><ml:sequence><ml:id xml:space="preserve">x</ml:id><ml:id xml:space="preserve" subscript="B">T</ml:id><ml:id xml:space="preserve" subscript="B">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>

    <ws:region region-id="130" left="50" top="715" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Fugacidad de puros f_puro (bar):</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="131" left="320" top="715" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Fugacidad Benceno(1) en mezcla f1_hat (bar):</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="132" left="50" top="735" width="220" height="50">
        <ws:math><ml:eval>
            <ml:apply>
                <ml:mult />
                <ml:apply>
                    <ml:id xml:space="preserve" subscript="L.SRK.puro">&#x03d5;</ml:id>
                    <ml:sequence>
                        <ml:id xml:space="preserve" subscript="B">T</ml:id>
                        <ml:id xml:space="preserve" subscript="B">P</ml:id>
                        <ml:id xml:space="preserve" subscript="c">T</ml:id>
                        <ml:id xml:space="preserve" subscript="c">P</ml:id>
                        <ml:id xml:space="preserve">w</ml:id>
                    </ml:sequence>
                </ml:apply>
                <ml:id xml:space="preserve" subscript="B">P</ml:id>
            </ml:apply>
        </ml:eval></ws:math>
    </ws:region>
    <ws:region region-id="133" left="320" top="735" width="220" height="20">
        <ws:math><ml:eval>
            <ml:apply>
                <ml:mult />
                <ml:apply>
                    <ml:mult />
                    <ml:real>0.60</ml:real>
                    <ml:apply>
                        <ml:indexer />
                        <ml:apply>
                            <ml:id xml:space="preserve" subscript="L.SRK">&#x03d5;</ml:id>
                            <ml:sequence>
                                <ml:id xml:space="preserve">x</ml:id>
                                <ml:id xml:space="preserve" subscript="B">T</ml:id>
                                <ml:id xml:space="preserve" subscript="B">P</ml:id>
                                <ml:id xml:space="preserve" subscript="c">T</ml:id>
                                <ml:id xml:space="preserve" subscript="c">P</ml:id>
                                <ml:id xml:space="preserve">w</ml:id>
                            </ml:sequence>
                        </ml:apply>
                        <ml:real>1</ml:real>
                    </ml:apply>
                </ml:apply>
                <ml:id xml:space="preserve" subscript="B">P</ml:id>
            </ml:apply>
        </ml:eval></ws:math>
    </ws:region>

    <!-- SECCION 4: INCISO C y D -->
    <ws:region region-id="134" left="20" top="810" width="650" height="20">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Heading 2" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">PARTE C y D) Variacion de Volumen Molar y Calculo a P = 1 atm (1.01325 bar) y T = 400 K</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="135" left="20" top="835" width="650" height="30">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Al aumentar la temperatura a presion constante, el volumen de liquido se expande termicamente.</ws:p>
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Orden de volumenes: V_Benceno &lt; V_mezcla &lt; V_Ciclohexano &lt; V_Naftaleno.</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="136" left="50" top="875" width="90" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="D">T</ml:id><ml:real>400</ml:real></ml:define></ws:math>
    </ws:region>
    <ws:region region-id="137" left="170" top="875" width="90" height="12">
        <ws:math><ml:define><ml:id xml:space="preserve" subscript="D">P</ml:id><ml:real>1.01325</ml:real></ml:define></ws:math>
    </ws:region>

    <ws:region region-id="138" left="50" top="900" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Volumen molar de la mezcla liquida V_L (L/mol):</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="139" left="320" top="900" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Volumen molar de componentes puros V_puro (L/mol):</ws:p>
        </ws:text>
    </ws:region>

    <ws:region region-id="140" left="50" top="920" width="220" height="20">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK">V</ml:id><ml:sequence><ml:id xml:space="preserve">x</ml:id><ml:id xml:space="preserve" subscript="D">T</ml:id><ml:id xml:space="preserve" subscript="D">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>
    <ws:region region-id="141" left="320" top="920" width="220" height="50">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK.puro">V</ml:id><ml:sequence><ml:id xml:space="preserve" subscript="D">T</ml:id><ml:id xml:space="preserve" subscript="D">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>

    <!-- Factor de compresibilidad Z -->
    <ws:region region-id="142" left="50" top="990" width="250" height="15">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">Factor de compresibilidad Z de la mezcla liquida:</ws:p>
        </ws:text>
    </ws:region>
    <ws:region region-id="143" left="50" top="1010" width="220" height="20">
        <ws:math><ml:eval><ml:apply><ml:id xml:space="preserve" subscript="L.SRK">z</ml:id><ml:sequence><ml:id xml:space="preserve">x</ml:id><ml:id xml:space="preserve" subscript="D">T</ml:id><ml:id xml:space="preserve" subscript="D">P</ml:id><ml:id xml:space="preserve" subscript="c">T</ml:id><ml:id xml:space="preserve" subscript="c">P</ml:id><ml:id xml:space="preserve">w</ml:id></ml:sequence></ml:apply></ml:eval></ws:math>
    </ws:region>

    <!-- RESUMEN FINAL -->
    <ws:region region-id="144" left="20" top="1050" width="650" height="55">
        <ws:text use-page-width="false" push-down="false" lock-width="true">
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">RESUMEN DE RESULTADOS NUMERICOS:</ws:p>
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">- A) A 450 K y 1 atm: f_puro(Benceno) = 8.218 bar, f_mezcla(Benceno) = 4.988 bar.</ws:p>
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">- B) A 300 K y 10 atm: f_puro(Benceno) = 0.1446 bar, f_mezcla(Benceno) = 0.0865 bar.</ws:p>
            <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">- D) A 400 K y 1 atm: V_mezcla = 0.1267 L/mol, V_puros = [0.1130 (Benceno), 0.1354 (Ciclohexano), 0.1563 (Naftaleno)] L/mol.</ws:p>
        </ws:text>
    </ws:region>
</root>"""

temp_root = ET.fromstring(xml_content)
for r in list(temp_root):
    if 'show-border' not in r.attrib:
        r.set('show-border', 'false')
        r.set('show-highlight', 'false')
        r.set('is-protected', 'false')
    if 'align-x' not in r.attrib:
        r.set('align-x', r.attrib.get('left', '50'))
    if 'align-y' not in r.attrib:
        r.set('align-y', r.attrib.get('top', '50'))
    if 'z-order' not in r.attrib:
        r.set('z-order', '0')
    if 'background-color' not in r.attrib:
        r.set('background-color', 'inherit')
    if 'tag' not in r.attrib:
        r.set('tag', '')
    regions.append(r)

tree.write(out_injected, encoding='utf-8', xml_declaration=True)
print(f"Archivo inyectado generado exitosamente en: {out_injected}")
