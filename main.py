import os
import chuc_nang as cn
import jsonpickle as json
from trich_dac_trung import trich_rut_dac_trung
from phan_cum_dac_trung import phan_cum_dac_trung
from tim_kiem_am_thanh import tinh_toan_do_tuong_dong
from phat_hien_not_am import tinh_thoi_luong_khung

# Đường dẫn đến thư mục chứa dữ liệu âm thanh
duong_dan_thu_muc = 'du_lieu'
# Đường dẫn tới file chứa metadata đặc trưng âm thanh
duong_dan_dac_trung_am_thanh = 'sieu_du_lieu/dac_trung_am_thanh.json'
# Đường dẫn tới file chứa metadata chuẩn hoá
duong_dan_chuan_hoa = 'sieu_du_lieu/chuan_hoa.json'
# đường dẫn tới file test
duong_dan_test = "du_lieu_test/hit_C4_20.wav"

# Tính thời lượng cho mỗi khung
tinh_thoi_luong_khung(duong_dan_thu_muc)      # chiều dài mỗi khung (số mẫu)

# Nếu tệp không có dữ liệu hoặc không tồn tại, thực hiện phân cụm đặc trưng
if(cn.kiem_tra_tap_tin_rong(duong_dan_dac_trung_am_thanh) or cn.kiem_tra_tap_tin_rong(duong_dan_chuan_hoa)):
    # chuẩn hoá toàn bộ dữ liệu
    ds_dac_trung_chuan_hoa = cn.chuan_hoa_dac_trung_du_lieu(duong_dan_thu_muc)
    # phân cụm các đặc trưng
    phan_cum_dac_trung(duong_dan_thu_muc, ds_dac_trung_chuan_hoa, 11)

# Đọc dữ liệu từ file JSON chứa các cụm đặc trưng đã lưu
with open(duong_dan_dac_trung_am_thanh, 'r') as file:
    noi_dung_json = file.read()

# Giải mã JSON thành danh sách đối tượng cụm
cac_cum = json.loads(noi_dung_json)

# Trích rút đặc trưng từ file âm thanh cần so sánh và chuẩn hoá 
dac_trung = cn.chuan_hoa_phan_phoi_chuan_mot_file(trich_rut_dac_trung(duong_dan_test)["dac_trung"], duong_dan_chuan_hoa)

# Tìm top 3 âm thanh giống nhất
top_3 = tinh_toan_do_tuong_dong(cac_cum, dac_trung, 3)

# In kết quả
print(f"Top 3 âm thanh giống nhất với {duong_dan_test}:", top_3)





