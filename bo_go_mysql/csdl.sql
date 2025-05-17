CREATE SCHEMA dac_trung;
USE dac_trung;

-- Tạo bảng đặc trưng âm thanh
CREATE TABLE dac_trung_am_thanh (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_tap_tin VARCHAR(255),
    bat_dau FLOAT,              -- thời điểm bắt đầu của khung trong file gốc (ms)
    ket_thuc FLOAT,              -- thời điểm kết thúc của khung trong file gốc (ms)
    toc_do_qua_diem_0 FLOAT,    
    nang_luong_trung_binh FLOAT,
    tan_so_trung_binh FLOAT,    
    do_bien_thien_tan_so FLOAT, 
    cao_do_trung_binh FLOAT,    
    do_bien_thien_cao_do FLOAT
);

