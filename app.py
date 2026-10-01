import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# -----------------------
# PAGE CONFIG + STYLE
# -----------------------
st.set_page_config(page_title="Car Price Predictor", layout="centered")

st.markdown("""
<style>
.main {background-color: #f5f7fa;}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-size: 16px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("cleaned_cars.csv")

# -----------------------
# DATA IMPROVEMENT
# -----------------------

# remove outliers
df = df[(df['price'] > df['price'].quantile(0.05)) & 
        (df['price'] < df['price'].quantile(0.95))]

df = df[df['km_driven'] < df['km_driven'].quantile(0.99)]

# add age feature
df['age'] = 2025 - df['year']

# -----------------------
# CREATE MAPPINGS
# -----------------------
brand_cat = df['brand'].astype('category')
df['brand_encoded'] = brand_cat.cat.codes
brand_mapping = dict(enumerate(brand_cat.cat.categories))

model_cat = df['model'].astype('category')
df['model_encoded'] = model_cat.cat.codes
model_mapping = dict(enumerate(model_cat.cat.categories))

fuel_cat = df['fuel'].astype('category')
df['fuel_encoded'] = fuel_cat.cat.codes
fuel_mapping = dict(enumerate(fuel_cat.cat.categories))

trans_cat = df['transmission'].astype('category')
df['trans_encoded'] = trans_cat.cat.codes
trans_mapping = dict(enumerate(trans_cat.cat.categories))

# -----------------------
# MODEL (IMPROVED)
# -----------------------
X = df[['age', 'km_driven', 'fuel_encoded', 'trans_encoded', 'brand_encoded', 'model_encoded']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

# -----------------------
# UI
# -----------------------
st.markdown("<h1 style='text-align: center;'>🚗 Car Price Prediction System</h1>", unsafe_allow_html=True)
st.markdown(f"### 🔍 Model Accuracy: {round(accuracy, 2)}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Year", 2000, 2025)
    fuel_name = st.selectbox("Fuel Type", list(fuel_mapping.values()))

with col2:
    km = st.number_input("KM Driven", 0, 200000)
    trans_name = st.selectbox("Transmission", list(trans_mapping.values()))

brand_name = st.selectbox("Brand", list(brand_mapping.values()))
model_name = st.selectbox("Car Model", list(model_mapping.values()))

# convert
fuel_code = list(fuel_mapping.keys())[list(fuel_mapping.values()).index(fuel_name)]
trans_code = list(trans_mapping.keys())[list(trans_mapping.values()).index(trans_name)]
brand_code = list(brand_mapping.keys())[list(brand_mapping.values()).index(brand_name)]
model_code = list(model_mapping.keys())[list(model_mapping.values()).index(model_name)]

# -----------------------
# PREDICTION
# -----------------------
if st.button("Predict Price"):
    age = 2025 - year

    input_df = pd.DataFrame([[age, km, fuel_code, trans_code, brand_code, model_code]],
                            columns=['age', 'km_driven', 'fuel_encoded', 'trans_encoded', 'brand_encoded', 'model_encoded'])

    pred = model.predict(input_df)

    st.markdown("### 💰 Estimated Price")
    st.success(f"₹ {int(pred[0]):,}")

    # category
    st.subheader("💡 Price Category")
    price = int(pred[0])
    if price < 300000:
        st.info("Budget Car 💰")
    elif price < 800000:
        st.info("Mid Range Car 🚗")
    else:
        st.info("Premium Car 🚀")

    # similar cars
    st.subheader("🔍 Similar Cars")

    filtered = df[
        (df['brand_encoded'] == brand_code) &
        (df['model_encoded'] == model_code)
    ]

    top5 = filtered[['brand', 'model', 'year', 'km_driven', 'price']] \
        .sort_values(by='price') \
        .head(5)

    st.dataframe(top5)