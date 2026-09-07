import pandas as pd
import json

file_path = r'C:\Users\nahue\Desktop\segundo cuatrimestre\Nueva carpeta\Yaws Handbook (corrected) of Thermodynamic and Physical Properties of Chemical Compounds - Yaws 2003 (2024).xlsx'

compounds_of_interest = ["2,4-dimethyltridecane", "2,4-dimethyltetradecane", "hexadecane", "air"]

def find_compound_data():
    xls = pd.ExcelFile(file_path)
    output = []
    
    output.append(f"Available sheets: {xls.sheet_names}")
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        
        # Determine the compound name column
        name_col = None
        for col in df.columns:
            if isinstance(col, str) and "name" in col.lower():
                name_col = col
                break
        
        if not name_col:
            # Maybe it's the second column
            if len(df.columns) > 1:
                name_col = df.columns[1]
            else:
                continue
                
        output.append(f"Searching in sheet '{sheet}' using column '{name_col}'")
        
        for comp in compounds_of_interest:
            # Case insensitive search
            mask = df[name_col].astype(str).str.lower().str.contains(comp, na=False)
            matches = df[mask]
            if not matches.empty:
                output.append(f"\nFound {comp} in {sheet}:")
                for index, row in matches.iterrows():
                    # output row dict
                    output.append(str(row.to_dict()))
                    
    with open("yaws_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    find_compound_data()
