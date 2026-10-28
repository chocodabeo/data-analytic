### 1. Chủ đề & Câu hỏi phân tích
	Tên đề tài: Phân tích Thực trạng Kinh doanh và Định lượng các Yếu tố Ảnh hưởng đến Lượng Tiêu thụ Ngành hàng Thời trang & Phụ kiện trên Sàn Thương mại Điện tử Tiki tại Việt Nam.
	Bối cảnh: Ngành hàng thời trang và phụ kiện (balo, túi xách, giày dép nam/nữ) trên sàn TMĐT Tiki có độ cạnh tranh cao và chu kỳ đổi mới sản phẩm nhanh. Các nhà bán hàng cần hiểu rõ mối liên kết giữa chiến lược định giá, tỷ lệ chiết khấu, uy tín thương hiệu (Tiki Trading, Official Store) và mức độ tương tác của khách hàng để tối ưu hóa sản lượng tiêu thụ mà không bào mòn biên lợi nhuận. 
	Người dùng kết quả: Các thương hiệu thời trang, nhà bán lẻ vừa và nhỏ (SMEs), và đội ngũ vận hành gian hàng trên sàn TMĐT Tiki.
	3–5 câu hỏi phân tích cụ thể:
	Thực trạng phân bố: Mức giá bán (price), tỷ lệ chiết khấu (discount_rate) và lượng tiêu thụ (quantity_sold) phân bố như thế nào giữa các phân khúc ngành hàng thời trang (giày dép, túi xách, phụ kiện)? 
	Mối liên kết giá & chiết khấu: Tỷ lệ giảm giá (%) có tương quan ra sao với lượng bán; có tồn tại "ngưỡng bão hòa" (điểm uốn mà việc tăng chiết khấu không còn làm tăng lượng bán tương xứng) hay không?
	Tác động của uy tín gian hàng: Điểm đánh giá trung bình (rating_average), số lượng nhận xét (review_count) và các huy hiệu chính hãng (badges / Tiki Trading) có mối liên hệ như thế nào đến sản lượng bán ra?
	Định lượng mô hình: Khi tổng hợp các yếu tố (giá bán, chiết khấu, phân loại danh mục, uy tín shop), đâu là các đặc trưng có hệ số liên kết mạnh nhất đến sự biến thiên của lượng hàng tiêu thụ?
	Điểm khác biệt: Tập trung khai thác sâu dữ liệu thị trường nội địa Việt Nam (Tiki) trên danh mục thời trang đa dạng, phân tích định lượng chi tiết điểm uốn chiết khấu thay vì chỉ thống kê mô tả cơ bản.
### 2. Dữ liệu nghiên cứu
	Nguồn/URL: Bộ dữ liệu “TIKI E-Commerce - Fashion Products Dataset” công khai trên nền tảng Kaggle (tác giả Michael Minh Pham).
	Đơn vị quan sát (1 dòng): Một sản phẩm thời trang/phụ kiện duy nhất được niêm yết bán trên sàn Tiki tại thời điểm thu thập dữ liệu.
	Quy mô: Khoảng 30.000 – 40.000 dòng bản ghi (gồm 6 danh mục sản phẩm thời trang gộp lại: backpack, fashion_accessories, men_bag, men_shoes, women_bag, women_shoes). 
	Biến mục tiêu (Target): quantity_sold (lượng sản phẩm đã bán) – biến số liên tục cho bài toán Hồi quy (Regression). 
	Các biến đặc trưng (Features):
	Định giá & Khuyến mãi: price (giá bán hiện tại), original_price (giá niêm yết), discount_rate / discount (tỷ lệ & số tiền giảm).
	Danh tiếng & Đánh giá: rating_average (điểm sao trung bình 1–5), review_count (số lượt đánh giá).
	Phân loại & Thương hiệu: category (danh mục: giày dép, túi, phụ kiện), brand_name (thương hiệu), badges / is_tiki_trading (cờ shop chính hãng / gian hàng Tiki). 
	Vấn đề missing/trùng/outlier:
	Missing: Cột giảm giá rỗng đối với sản phẩm bán nguyên giá; sản phẩm mới chưa có lượt review/rating.
	Trùng lặp: Trùng ID sản phẩm xuất hiện ở nhiều danh mục con.
	Outlier: Sản phẩm có lượng bán bằng 0 hoặc các sản phẩm cao cấp có giá đột biến.
	Rủi ro truy cập & Phương án dự phòng: Tệp dữ liệu đã tải đầy đủ về máy cá nhân và lưu trữ trên GitHub/Google Drive của nhóm. Dự phòng: Nếu dữ liệu khuyết quá nhiều trường, nhóm dùng bộ dữ liệu phụ Shopee E-commerce trên Kaggle.
