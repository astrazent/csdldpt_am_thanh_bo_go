import os
import numpy as np
import kmeans as db
from cum_va_dac_trung import DacTrung

# Đường dẫn đến thư mục chứa các tệp dữ liệu cần trích đặc trưng

def phan_cum_dac_trung(ds_dac_trung_chuan_hoa, so_cum=11):
    """
    Hàm thực hiện phân cụm đặc trưng đã chuẩn hóa và trả về danh sách các cụm.
    """

    # Tạo danh sách đối tượng DacTrung sau khi chuẩn hoá
    danh_sach_dac_trung = [
        DacTrung(lien_ket=duong_dan, dac_trung=dac_trung)
        for duong_dan, dac_trung in ds_dac_trung_chuan_hoa
    ]

    # Phân cụm bằng KMeans
    cac_cum = db.phan_cum_bang_kmeans(danh_sach_dac_trung, so_cum)
    
    # Lưu kết quả
    db.luu_du_lieu(cac_cum)

    return cac_cum


