import xml.etree.ElementTree as ET
import win32com.client
import os

TEMPLATE_PATH = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Prueba_Final_Renderizada.xmcd'
OUTPUT_RAW = r'C:\Users\nahue\Desktop\segundo cuatrimestre\TP1_Fenomenos_Transporte_Resuelto.xmcd'
OUTPUT_RENDERED = r'C:\Users\nahue\Desktop\segundo cuatrimestre\TP1_Fenomenos_Transporte_Final.xmcd'

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

def r_id(name, sub=None):
    if sub:
        return f'<ml:id xml:space="preserve" subscript="{sub}">{name}</ml:id>'
    return f'<ml:id xml:space="preserve">{name}</ml:id>'

def r_num(val):
    return f'<ml:real>{val}</ml:real>'

def op_add(a, b):
    return f'<ml:apply><ml:plus/>{a}{b}</ml:apply>'

def op_sub(a, b):
    return f'<ml:apply><ml:minus/>{a}{b}</ml:apply>'

def op_mul(a, b):
    return f'<ml:apply><ml:mult/>{a}{b}</ml:apply>'

def op_div(a, b):
    return f'<ml:apply><ml:div/>{a}{b}</ml:apply>'

def op_pow(a, b):
    return f'<ml:apply><ml:pow/>{a}{b}</ml:apply>'

def op_neg(a):
    return f'<ml:apply><ml:neg/>{a}</ml:apply>'

def op_parens(a):
    return f'<ml:parens>{a}</ml:parens>'

def op_call(func_id, *args):
    if len(args) == 1:
        return f'<ml:apply>{func_id}{args[0]}</ml:apply>'
    args_xml = ''.join(args)
    return f'<ml:apply>{func_id}<ml:sequence>{args_xml}</ml:sequence></ml:apply>'

def op_index(arr_id, idx):
    return f'<ml:apply><ml:indexer/>{arr_id}{idx}</ml:apply>'

def define_var(target_id, expr):
    return f'<ml:define>{target_id}{expr}</ml:define>'

def define_func(func_name, sub, arg_names, body_expr):
    sub_attr = f' subscript="{sub}"' if sub else ''
    bvars = ''.join(f'<ml:id xml:space="preserve">{a}</ml:id>' for a in arg_names)
    return f"""<ml:define>
        <ml:function>
            <ml:id xml:space="preserve"{sub_attr}>{func_name}</ml:id>
            <ml:boundVars>{bvars}</ml:boundVars>
        </ml:function>
        {body_expr}
    </ml:define>"""

def eval_expr(expr):
    return f'<ml:eval placeholderMultiplicationStyle="default">{expr}</ml:eval>'

tree = ET.parse(TEMPLATE_PATH)
root = tree.getroot()
regions = root.find('.//{http://schemas.mathsoft.com/worksheet30}regions')
for r in list(regions):
    regions.remove(r)

