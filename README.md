# BÁO CÁO CUỐI KÌ: HỆ CSDL LƯU TRỮ VÀ TÌM KIẾM TIẾNG NHẠC CỤ THUỘC BỘ GÕ

**Nhóm BTL 15 - Nhóm lớp 04**  
- B21DCCN096 – Phan Gia Nguyên  
- B20DCCN194 – Đặng Anh Đức  
- B21DCCN763 – Vũ Anh Tuấn  

---

## 1. Giới thiệu đề tài

Đề tài của chúng em tập trung xây dựng một hệ cơ sở dữ liệu (CSDL) lưu trữ và tìm kiếm tiếng nhạc cụ thuộc bộ gõ. Mục tiêu là tạo ra bộ dữ liệu âm thanh có ít nhất 100 file và phát triển hệ thống có khả năng:

- Trích xuất các đặc trưng âm thanh phù hợp từ các file nhạc cụ thuộc bộ gõ.
- Phân cụm để nhận diện các nhóm âm thanh khác nhau.
- Tìm kiếm và trả về các file âm thanh tương đồng nhất với file đầu vào.

---

## 2. Các phương pháp sử dụng

- **Xử lý âm thanh:**  
  Chúng em sử dụng kỹ thuật chia khung âm thanh, trích xuất các đặc trưng như tần số, năng lượng, Tốc độ qua điểm 0 (zero-crossing rate), và các đặc trưng phổ khác.

- **Chuẩn hóa dữ liệu:**  
  Đặc trưng sau khi trích xuất được chuẩn hóa bằng phương pháp phân phối chuẩn (z-score). Đặc biệt, chúng em sử dụng giá trị trung vị để tránh ảnh hưởng của các giá trị ngoại lai.

- **Phân cụm:**  
  Áp dụng thuật toán KMeans để phân nhóm các file âm thanh dựa trên đặc trưng đã chuẩn hóa.

- **Tìm kiếm:**  
  Dựa vào khoảng cách giữa các đặc trưng của file âm thanh đầu vào và các cụm đã có, hệ thống trả về 3 file âm thanh tương đồng nhất.

---

## 3. Cấu trúc file chính

- `cum_va_dac_trung.py`: Xử lý phân cụm đặc trưng âm thanh đã trích xuất, tính toán cụm trung tâm và cập nhật nhãn cụm cho các mẫu dữ liệu.
- `kmeans.py`: Cấu hình mô hình KMeans để phân cụm đặc trưng, đồng thời lưu trữ các cụm vào metadata
- `main.py`: Tập tin chạy chính, điều phối toàn bộ quy trình từ đọc dữ liệu, trích xuất đặc trưng, phân cụm, đến tìm kiếm và đánh giá kết quả.
- `phan_cum_dac_trung.py`: Gán cụm cho đặc trưng mới khi có dữ liệu âm thanh mới, phục vụ cho việc tìm kiếm âm thanh tương đồng.
- `phat_hien_not_am.py`: Phát hiện nốt âm trong tín hiệu âm thanh, chia tín hiệu thành các khung thời gian nhỏ để trích xuất đặc trưng chính xác hơn.
- `tim_kiem_am_thanh.py`: Tìm kiếm các đoạn âm thanh tương đồng dựa trên đặc trưng và cụm đã phân tích, trả về kết quả phù hợp nhất.
- `trich_dac_trung.py`: Trích xuất đặc trưng âm thanh từ dữ liệu đầu vào, ví dụ cao độ, biến thiên tần số, hoặc các đặc trưng khác phục vụ phân tích.
- `luu_tru_dac_trung.py`: Trích xuất các thông tin về đặc trưng để phục vụ cho việc lưu trữ trong cơ sở dữ liệu
- `truc_quan_hoa_dac_trung.py`: Trực quan hoá đặc trưng âm thanh, hiển thị biểu đồ các chỉ số âm thanh theo thời gian.
- `requirements.txt`: Danh sách các thư viện Python cần thiết cho dự án, ví dụ `numpy`, `scipy`, `librosa`, `scikit-learn`, `pandas`,...
- `README.md`: Tài liệu hướng dẫn sử dụng dự án, bao gồm cách cài đặt, chạy thử và mô tả các chức năng chính của hệ thống.

