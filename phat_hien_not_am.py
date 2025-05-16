import os
import json
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def phat_hien_not_am_thanh(duong_dan_file):
    # ===== BƯỚC 1: ĐỌC FILE ÂM THANH =====
    tan_so_mau, tin_hieu = wavfile.read(duong_dan_file)

    # Nếu là âm thanh stereo -> lấy 1 kênh
    if tin_hieu.ndim > 1:
        tin_hieu = tin_hieu[:, 0]

    # Chuẩn hóa tín hiệu về [-1, 1]
    tin_hieu = tin_hieu.astype(np.float32)
    tin_hieu = tin_hieu / np.max(np.abs(tin_hieu))

    # ===== BƯỚC 2: TÍNH NĂNG LƯỢNG RMS =====
    kich_thuoc_khung = 2048
    buoc_nhay = 512

    danh_sach_rms = []
    vi_tri_khung = []

    for i in range(0, len(tin_hieu) - kich_thuoc_khung, buoc_nhay):
        khung = tin_hieu[i:i + kich_thuoc_khung]
        nang_luong = np.sqrt(np.mean(khung**2))
        danh_sach_rms.append(nang_luong)
        vi_tri_khung.append(i)

    danh_sach_rms = np.array(danh_sach_rms)
    thoi_gian_khung = np.array(vi_tri_khung) / tan_so_mau

    # ===== BƯỚC 3: PHÁT HIỆN ONSET =====
    sai_khac = np.diff(danh_sach_rms)
    chi_so_onset = np.where(sai_khac > 0.02)[0]

    # Loại bỏ điểm trùng lặp trong khoảng < 100ms
    khoang_cach_toi_thieu = int(0.1 * tan_so_mau / buoc_nhay)
    onsets_loc = []
    cuoi_cung = -khoang_cach_toi_thieu

    for chi_so in chi_so_onset:
        if chi_so - cuoi_cung >= khoang_cach_toi_thieu:
            onsets_loc.append(chi_so)
            cuoi_cung = chi_so

    # ===== BƯỚC 4: ƯỚC LƯỢNG OFFSET =====
    danh_sach_thoi_gian = []
    nguong_offset = 0.01

    for onset in onsets_loc:
        for i in range(onset + 1, len(danh_sach_rms)):
            if danh_sach_rms[i] < nguong_offset:
                bat_dau = vi_tri_khung[onset] / tan_so_mau
                ket_thuc = vi_tri_khung[i] / tan_so_mau
                danh_sach_thoi_gian.append((bat_dau, ket_thuc))
                break
        else:
            bat_dau = vi_tri_khung[onset] / tan_so_mau
            ket_thuc = len(tin_hieu) / tan_so_mau
            danh_sach_thoi_gian.append((bat_dau, ket_thuc))

    # ===== BƯỚC 5: IN KẾT QUẢ =====
    # print("Thời gian các nốt được phát hiện:")
    # for i, (bat_dau, ket_thuc) in enumerate(danh_sach_thoi_gian):
    #     print(f"Nốt {i+1}: {bat_dau:.2f}s → {ket_thuc:.2f}s (thời lượng: {ket_thuc - bat_dau:.2f}s)")

    # ===== BƯỚC 6: VẼ ĐỒ THỊ (TÙY CHỌN) =====
    # plt.figure(figsize=(12, 4))
    # plt.plot(thoi_gian_khung, danh_sach_rms, label='Năng lượng RMS')
    # for bat_dau, ket_thuc in danh_sach_thoi_gian:
    #     plt.axvspan(bat_dau, ket_thuc, color='orange', alpha=0.3)
    # plt.title("Onset và thời lượng nốt dựa trên năng lượng RMS")
    # plt.xlabel("Thời gian (s)")
    # plt.ylabel("RMS")
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    # ===== BƯỚC 5: TÍNH PHÂN PHỐI CHUẨN TỪ THỜI GIAN =====
    thoi_luong_cac_not = [ket_thuc - bat_dau for bat_dau, ket_thuc in danh_sach_thoi_gian]
    thoi_luong_cac_not = np.array(thoi_luong_cac_not)

    trung_vi = np.median(thoi_luong_cac_not)

    return trung_vi

def tinh_thoi_luong_khung(duong_dan_thu_muc):
    danh_sach_trung_vi = []
    
    for ten_file in os.listdir(duong_dan_thu_muc):
        duong_dan_file = os.path.join(duong_dan_thu_muc, ten_file)
        
        if os.path.isfile(duong_dan_file) and ten_file.lower().endswith('.wav'):
            trung_vi_file = phat_hien_not_am_thanh(duong_dan_file)
            # Nếu hàm trả về 0 có thể bỏ qua hoặc vẫn tính tùy bạn
            if trung_vi_file > 0:
                danh_sach_trung_vi.append(trung_vi_file)
    
    if len(danh_sach_trung_vi) > 0:
        trung_vi_thu_muc = np.median(danh_sach_trung_vi) * 1000 # ms
    else:
        trung_vi_thu_muc = 0  # hoặc None
    
    # Lưu giá trị vào file
    duong_dan_json = "sieu_du_lieu/do_dai_khung.json"
    with open(duong_dan_json, "w", encoding="utf-8") as f:
        json.dump({"do_dai_khung": trung_vi_thu_muc}, f, ensure_ascii=False, indent=4)
    
    return trung_vi_thu_muc