class MathcadDoc:
    def __init__(self, regions_el):
        self.regions = regions_el
        self.cur_id = 0
        self.top = 40
        self.left_margin = 40

    def next_id(self):
        self.cur_id += 1
        return self.cur_id

    def add_space(self, pts=20):
        self.top += pts

    def add_title(self, text):
        self.top += 10
        reg_id = self.next_id()
        xml = f"""<ws:region region-id="{reg_id}" left="{self.left_margin}" top="{self.top}" width="540" height="28" align-x="{self.left_margin}" align-y="{self.top+20}" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
            <ws:text use-page-width="false" push-down="false" lock-width="true">
                <ws:p style="Heading 1" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">{text}</ws:p>
            </ws:text>
        </ws:region>"""
        self._append(xml)
        self.top += 45

    def add_subtitle(self, text):
        self.top += 18
        reg_id = self.next_id()
        xml = f"""<ws:region region-id="{reg_id}" left="{self.left_margin}" top="{self.top}" width="540" height="22" align-x="{self.left_margin}" align-y="{self.top+16}" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
            <ws:text use-page-width="false" push-down="false" lock-width="true">
                <ws:p style="Heading 2" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">{text}</ws:p>
            </ws:text>
        </ws:region>"""
        self._append(xml)
        self.top += 35

    def add_text(self, text, width=540, left=None, advance=28):
        if left is None:
            left = self.left_margin
        reg_id = self.next_id()
        xml = f"""<ws:region region-id="{reg_id}" left="{left}" top="{self.top}" width="{width}" height="20" align-x="{left}" align-y="{self.top+14}" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
            <ws:text use-page-width="false" push-down="false" lock-width="true">
                <ws:p style="Normal" margin-left="inherit" margin-right="inherit" text-indent="inherit" text-align="inherit" list-style-type="inherit" tabs="inherit">{text}</ws:p>
            </ws:text>
        </ws:region>"""
        self._append(xml)
        if advance:
            self.top += advance

    def add_math(self, math_xml, left=None, width=200, height=30, advance=45):
        if left is None:
            left = self.left_margin
        reg_id = self.next_id()
        xml = f"""<ws:region region-id="{reg_id}" left="{left}" top="{self.top}" width="{width}" height="{height}" align-x="{left}" align-y="{self.top+18}" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
            <ws:math optimize="false" disable-calc="false">
                {math_xml}
            </ws:math>
        </ws:region>"""
        self._append(xml)
        if advance:
            self.top += advance

    def _append(self, xml_str):
        wrapped = f'<root xmlns:ws="{NS["ws"]}" xmlns:ml="{NS["ml"]}" xmlns:u="{NS["u"]}">{xml_str}</root>'
        temp = ET.fromstring(wrapped)
        for r in list(temp):
            self.regions.append(r)

doc = MathcadDoc(regions)

# ==================== ENCABEZADO ====================
doc.add_title("FENÓMENOS DE TRANSPORTE (2026) - TRABAJO PRÁCTICO Nº 1")
doc.add_subtitle("Determinación de Composición y Estimación de Propiedades en Mezclas y Aire")
doc.add_text("Autor: Cátedra de Fenómenos de Transporte / Resolución Integral Automatizada")
doc.add_text("------------------------------------------------------------------------------------------------------------------------", advance=35)

# ==================== 1. CONFIGURACIÓN ====================
doc.add_subtitle("1. Configuración General y Definición de Unidades")
doc.add_math(define_var(r_id("ORIGIN"), r_num(1)), left=40, width=100, advance=0)
doc.add_math(define_var(r_id("cP"), op_mul(r_num(0.01), r_id("poise"))), left=200, width=140, advance=50)

# ==================== 2. PESOS MOLECULARES ====================
doc.add_subtitle("2. Pesos Moleculares (Orden estricto de compuestos)")
doc.add_text("1: 2,4-Dimetiltridecano | 2: 2,4-Dimetiltetradecano | 3: Hexadecano | Aire", advance=30)

doc.add_math(define_var(r_id("MW", "1"), op_div(op_mul(op_mul(r_num(212.419), r_num(0.001)), r_id("kg")), r_id("mole"))), left=40, width=130, advance=0)
doc.add_math(define_var(r_id("MW", "2"), op_div(op_mul(op_mul(r_num(226.446), r_num(0.001)), r_id("kg")), r_id("mole"))), left=180, width=130, advance=0)
doc.add_math(define_var(r_id("MW", "3"), op_div(op_mul(op_mul(r_num(226.446), r_num(0.001)), r_id("kg")), r_id("mole"))), left=320, width=130, advance=0)
doc.add_math(define_var(r_id("MW", "aire"), op_div(op_mul(op_mul(r_num(28.951), r_num(0.001)), r_id("kg")), r_id("mole"))), left=460, width=130, advance=55)

# ==================== 3. VISCOSIDAD DE LÍQUIDOS PUROS ====================
doc.add_subtitle("3. Viscosidad de Líquidos Puros (Yaws 2003)")
doc.add_text("Correlación: log10(mu / cP) = A + B/(T/K) + C*(T/K) + D*(T/K)^2", advance=28)
doc.add_text("Matriz de coeficientes de viscosidad [A, B, C, D] para los 3 hidrocarburos:", advance=30)

