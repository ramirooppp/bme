"""
Test creating a Mathcad 15 plot by cloning a blob and modifying expression names.

Strategy:
1. Take the simplest working plot blob (item 73: k.M vs T.ran, 1 trace)
2. Clone it as-is into a new xmcd file with the math already defined
3. See if Mathcad recalculates it correctly via COM

Then:
4. Modify the expression names in the blob to match different functions
5. See if Mathcad recalculates correctly
"""
import xml.etree.ElementTree as ET
import base64, gzip, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

# Extract blob from Grupo J
filepath = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns_ws = 'http://schemas.mathsoft.com/worksheet30'
ns = {'ws': ns_ws}

# Get item 73 blob (k.M vs T.ran)
for item in root.findall('.//ws:binaryContent/ws:item', ns):
    if item.attrib.get('item-id') == '73':
        blob_b64 = item.text
        break

# Also get item 8 blob (3-trace μ vs T.ran with more detail)
for item in root.findall('.//ws:binaryContent/ws:item', ns):
    if item.attrib.get('item-id') == '8':
        blob3_b64 = item.text
        break

print(f"Got 1-trace blob (item 73): {len(blob_b64)} chars base64")
print(f"Got 3-trace blob (item 8): {len(blob3_b64)} chars base64")

# Now load our working template
template_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\TP1_Fenomenos_Transporte_Final.xmcd'
tree2 = ET.parse(template_path)
root2 = tree2.getroot()

# Find max item-id and region-id
max_item_id = 0
for item in root2.findall(f'.//{{{ns_ws}}}item'):
    iid = int(item.attrib.get('item-id', '0'))
    if iid > max_item_id:
        max_item_id = iid

max_region_id = 0
max_top = 0
for region in root2.findall(f'.//{{{ns_ws}}}region'):
    rid = int(region.attrib.get('region-id', '0'))
    top = float(region.attrib.get('top', '0'))
    if rid > max_region_id:
        max_region_id = rid
    if top > max_top:
        max_top = top

print(f"\nTemplate max item-id: {max_item_id}")
print(f"Template max region-id: {max_region_id}")
print(f"Template max top: {max_top}")

# Add the plot blob to binaryContent
new_item_id = max_item_id + 1
bc = root2.find(f'.//{{{ns_ws}}}binaryContent')
if bc is None:
    # Create binaryContent
    bc = ET.SubElement(root2, f'{{{ns_ws}}}binaryContent')

new_item = ET.SubElement(bc, f'{{{ns_ws}}}item')
new_item.set('item-id', str(new_item_id))
new_item.set('content-encoding', 'gzip')
new_item.text = blob_b64

# Add plot region
regions = root2.find(f'.//{{{ns_ws}}}regions')
new_region = ET.SubElement(regions, f'{{{ns_ws}}}region')
new_region_id = max_region_id + 1
new_top = int(max_top) + 60
new_region.set('region-id', str(new_region_id))
new_region.set('left', '30')
new_region.set('top', str(new_top))
new_region.set('width', '300')
new_region.set('height', '200')
new_region.set('align-x', '30')
new_region.set('align-y', str(new_top))
new_region.set('show-border', 'false')
new_region.set('show-highlight', 'false')
new_region.set('is-protected', 'false')
new_region.set('z-order', '0')
new_region.set('background-color', 'inherit')
new_region.set('tag', '')

plot_el = ET.SubElement(new_region, f'{{{ns_ws}}}plot')
plot_el.set('disable-calc', 'false')
plot_el.set('item-idref', str(new_item_id))

# Save
out_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Test_Plot_Clonado.xmcd'
tree2.write(out_path, xml_declaration=True, encoding='UTF-8')

print(f"\nSaved test file to: {out_path}")
print(f"  New region-id: {new_region_id}")
print(f"  New item-id: {new_item_id}")
print(f"  Plot top position: {new_top}")

# Now try to open and recalculate with COM
print("\nAttempting COM recalculation...")
try:
    import win32com.client
    mc = win32com.client.Dispatch('Mathcad.Application')
    mc.Visible = False
    ws = mc.Open(out_path)
    ws.Recalculate()
    
    # Check for errors
    err_count = 0
    for i in range(ws.Regions.Count):
        r = ws.Regions.Item(i)
        if hasattr(r, 'Error') and r.Error:
            err_count += 1
    
    ws.SaveAs(out_path)
    ws.Close(2)
    mc.Quit(2)
    
    print(f"COM recalculation complete! Errors: {err_count}")
except Exception as e:
    print(f"COM error: {e}")
    try:
        mc.Quit(2)
    except:
        pass
