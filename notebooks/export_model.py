import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Đọc dữ liệu
data_path = r"D:\Dabeo\work\data-analytic\data\cleaned_tiki_data_final.csv"
df = pd.read_csv(data_path)

numeric_features = [
    "price",
    "original_price",
    "discount_rate",
    "discount_amount",
    "rating_imputed",
    "review_count",
    "favourite_count",
    "number_of_images",
    "has_no_review",
    "has_discount",
    "is_oem",
]
categorical_features = ["category_clean", "fulfillment_type"]

X = df[numeric_features + categorical_features]
y = df["log_quantity_sold"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Fit encoder & scaler
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_train_cat = ohe.fit_transform(X_train[categorical_features])

scaler = StandardScaler()
X_train_num = scaler.fit_transform(X_train[numeric_features])

X_train_proc = np.hstack([X_train_num, X_train_cat])

# Huấn luyện mô hình tối ưu
rf_model = RandomForestRegressor(
    n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
)
rf_model.fit(X_train_proc, y_train)

# Đóng gói đối tượng
artifacts = {
    "model": rf_model,
    "scaler": scaler,
    "ohe": ohe,
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
}

joblib.dump(artifacts, r"D:\Dabeo\work\data-analytic\tiki_sales_model.joblib")
print("✅ Đã xuất mô hình thành công: tiki_sales_model.joblib")