doc.add_math(define_var(r_id("A", "visc"), f'<ml:matrix rows="3" cols="1">{r_num(-5.0263)}{r_num(-4.9814)}{r_num(-8.1894)}</ml:matrix>'), left=40, width=80, advance=0)
doc.add_math(define_var(r_id("B", "visc"), f'<ml:matrix rows="3" cols="1">{r_num(1034.3)}{r_num(1056.5)}{r_num(1557.1)}</ml:matrix>'), left=160, width=80, advance=0)
doc.add_math(define_var(r_id("C", "visc"), f'<ml:matrix rows="3" cols="1">{r_num(0.0087)}{r_num(0.0084)}{r_num(0.0153)}</ml:matrix>'), left=280, width=80, advance=0)
doc.add_math(define_var(r_id("D", "visc"), f'<ml:matrix rows="3" cols="1">{r_num(-0.000008276)}{r_num(-0.0000079353)}{r_num(-0.000012371)}</ml:matrix>'), left=400, width=90, advance=100)

doc.add_text("Funciones de Viscosidad con unidades nativas:", advance=28)

def build_visc_expr(A, B, C, D):
    T_ad = op_div(r_id("T"), r_id("K"))
    t1 = op_add(r_num(A), op_div(r_num(B), T_ad))
    t2 = op_add(t1, op_mul(r_num(C), T_ad))
    t3 = op_add(t2, op_mul(r_num(D), op_pow(T_ad, r_num(2))))
    return op_mul(op_pow(r_num(10), op_parens(t3)), r_id("cP"))

doc.add_math(define_func("mu", "1", ["T"], build_visc_expr(-5.0263, 1034.3, 0.0087, -0.000008276)), left=40, width=500, advance=50)
doc.add_math(define_func("mu", "2", ["T"], build_visc_expr(-4.9814, 1056.5, 0.0084, -0.0000079353)), left=40, width=500, advance=50)
doc.add_math(define_func("mu", "3", ["T"], build_visc_expr(-8.1894, 1557.1, 0.0153, -0.000012371)), left=40, width=500, advance=60)

# ==================== 4. DENSIDAD DE LÍQUIDOS PUROS ====================
doc.add_subtitle("4. Densidad de Líquidos Puros (Yaws 2003)")
doc.add_text("Correlación: rho = A * B^(-(1 - T/Tc)^n) [g/cm^3]", advance=30)

def build_den_expr(A, B, Tc, n):
    Tc_dim = op_mul(r_num(Tc), r_id("K"))
    term = op_pow(op_parens(op_sub(r_num(1), op_div(r_id("T"), Tc_dim))), r_num(n))
    exp_factor = op_pow(r_num(B), op_parens(op_neg(term)))
    unit_den = op_mul(r_num(1000), op_div(r_id("kg"), op_pow(r_id("m"), r_num(3))))
    return op_mul(op_mul(r_num(A), exp_factor), unit_den)

doc.add_math(define_func("rho", "1", ["T"], build_den_expr(0.2460, 0.2617, 683.39, 0.2857)), left=40, width=450, advance=50)
doc.add_math(define_func("rho", "2", ["T"], build_den_expr(0.2463, 0.2613, 695.62, 0.2857)), left=40, width=450, advance=50)
doc.add_math(define_func("rho", "3", ["T"], build_den_expr(0.2435, 0.2544, 720.60, 0.3238)), left=40, width=450, advance=60)

# ==================== 5. CONDUCTIVIDAD TÉRMICA DE LÍQUIDOS PUROS ====================
doc.add_subtitle("5. Conductividad Térmica de Líquidos Puros (Yaws 2003)")
doc.add_text("Correlación: k = (A + B*(T/K) + C*(T/K)^2) [W/(m*K)]", advance=30)