### 3. Kế hoạch công việc (Quy trình chi tiết)
	Thu thập & Hợp nhất dữ liệu: Gộp 6 file CSV danh mục thành 1 bảng dữ liệu lớn duy nhất, thêm cột category nhận diện phân loại. 
	Data Cleaning: Loại bỏ bản ghi trùng lặp (drop_duplicates), xử lý giá trị khuyết thiếu (imputation bằng median cho biến số liên tục), lọc ngoại lai bằng IQR.
	EDA (Khám phá dữ liệu): Trực quan hóa phân phối giá, tỷ lệ chiết khấu và lượng bán theo từng danh mục; vẽ Heatmap ma trận tương quan; phân tích điểm uốn chiết khấu qua Scatter plot.
	Feature Engineering:
	Tính số tiền giảm tuyệt đối: discount_amount = original_price - price.
	Tạo biến nhị phân: has_discount (có giảm giá hay không), is_official (shop chính hãng).
	Chuẩn hóa biến mục tiêu bằng phép biến đổi log⁡(quantity_sold+1) do phân phối bị lệch phải nặng.
	Data Split: Phân tách 80% tập Train và 20% tập Test, cố định random_state=42. 
	Mô hình hóa: Huấn luyện mô hình cơ sở (Baseline) → Huấn luyện các mô hình chính (Linear Regression / Ridge, Random Forest Regressor). 
	Đánh giá & Rút ra insight: Tính toán MAE, RMSE, R^2; biến đổi ngược lại scale gốc để diễn giải sai số; trích xuất Feature Importance để đưa ra khuyến nghị thực tế. 
	Đóng gói sản phẩm: Hoàn thiện source code, slide, báo cáo PDF và ứng dụng Streamlit dự báo lượng bán. 
### 4. Kỹ thuật áp dụng
	Preprocessing & Encoding: Điền trung vị cho biến số; One-Hot Encoding cho category; RobustScaler / StandardScaler cho các biến số trước khi đưa vào mô hình tuyến tính.
	Thuật toán:
	Multiple Linear Regression / Ridge: Giữ tính minh bạch, diễn giải rõ ràng hệ số góc từng thuộc tính. 
	Random Forest Regressor: Bắt trọn các tương tác phi tuyến phức tạp giữa giá bán, chiết khấu và lượng tiêu thụ. 
	Phòng chống Data Leakage: Tách Train/Test độc lập trước; toàn bộ bước fit scaler/encoder chỉ chạy trên Train rồi transform sang Test. Không dùng các biến phát sinh sau bán hàng làm feature.
### 5. Thực nghiệm & Đánh giá
	Baseline: Median/Mean của quantity_sold trên tập huấn luyện. 
	Mô hình chính: Multiple Linear Regression và Random Forest Regressor. 
	Kỹ thuật kiểm thử: 80% Train – 20% Test, kết hợp 5-Fold Cross Validation trên tập Train. 
	Metrics: MAE, RMSE (đánh giá trên đơn vị sản phẩm sau khi inverse log) và R^2 (đo lường tỷ lệ giải thích phương sai). 
	Phân tích lỗi (Error Analysis): Phân tích nhóm sản phẩm có độ lệch phần dư (Residual) cao nhất để giải thích nguyên nhân dự báo lệch.
### 6. Sản phẩm bàn giao
	raw_data/ (6 file CSV gốc) và cleaned_tiki_data.csv. 
	Notebooks: 01_Data_Cleaning.ipynb, 02_EDA.ipynb, 03_Modeling.ipynb. 
	Thư mục images/ chứa toàn bộ biểu đồ xuất chất lượng cao (.png). 
	Ứng dụng Streamlit demo tương tác cho phép chọn danh mục, mức giá, chiết khấu để ước tính sản lượng bán. 

