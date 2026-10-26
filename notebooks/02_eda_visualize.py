import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Thiết lập giao diện biểu đồ
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

# 1. Tạo thư mục lưu hình ảnh báo cáo nếu chưa có
output_img_dir = r"D:\Dabeo\work\data-analytic\images"
os.makedirs(output_img_dir, exist_ok=True)

# 2. Đọc dữ liệu sạch
data_path = r"D:\Dabeo\work\data-analytic\data\cleaned_tiki_data_final.csv"
df = pd.read_csv(data_path)

print(f"📊 Đang tiến hành EDA trên {len(df)} dòng dữ liệu...")

# ==========================================
# BIỂU ĐỒ 1: PHÂN BỐ GIÁ BÁN & LƯỢNG BÁN THEO DANH MỤC
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Boxplot giá bán theo danh mục
sns.boxplot(
    data=df,
    x="category_clean",
    y="price",
    ax=axes[0],
    palette="Set2",
    showfliers=False,
)
axes[0].set_title(
    "Phân Bố Giá Bán Theo Danh Mục (Đã ẩn ngoại lai cực trị)",
    fontsize=13,
    fontweight="bold",
)
axes[0].set_xlabel("Danh mục", fontsize=11)
axes[0].set_ylabel("Giá bán (VNĐ)", fontsize=11)
axes[0].tick_params(axis="x", rotation=30)

# Barplot trung bình lượng bán thực tế theo danh mục
sales_by_cat = (
    df.groupby("category_clean")["quantity_sold"]
    .mean()
    .reset_index()
    .sort_values(by="quantity_sold", ascending=False)
)
sns.barplot(
    data=sales_by_cat,
    x="category_clean",
    y="quantity_sold",
    ax=axes[1],
    palette="Blues_r",
)
axes[1].set_title(
    "Lượng Bán Trung Bình Theo Danh Mục", fontsize=13, fontweight="bold"
)
axes[1].set_xlabel("Danh mục", fontsize=11)
axes[1].set_ylabel("Lượng bán trung bình (Sản phẩm)", fontsize=11)
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
fig1_path = os.path.join(output_img_dir, "01_distribution_by_category.png")
plt.savefig(fig1_path, dpi=300)
plt.close()
print(" -> Đã lưu: 01_distribution_by_category.png")

# ==========================================
# BIỂU ĐỒ 2: TỶ LỆ GIẢM GIÁ & ĐIỂM UỐN LƯỢNG TIÊU THỤ
# ==========================================
# Nhóm tỷ lệ giảm giá theo các khoảng 10% để tìm điểm bão hòa
df["discount_bin"] = pd.cut(
    df["discount_rate"],
    bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 100],
    labels=[
        "0-10%",
        "10-20%",
        "20-30%",
        "30-40%",
        "40-50%",
        "50-60%",
        "60-70%",
        "70-80%",
        ">80%",
    ],
    include_lowest=True,
)

discount_perf = (
    df.groupby("discount_bin", observed=False)["quantity_sold"]
    .agg(["mean", "median", "count"])
    .reset_index()
)

plt.figure(figsize=(10, 5))
ax = sns.lineplot(
    data=discount_perf,
    x="discount_bin",
    y="mean",
    marker="o",
    color="crimson",
    linewidth=2.5,
    label="Lượng bán TB",
)
plt.title(
    "Mối Liên Hệ Giữa Tỷ Lệ Giảm Giá và Lượng Bán (Tìm Điểm Uốn)",
    fontsize=13,
    fontweight="bold",
)
plt.xlabel("Khoảng Chiết Khấu (%)", fontsize=11)
plt.ylabel("Lượng bán trung bình", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)

fig2_path = os.path.join(output_img_dir, "02_discount_saturation_curve.png")
plt.savefig(fig2_path, dpi=300)
plt.close()
print(" -> Đã lưu: 02_discount_saturation_curve.png")

# ==========================================
# BIỂU ĐỒ 3: UY TÍN (OEM vs CÓ THƯƠNG HIỆU) & TIỆN ÍCH
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# So sánh OEM vs Brand
oem_sales = (
    df.groupby("is_oem")["quantity_sold"]
    .mean()
    .reset_index()
    .replace({0: "Có Thương Hiệu", 1: "OEM (Không hiệu)"})
)
sns.barplot(
    data=oem_sales, x="is_oem", y="quantity_sold", ax=axes[0], palette="viridis"
)
axes[0].set_title(
    "Sức Mua: Hàng Có Thương Hiệu vs. OEM", fontsize=12, fontweight="bold"
)
axes[0].set_ylabel("Lượng bán trung bình")
axes[0].set_xlabel("")

# Tác động của Video mô tả
video_sales = (
    df.groupby("has_video")["quantity_sold"]
    .mean()
    .reset_index()
    .replace({False: "Không Video", True: "Có Video"})
)
sns.barplot(
    data=video_sales,
    x="has_video",
    y="quantity_sold",
    ax=axes[1],
    palette="magma",
)
axes[1].set_title(
    "Tác Động Của Việc Đăng Kèm Video Đến Lượng Bán",
    fontsize=12,
    fontweight="bold",
)
axes[1].set_ylabel("Lượng bán trung bình")
axes[1].set_xlabel("")

plt.tight_layout()
fig3_path = os.path.join(output_img_dir, "03_reputation_and_features.png")
plt.savefig(fig3_path, dpi=300)
plt.close()
print(" -> Đã lưu: 03_reputation_and_features.png")

# ==========================================
# BIỂU ĐỒ 4: HEATMAP MA TRẬN TƯƠNG QUAN
# ==========================================
corr_cols = [
    "price",
    "discount_rate",
    "discount_amount",
    "rating_imputed",
    "review_count",
    "favourite_count",
    "number_of_images",
    "quantity_sold",
    "log_quantity_sold",
]

corr_matrix = df[corr_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True,
    linewidths=0.5,
)
plt.title(
    "Ma Trận Hệ Số Tương Quan (Pearson Correlation Heatmap)",
    fontsize=13,
    fontweight="bold",
)
plt.tight_layout()

fig4_path = os.path.join(output_img_dir, "04_correlation_heatmap.png")
plt.savefig(fig4_path, dpi=300)
plt.close()
print(" -> Đã lưu: 04_correlation_heatmap.png")

print("\n" + "=" * 55)
print(f"🎉 EDA HOÀN TẤT! Toàn bộ 4 biểu đồ đã được lưu trong thư mục:")
print(f"📁 {output_img_dir}")
print("=" * 55)