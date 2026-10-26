import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. Đọc dữ liệu đã làm sạch
data_path = r"D:\Dabeo\work\data-analytic\data\cleaned_tiki_data_final.csv"
output_img_dir = r"D:\Dabeo\work\data-analytic\images"
os.makedirs(output_img_dir, exist_ok=True)

df = pd.read_csv(data_path)
print(f"📊 Bắt đầu huấn luyện mô hình trên {len(df)} dòng dữ liệu...")

# 2. Phân chia biến đầu vào (Features) và Biến mục tiêu (Target)
target_col = "log_quantity_sold"

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
y = df[target_col]
y_raw = df["quantity_sold"]  # Dùng để đo đạc sai số trên số sản phẩm thực tế

# 3. Phân chia 80% Train - 20% Test (Tránh rò rỉ dữ liệu)
X_train, X_test, y_train, y_test, y_train_raw, y_test_raw = train_test_split(
    X, y, y_raw, test_size=0.2, random_state=42
)
print(f"-> Tập Train: {X_train.shape[0]} dòng | Tập Test: {X_test.shape[0]} dòng")

# 4. Tiền xử lý (Fit trên Train, Transform sang Test)
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_train_cat = ohe.fit_transform(X_train[categorical_features])
X_test_cat = ohe.transform(X_test[categorical_features])
cat_feature_names = ohe.get_feature_names_out(categorical_features).tolist()

scaler = StandardScaler()
X_train_num = scaler.fit_transform(X_train[numeric_features])
X_test_num = scaler.transform(X_test[numeric_features])

X_train_proc = np.hstack([X_train_num, X_train_cat])
X_test_proc = np.hstack([X_test_num, X_test_cat])
all_feature_names = numeric_features + cat_feature_names

# 5. Hàm đánh giá chỉ số
results = []


def evaluate_model(name, y_true_log, y_pred_log, y_true_raw):
    # Nghịch đảo thang log về sản phẩm gốc: expm1(y) = exp(y) - 1
    y_pred_raw = np.clip(np.expm1(y_pred_log), 0, None)

    r2 = r2_score(y_true_log, y_pred_log)
    rmse_raw = np.sqrt(mean_squared_error(y_true_raw, y_pred_raw))
    mae_raw = mean_absolute_error(y_true_raw, y_pred_raw)

    results.append(
        {
            "Mô hình": name,
            "R2 (Log Scale)": round(r2, 4),
            "MAE (Sản phẩm)": round(mae_raw, 2),
            "RMSE (Sản phẩm)": round(rmse_raw, 2),
        }
    )
    return y_pred_raw


# ==========================================
# 6. HUẤN LUYỆN MÔ HÌNH
# ==========================================

# Mô hình 1: Baseline (Median)
print("\n[1/3] Đang chạy mô hình Baseline (Median)...")
baseline_model = DummyRegressor(strategy="median")
baseline_model.fit(X_train_proc, y_train)
y_pred_base = baseline_model.predict(X_test_proc)
evaluate_model("Baseline (Median)", y_test, y_pred_base, y_test_raw)

# Mô hình 2: Hồi quy Ridge (Linear Regression chuẩn hóa)
print("[2/3] Đang chạy mô hình Ridge Regression...")
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train_proc, y_train)
y_pred_ridge = ridge_model.predict(X_test_proc)
evaluate_model("Ridge Regression", y_test, y_pred_ridge, y_test_raw)

# Mô hình 3: Random Forest Regressor
print("[3/3] Đang chạy Random Forest Regressor (n_estimators=100)...")
rf_model = RandomForestRegressor(
    n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
)
rf_model.fit(X_train_proc, y_train)
y_pred_rf = rf_model.predict(X_test_proc)
y_pred_rf_raw = evaluate_model(
    "Random Forest Regressor", y_test, y_pred_rf, y_test_raw
)

# In bảng so sánh kết quả
results_df = pd.DataFrame(results)
print("\n" + "=" * 65)
print("🏆 BẢNG KẾT QUẢ ĐÁNH GIÁ CÁC MÔ HÌNH")
print("=" * 65)
print(results_df.to_string(index=False))

# Lưu bảng kết quả ra file csv nộp kèm
results_df.to_csv(
    r"D:\Dabeo\work\data-analytic\data\model_results_comparison.csv",
    index=False,
    encoding="utf-8-sig",
)

# ==========================================
# 7. TRÍCH XUẤT ĐỘ QUAN TRỌNG CỦA ĐẶC TRƯNG (FEATURE IMPORTANCE)
# ==========================================
importances = rf_model.feature_importances_
feat_importances = pd.Series(importances, index=all_feature_names).sort_values(
    ascending=True
)

plt.figure(figsize=(10, 7))
feat_importances.tail(12).plot(kind="barh", color="teal")
plt.title(
    "Top 12 Đặc Trưng Có Ảnh Hưởng Mạnh Nhất Đến Lượng Bán (Random Forest)",
    fontsize=12,
    fontweight="bold",
)
plt.xlabel("Mức độ quan trọng (Importance Score)")
plt.tight_layout()
fig_imp_path = os.path.join(output_img_dir, "05_feature_importance.png")
plt.savefig(fig_imp_path, dpi=300)
plt.close()
print(f"\n-> Đã lưu biểu đồ: 05_feature_importance.png")

# ==========================================
# 8. PHÂN TÍCH LỖI (RESIDUAL & ERROR ANALYSIS)
# ==========================================
residuals = y_test_raw - y_pred_rf_raw
error_df = pd.DataFrame(
    {
        "y_actual": y_test_raw,
        "y_pred": y_pred_rf_raw,
        "residual": residuals,
        "abs_error": np.abs(residuals),
    }
)

plt.figure(figsize=(9, 5))
plt.scatter(
    y_pred_rf_raw,
    residuals,
    alpha=0.3,
    color="darkorange",
    edgecolors="none",
    s=25,
)
plt.axhline(0, color="navy", linestyle="--", linewidth=1.5)
plt.title(
    "Biểu Đồ Phân Tích Phần Dư (Residuals vs Predicted Values)",
    fontsize=12,
    fontweight="bold",
)
plt.xlabel("Lượng bán dự báo (Predicted Quantity)")
plt.ylabel("Phần dư sai số (Actual - Predicted)")
plt.tight_layout()
fig_res_path = os.path.join(output_img_dir, "06_residual_analysis.png")
plt.savefig(fig_res_path, dpi=300)
plt.close()
print(f"-> Đã lưu biểu đồ: 06_residual_analysis.png")

# Top 5 trường hợp mô hình đoán lệch nhiều nhất để phân tích nguyên nhân
print("\n--- TOP 5 SẢN PHẨM CÓ SAI SỐ LỚN NHẤT (ĐỂ PHÂN TÍCH LỖI TRONG BÁO CÁO) ---")
worst_cases_idx = error_df.sort_values(by="abs_error", ascending=False).head(5).index
worst_cases = df.loc[
    worst_cases_idx,
    ["name", "category_clean", "price", "discount_rate", "quantity_sold"],
]
worst_cases["predicted_sold"] = (
    error_df.loc[worst_cases_idx, "y_pred"].round(1).values
)
worst_cases["error"] = error_df.loc[worst_cases_idx, "abs_error"].round(1).values
print(worst_cases.to_string(index=False))

print("\n" + "=" * 65)
print("🎉 ĐÃ HOÀN TẤT TOÀN BỘ PHẦN MÔ HÌNH HÓA VÀ THỰC NGHIỆM!")
print("=" * 65)