import pandas as pd
import json

file_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Nueva carpeta\Yaws Handbook (corrected) of Thermodynamic and Physical Properties of Chemical Compounds - Yaws 2003 (2024).xlsx'

search_terms = ["air"] # We already found the organics, we only need Air!

sheets_of_interest = ['Cp G (Inorg)', 'Cp L (Inorg)', 'Gas Viscos (Inorg)', 'K gas-Thermal Cond (Inorg)', 'Liq Viscos (Inorg)', 'ρ liq (Inorg)']
# Actually I'll just check all Inorg sheets, but for speed just those. Wait, thermal cond inorg might not be there. Let's just list the sheets.
xls = pd.ExcelFile(file_path)

output = []
for sheet in xls.sheet_names:
    if 'Inorg' not in sheet and 'Air' not in sheet and 'air' not in sheet.lower():
        continue
    df = pd.read_excel(file_path, sheet_name=sheet)
    for index, row in df.iterrows():
        # check all values
        for val in row.values:
            if isinstance(val, str) and val.strip().lower() == "air":
                output.append(f"\n--- SHEET: {sheet} ---")
                output.append(str(row.to_dict()))
                break

with open("yaws_air.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

