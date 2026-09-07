import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\clase24.8.26.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30', 'ml': 'http://schemas.mathsoft.com/math30'}

regions = root.findall('.//ws:region', ns)

# Check R32 (X_etileno)
print("=== R32 ===")
print(ET.tostring(regions[31].find('ws:math', ns), encoding='unicode'))

# Check R45 (eps initial)
print("=== R45 ===")
print(ET.tostring(regions[44].find('ws:math', ns), encoding='unicode'))

# Check R47 (f initial)
print("=== R47 ===")
print(ET.tostring(regions[46].find('ws:math', ns), encoding='unicode'))

# Check R54 (mixer 1)
print("=== R54 ===")
print(ET.tostring(regions[53].find('ws:math', ns), encoding='unicode'))

# Check R59 (conversion eq)
print("=== R59 ===")
print(ET.tostring(regions[58].find('ws:math', ns), encoding='unicode'))

# Check R60 (reactor eq)
print("=== R60 ===")
print(ET.tostring(regions[59].find('ws:math', ns), encoding='unicode'))

# Check R81 (Find call)
print("=== R81 ===")
print(ET.tostring(regions[80].find('ws:math', ns), encoding='unicode'))
