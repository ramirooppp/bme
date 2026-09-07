import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'c:\Users\nahue\Desktop\segundo cuatrimestre\Grupo J-Trabajo Practico N°1.xmcd'
tree = ET.parse(filepath)

regions = tree.findall('.//{http://schemas.mathsoft.com/worksheet30}region')
print(f'Total regions: {len(regions)}')

for i, r in enumerate(regions):
    text_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}text')
    math_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}math')
    plot_el = r.find('.//{http://schemas.mathsoft.com/worksheet30}plot')
    if text_el is not None:
        p_texts = [p.text for p in text_el.findall('.//{http://schemas.mathsoft.com/worksheet30}p') if p.text]
        print(f'R{i+1:02d} [TEXT]: {" | ".join(p_texts)}')
    elif math_el is not None:
        err = math_el.attrib.get('error', '')
        define = math_el.find('.//{http://schemas.mathsoft.com/math30}define')
        eval_el = math_el.find('.//{http://schemas.mathsoft.com/math30}eval')
        if define is not None:
            func = define.find('.//{http://schemas.mathsoft.com/math30}function')
            id_el = define.find('.//{http://schemas.mathsoft.com/math30}id')
            if func is not None:
                fn_id = func.find('.//{http://schemas.mathsoft.com/math30}id')
                sub = fn_id.attrib.get('subscript', '')
                print(f'R{i+1:02d} [MATH-FUNC]: {fn_id.text}_{sub} (err: {err})')
            elif id_el is not None:
                sub = id_el.attrib.get('subscript', '')
                print(f'R{i+1:02d} [MATH-VAR]: {id_el.text}_{sub} (err: {err})')
            else:
                print(f'R{i+1:02d} [MATH-DEF] (err: {err})')
        elif eval_el is not None:
            id_el = eval_el.find('.//{http://schemas.mathsoft.com/math30}id')
            var_name = id_el.text if id_el is not None else 'expr'
            sub = id_el.attrib.get('subscript', '') if id_el is not None else ''
            print(f'R{i+1:02d} [MATH-EVAL]: {var_name}_{sub} = (err: {err})')
        else:
            print(f'R{i+1:02d} [MATH-OTHER] (err: {err})')
    elif plot_el is not None:
        print(f'R{i+1:02d} [PLOT]')