def build_k_expr(A, B, C):
    T_ad = op_div(r_id("T"), r_id("K"))
    t1 = op_add(r_num(A), op_mul(r_num(B), T_ad))
    poly = op_add(t1, op_mul(r_num(C), op_pow(T_ad, r_num(2))))
    unit_k = op_div(r_id("watt"), op_mul(r_id("m"), r_id("K")))
    return op_mul(op_parens(poly), unit_k)

doc.add_math(define_func("k", "1", ["T"], build_k_expr(0.1496, -0.00003938, -0.00000019208)), left=40, width=450, advance=50)
doc.add_math(define_func("k", "2", ["T"], build_k_expr(0.1461, -0.000032788, -0.00000018813)), left=40, width=450, advance=50)
doc.add_math(define_func("k", "3", ["T"], build_k_expr(0.1890, -0.00012226, -0.00000013059)), left=40, width=450, advance=60)

# ==================== 6. CALOR ESPECÍFICO MÁSICO DE LÍQUIDOS PUROS ====================
doc.add_subtitle("6. Calor Específico Másico de Líquidos Puros (Yaws 2003)")
doc.add_text("Correlación: cp_masico = (A + B*(T/K) + C*(T/K)^2 + D*(T/K)^3) / MW [J/(kg*K)]", advance=30)

def build_cp_expr(sub, A, B, C, D):
    T_ad = op_div(r_id("T"), r_id("K"))
    t1 = op_add(r_num(A), op_mul(r_num(B), T_ad))
    t2 = op_add(t1, op_mul(r_num(C), op_pow(T_ad, r_num(2))))
    poly = op_add(t2, op_mul(r_num(D), op_pow(T_ad, r_num(3))))
    unit_cp_mol = op_div(r_id("joule"), op_mul(r_id("mole"), r_id("K")))
    cp_molar = op_mul(op_parens(poly), unit_cp_mol)
    return op_div(cp_molar, r_id("MW", sub))

doc.add_math(define_func("cp", "1", ["T"], build_cp_expr("1", 258.507, 1.3429, -0.0034546, 0.0000040075)), left=40, width=500, advance=50)
doc.add_math(define_func("cp", "2", ["T"], build_cp_expr("2", 266.096, 1.4888, -0.0037813, 0.0000042498)), left=40, width=500, advance=50)
doc.add_math(define_func("cp", "3", ["T"], build_cp_expr("3", 89.101, 2.7062, -0.0061478, 0.000005752)), left=40, width=500, advance=60)

# ==================== 7. RESOLUCIÓN DEL SISTEMA LINEAL (INCISO B) ====================
doc.add_subtitle("7. Inciso b) Determinación de la Composición Molar de la Mezcla")
doc.add_text("Valores experimentales dados por el enunciado:", advance=28)

doc.add_math(define_var(r_id("T", "exp1"), op_mul(r_num(273), r_id("K"))), left=40, width=110, advance=0)
doc.add_math(define_var(r_id("mu", "exp1"), op_mul(r_num(4.053), r_id("cP"))), left=170, width=120, advance=0)
doc.add_math(define_var(r_id("T", "exp2"), op_mul(r_num(340), r_id("K"))), left=310, width=110, advance=0)
doc.add_math(define_var(r_id("mu", "exp2"), op_mul(r_num(1.167), r_id("cP"))), left=440, width=120, advance=45)

doc.add_text("Matriz del sistema M (orden columna) y vector término independiente b:", advance=28)

m_col1 = f"{r_num(1)}{op_div(op_call(r_id('mu','1'), r_id('T','exp1')), r_id('cP'))}{op_div(op_call(r_id('mu','1'), r_id('T','exp2')), r_id('cP'))}"
m_col2 = f"{r_num(1)}{op_div(op_call(r_id('mu','2'), r_id('T','exp1')), r_id('cP'))}{op_div(op_call(r_id('mu','2'), r_id('T','exp2')), r_id('cP'))}"
m_col3 = f"{r_num(1)}{op_div(op_call(r_id('mu','3'), r_id('T','exp1')), r_id('cP'))}{op_div(op_call(r_id('mu','3'), r_id('T','exp2')), r_id('cP'))}"
mat_M_xml = f'<ml:matrix rows="3" cols="3">{m_col1}{m_col2}{m_col3}</ml:matrix>'

