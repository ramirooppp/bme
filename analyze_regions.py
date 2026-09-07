import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\nahue\Desktop\segundo cuatrimestre\inspect_readable.txt', 'r', encoding='utf-8') as f:
    text = f.read()

regions = text.split('--- R')
for r in regions[1:]:
    header = r.split('\n')[0]
    content = '\n'.join(r.split('\n')[1:])
    # print summary of region
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    if 'TEXT' in header:
        print(f"[{header}] {lines[0] if lines else ''}")
    elif 'PLOT' in header:
        print(f"[{header}]")
    elif 'MATH' in header:
        # extract error and key identifiers
        import xml.etree.ElementTree as ET
        try:
            el = ET.fromstring(content)
            err = el.attrib.get('error', '')
            # find all tags of interest
            ids = [i.text + ('_' + i.attrib.get('subscript','') if i.attrib.get('subscript') else '') for i in el.findall('.//{http://schemas.mathsoft.com/math30}id')]
            reals = [i.text for i in el.findall('.//{http://schemas.mathsoft.com/math30}real')]
            eval_tag = el.find('.//{http://schemas.mathsoft.com/math30}eval')
            define_tag = el.find('.//{http://schemas.mathsoft.com/math30}define')
            equal_tag = el.find('.//{http://schemas.mathsoft.com/math30}equal')
            kind = "DEF" if define_tag is not None else ("EVAL" if eval_tag is not None else ("EQUAL" if equal_tag is not None else "OTHER"))
            print(f"[{header}] Kind={kind} IDs={ids[:6]} Err='{err}'")
        except Exception as e:
            print(f"[{header}] parse err: {e}")
