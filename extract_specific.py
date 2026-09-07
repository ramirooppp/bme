import pandas as pd
import json

file_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Nueva carpeta\Yaws Handbook (corrected) of Thermodynamic and Physical Properties of Chemical Compounds - Yaws 2003 (2024).xlsx'

sheets_of_interest = [
    'Liq Viscos (Org)', 'ρ liq (Org)', 'K liq-Thermal Cond (Organic)', 'Cp L (Org)',
    'Cp G (Inorg)', 'Gas Viscos (Inorg)', 'K gas-Thermal Cond (Organic)', 'K gas-Thermal Cond (Inorg)',
    'Cp G (Inorg)', 'Cp G (Organic)'
]

search_terms = ["C15H32", "C16H34", "Air", "air", "AIR"]

def extract_specific():
    xls = pd.ExcelFile(file_path)
    output = []
    
    for sheet in sheets_of_interest:
        if sheet not in xls.sheet_names:
            # Maybe slight mismatch in name
            for s in xls.sheet_names:
                if sheet.lower() in s.lower() or "cond" in sheet.lower():
                    pass # just trying exact matches for now
            if sheet not in xls.sheet_names:
                continue
                
        df = pd.read_excel(file_path, sheet_name=sheet)
        output.append(f"\n--- SHEET: {sheet} ---")
        
        # Search all string columns for the terms
        for index, row in df.iterrows():
            row_str = " ".join([str(x) for x in row.values])
            found = False
            for term in search_terms:
                if term in row_str or term.lower() in row_str.lower():
                    found = True
            if found:
                output.append(str(row.to_dict()))
                
    with open("yaws_specific.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    extract_specific()
