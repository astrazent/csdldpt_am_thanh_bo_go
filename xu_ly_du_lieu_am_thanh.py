import os
import mysql.connector
import jsonpickle as json
import kmeans_va_config_db as db
from trich_dac_trung import trich_rut_dac_trung

# Kết nối đến cơ sở dữ liệu MySQL
ket_noi_csdl = mysql.connector.connect(
    host="localhost",
    port="3308",
    user="root",
    password="admin",
    database="nba_search"
)
truy_van = ket_noi_csdl.cursor()

# Thư mục chứa các file âm thanh
thu_muc_du_lieu = 'data'

# Lấy danh sách tất cả các file trong thư mục
ds_tap_tin = os.listdir(thu_muc_du_lieu)

# Danh sách chứa các đặc trưng dạng vector
ds_vector_dac_trung = []

# Danh sách chứa đặc trưng dạng dictionary để lưu file
ds_dac_trung_dict = []

def trich_xuat_dac_trung():
    """
    Trích xuất đặc trưng từ tất cả file trong thư mục dữ liệu.
    Lưu vào 2 danh sách: dạng vector (cho phân cụm) và dạng dictionary (lưu JSON).
    """
    for ten_file in ds_tap_tin:
        dac_trung_cua_file = trich_rut_dac_trung(os.path.join(thu_muc_du_lieu, ten_file))
        for dac_trung in dac_trung_cua_file:
            ds_vector_dac_trung.append(dac_trung)
            ds_dac_trung_dict.append({ten_file: dac_trung})

    print('Hoàn tất trích xuất đặc trưng!')
    print(ds_dac_trung_dict)

trich_xuat_dac_trung()

def luu_dac_trung_vao_json(ds_dict):
    """
    Lưu danh sách đặc trưng vào file JSON để dùng lại sau này.
    """
    du_lieu_json = json.dumps(ds_dict)
    with open("features/data.json", "w") as file:
        file.write(du_lieu_json)

luu_dac_trung_vao_json(ds_dac_trung_dict)

# Ghi dữ liệu vào bảng MySQL
for muc in ds_dac_trung_dict:
    for ten_file, vector in muc.items():
        lenh_sql = """
        INSERT INTO dac_trung_am_thanh (
            ten_tap_tin,
            toc_do_qua_diem_0,
            nang_luong_trung_binh,
            tan_so_trung_binh,
            do_bien_thien_tan_so,
            cao_do_trung_binh,
            do_bien_thien_cao_do
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        gia_tri = (ten_file, vector[0], vector[1], vector[2], vector[3], vector[4], vector[5])
        truy_van.execute(lenh_sql, gia_tri)

# Xác nhận các thay đổi vào CSDL
ket_noi_csdl.commit()
print(truy_van.rowcount, "đặc trưng đã được thêm vào CSDL.")

# Phân cụm các đặc trưng và lưu kết quả
cac_cum = db.ClusterUseKmeans(ds_vector_dac_trung)
# luu.save(cac_cum)  # Có thể bật lại nếu muốn lưu cụm
