"""
Test 2: Create a minimal xmcd file with a cloned plot blob.
Use the raw XML approach instead of ET.write which mangles namespaces.
"""
import xml.etree.ElementTree as ET
import base64, gzip, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# Extract blob from Grupo J
filepath = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)
root = tree.getroot()
ns = {'ws': 'http://schemas.mathsoft.com/worksheet30'}

blobs = {}
for item in root.findall('.//ws:binaryContent/ws:item', ns):
    item_id = item.attrib.get('item-id')
    blobs[item_id] = item.text

# Get the 1-trace blob (k.M vs T.ran)
blob_1trace = blobs['73']
# Get the 3-trace blob (μ vs T.ran with μ₁, μ₂, μ₃)
blob_3trace = blobs['8']

print(f"1-trace blob: {len(blob_1trace)} chars")
print(f"3-trace blob: {len(blob_3trace)} chars")

# Now read the raw TP1 Final XML and inject the plot
tp1_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\TP1_Fenomenos_Transporte_Final.xmcd'
with open(tp1_path, 'r', encoding='utf-8') as f:
    xml_text = f.read()

# Check if binaryContent already exists
if '<binaryContent>' in xml_text or '<ws:binaryContent>' in xml_text:
    print("binaryContent already exists in TP1")
    # Find it and add items
    # Look for </binaryContent> or </ws:binaryContent>
    bc_close = '</binaryContent>'
    if bc_close not in xml_text:
        bc_close = '</ws:binaryContent>'
    if bc_close in xml_text:
        insert_before = xml_text.index(bc_close)
        new_items = f"""
        <item item-id="70" content-encoding="gzip">{blob_1trace}</item>
        <item item-id="71" content-encoding="gzip">{blob_3trace}</item>
"""
        xml_text = xml_text[:insert_before] + new_items + xml_text[insert_before:]
        print("Added items to existing binaryContent")
else:
    # Add binaryContent before closing </worksheet>
    ws_close = '</worksheet>'
    if ws_close not in xml_text:
        ws_close = '</ws:worksheet>'
    insert_before = xml_text.index(ws_close)
    bc_section = f"""
    <binaryContent>
        <item item-id="70" content-encoding="gzip">{blob_1trace}</item>
        <item item-id="71" content-encoding="gzip">{blob_3trace}</item>
    </binaryContent>
"""
    xml_text = xml_text[:insert_before] + bc_section + xml_text[insert_before:]
    print("Added new binaryContent section")

# Now add plot regions before </regions>
regions_close = '</regions>'
if regions_close not in xml_text:
    regions_close = '</ws:regions>'

insert_before = xml_text.rindex(regions_close)  # last occurrence

plot_regions = """
        <region region-id="200" left="30" top="3520" width="300" height="200" align-x="30" align-y="3520" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
            <plot disable-calc="false" item-idref="70" />
        </region>
        <region region-id="201" left="30" top="3780" width="300" height="200" align-x="30" align-y="3780" show-border="false" show-highlight="false" is-protected="false" z-order="0" background-color="inherit" tag="">
            <plot disable-calc="false" item-idref="71" />
        </region>
"""
xml_text = xml_text[:insert_before] + plot_regions + xml_text[insert_before:]
print("Added plot regions")

# Save
out_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Test_Plot_Clonado.xmcd'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(xml_text)
print(f"Saved to: {out_path}")

# Now try COM
print("\nAttempting COM open + recalculate...")
try:
    import win32com.client
    mc = win32com.client.Dispatch('Mathcad.Application')
    mc.Visible = False
    import os
    ws = mc.Worksheets.Open(os.path.abspath(out_path))
    print(f"Opened successfully! Regions: {ws.Regions.Count}")
    ws.Recalculate()
    
    # Check for plot regions
    plot_count = 0
    err_count = 0
    for i in range(ws.Regions.Count):
        r = ws.Regions.Item(i)
        try:
            rtype = r.Type
            if rtype == 6:  # possible plot type
                plot_count += 1
        except:
            pass
        try:
            if r.Error:
                err_count += 1
        except:
            pass
    
    print(f"Plot regions detected: {plot_count}")
    print(f"Errors: {err_count}")
    
    save_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Test_Plot_Rendered.xmcd'
    ws.SaveAs(os.path.abspath(save_path))
    ws.Close(2)
    mc.Quit(2)
    print(f"Saved rendered version to: {save_path}")
except Exception as e:
    print(f"COM error: {e}")
    import traceback
    traceback.print_exc()
    try:
        mc.Quit(2)
    except:
        pass