## 4. Hướng dẫn sử dụng

### 4.1 Cài đặt môi trường

Chạy lệnh sau để cài đặt thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 4.2 Chuẩn bị dữ liệu

- Đặt các file âm thanh định dạng `.wav` vào thư mục `du_lieu/` (tự tạo) để làm dữ liệu huấn luyện.
- Các file dùng để kiểm thử nên được đặt vào thư mục `du_lieu_test/` (tự tạo).
- Tạo thêm thư mục `sieu_du_lieu/` (tự tạo) để lưu các metadata

---

### 4.3 Tạo Container MySQL bằng Docker (tuỳ chọn)
#### Bước 1: Tải docker tại trang chủ (nếu chưa có)
Link trang chủ: `https://www.docker.com/`

#### Bước 2: Tạo docker container mySQL (nếu chưa có)
Mở thư mục `bo_go_mysql` bằng CMD, sau đó chạy lệnh (nhớ mở docker trước khi chạy):

```bash
docker-compose up -d
```

#### Bước 3: Kết nối tới mySQL
Nhập thông tin server mySQL vừa tạo và kết nối:

```bash
password: admin
database: dac_trung_bo_go
port: 3308
```

### Buớc 4: Thêm CSDL
Chạy file script `csdl.sql` để thêm CSDL cho server


### 4.4 Chạy chương trình chính

nhập thông tin đường dẫn vào các biến `duong_dan_thu_muc` `duong_dan_dac_trung_am_thanh` `duong_dan_chuan_hoa` `duong_dan_test` trong file `main.py`để thực hiện các bước sau:

- Trích xuất đặc trưng  
- Chuẩn hóa và lưu đặc trưng  
- Phân cụm bằng KMeans 
- Tìm kiếm 3 âm thanh tương đồng nhất với `duong_dan_test`
- Lưu kết quả vào cơ sở dữ liệu

```bash
python main.py
```

### 4.5 Trực quan hoá đặc trưng 

Chạy file `truc_quan_hoa_dac_trung.py` để trích xuất và hiển thị trực quan các đặc trưng âm thanh từ file `.wav`.

Cách sử dụng:

1. Nhập thông tin đường dẫn file vào biến `tep_am_thanh` (đảm bảo file âm thanh `.wav` ta muốn phân tích nằm trong thư mục `du_lieu_test/` hoặc ta có thể nhập đường dẫn đầy đủ đến file).

2. Mở terminal hoặc command prompt, chạy lệnh:

```bash
python truc_quan_hoa_dac_trung.py
```

## 5. Một số lưu ý
- Hệ thống sử dụng **chuẩn hóa z-score** (phân phối chuẩn) để xử lý đặc trưng, nhằm đưa tất cả các đặc trưng về cùng một thang đo và **giảm ảnh hưởng của các giá trị ngoại lai (outlier).

- **Độ dài khung âm thanh** được xác định bằng cách:
  1. Với mỗi file `.wav`, hệ thống phát hiện các nốt âm và tính **thời gian trung vị** của các nốt trong file đó.
  2. Sau đó, lấy **giá trị trung vị của tất cả các thời gian trung vị** trên toàn bộ thư mục âm thanh (`du_lieu/`) để xác định độ dài khung tối ưu dùng cho toàn hệ thống.
  3. Giá trị này được lưu vào file `sieu_du_lieu/do_dai_khung.json` để tái sử dụng ở các bước xử lý tiếp theo mà không cần tính toán lại mỗi lần.

- Thư mục `du_lieu/` và `du_lieu_test/` được giữ trống trong Git để tránh commit dữ liệu lớn. Tuy nhiên, ta phải đảm bảo có các file .wav trong thư mục này khi chạy hệ thống.



---

> Nhóm rất mong nhận được sự góp ý từ thầy để hoàn thiện sản phẩm tốt hơn.  
> **Chân thành cảm ơn thầy đã theo dõi và đánh giá dự án của nhóm!**

**Ngày hoàn thành: [19/05/2025]**