doc.add_math(define_var(r_id("M"), mat_M_xml), left=40, width=220, advance=0)

b_entries = f"{r_num(1)}{op_div(r_id('mu','exp1'), r_id('cP'))}{op_div(r_id('mu','exp2'), r_id('cP'))}"
mat_b_xml = f'<ml:matrix rows="3" cols="1">{b_entries}</ml:matrix>'

doc.add_math(define_var(r_id("b"), mat_b_xml), left=300, width=120, advance=95)

doc.add_text("Resolución matricial exacta en Mathcad:  x := M^-1 * b", advance=28)
doc.add_math(define_var(r_id("x"), op_mul(op_pow(r_id("M"), r_num(-1)), r_id("b"))), left=40, width=140, advance=0)
doc.add_math(eval_expr(r_id("x")), left=220, width=120, advance=90)

doc.add_text("Fracciones molares individuales calculadas:", advance=28)
doc.add_math(define_var(r_id("x", "1"), op_index(r_id("x"), r_num(1))), left=40, width=80, advance=0)
doc.add_math(define_var(r_id("x", "2"), op_index(r_id("x"), r_num(2))), left=180, width=80, advance=0)
doc.add_math(define_var(r_id("x", "3"), op_index(r_id("x"), r_num(3))), left=320, width=80, advance=50)

# ==================== 8. PROPIEDADES DE LA MEZCLA (INCISO C) ====================
doc.add_subtitle("8. Inciso c) Modelos y Estimación de Propiedades de la Mezcla")
doc.add_text("Definición de funciones de mezcla con comportamiento ideal:", advance=30)

# mu_M(T)
term_mu1 = op_mul(r_id("x", "1"), op_call(r_id("mu", "1"), r_id("T")))
term_mu2 = op_mul(r_id("x", "2"), op_call(r_id("mu", "2"), r_id("T")))
term_mu3 = op_mul(r_id("x", "3"), op_call(r_id("mu", "3"), r_id("T")))
mu_M_body = op_add(op_add(term_mu1, term_mu2), term_mu3)
doc.add_math(define_func("mu", "M", ["T"], mu_M_body), left=40, width=450, advance=45)

# MW_M
term_mw1 = op_mul(r_id("x", "1"), r_id("MW", "1"))
term_mw2 = op_mul(r_id("x", "2"), r_id("MW", "2"))
term_mw3 = op_mul(r_id("x", "3"), r_id("MW", "3"))
MW_M_body = op_add(op_add(term_mw1, term_mw2), term_mw3)
doc.add_math(define_var(r_id("MW", "M"), MW_M_body), left=40, width=350, advance=45)

# rho_M(T) = MW_M / sum(x_i * MW_i / rho_i)
v1 = op_div(op_mul(r_id("x", "1"), r_id("MW", "1")), op_call(r_id("rho", "1"), r_id("T")))
v2 = op_div(op_mul(r_id("x", "2"), r_id("MW", "2")), op_call(r_id("rho", "2"), r_id("T")))
v3 = op_div(op_mul(r_id("x", "3"), r_id("MW", "3")), op_call(r_id("rho", "3"), r_id("T")))
rho_M_body = op_div(r_id("MW", "M"), op_parens(op_add(op_add(v1, v2), v3)))
doc.add_math(define_func("rho", "M", ["T"], rho_M_body), left=40, width=450, advance=50)

# k_M(T)
term_k1 = op_mul(r_id("x", "1"), op_call(r_id("k", "1"), r_id("T")))
term_k2 = op_mul(r_id("x", "2"), op_call(r_id("k", "2"), r_id("T")))
term_k3 = op_mul(r_id("x", "3"), op_call(r_id("k", "3"), r_id("T")))
k_M_body = op_add(op_add(term_k1, term_k2), term_k3)
doc.add_math(define_func("k", "M", ["T"], k_M_body), left=40, width=450, advance=45)

