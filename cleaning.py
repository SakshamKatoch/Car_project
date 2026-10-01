# DATA CLEANING
import pandas as pd

# load dataset
df = pd.read_csv("cars.csv")

# remove missing values
df = df.dropna()

# remove duplicates
df = df.drop_duplicates()

# rename columns (based on your dataset)
df.columns = ['brand', 'model', 'year', 'age', 'km_driven', 'transmission', 'owner', 'fuel', 'posted_date', 'additional_info', 'price']

# -------------------------------
# CLEAN NUMERIC COLUMNS PROPERLY
# -------------------------------

# clean km_driven (remove text like "kms", commas)
df['km_driven'] = df['km_driven'].astype(str)
df['km_driven'] = df['km_driven'].str.replace(',', '')
df['km_driven'] = df['km_driven'].str.extract('(\d+)')
df['km_driven'] = pd.to_numeric(df['km_driven'], errors='coerce')

# clean price (remove ₹, commas)
df['price'] = df['price'].astype(str)
df['price'] = df['price'].str.replace(',', '')
df['price'] = df['price'].str.replace('₹', '')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# remove rows where conversion failed
df = df.dropna(subset=['km_driven', 'price'])

# fix other numeric columns
df['year'] = df['year'].astype(int)
df['age'] = df['age'].astype(int)

# remove unnecessary columns
df = df.drop(['posted_date', 'additional_info'], axis=1)

# save cleaned dataset
df.to_csv("cleaned_cars.csv", index=False)

# final check
print("✅ Cleaned dataset saved")
print("Rows:", len(df))
print(df.head())