# Step 3: Apply only the fixes you reviewed and approved.
# Re-profile after, to confirm the issues are actually resolved.
import pandas as pd
import numpy as np

def apply_fixes(input_path, output_path):
    # Load the messy dataset
    df = pd.read_excel(input_path)
    
    # 1. CustomerID: Drop duplicate records
    df = df.drop_duplicates(subset=['CustomerID'], keep='first')
    
    # 2. First_Name: Trim whitespace
    if 'First_Name' in df.columns:
        df['First_Name'] = df['First_Name'].str.strip()
    
    # 3. Last_Name: Remove stray characters, trim whitespace
    if 'Last_Name' in df.columns:
        df['Last_Name'] = df['Last_Name'].str.replace(r'[/._]', '', regex=True).str.strip()
    
    # 4. Phone_Number: "N/a" -> NaN, remove non-digit formatting, handle float parsing
    if 'Phone_Number' in df.columns:
        df['Phone_Number'] = df['Phone_Number'].replace('N/a', np.nan)
        # Convert to string. If loaded as float, strip the trailing '.0' before regex
        df['Phone_Number'] = df['Phone_Number'].astype(str).str.replace(r'\.0$', '', regex=True)
        # Remove non-digit characters
        df['Phone_Number'] = df['Phone_Number'].str.replace(r'\D', '', regex=True)
        # Convert empty/'nan' strings back to np.nan
        df['Phone_Number'] = df['Phone_Number'].replace({'': np.nan, 'nan': np.nan})
        
        # VERIFICATION: Print first 10 non-null phone numbers and their lengths
        print("--- Phone Number Verification ---")
        sample_phones = df['Phone_Number'].dropna().head(10)
        for val in sample_phones:
            print(f"Number: {val} | Length: {len(val)}")
        print("---------------------------------")
    
    # 5. Address: Trim whitespace only
    if 'Address' in df.columns:
        df['Address'] = df['Address'].replace('N/a', np.nan)
        df['Address'] = df['Address'].str.strip()
    
    # 6. Paying Customer: "N/a" -> NaN, normalize Yes/No and Y/N
    if 'Paying Customer' in df.columns:
        df['Paying Customer'] = df['Paying Customer'].replace('N/a', np.nan)
        df['Paying Customer'] = df['Paying Customer'].replace({'Yes': True, 'Y': True, 'No': False, 'N': False})
    
    # 7. Do_Not_Contact: Normalize Yes/No and Y/N
    if 'Do_Not_Contact' in df.columns:
        df['Do_Not_Contact'] = df['Do_Not_Contact'].replace({'Yes': True, 'Y': True, 'No': False, 'N': False})
    
    # 8. Not_Useful_Column: Drop the column
    if 'Not_Useful_Column' in df.columns:
        df = df.drop(columns=['Not_Useful_Column'])
        
    # Save the cleaned dataset
    df['Phone_Number'] = df['Phone_Number'].astype('string')
    df.to_csv(output_path, index=False)
    print(f"Data cleaning complete. Saved to {output_path}")

if __name__ == "__main__":
    input_file = "data/Customer_Call_List.xlsx"
    output_file = "data/Cleaned_Customer_Call_List.csv"
    
    apply_fixes(input_file, output_file)