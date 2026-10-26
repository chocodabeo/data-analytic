import pandas as pd
import numpy as np

# 1. Đọc dữ liệu
file_path = r"D:\Dabeo\work\data-analytic\data\cleaned_tiki_data.csv"
df = pd.read_csv(file_path)

print("--- KIỂM TRA TRẠNG THÁI HIỆN TẠI ---")
print(f"Tổng số dòng: {len(df)}")
zero_ratings = (df["rating_average"] == 0).sum()
zero_sold = (df["quantity_sold"] == 0).sum()
print(f"Số sản phẩm có rating = 0 (chưa có đánh giá): {zero_ratings} ({zero_ratings/len(df)*100:.2f}%)")
print(f"Số sản phẩm có quantity_sold = 0 (chưa bán được đơn nào): {zero_sold} ({zero_sold/len(df)*100:.2f}%)")

# 2. Xử lý Missing ẩn của rating_average:
# Tạo cờ đánh dấu sản phẩm chưa có người đánh giá
df["has_no_review"] = ((df["review_count"] == 0) | (df["rating_average"] == 0)).astype(int)

# Tính trung vị rating của các sản phẩm ĐÃ CÓ đánh giá (> 0)
median_rating = df[df["rating_average"] > 0]["rating_average"].median()
print(f"\n-> Điểm rating trung vị của các sản phẩm đã có đánh giá: {median_rating}")

# Imputation: Thay các giá trị 0.0 bằng median_rating
df["rating_imputed"] = df["rating_average"].replace(0.0, median_rating)

# 3. Xuất file cleaned_tiki_data_v2.csv đã xử lý toàn diện
output_path = r"D:\Dabeo\work\data-analytic\data\cleaned_tiki_data_final.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n" + "="*50)
print(f"✅ ĐÃ HOÀN TẤT BƯỚC DATA CLEANING TOÀN DIỆN!")
print(f"File sạch cuối cùng: {output_path}")
print("="*50)