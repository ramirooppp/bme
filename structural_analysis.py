"""
Structural analysis of a Mathcad 15 plot blob.
Objective: Map every byte to understand the full format.

Strategy: Use the simplest blob (single-trace plot k.M vs T.ran) 
and annotate the structure.
"""
import xml.etree.ElementTree as ET
import base64, gzip, sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30'}

# Get the simplest plot blob - k.M vs T.ran (item 73, 1086 bytes)
items = {}
for item in root.findall('.//ws:binaryContent/ws:item', ns):
    item_id = item.attrib.get('item-id')
    encoding = item.attrib.get('content-encoding', 'none')
    b64_text = item.text
    if not b64_text:
        continue
    raw = base64.b64decode(b64_text)
    if encoding == 'gzip':
        try:
            data = gzip.decompress(raw)
        except:
            data = raw
    else:
        data = raw
    items[item_id] = data

# Use the 1-trace plot: k.M vs T.ran (item 73)  
data = items['73']
print(f"Analyzing item 73 (k.M vs T.ran), size={len(data)} bytes")
print()

# Full annotated hex dump
for offset in range(0, len(data), 16):
    hex_part = ' '.join(f'{b:02x}' for b in data[offset:offset+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f'{offset:04x}: {hex_part:<48} {ascii_part}')

print("\n\n--- Comparison: 3-trace plot ρ vs T.ran (item 21), size ---")
data2 = items['21']
print(f"Item 21 (3-trace ρ vs T.ran), size={len(data2)} bytes")
print(f"Difference: {len(data2) - len(data)} bytes\n")

# Full hex dump of item 21
for offset in range(0, len(data2), 16):
    hex_part = ' '.join(f'{b:02x}' for b in data2[offset:offset+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data2[offset:offset+16])
    print(f'{offset:04x}: {hex_part:<48} {ascii_part}')

# Also dump template blob (item 1 from QQplot)
print("\n\n--- Also checking if Grupo J has a plotTemplate ---")
for item in root.findall('.//ws:plotTemplate', ns):
    print(f"Found plotTemplate: {ET.tostring(item, encoding='unicode')}")

# Check settings
for settings in root.findall('.//ws:editor', ns):
    pt = settings.find('ws:plotTemplate', ns)
    if pt is not None:
        xy = pt.find('ws:xy', ns)
        if xy is not None:
            idref = xy.attrib.get('item-idref')
            print(f"plotTemplate xy item-idref: {idref}")
            if idref in items:
                tdata = items[idref]
                print(f"Template blob size: {len(tdata)} bytes")
                print("Template blob hex dump:")
                for offset in range(0, len(tdata), 16):
                    hex_part = ' '.join(f'{b:02x}' for b in tdata[offset:offset+16])
                    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in tdata[offset:offset+16])
                    print(f'{offset:04x}: {hex_part:<48} {ascii_part}')
