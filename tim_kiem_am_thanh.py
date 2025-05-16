import os
import math
import pandas as pd
import jsonpickle as json
from collections import Counter
from cum_va_dac_trung import Cum

def tinh_khoang_cach_euclidean(dac_trung1, dac_trung2):
    """
    Tính khoảng cách Euclidean giữa hai vector đặc trưng.

    Tham số:
        dac_trung1 (list): Vector đặc trưng thứ nhất.
        dac_trung2 (list): Vector đặc trưng thứ hai.

    Trả về:
        float: Khoảng cách Euclidean.
    """
    tong = sum((dac_trung1[i] - dac_trung2[i]) ** 2 for i in range(len(dac_trung1)))
    return math.sqrt(tong)

def loai_bo_file(danh_sach_cum, danh_sach_file_can_xoa):
    """
    Loại bỏ các phần tử có chứa tên file nằm trong 'danh_sach_file_can_xoa' khỏi tất cả các cụm và log các file bị loại.

    :param danh_sach_cum: Danh sách các cụm, mỗi cụm là danh sách các cặp [file_path, distance]
    :param danh_sach_file_can_xoa: Danh sách tên file cần loại bỏ
    :return: Danh sách sau khi đã loại bỏ các file
    """
    # Chuẩn hóa danh sách tên file cần xóa: chỉ lấy tên file (không lấy đường dẫn)
    ten_file_can_xoa_gon = set(os.path.basename(f) for f in danh_sach_file_can_xoa)

    danh_sach_moi = []
    for i, cum in enumerate(danh_sach_cum):
        cum_moi = []
        for cap in cum:
            ten_file = os.path.basename(cap[0])
            if ten_file not in ten_file_can_xoa_gon:
                cum_moi.append(cap)
        danh_sach_moi.append(cum_moi)
    return danh_sach_moi


def tinh_toan_do_tuong_dong(cac_cum, dac_trung, soLuong=3):
    """
    Tính toán độ tương đồng giữa một tập đặc trưng đầu vào và các cụm đã có,
    sau đó trả về N âm thanh (link) giống nhất dựa trên khoảng cách Euclidean trung bình nhỏ nhất.

    Tham số:
        cac_cum (list): Danh sách các cụm đã được huấn luyện trước (đối tượng Cluster).
        dac_trung (list): Danh sách đặc trưng đầu vào (mỗi phần tử là 1 vector đặc trưng).
        soLuong (int): Số lượng âm thanh giống nhất cần trả về (mặc định là 3).

    Trả về:
        list: Top N đường dẫn đến các âm thanh giống nhất.
    """
    danh_sach_nhan = []
    for dt in dac_trung:
        # Tìm cụm gần nhất
        khoang_cach_nho_nhat = float('inf')
        cum_gan_nhat = 0
        for i in range(len(cac_cum)):
            kc = tinh_khoang_cach_euclidean(cac_cum[i].tam, dt)
            if kc < khoang_cach_nho_nhat:
                khoang_cach_nho_nhat = kc
                cum_gan_nhat = i

        danh_sach_khoang_cach = []
        danh_sach_link = []

        for f in cac_cum[cum_gan_nhat].dac_trung:
            kc = tinh_khoang_cach_euclidean(dt, f.dac_trung)
            # print("Khoảng cách với đặc trưng cụm:", kc, " - liên kết:", f.lien_ket)

            if kc > 10000:
                continue

            danh_sach_khoang_cach.append(kc)
            danh_sach_link.append(f.lien_ket)

        cap_khoang_cach_link = sorted(zip(danh_sach_link, danh_sach_khoang_cach), key=lambda x: x[1])

        # lọc các tên file đã xuất hiện trong danh sách 
        danh_sach_loc = []
        da_xuat_hien = set()
        for link, kc in cap_khoang_cach_link:
            if link not in da_xuat_hien:
                danh_sach_loc.append([link, kc])
                da_xuat_hien.add(link)

        if cap_khoang_cach_link:
            danh_sach_nhan.append(danh_sach_loc)

    top_ket_qua = []
    sl = 0  # Số lượng phần tử đã có trong top_ket_qua
    while sl < soLuong and danh_sach_nhan:
        danh_sach_gan_nhat = []

        for danh_sach in danh_sach_nhan:
            if danh_sach:
                link, kc = danh_sach[0]
                danh_sach_gan_nhat.append((link, kc))

        if not danh_sach_gan_nhat:
            break

        df = pd.DataFrame(danh_sach_gan_nhat, columns=['duong_dan', 'khoang_cach'])
        trung_binh_kc = df.groupby('duong_dan')['khoang_cach'].mean()

        so_luong_can_bo_sung = soLuong - sl
        top_con_lai = trung_binh_kc.nsmallest(so_luong_can_bo_sung).index.tolist()

        top_ket_qua.extend(top_con_lai)
        sl = len(top_ket_qua)
        
        # loại bỏ file đã duyệt rồi khỏi danh sách
        if sl < soLuong:
            danh_sach_nhan = loai_bo_file(danh_sach_nhan, top_ket_qua)

    return top_ket_qua
