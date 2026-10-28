# 🛒 Phân Tích Thực Trạng Kinh Doanh & Định Lượng Lượng Tiêu Thụ Ngành Thời Trang - Tiki

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Completed-success)](#)

> **Tên đề tài:** Phân tích thực trạng kinh doanh và định lượng các yếu tố ảnh hưởng đến lượng tiêu thụ ngành hàng Thời trang & Phụ kiện trên sàn Thương mại Điện tử Tiki tại Việt Nam.

---

## 📌 1. Bối cảnh & Mục tiêu Nghiên cứu

### 1.1. Bối cảnh thị trường
Ngành hàng **Thời trang & Phụ kiện** (balo, túi xách, giày dép nam/nữ) trên sàn TMĐT Tiki có độ cạnh tranh gay gắt cùng chu kỳ đổi mới mẫu mã rất nhanh. Các nhà bán hàng cần nắm bắt chính xác tương quan giữa chiến lược định giá, mức chiết khấu, uy tín thương hiệu (*Tiki Trading*, *Official Store*) và tương tác khách hàng để tối ưu sản lượng bán mà không bào mòn biên lợi nhuận.

* **Đối tượng thụ hưởng:** Thương hiệu thời trang, doanh nghiệp bán lẻ vừa và nhỏ (SMEs), và đội ngũ vận hành gian hàng TMĐT trên Tiki.
* **Điểm khác biệt:** Khai thác sâu dữ liệu thị trường nội địa Việt Nam, đi sâu vào bài toán định lượng và xác định **điểm uốn chiết khấu** thay vì chỉ dừng lại ở thống kê mô tả.

### 1.2. Câu hỏi phân tích trọng tâm
1. **Phân bố thực trạng:** Mức giá (`price`), tỷ lệ chiết khấu (`discount_rate`) và lượng tiêu thụ (`quantity_sold`) phân bố như thế nào giữa các phân khúc danh mục?
2. **Mối liên hệ giá & khuyến mãi:** Tỷ lệ giảm giá có quan hệ ra sao với sản lượng bán? Liệu có tồn tại *"ngưỡng bão hòa"* (điểm uốn mà việc tăng chiết khấu không còn đem lại hiệu quả tăng doanh số tương ứng)?
3. **Giá trị uy tín gian hàng:** Điểm đánh giá (`rating_average`), số lượt nhận xét (`review_count`) và huy hiệu chính hãng (`is_tiki_trading`, `badges`) tác động đến sức mua thế nào?
4. **Mô hình định lượng:** Khi tổng hợp tất cả các thuộc tính, đâu là những đặc trưng có ảnh hưởng mạnh nhất đến biến thiên của sản lượng tiêu thụ?

---

## 📊 2. Dữ liệu Nghiên cứu

* **Nguồn dữ liệu:** [TIKI E-Commerce - Fashion Products Dataset](https://www.kaggle.com/) trên Kaggle (Tác giả: *Michael Minh Pham*).
* **Đơn vị quan sát (1 dòng):** Một sản phẩm thời trang/phụ kiện duy nhất được niêm yết bán trên Tiki tại thời điểm thu thập.
* **Quy mô:** ~30.000 – 40.000 bản ghi (gộp từ 6 danh mục: `backpack`, `fashion_accessories`, `men_bag`, `men_shoes`, `women_bag`, `women_shoes`).
* **Biến mục tiêu (Target):** `quantity_sold` (Biến số liên tục – Bài toán **Regression**).

### Danh mục biến đặc trưng (Features)

| Nhóm đặc trưng | Biến số | Diễn giải |
| :--- | :--- | :--- |
| **Định giá & Khuyến mãi** | `price`, `original_price` | Giá bán hiện tại và giá niêm yết gốc |
| | `discount`, `discount_rate` | Số tiền giảm tuyệt đối và tỷ lệ % chiết khấu |
| **Đánh giá & Tương tác** | `rating_average` | Điểm đánh giá trung bình của sản phẩm (thang 1–5 ⭐) |
| | `review_count` | Tổng số lượt nhận xét/đánh giá thực tế |
| **Phân loại & Thương hiệu** | `category` | Danh mục sản phẩm (giày, túi, balo, phụ kiện,...) |
| | `brand_name` | Tên nhãn hàng niêm yết |
| | `is_tiki_trading`, `badges` | Gian hàng chính hãng/Tiki Trading vận hành |

### Thách thức & Xử lý dữ liệu
* **Missing values:** Khuyết tỷ lệ chiết khấu ở sản phẩm bán nguyên giá; sản phẩm mới chưa phát sinh đánh giá (`rating_average`, `review_count`).
* **Trùng lặp (Duplicates):** Trùng `product_id` do xuất hiện chéo ở nhiều danh mục con.
* **Ngoại lai (Outliers):** Sản phẩm có lượng bán bằng 0 hoặc các mặt hàng cao cấp có giá niêm yết đột biến.
* **Phương án dự phòng:** Dữ liệu đã được sao lưu toàn bộ trên GitHub/Google Drive cá nhân. Dự phòng nguồn phụ: *Shopee E-commerce Dataset* trên Kaggle nếu tỷ lệ thiếu thông tin vượt ngưỡng cho phép.

---

## 🛠️ 3. Quy trình Triển khai (Pipeline)

1. **Thu thập & Hợp nhất:** Gộp 6 tệp CSV danh mục vào một DataFrame thống nhất và gắn thẻ `category`.
2. **Làm sạch (Data Cleaning):** Khử trùng lặp (`drop_duplicates`), điền khuyết giá trị liên tục bằng Median, xử lý ngoại lai thông qua IQR.
3. **Khám phá dữ liệu (EDA):** Trực quan hóa tương quan giá – chiết khấu – lượt mua; xác định điểm bão hòa khuyến mãi qua Scatter Plot.
4. **Kỹ thuật trích xuất đặc trưng (Feature Engineering):**
   * Tính số tiền giảm: `discount_amount` = `original_price` - `price`
   * Nhị phân hóa: `has_discount` (0 hoặc 1), `is_official` (0 hoặc 1)
   * Chuẩn hóa lệch phải biến mục tiêu: áp dụng biến đổi `log(y + 1)` cho `quantity_sold`
5. **Chia tập dữ liệu:** Tách độc lập 80% Train và 20% Test (cố định `random_state=42`).
6. **Mô hình hóa & Đánh giá:** Huấn luyện mô hình cơ sở ➔ Ridge Regression ➔ Random Forest; phân tích Feature Importance và sai số phần dư (Residual Error).
7. **Đóng gói sản phẩm:** Xây dựng dashboard tương tác dự báo trên nền tảng **Streamlit**.

---

## 🧠 4. Kỹ thuật & Thuật toán Áp dụng

* **Tiền xử lý & Encoding:**
  * Median Imputation cho biến định lượng.
  * One-Hot Encoding cho biến phân loại (`category`).
  * `RobustScaler` / `StandardScaler` chuẩn hóa dữ liệu cho mô hình tuyến tính.
* **Mô hình dự báo:**
  * **Multiple Linear Regression / Ridge:** Đảm bảo tính minh bạch, diễn giải rõ ràng trọng số từng thuộc tính.
  * **Random Forest Regressor:** Bắt trọn mối quan hệ phi tuyến tính phức tạp giữa giá bán, chiết khấu và hành vi tiêu dùng.
* **Phòng chống Data Leakage:** Tách tập Train/Test nghiêm ngặt từ đầu; toàn bộ bước `fit` của Scaler và Encoder chỉ thực thi trên tập Train rồi `transform` sang Test. Tuyệt đối không dùng các biến hậu bán hàng làm đầu vào dự báo.

---

## 📈 5. Thực nghiệm & Tiêu chí Đánh giá

* **Mô hình so sánh:**
  * **Baseline Model:** Dự báo bằng Mean/Median của `quantity_sold` trên tập huấn luyện.
  * **Candidate Models:** Multiple Linear Regression / Ridge, Random Forest Regressor.
* **Phương pháp kiểm thử:** Phân tách Train/Test 80/20 kết hợp **5-Fold Cross Validation** trên tập Train.
* **Thước đo đánh giá (Metrics):**
  * **MAE (Mean Absolute Error):** Sai số tuyệt đối trung bình (được nghịch đảo về đơn vị sản phẩm gốc sau phép biến đổi log).
  * **RMSE (Root Mean Squared Error):** Phạt nặng các điểm sai số lớn.
  * **$R^2$ (R-Squared):** Tỷ lệ giải thích biến thiên của sản lượng bán ra.
* **Phân tích sai số (Error Analysis):** Lọc nhóm sản phẩm có độ lệch phần dư (Residuals) lớn nhất để nhận diện các yếu tố nhiễu ngoài mô hình (ví dụ: hiệu ứng viral, thương hiệu cao cấp cá biệt).

---

## 📁 6. Cấu trúc Thư mục Dự án

```text
├── data/
│   ├── raw/                 # 6 tệp CSV dữ liệu gốc tải từ Kaggle
│   └── cleaned_tiki_data.csv# Dữ liệu sạch sau tiền xử lý
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb # Quy trình làm sạch, gộp file & xử lý khuyết
│   ├── 02_EDA.ipynb           # Trực quan hóa phân phối & phân tích tương quan
│   └── 03_Modeling.ipynb      # Huấn luyện mô hình, tinh chỉnh & đánh giá
├── images/                  # Biểu đồ và hình ảnh trực quan hóa xuất ra (.png)
├── app/
│   └── streamlit_app.py     # Ứng dụng demo dự báo sản lượng bán
├── requirements.txt         # Danh sách thư viện phụ thuộc
└── README.md                # Tài liệu hướng dẫn dự án