# cp_M(T) = sum(x_i * MW_i * cp_i) / MW_M
c1 = op_mul(op_mul(r_id("x", "1"), r_id("MW", "1")), op_call(r_id("cp", "1"), r_id("T")))
c2 = op_mul(op_mul(r_id("x", "2"), r_id("MW", "2")), op_call(r_id("cp", "2"), r_id("T")))
c3 = op_mul(op_mul(r_id("x", "3"), r_id("MW", "3")), op_call(r_id("cp", "3"), r_id("T")))
cp_M_body = op_div(op_parens(op_add(op_add(c1, c2), c3)), r_id("MW", "M"))
doc.add_math(define_func("cp", "M", ["T"], cp_M_body), left=40, width=450, advance=55)

# ==================== VERIFICACIÓN EXPERIMENTAL ====================
doc.add_subtitle("Demostración de la Viscosidad de Mezcla calculada vs Datos Experimentales:")
doc.add_text("Evaluación a 273 K en cP (Valor experimental esperado: 4.053 cP):", advance=25)
doc.add_math(eval_expr(op_div(op_call(r_id("mu", "M"), op_mul(r_num(273), r_id("K"))), r_id("cP"))), left=40, width=160, advance=40)

doc.add_text("Evaluación a 340 K en cP (Valor experimental esperado: 1.167 cP):", advance=25)
doc.add_math(eval_expr(op_div(op_call(r_id("mu", "M"), op_mul(r_num(340), r_id("K"))), r_id("cP"))), left=40, width=160, advance=50)

# ==================== 9. TABLA RESUMEN A 298.15 K (INCISO D) ====================
doc.add_subtitle("9. Inciso d) Tabla Resumen de Propiedades Valuadas a 298.15 K (Sistema Internacional)")
doc.add_text("Temperatura estándar de evaluación: T_0 := 298.15 * K", advance=25)
doc.add_math(define_var(r_id("T", "0"), op_mul(r_num(298.15), r_id("K"))), left=40, width=120, advance=45)

doc.add_text("1. Viscosidad Dinámica [Pa*s]:  (1: 2,4-DM-tridecano | 2: 2,4-DM-tetradecano | 3: Hexadecano | Mezcla)", advance=28)
doc.add_math(eval_expr(op_call(r_id("mu", "1"), r_id("T", "0"))), left=40, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("mu", "2"), r_id("T", "0"))), left=170, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("mu", "3"), r_id("T", "0"))), left=300, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("mu", "M"), r_id("T", "0"))), left=430, width=130, advance=45)

doc.add_text("2. Densidad [kg/m^3]:  (1: 2,4-DM-tridecano | 2: 2,4-DM-tetradecano | 3: Hexadecano | Mezcla)", advance=28)
doc.add_math(eval_expr(op_call(r_id("rho", "1"), r_id("T", "0"))), left=40, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("rho", "2"), r_id("T", "0"))), left=170, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("rho", "3"), r_id("T", "0"))), left=300, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("rho", "M"), r_id("T", "0"))), left=430, width=130, advance=45)

doc.add_text("3. Conductividad Térmica [W/(m*K)]:  (1: 2,4-DM-tridecano | 2: 2,4-DM-tetradecano | 3: Hexadecano | Mezcla)", advance=28)
doc.add_math(eval_expr(op_call(r_id("k", "1"), r_id("T", "0"))), left=40, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("k", "2"), r_id("T", "0"))), left=170, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("k", "3"), r_id("T", "0"))), left=300, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("k", "M"), r_id("T", "0"))), left=430, width=130, advance=45)

doc.add_text("4. Calor Específico Másico [J/(kg*K)]:  (1: 2,4-DM-tridecano | 2: 2,4-DM-tetradecano | 3: Hexadecano | Mezcla)", advance=28)
doc.add_math(eval_expr(op_call(r_id("cp", "1"), r_id("T", "0"))), left=40, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("cp", "2"), r_id("T", "0"))), left=170, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("cp", "3"), r_id("T", "0"))), left=300, width=120, advance=0)
doc.add_math(eval_expr(op_call(r_id("cp", "M"), r_id("T", "0"))), left=430, width=130, advance=55)

