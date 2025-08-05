
import pandas as pd
import numpy as np

# Load Excel file
excel_file = "energygoodsandservices2023100425.xlsx"  # <-- Place the downloaded ONS Excel file in the same directory
sheet_name = "A10 Constrained Values 2023"

# Load and clean data
df_raw = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2)
df_raw.rename(columns={df_raw.columns[0]: 'Product Group'}, inplace=True)
df_clean = df_raw[df_raw['Product Group'].notna()].copy()

# Reshape to long format
df_melted = df_clean.melt(id_vars=['Product Group'], var_name='Industry', value_name='Annual Spend (£000s)')
df_melted = df_melted[pd.to_numeric(df_melted['Annual Spend (£000s)'], errors='coerce').notnull()]
df_melted['Annual Spend (£000s)'] = df_melted['Annual Spend (£000s)'].astype(float)

# Function to distribute annual spend across 12 months
def distribute_monthly(amount):
    weights = np.random.dirichlet(np.ones(12), size=1)[0]
    return (weights * amount).round(2)

# Create monthly dataset
monthly_records = []
for _, row in df_melted.iterrows():
    monthly_values = distribute_monthly(row['Annual Spend (£000s)'])
    for month_idx, value in enumerate(monthly_values, start=1):
        monthly_records.append({
            'Product Group': row['Product Group'],
            'Industry': row['Industry'],
            'Month': f'2023-{month_idx:02d}',
            'Monthly Spend (£000s)': value
        })

df_monthly = pd.DataFrame(monthly_records)

# Export to CSV
df_monthly.to_csv("simulated_monthly_spend_data.csv", index=False)
print("✅ Monthly spend data generated and saved as 'simulated_monthly_spend_data.csv'")
