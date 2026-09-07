"""
Deep analysis of a single Mathcad 15 plot blob - focus on expression placeholders
"""
import xml.etree.ElementTree as ET
import base64, gzip, zlib, sys, struct

sys.stdout.reconfigure(encoding='utf-8')

# Use Grupo J which has many plots with known expressions
filepath = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30'}

# Map item_id -> blob data
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
            try:
                data = zlib.decompress(raw, -15)
            except:
                data = raw
    else:
        data = raw
    items[item_id] = data

# Find plot regions and their positions + idrefs
for region in root.findall('.//ws:region', ns):
    plot = region.find('ws:plot', ns)
    if plot is None:
        continue
    rid = region.attrib.get('region-id')
    top = region.attrib.get('top')
    idref = plot.attrib.get('item-idref')
    
    data = items.get(idref)
    if not data:
        continue
    
    print(f"\n{'='*80}")
    print(f"PLOT region-id={rid}, top={top}, item-idref={idref}, blob size={len(data)} bytes")
    print(f"{'='*80}")
    
    # Find ALL UTF-16LE strings
    print(f"\n--- UTF-16LE strings ---")
    i = 0
    while i < len(data) - 1:
        chars = []
        start = i
        while i < len(data) - 1:
            lo, hi = data[i], data[i+1]
            # Accept printable ASCII + common math symbols in low byte
            if hi == 0 and (32 <= lo < 127 or lo in [0xB5, 0xB7, 0xC0]):  # mu, etc
                chars.append(chr(lo))
                i += 2
            elif hi == 0x03 and 0x91 <= lo <= 0xC9:  # Greek letters (U+0391-U+03C9)
                chars.append(chr(lo + hi * 256))
                i += 2
            else:
                break
        if len(chars) >= 1:
            s = ''.join(chars)
            # Show context bytes before the string
            ctx_start = max(0, start - 4)
            ctx = ' '.join(f'{b:02x}' for b in data[ctx_start:start])
            print(f"  offset {start:4d} [ctx: {ctx}]: '{s}' (len={len(chars)})")
        else:
            i += 1
    
    # Full hex dump of the blob
    print(f"\n--- Full hex dump ---")
    for offset in range(0, len(data), 16):
        hex_part = ' '.join(f'{b:02x}' for b in data[offset:offset+16])
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        print(f'{offset:04x}: {hex_part:<48} {ascii_part}')
    
    # Only analyze first 2 plots
    if int(rid) > 400:
        break