# ==================== 10. PROPIEDADES DEL AIRE GASEOSO (INCISO E) ====================
doc.add_subtitle("10. Inciso e) Propiedades del Aire Gaseoso (Capítulo 4 - Yaws Handbook)")
doc.add_text("Estimación de propiedades para el aire gaseoso a baja presión en función de T:", advance=30)

# cp_aire(T)
def build_cp_air_expr():
    T_ad = op_div(r_id("T"), r_id("K"))
    t1 = op_add(r_num(29.643), op_mul(r_num(-0.0051373), T_ad))
    t2 = op_add(t1, op_mul(r_num(0.000013106), op_pow(T_ad, r_num(2))))
    poly = op_add(t2, op_mul(r_num(-0.0000000048325), op_pow(T_ad, r_num(3))))
    unit_cp_mol = op_div(r_id("joule"), op_mul(r_id("mole"), r_id("K")))
    return op_div(op_mul(op_parens(poly), unit_cp_mol), r_id("MW", "aire"))

doc.add_math(define_func("cp", "aire", ["T"], build_cp_air_expr()), left=40, width=500, advance=50)

# k_aire(T)
def build_k_air_expr():
    T_ad = op_div(r_id("T"), r_id("K"))
    t1 = op_add(r_num(-0.00038603), op_mul(r_num(0.00010311), T_ad))
    t2 = op_add(t1, op_mul(r_num(-0.000000054199), op_pow(T_ad, r_num(2))))
    poly = op_add(t2, op_mul(r_num(0.000000000017429), op_pow(T_ad, r_num(3))))
    unit_k = op_div(r_id("watt"), op_mul(r_id("m"), r_id("K")))
    return op_mul(op_parens(poly), unit_k)

doc.add_math(define_func("k", "aire", ["T"], build_k_air_expr()), left=40, width=500, advance=50)

# mu_aire(T) - micropoise a Pa*s (1 micropoise = 10^-7 Pa*s)
def build_mu_air_expr():
    T_ad = op_div(r_id("T"), r_id("K"))
    t1 = op_add(r_num(4.5608), op_mul(r_num(0.70077), T_ad))
    t2 = op_add(t1, op_mul(r_num(-0.00037287), op_pow(T_ad, r_num(2))))
    poly = op_add(t2, op_mul(r_num(0.000000090437), op_pow(T_ad, r_num(3))))
    unit_mu = op_mul(r_num(0.0000001), op_mul(r_id("Pa"), r_id("s")))
    return op_mul(op_parens(poly), unit_mu)

doc.add_math(define_func("mu", "aire", ["T"], build_mu_air_expr()), left=40, width=500, advance=55)

doc.add_text("Evaluación de Propiedades del Aire a 298.15 K en Sistema Internacional (SI):", advance=28)
doc.add_math(eval_expr(op_call(r_id("cp", "aire"), r_id("T", "0"))), left=40, width=150, advance=0)
doc.add_math(eval_expr(op_call(r_id("k", "aire"), r_id("T", "0"))), left=210, width=150, advance=0)
doc.add_math(eval_expr(op_call(r_id("mu", "aire"), r_id("T", "0"))), left=380, width=150, advance=55)

# ==================== 11. RANGO DE TEMPERATURA Y DEFINICIONES PARA GRÁFICOS ====================
doc.add_subtitle("11. Rango de Temperatura y Variables para Gráficos (270 K a 500 K)")
doc.add_text("Definición de rangos de temperatura con y sin unidades para graficar:", advance=28)

# T := 270 * K, 275 * K .. 500 * K  (Rango dimensional con Kelvin)
range_seq_dim = f"<ml:sequence>{op_mul(r_num(270), r_id('K'))}{op_mul(r_num(275), r_id('K'))}{op_mul(r_num(500), r_id('K'))}</ml:sequence>"
doc.add_math(define_var(r_id("T"), range_seq_dim), left=40, width=180, advance=0)

