import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tiki Sales Predictor", page_icon="🛍️", layout="wide"
)

# Tải mô hình
@st.cache_resource
def load_artifacts():
    return joblib.load("tiki_sales_model.joblib")

artifacts = load_artifacts()
model = artifacts["model"]
scaler = artifacts["scaler"]
ohe = artifacts["ohe"]

st.title("🛍️ Hệ Thống Dự Báo Lượng Tiêu Thụ Sản Phẩm Tiki")
st.markdown(
    "Mô hình học máy hỗ trợ người bán tối ưu giá, chiết khấu và bài đăng bán hàng."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Thông Tin Sản Phẩm & Định Giá")
    category = st.selectbox(
        "Danh mục ngành hàng",
        [
            "backpacks_suitcases",
            "fashion_accessories",
            "men_bags",
            "men_shoes",
            "women_bags",
            "women_shoes",
        ],
    )
    original_price = st.number_input(
        "Giá niêm yết ban đầu (VNĐ)",
        min_value=10000,
        max_value=10000000,
        value=200000,
        step=10000,
    )
    discount_rate = st.slider(
        "Tỷ lệ giảm giá (%)",
        min_value=0.0,
        max_value=90.0,
        value=15.0,
        step=1.0,
    )
    fulfillment = st.selectbox(
        "Hình thức vận hành", ["dropship", "cross_border", "seller_delivery", "other"]
    )
    is_oem = st.radio(
        "Loại nguồn hàng",
        [0, 1],
        format_func=lambda x: "Hàng có thương hiệu (Brand)"
        if x == 0
        else "Hàng gia công OEM (Không hiệu)",
    )

with col2:
    st.subheader("⭐ Tương Tác & Chất Lượng Bài Đăng")
    rating = st.slider(
        "Điểm đánh giá dự kiến (sao)",
        min_value=1.0,
        max_value=5.0,
        value=4.7,
        step=0.1,
    )
    review_count = st.number_input(
        "Số lượt đánh giá hiện có", min_value=0, max_value=50000, value=20, step=5
    )
    favourite_count = st.number_input(
        "Lượt yêu thích", min_value=0, max_value=20000, value=10, step=5
    )
    num_images = st.slider(
        "Số lượng hình ảnh đăng tải", min_value=1, max_value=20, value=5
    )

# Tính toán các thuộc tính phụ thuộc
price = original_price * (1 - discount_rate / 100)
discount_amount = original_price - price
has_discount = 1 if discount_amount > 0 else 0
has_no_review = 1 if review_count == 0 else 0

st.divider()

if st.button("🚀 BẮT ĐẦU DỰ BÁO DOANH SỐ", use_container_width=True):
    # Chuẩn bị vector đặc trưng
    df_num = pd.DataFrame(
        [
            [
                price,
                original_price,
                discount_rate,
                discount_amount,
                rating,
                review_count,
                favourite_count,
                num_images,
                has_no_review,
                has_discount,
                is_oem,
            ]
        ],
        columns=artifacts["numeric_features"],
    )

    df_cat = pd.DataFrame(
        [[category, fulfillment]], columns=artifacts["categorical_features"]
    )

    # Transform
    X_num = scaler.transform(df_num)
    X_cat = ohe.transform(df_cat)
    X_input = np.hstack([X_num, X_cat])

    # Dự báo
    pred_log = model.predict(X_input)[0]
    pred_quantity = max(0, int(np.expm1(pred_log)))

    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Giá bán thực tế sau giảm", f"{price:,.0f} đ")
    res_col2.metric("Số tiền giảm trực tiếp", f"{discount_amount:,.0f} đ")
    res_col3.metric("LƯỢNG BÁN DỰ KIẾN", f"~ {pred_quantity:,} sản phẩm")