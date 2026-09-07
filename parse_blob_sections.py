"""
Reverse-engineer the Mathcad 15 plot blob format by parsing the tree structure.

Based on observation:
- The blob starts with a class registry (eqRegion, docRegion, mcObject, etc.)
- Then a "tree" section with node entries
- Each node entry starts with an ID byte (sequential) and a type byte (0x32 = tree node)
- Nodes contain child references, literals (UTF-16LE strings), and operators

Key insight from comparing blobs:
- The tree section encodes the MATH EXPRESSION AST (same format as Mathcad's internal expression tree)
- After the tree, we have: d2_graph_format > graphData > axisFormat > trace2D > NumericalFormat

Let me parse a blob and identify each section precisely.
"""
import xml.etree.ElementTree as ET
import base64, gzip, sys, struct

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30'}

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

# Analyze the simplest blob: item 73 (k.M vs T.ran, 1 trace)
data = items['73']
print(f"=== Item 73 (k.M vs T.ran, 1 trace, {len(data)} bytes) ===\n")

# The format is an MFC archive. Let me parse key sections:
# Starting after the class registry, find the "tree" keyword
tree_start = data.find(b'tree')
print(f"'tree' at offset {tree_start}")

# The d2_graph_format section 
graph_start = data.find(b'd2_graph_format')
print(f"'d2_graph_format' at offset {graph_start}")

# graphData section
gd_start = data.find(b'graphData')
print(f"'graphData' at offset {gd_start}")

# axisFormat section
af_start = data.find(b'axisFormat')
print(f"'axisFormat' at offset {af_start}")

# trace2D section
t2d_start = data.find(b'trace2D')
print(f"'trace2D' at offset {t2d_start}")

# NumericalFormat section
nf_start = data.find(b'NumericalFormat')
print(f"'NumericalFormat' at offset {nf_start}")

# So the sections are:
# 1. Header + class registry: 0 to tree_start
# 2. Expression tree: tree_start to graph_start  
# 3. d2_graph_format: graph_start
# 4. graphData: gd_start
# 5. axisFormat: af_start
# 6. trace2D: t2d_start
# 7. NumericalFormat: nf_start

print(f"\nSection sizes:")
print(f"  Header+Registry: {tree_start} bytes")
print(f"  Expression tree: {graph_start - tree_start} bytes")
print(f"  d2_graph_format header: {gd_start - graph_start} bytes")
print(f"  graphData: {af_start - gd_start} bytes")
print(f"  axisFormat: {t2d_start - af_start} bytes")
print(f"  trace2D: {nf_start - t2d_start} bytes")
print(f"  NumericalFormat: {len(data) - nf_start} bytes")

# Now let's look at what's between tree and d2_graph_format - the expression tree
expr_tree = data[tree_start:graph_start]
print(f"\n--- Expression tree ({len(expr_tree)} bytes) ---")
for offset in range(0, len(expr_tree), 16):
    abs_off = tree_start + offset
    hex_part = ' '.join(f'{b:02x}' for b in expr_tree[offset:offset+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in expr_tree[offset:offset+16])
    print(f'{abs_off:04x}: {hex_part:<48} {ascii_part}')

# Now compare with 3-trace blob (item 21, ρ vs T.ran)
data2 = items['21']
tree_start2 = data2.find(b'tree')
graph_start2 = data2.find(b'd2_graph_format')
gd_start2 = data2.find(b'graphData')
af_start2 = data2.find(b'axisFormat')
t2d_start2 = data2.find(b'trace2D')
nf_start2 = data2.find(b'NumericalFormat')

print(f"\n=== Item 21 (ρ vs T.ran, 3 traces, {len(data2)} bytes) ===")
print(f"Section sizes:")
print(f"  Header+Registry: {tree_start2} bytes")
print(f"  Expression tree: {graph_start2 - tree_start2} bytes")
print(f"  d2_graph_format header: {gd_start2 - graph_start2} bytes")
print(f"  graphData: {af_start2 - gd_start2} bytes")
print(f"  axisFormat: {t2d_start2 - af_start2} bytes")
print(f"  trace2D: {nf_start2 - t2d_start2} bytes")
print(f"  NumericalFormat: {len(data2) - nf_start2} bytes")

# Compare graphData sections
print(f"\n--- graphData comparison ---")
gd1 = data[gd_start:af_start]
gd2 = data2[gd_start2:af_start2]
print(f"Item 73 graphData:")
for o in range(0, len(gd1), 16):
    hex_part = ' '.join(f'{b:02x}' for b in gd1[o:o+16])
    print(f'  {hex_part}')
print(f"Item 21 graphData:")
for o in range(0, len(gd2), 16):
    hex_part = ' '.join(f'{b:02x}' for b in gd2[o:o+16])
    print(f'  {hex_part}')

# axisFormat comparison
print(f"\n--- axisFormat comparison ---")
af1 = data[af_start:t2d_start]
af2 = data2[af_start2:t2d_start2]
print(f"Item 73 axisFormat ({len(af1)} bytes):")
for o in range(0, len(af1), 16):
    hex_part = ' '.join(f'{b:02x}' for b in af1[o:o+16])
    print(f'  {hex_part}')
print(f"Item 21 axisFormat ({len(af2)} bytes):")
for o in range(0, len(af2), 16):
    hex_part = ' '.join(f'{b:02x}' for b in af2[o:o+16])
    print(f'  {hex_part}')

# trace2D comparison
print(f"\n--- trace2D comparison ---")
t1 = data[t2d_start:nf_start]
t2 = data2[t2d_start2:nf_start2]
print(f"Item 73 trace2D ({len(t1)} bytes):")
for o in range(0, len(t1), 16):
    hex_part = ' '.join(f'{b:02x}' for b in t1[o:o+16])
    print(f'  {hex_part}')
print(f"Item 21 trace2D ({len(t2)} bytes):")
for o in range(0, len(t2), 16):
    hex_part = ' '.join(f'{b:02x}' for b in t2[o:o+16])
    print(f'  {hex_part}')

# NumericalFormat comparison
print(f"\n--- NumericalFormat comparison ---")
n1 = data[nf_start:]
n2 = data2[nf_start2:]
print(f"Item 73 NumericalFormat ({len(n1)} bytes):")
for o in range(0, len(n1), 16):
    hex_part = ' '.join(f'{b:02x}' for b in n1[o:o+16])
    print(f'  {hex_part}')
print(f"Item 21 NumericalFormat ({len(n2)} bytes):")
for o in range(0, len(n2), 16):
    hex_part = ' '.join(f'{b:02x}' for b in n2[o:o+16])
    print(f'  {hex_part}')
