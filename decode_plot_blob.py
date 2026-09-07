"""
Decode Mathcad 15 plot binary blobs - extract from actual xmcd files to avoid transcription errors.
"""
import xml.etree.ElementTree as ET
import base64, gzip, zlib, sys, struct, io

sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    (r'C:\Users\nahue\Desktop\segundo cuatrimestre\mathcad\Test_Grafico.xmcd', 'Test_Grafico'),
    (r'C:\Users\nahue\Desktop\segundo cuatrimestre\mathcad\Ejercicio_2_Con_Graficos.xmcd', 'Ejercicio_2'),
    (r'C:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd', 'Grupo_J'),
]

for filepath, label in FILES:
    try:
        tree = ET.parse(filepath)
    except Exception as e:
        print(f"Cannot parse {filepath}: {e}")
        continue
    
    root = tree.getroot()
    
    # Find all plot regions and their item-idrefs
    plot_idrefs = set()
    ns = {'ws': 'http://schemas.mathsoft.com/worksheet30'}
    for region in root.findall('.//ws:region', ns):
        plot = region.find('ws:plot', ns)
        if plot is not None:
            idref = plot.attrib.get('item-idref')
            if idref:
                plot_idrefs.add(idref)
    
    if not plot_idrefs:
        print(f"\n{label}: No plot regions found")
        continue
    
    print(f"\n{label}: Found plot idrefs: {plot_idrefs}")
    
    # Find binary content items
    for item in root.findall('.//ws:binaryContent/ws:item', ns):
        item_id = item.attrib.get('item-id')
        if item_id not in plot_idrefs:
            continue
        
        encoding = item.attrib.get('content-encoding', 'none')
        b64_text = item.text
        if not b64_text:
            print(f"  Item {item_id}: empty")
            continue
        
        raw = base64.b64decode(b64_text)
        
        if encoding == 'gzip':
            try:
                data = gzip.decompress(raw)
            except Exception:
                # Try raw deflate
                try:
                    data = zlib.decompress(raw, -15)
                except Exception:
                    try:
                        data = zlib.decompress(raw)
                    except Exception as e:
                        print(f"  Item {item_id}: cannot decompress: {e}")
                        # just use raw
                        data = raw
        else:
            data = raw
        
        print(f"\n{'='*80}")
        print(f"FILE: {label}, ITEM: {item_id}")
        print(f"Compressed: {len(raw)} bytes, Decompressed: {len(data)} bytes")
        print(f"{'='*80}")
        
        # Hex dump first 512 bytes
        print(f"\n--- First 512 bytes (hex) ---")
        for offset in range(0, min(512, len(data)), 16):
            hex_part = ' '.join(f'{b:02x}' for b in data[offset:offset+16])
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
            print(f'{offset:04x}: {hex_part:<48} {ascii_part}')
        
        # Search for printable ASCII strings (length >= 2)
        print(f"\n--- ASCII strings (length >= 2) ---")
        current = []
        for i, b in enumerate(data):
            if 32 <= b < 127:
                current.append(chr(b))
            else:
                if len(current) >= 2:
                    s = ''.join(current)
                    print(f"  offset {i-len(current):4d}: '{s}'")
                current = []
        if len(current) >= 2:
            s = ''.join(current)
            print(f"  offset {len(data)-len(current):4d}: '{s}'")
        
        # Search for UTF-16LE strings
        print(f"\n--- UTF-16LE strings (length >= 2 chars) ---")
        i = 0
        while i < len(data) - 1:
            chars = []
            start = i
            while i < len(data) - 1:
                lo, hi = data[i], data[i+1]
                if hi == 0 and 32 <= lo < 127:
                    chars.append(chr(lo))
                    i += 2
                else:
                    break
            if len(chars) >= 2:
                s = ''.join(chars)
                print(f"  offset {start:4d}: '{s}'")
            else:
                i += 1
        
        # Full hex dump (last 256 bytes)
        if len(data) > 512:
            print(f"\n--- Last 256 bytes (hex) ---")
            start = max(512, len(data) - 256)
            for offset in range(start, len(data), 16):
                hex_part = ' '.join(f'{b:02x}' for b in data[offset:offset+16])
                ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
                print(f'{offset:04x}: {hex_part:<48} {ascii_part}')