# T_ad := 270, 275 .. 500  (Rango adimensional para graficar sin unidades)
range_seq_ad = f"<ml:sequence>{r_num(270)}{r_num(275)}{r_num(500)}</ml:sequence>"
doc.add_math(define_var(r_id("T", "ad"), range_seq_ad), left=260, width=160, advance=50)

doc.add_text("Funciones auxiliares adimensionales para graficar de forma directa:", advance=28)

# mu1_p(T) := mu1(T) / cP
doc.add_math(define_func("mu1", "p", ["T"], op_div(op_call(r_id("mu", "1"), r_id("T")), r_id("cP"))), left=40, width=130, advance=0)
doc.add_math(define_func("mu2", "p", ["T"], op_div(op_call(r_id("mu", "2"), r_id("T")), r_id("cP"))), left=180, width=130, advance=0)
doc.add_math(define_func("mu3", "p", ["T"], op_div(op_call(r_id("mu", "3"), r_id("T")), r_id("cP"))), left=320, width=130, advance=0)
doc.add_math(define_func("muM", "p", ["T"], op_div(op_call(r_id("mu", "M"), r_id("T")), r_id("cP"))), left=460, width=130, advance=55)

doc.add_text("INSTRUCCIONES CLARAS PARA INSERTAR LOS GRÁFICOS (X-Y PLOT):", advance=26)
doc.add_text("1. Inserte un gráfico presionando Ctrl + 2 (o menú Insertar -> Gráfico -> Gráfico X-Y).", advance=24)
doc.add_text("2. En el eje horizontal (marcador central abajo), ingrese exactamente: T", advance=24)
doc.add_text("3. En el eje vertical (marcador central izquierda), ingrese las trazas separadas por coma:", advance=24)
doc.add_text("   - Gráfico de Viscosidad:  mu1_p(T) , mu2_p(T) , mu3_p(T) , muM_p(T)", advance=24)
doc.add_text("   - Gráfico de Densidad:    rho_1(T)/(g/cm^3) , rho_2(T)/(g/cm^3) , rho_3(T)/(g/cm^3) , rho_M(T)/(g/cm^3)", advance=24)
doc.add_text("   - Gráfico de Conductividad: k_1(T)/(watt/(m*K)) , k_2(T)/(watt/(m*K)) , k_3(T)/(watt/(m*K)) , k_M(T)/(watt/(m*K))", advance=24)
doc.add_text("   - Gráfico de Calor Específico: cp_1(T)/(joule/(kg*K)) , cp_2(T)/(joule/(kg*K)) , cp_3(T)/(joule/(kg*K)) , cp_M(T)/(joule/(kg*K))", advance=26)
doc.add_text("4. Configuración de Markers en Viscosidad:", advance=24)
doc.add_text("   Haga doble clic en el gráfico de viscosidad -> pestaña 'Ejes X-Y' -> active 'Markers'.", advance=24)
doc.add_text("   En los dos marcadores del eje X coloque: 273*K y 340*K  (o 273 y 340 si el eje X es T/K).", advance=24)
doc.add_text("   En los dos marcadores del eje Y coloque: 4.053 y 1.167.", advance=30)

# Save raw XML
tree.write(OUTPUT_RAW, encoding='utf-8', xml_declaration=True)
print(f"Worksheet XML written to: {OUTPUT_RAW}")

# Render with Mathcad COM API
mc = win32com.client.Dispatch('Mathcad.Application')
try:
    ws = mc.Worksheets.Open(os.path.abspath(OUTPUT_RAW))
    ws.Recalculate()
    ws.SaveAs(os.path.abspath(OUTPUT_RENDERED))
    ws.Close(2)
    print(f"Recalculation and visual rendering completed: {OUTPUT_RENDERED}")
except Exception as e:
    print(f"COM error: {e}")
finally:
    mc.Quit(2)
