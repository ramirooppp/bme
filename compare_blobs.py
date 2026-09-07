"""
Compare multiple plot blobs from Grupo J to reverse-engineer the format.
Focus on finding expression placeholders in each blob.
"""
import xml.etree.ElementTree as ET
import base64, gzip, zlib, sys

sys.stdout.reconfigure(encoding='utf-8')

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
            data = raw
    else:
        data = raw
    items[item_id] = data

# Find plot regions
plots = []
for region in root.findall('.//ws:region', ns):
    plot = region.find('ws:plot', ns)
    if plot is None:
        continue
    rid = region.attrib.get('region-id')
    top = region.attrib.get('top')
    idref = plot.attrib.get('item-idref')
    plots.append((rid, top, idref))

print(f"Found {len(plots)} plot regions\n")

def extract_utf16_strings(data):
    """Extract all UTF-16LE strings from binary data"""
    strings = []
    i = 0
    while i < len(data) - 1:
        chars = []
        start = i
        while i < len(data) - 1:
            code = data[i] + data[i+1] * 256
            # Accept printable ASCII, Greek letters, common math
            if (32 <= code < 127) or (0x0391 <= code <= 0x03C9) or code in [0xB5, 0xB7, 0x2212, 0x00B2, 0x00B3]:
                chars.append(chr(code))
                i += 2
            else:
                break
        if len(chars) >= 1:
            strings.append((start, ''.join(chars)))
        else:
            i += 1
    return strings

def extract_ascii_strings(data):
    """Extract ASCII strings"""
    strings = []
    current = []
    for i, b in enumerate(data):
        if 32 <= b < 127:
            current.append(chr(b))
        else:
            if len(current) >= 3:
                strings.append((i - len(current), ''.join(current)))
            current = []
    if len(current) >= 3:
        strings.append((len(data) - len(current), ''.join(current)))
    return strings

for rid, top, idref in plots:
    data = items.get(idref)
    if not data:
        continue
    
    print(f"--- Plot region-id={rid}, top={top}, item={idref}, size={len(data)} ---")
    
    # Extract UTF-16LE strings
    utf16 = extract_utf16_strings(data)
    # Filter to meaningful strings (length > 1 or Greek)
    meaningful_utf16 = [(off, s) for off, s in utf16 if len(s) > 1 or ord(s[0]) > 127]
    
    print(f"  UTF-16LE strings: {[(s, off) for off, s in meaningful_utf16]}")
    
    # Extract ASCII strings  
    ascii_s = extract_ascii_strings(data)
    # Filter to known class names and other interesting strings
    interesting = [(off, s) for off, s in ascii_s if s not in ['eqRegion', 'docRegion', 'mcObject', 'shpBox', 'shpRect', 'docRegionAttribute', 'tree']]
    print(f"  ASCII strings: {[(s, off) for off, s in interesting]}")
    print()
