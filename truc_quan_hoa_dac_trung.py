import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

def toc_do_qua_diem_0(khung):
    dem = 0
    for i in range(1, len(khung)):
        if (khung[i-1] >= 0 and khung[i] < 0) or (khung[i-1] < 0 and khung[i] >= 0):
            dem += 1
    return dem / len(khung)

def nang_luong_trung_binh(khung):
    return np.mean(np.square(khung))

def tan_so_trung_binh(khung, tan_so_mau):
    fft = np.fft.rfft(khung)
    bien_do = np.abs(fft)
    cac_tan_so = np.fft.rfftfreq(len(khung), d=1/tan_so_mau)
    if np.sum(bien_do) == 0:
        return 0
    tan_so_tb = np.sum(cac_tan_so * bien_do) / np.sum(bien_do)
    return tan_so_tb

def bien_thien_tan_so(ds_khung, tan_so_mau):
    ds_tan_so = [tan_so_trung_binh(k, tan_so_mau) for k in ds_khung]
    return np.std(ds_tan_so)

def cao_do_trung_binh(khung, tan_so_mau):
    tu_tuong_quan = np.correlate(khung, khung, mode='full')
    tu_tuong_quan = tu_tuong_quan[len(tu_tuong_quan)//2:]
    dao_ham = np.diff(tu_tuong_quan)
    chi_so_duong = np.where(dao_ham > 0)[0]
    if len(chi_so_duong) == 0:
        return 0
    bat_dau = chi_so_duong[0]
    dinh = np.argmax(tu_tuong_quan[bat_dau:]) + bat_dau
    if dinh == 0:
        return 0
    cao_do = tan_so_mau / dinh
    return cao_do

def bien_thien_cao_do(ds_khung, tan_so_mau):
    ds_cao_do = [cao_do_trung_binh(k, tan_so_mau) for k in ds_khung]
    return np.std(ds_cao_do)

def chia_khung_am_thanh(tin_hieu, kich_thuoc_khung, buoc_nhay):
    cac_khung = []
    for bat_dau in range(0, len(tin_hieu) - kich_thuoc_khung + 1, buoc_nhay):
        cac_khung.append(tin_hieu[bat_dau:bat_dau+kich_thuoc_khung])
    return cac_khung

def trich_dac_trung(file_am_thanh, thoi_luong_khung=0.5, buoc_nhay=0.25):
    am_thanh = AudioSegment.from_file(file_am_thanh)
    mau = np.array(am_thanh.get_array_of_samples())
    if am_thanh.channels == 2:
        mau = mau[::2]  # chọn 1 kênh nếu stereo
    tan_so_mau = am_thanh.frame_rate

    kich_thuoc_khung = int(thoi_luong_khung * tan_so_mau)
    buoc_nhay_mau = int(buoc_nhay * tan_so_mau)
    cac_khung = chia_khung_am_thanh(mau, kich_thuoc_khung, buoc_nhay_mau)

    ds_zcr = []
    ds_nang_luong = []
    ds_tan_so_tb = []
    ds_cao_do = []

    for khung in cac_khung:
        ds_zcr.append(toc_do_qua_diem_0(khung))
        ds_nang_luong.append(nang_luong_trung_binh(khung))
        ds_tan_so_tb.append(tan_so_trung_binh(khung, tan_so_mau))
        ds_cao_do.append(cao_do_trung_binh(khung, tan_so_mau))

    bien_thien_ts = np.std(ds_tan_so_tb)
    bien_thien_cd = np.std(ds_cao_do)

    return {
        'toc_do_quet_0': ds_zcr,
        'nang_luong_tb': ds_nang_luong,
        'tan_so_tb': ds_tan_so_tb,
        'bien_thien_ts': bien_thien_ts,
        'cao_do_tb': ds_cao_do,
        'bien_thien_cd': bien_thien_cd,
        'thoi_gian_khung': np.arange(len(cac_khung)) * buoc_nhay
    }

def ve_bieu_do(dac_trung, ten_file):
    t = dac_trung['thoi_gian_khung']
    plt.figure(figsize=(14, 10))

    plt.subplot(4,1,1)
    plt.plot(t, dac_trung['toc_do_quet_0'], label='Tốc độ qua điểm 0')
    plt.legend()
    plt.ylabel('ZCR')

    plt.subplot(4,1,2)
    plt.plot(t, dac_trung['nang_luong_tb'], label='Năng lượng TB', color='orange')
    plt.legend()
    plt.ylabel('Năng lượng')

    plt.subplot(4,1,3)
    plt.plot(t, dac_trung['tan_so_tb'], label='Tần số TB', color='green')
    plt.legend()
    plt.ylabel('Tần số (Hz)')

    plt.subplot(4,1,4)
    plt.plot(t, dac_trung['cao_do_tb'], label='Cao độ TB', color='red')
    plt.legend()
    plt.ylabel('Cao độ (Hz)')
    plt.xlabel('Thời gian (s)')

    plt.suptitle(
        f'Biểu đồ đặc trưng âm thanh theo thời gian\nTệp: {ten_file}\n'
        f'Biến thiên tần số: {dac_trung["bien_thien_ts"]:.2f}, Biến thiên cao độ: {dac_trung["bien_thien_cd"]:.2f}'
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Ví dụ chạy với 1 file âm thanh
# tep_am_thanh = 'du_lieu_test/hit_C4_20.wav'  # Thay bằng file test
tep_am_thanh = 'du_lieu/hit_C4_5.wav'  # Thay bằng file similar
dac_trung = trich_dac_trung(tep_am_thanh)
ve_bieu_do(dac_trung, tep_am_thanh)
