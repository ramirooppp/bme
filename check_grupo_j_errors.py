import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30', 'ml': 'http://schemas.mathsoft.com/math30'}

regions = root.findall('.//ws:region', ns)
print(f'Total regions in Grupo J: {len(regions)}')

errors = []
for i, r in enumerate(regions):
    rid = r.attrib.get('region-id')
    m = r.find('ws:math', ns)
    t = r.find('ws:text', ns)
    p = r.find('ws:plot', ns)
    if m is not None:
        err = m.attrib.get('error', '')
        tokens = ' '.join([x.strip() for x in m.itertext() if x.strip()])
        if err:
            errors.append((i+1, rid, err, tokens))
            print(f'R{i+1:02d} [ERROR] id={rid}: err="{err}" -> tokens="{tokens}"')

print(f'\nTotal math errors in file: {len(errors)}')

# Let's inspect sections and check against TP 1
# Inciso a: Liquid properties & plots (viscosity, density, k, Cp)
# Inciso b: Solve block for x1, x2, x3 from viscosity data at 273 K and 340 K
# Inciso c: Mixture properties (mu_M, rho_M, k_M, Cp_M) and plots with markers
# Inciso d: Summary table at 298.15 K (SI units)
# Inciso e: Air properties at 298.15 K and polynomials
