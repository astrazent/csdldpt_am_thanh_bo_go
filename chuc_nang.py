import os
import numpy as np
import json
from trich_dac_trung import trich_rut_dac_trung

def chuan_hoa_phan_phoi_chuan(danh_sach_dac_trung, duong_dan_metadata='sieu_du_lieu/chuan_hoa.json'):
    """
    Chuẩn hoá danh sách vector đặc trưng âm thanh theo phân phối chuẩn (Z-score normalization)
    và lưu thông tin trung bình, độ lệch chuẩn vào file metadata JSON.

    Tham số:
        danh_sach_dac_trung (list of list): Danh sách vector đặc trưng, mỗi phần tử là 1 list gồm nhiều đặc trưng.
        duong_dan_metadata (str): Đường dẫn tới file metadata để lưu giá trị trung bình và độ lệch chuẩn.

    Trả về:
        tuple: 
            - list of list: Danh sách vector đặc trưng đã được chuẩn hoá.
    """
    du_lieu = np.array(danh_sach_dac_trung)
    gtri_tb = du_lieu.mean(axis=0)
    do_lech_chuan = du_lieu.std(axis=0)

    # Tránh chia cho 0
    do_lech_chuan[do_lech_chuan == 0] = 1

    # Chuẩn hoá
    du_lieu_chuan_hoa = (du_lieu - gtri_tb) / do_lech_chuan

    # Lưu metadata
    metadata = {
        "mean": gtri_tb.tolist(),
        "std": do_lech_chuan.tolist()
    }
    with open(duong_dan_metadata, 'w') as file:
        json.dump(metadata, file, indent=4)

    return du_lieu_chuan_hoa.tolist()

def chuan_hoa_phan_phoi_chuan_mot_file(dac_trung, duong_dan_metadata='sieu_du_lieu/chuan_hoa.json'):
    """
    Chuẩn hoá các vector đặc trưng (từ 1 tệp duy nhất) dựa trên thông tin trung bình và độ lệch chuẩn
    đã lưu trong file metadata JSON.

    Tham số:
        dac_trung (list of list): Danh sách vector đặc trưng cần chuẩn hoá.
        duong_dan_metadata (str): Đường dẫn tới file metadata chứa mean và std.

    Trả về:
        list of list: Danh sách vector đặc trưng đã được chuẩn hoá.
    """

    # Đọc metadata
    with open(duong_dan_metadata, 'r') as file:
        metadata = json.load(file)
    mean = np.array(metadata['mean'])
    std = np.array(metadata['std'])

    # Tránh chia cho 0
    std[std == 0] = 1

    # Chuẩn hoá từng vector trong danh sách
    dac_trung = np.array(dac_trung)
    dac_trung_chuan_hoa = (dac_trung - mean) / std

    return dac_trung_chuan_hoa.tolist()


def kiem_tra_tap_tin_rong(file_path):
    """
    Kiểm tra xem tệp có dữ liệu hay không.
    Nếu tệp không có dữ liệu hoặc không tồn tại, trả về True, 
    ngược lại nếu tệp có dữ liệu thì trả về False.

    Tham số:
        file_path (str): Đường dẫn đến tệp cần kiểm tra.
    
    Trả về:
        bool: True nếu tệp không có dữ liệu hoặc không tồn tại, False nếu tệp đã có dữ liệu.
    """
    # Kiểm tra nếu tệp đã có dữ liệu
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            noi_dung_json = file.read()

        # Kiểm tra nếu tệp có dữ liệu
        if noi_dung_json.strip():  # strip() loại bỏ khoảng trắng đầu/cuối
            return False
        else:
            return True
    else:
        return True

def chuan_hoa_dac_trung_du_lieu(duong_dan_thu_muc):
    """
    Hàm thực hiện:
    1. Đọc tất cả tệp âm thanh trong thư mục đầu vào.
    2. Trích xuất đặc trưng từ mỗi tệp.
    3. Chuẩn hoá đặc trưng theo phân phối chuẩn (Z-score).
    4. Trả về danh sách đặc trưng chuẩn hóa kèm đường dẫn.

    Tham số:
        duong_dan_thu_muc (str): Đường dẫn đến thư mục chứa các tệp dữ liệu.

    Trả về:
        tuple:
            - list: Danh sách các tuple (đường dẫn, vector đặc trưng đã chuẩn hoá).
    """

    du_lieu_tho = []

    # Bước 1: Trích xuất đặc trưng từ các tệp
    for ten_tap_tin in os.listdir(duong_dan_thu_muc):
        duong_dan_tap_tin = os.path.join(duong_dan_thu_muc, ten_tap_tin)
        cac_dac_trung = trich_rut_dac_trung(duong_dan_tap_tin)

        for dac_trung_don in cac_dac_trung:
            du_lieu_tho.append((duong_dan_tap_tin, dac_trung_don))

    # Bước 2: Chuẩn hoá
    tat_ca_vector = [dt[1] for dt in du_lieu_tho]
    du_lieu_chuan_hoa = chuan_hoa_phan_phoi_chuan(tat_ca_vector)

    # Gắn lại đường dẫn với vector đã chuẩn hoá
    ds_dac_trung_chuan_hoa = [
        (du_lieu_tho[i][0], du_lieu_chuan_hoa[i])
        for i in range(len(du_lieu_chuan_hoa))
    ]

    return ds_dac_trung_chuan_hoa

