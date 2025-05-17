import numpy as np
import json
from pydub import AudioSegment

'''
    Trích rút đặc trưng từ tệp âm thanh
'''
def trich_rut_dac_trung(duong_dan_tap_tin):
    am_thanh, _ = doc_tap_tin_am_thanh(duong_dan_tap_tin)
    thong_tin_khung = chia_khung_am_thanh(am_thanh)
    dac_trung = []
    ds_bat_dau = []
    ds_ket_thuc = []
    for item in thong_tin_khung:
        khung = item["khung"]      
        bat_dau = item["bat_dau"]  
        ket_thuc = item["ket_thuc"] 

        # loại bỏ các frame bị câm
        if(kiem_tra_khong_im_lang(khung)):
            cao_do_tb = cao_do_trung_binh(khung)
            tan_so_tb = tan_so_trung_binh(khung)
            nang_luong_tb = nang_luong_trung_binh(khung)
            bien_thien_ts = bien_thien_tan_so(khung)
            bien_thien_cd = bien_thien_cao_do(khung)
            toc_do_quet_0 = toc_do_qua_diem_0(khung)
            dac_trung.append([nang_luong_tb, toc_do_quet_0, tan_so_tb, bien_thien_ts, cao_do_tb, bien_thien_cd])
            ds_bat_dau.append(bat_dau)
            ds_ket_thuc.append(ket_thuc)
    return {
        "dac_trung": dac_trung,
        "bat_dau": ds_bat_dau,
        "ket_thuc": ds_ket_thuc
    }

'''
    Chia âm thanh thành các khung có thời gian lấy từ file, gối đầu nhau mỗi lần
'''
def chia_khung_am_thanh(am_thanh):
    with open("sieu_du_lieu/do_dai_khung.json", "r", encoding="utf-8") as f:
        du_lieu = json.load(f)
    do_dai_khung = int(du_lieu["do_dai_khung"])
    buoc_nhay = do_dai_khung // 2

    ds_khung = []

    for i in range(0, len(am_thanh) - do_dai_khung + 1, buoc_nhay):
        khung = am_thanh[i:i + do_dai_khung]
        bat_dau = i
        ket_thuc = i + do_dai_khung
        ds_khung.append({
            "khung": khung,
            "bat_dau": bat_dau,
            "ket_thuc": ket_thuc # (khung)
        })

    return ds_khung

'''
    Đọc tệp âm thanh bằng thư viện AudioSegment
'''
def doc_tap_tin_am_thanh(ten_tap_tin):
    am_thanh = AudioSegment.from_file(ten_tap_tin)
    am_thanh = am_thanh.set_channels(1)  # Chuyển thành mono
    toc_do_lay_mau = am_thanh.frame_rate    # Lấy sample rate
    return am_thanh, toc_do_lay_mau

'''
    Tính năng lượng trung bình (RMS energy)
'''
def nang_luong_trung_binh(am_thanh):
    return am_thanh.rms

'''
    Tính tốc độ qua điểm 0 (Zero Crossing Rate)
'''
def toc_do_qua_diem_0(am_thanh):
    mau = np.array(am_thanh.get_array_of_samples())
    zero_crossings = np.where(np.diff(np.sign(mau)))[0]
    zcr = len(zero_crossings) / len(mau)
    return zcr

'''
    Kiểm tra xem khung âm thanh có im lặng không (>= 75% mẫu nhỏ hơn ngưỡng)
'''
def kiem_tra_khong_im_lang(am_thanh):
    mau = np.array(am_thanh.get_array_of_samples())
    nguong_im_lang = 280
    so_mau_im_lang = len(np.where(abs(mau) < nguong_im_lang)[0])
    ty_le_im_lang = so_mau_im_lang / len(mau)
    return ty_le_im_lang < 0.75

'''
    Tính độ biến thiên tần số (frequency variation)
'''
def bien_thien_tan_so(am_thanh):
    mau = np.array(am_thanh.get_array_of_samples())
    pho = np.fft.fft(mau)
    bien_thien = np.abs(np.diff(pho))
    trung_binh_bien_thien = np.mean(bien_thien)
    return trung_binh_bien_thien

'''
    Tính tần số trung bình trong miền tần số
'''
def tan_so_trung_binh(am_thanh):
    mau = np.array(am_thanh.get_array_of_samples())
    tan_so = np.fft.fftfreq(len(mau), d=1.0/am_thanh.frame_rate)
    pho = np.fft.fft(mau)
    tan_so_tb = np.abs(pho).dot(np.abs(tan_so)) / np.sum(np.abs(pho))
    return tan_so_tb

'''
    Tính độ biến thiên cao độ (pitch variation)
'''
def bien_thien_cao_do(am_thanh):
    mau = np.array(am_thanh.get_array_of_samples())
    kich_thuoc_cua_so = int(am_thanh.frame_rate / 100.0)
    buoc_nhay = kich_thuoc_cua_so // 2

    cac_tan_so_cb = []
    for i in range(0, len(mau) - kich_thuoc_cua_so, buoc_nhay):
        cua_so = mau[i:i+kich_thuoc_cua_so]
        pho = np.fft.fft(cua_so)
        tan_so = np.fft.fftfreq(len(cua_so), d=1.0/am_thanh.frame_rate)
        chi_so_duong = np.where(tan_so > 0)
        pho = pho[chi_so_duong]
        tan_so = tan_so[chi_so_duong]
        dinh = np.argmax(np.abs(pho))
        tan_so_cb = tan_so[dinh]
        cac_tan_so_cb.append(tan_so_cb)

    bien_thien = np.abs(np.diff(cac_tan_so_cb))
    bien_thien_tb = np.mean(bien_thien)
    return bien_thien_tb

'''
    Tính cao độ trung bình (average pitch)
'''
def cao_do_trung_binh(am_thanh):
    mau = np.array(am_thanh.get_array_of_samples())
    pho = np.fft.fft(mau)
    tan_so = np.fft.fftfreq(len(mau), d=1.0/am_thanh.frame_rate)
    chi_so_duong = np.where(tan_so > 0)
    tan_so = tan_so[chi_so_duong]
    pho = pho[chi_so_duong]
    dinh = np.argmax(np.abs(pho))
    tan_so_co_ban = tan_so[dinh]

    cao_do = 0.0
    if tan_so_co_ban > 0:
        cao_do = am_thanh.frame_rate / tan_so_co_ban
    return cao_do