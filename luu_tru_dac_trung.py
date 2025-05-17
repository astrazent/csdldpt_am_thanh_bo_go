import os
import mysql.connector
import jsonpickle as json
import kmeans as db
from trich_dac_trung import trich_rut_dac_trung

# Thư mục chứa các file âm thanh
thu_muc_du_lieu = 'du_lieu'

# Lấy danh sách tất cả các file trong thư mục
ds_tap_tin = os.listdir(thu_muc_du_lieu)

# Danh sách chứa các đặc trưng dạng vector
ds_vector_dac_trung = []

def thong_tin_dac_trung():
    """
    Trích xuất đặc trưng từ tất cả file trong thư mục dữ liệu.
    Lưu vào 2 danh sách: dạng vector (cho phân cụm) và dạng dictionary (lưu JSON).
    Mỗi dictionary chứa: tên file, đặc trưng, thời điểm bắt đầu và kết thúc.
    """
    # Danh sách chứa thông tin đặc trưng dạng dictionary để lưu file
    ds_dac_trung_dict = []

    for ten_file in ds_tap_tin:
        duong_dan = os.path.join(thu_muc_du_lieu, ten_file)
        ket_qua = trich_rut_dac_trung(duong_dan)

        ds_dac_trung = ket_qua["dac_trung"]
        ds_bat_dau = ket_qua["bat_dau"]
        ds_ket_thuc = ket_qua["ket_thuc"]

        for i in range(len(ds_dac_trung)):
            dac_trung = [float(x) for x in ds_dac_trung[i]]  # Ép về float từ np.float64
            bat_dau = int(ds_bat_dau[i])
            ket_thuc = int(ds_ket_thuc[i])

            ds_vector_dac_trung.append(dac_trung)
            ds_dac_trung_dict.append({
                "ten_file": ten_file,
                "bat_dau": bat_dau,
                "ket_thuc": ket_thuc,
                "dac_trung": dac_trung
            })
    return ds_dac_trung_dict

def luu_dac_trung_vao_json(ds_dict):
    """
    Lưu danh sách đặc trưng vào file JSON để dùng lại sau này.
    """
    du_lieu_json = json.dumps(ds_dict)
    with open("sieu_du_lieu/dac_trung_am_thanh.json", "w") as file:
        file.write(du_lieu_json)

def them_dac_trung_vao_db():
    ds_dac_trung_dict = thong_tin_dac_trung()

    # thiết lập kết nối tới mySQL
    try:
        ket_noi_csdl = mysql.connector.connect(
            host="localhost",
            port="3308",
            user="root",
            password="admin",
            database="dac_trung_bo_go"
        )
        print("Kết nối CSDL thành công")
    except Exception as e:
        print("Không thể kết nối tới MySQL. Chi tiết lỗi:")
        print(e)

    truy_van = ket_noi_csdl.cursor()
    so_dong = 0

    try:
        ket_noi_csdl.start_transaction()

        for muc in ds_dac_trung_dict:
            ten_file = muc["ten_file"]
            bat_dau = muc["bat_dau"]
            ket_thuc = muc["ket_thuc"]
            vector = muc["dac_trung"]

            lenh_sql = """
                INSERT INTO dac_trung_am_thanh (
                    ten_tap_tin,
                    bat_dau,
                    ket_thuc,
                    toc_do_qua_diem_0,
                    nang_luong_trung_binh,
                    tan_so_trung_binh,
                    do_bien_thien_tan_so,
                    cao_do_trung_binh,
                    do_bien_thien_cao_do
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            gia_tri = (
                ten_file,
                bat_dau,
                ket_thuc,
                vector[0],
                vector[1],
                vector[2],
                vector[3],
                vector[4],
                vector[5]
            )

            truy_van.execute(lenh_sql, gia_tri)
            so_dong += 1

        ket_noi_csdl.commit()
        print(f"{so_dong} đặc trưng đã được thêm vào CSDL.")

    except Exception as e:
        ket_noi_csdl.rollback()
        print("Lỗi khi thêm dữ liệu. Đã rollback transaction.")
        print("Chi tiết lỗi:", e)

    finally:
        truy_van.close()
        ket_noi_csdl.close()
    
    # Phân cụm các đặc trưng và lưu kết quả
    # cac_cum = db.phan_cum_bang_kmeans(ds_vector_dac_trung, 11)
    # db.luu_du_lieu(cac_cum)  # Lưu cụm vào metadata

def lay_dac_trung_tu_db(dieu_kien_sql: str, ten_cot: list):
    """
    Lấy dữ liệu đặc trưng từ bảng dac_trung_am_thanh theo điều kiện SQL chuỗi.

    - dieu_kien_sql: chuỗi điều kiện SQL (VD: "ten_tap_tin = 'test.wav' AND tan_so_trung_binh > 100")
    - ten_cot: danh sách tên các cột cần lấy (VD: ["tan_so_trung_binh", "nang_luong_trung_binh"])
    """

    # Kết nối MySQL
    ket_noi = mysql.connector.connect(
        host="localhost",
        port="3308",
        user="root",
        password="admin",
        database="dac_trung_bo_go"
    )
    truy_van = ket_noi.cursor()

    # Câu lệnh SELECT
    cot_chon = ", ".join(ten_cot)
    lenh_sql = f"SELECT {cot_chon} FROM dac_trung_am_thanh"

    if dieu_kien_sql:
        lenh_sql += f" WHERE {dieu_kien_sql}"

    # Thực thi truy vấn
    truy_van.execute(lenh_sql)
    ket_qua = truy_van.fetchall()

    # Đóng kết nối
    truy_van.close()
    ket_noi.close()

    return ket_qua

# them_dac_trung_vao_db()