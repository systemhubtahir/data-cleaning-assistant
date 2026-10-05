# Step 1: Profile the messy dataset yourself, before involving AI.
# Load your CSV, run df.info(), df.isnull().sum(), inspect a few bad rows.
# Write this yourself.
import pandas as pd
import json

# Load the raw dataset
df = pd.read_excel("data/Customer_Call_List.xlsx")

print("=== Shape ===")
print(df.shape)

print("\n=== Column dtypes ===")
print(df.dtypes)

print("\n=== Missing values per column ===")
print(df.isnull().sum())

print("\n=== Sample of rows with any missing value ===")
print(df[df.isnull().any(axis=1)].to_string())

print("\n=== Unique values in Paying Customer ===")
print(df["Paying Customer"].unique())

print("\n=== Unique values in Do_Not_Contact ===")
print(df["Do_Not_Contact"].unique())

print("\n=== Duplicate rows (excluding CustomerID) ===")
dupes = df.drop(columns=["CustomerID"]).duplicated(keep=False)
print(df[dupes].to_string())

# Build a structured profile to hand to the AI in the next step.
# We send this summary -- not the raw dataframe -- to keep the prompt small
# and avoid sending unnecessary personal data to the API.
profile = {
    "shape": list(df.shape),
    "dtypes": df.dtypes.astype(str).to_dict(),
    "missing_values": df.isnull().sum().to_dict(),
    "unique_values_sample": {
        "Paying Customer": df["Paying Customer"].astype(str).unique().tolist(),
        "Do_Not_Contact": df["Do_Not_Contact"].astype(str).unique().tolist(),
    },
    "sample_bad_rows": df[df.isnull().any(axis=1)].head(5).to_dict(orient="records"),
}

with open("reports/profile.json", "w") as f:
    json.dump(profile, f, indent=2, default=str)

print("\nProfile saved to reports/profile.json")