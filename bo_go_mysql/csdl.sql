-- Tạo bảng đặc trưng âm thanh
CREATE TABLE dac_trung_am_thanh (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_tap_tin VARCHAR(255),
    bat_dau INT,              -- thời điểm bắt đầu của khung trong file gốc (đơn vị: khung)
    ket_thuc INT,              -- thời điểm kết thúc của khung trong file gốc (đơn vị: khung)
    toc_do_qua_diem_0 FLOAT,    
    nang_luong_trung_binh FLOAT,
    tan_so_trung_binh FLOAT,    
    do_bien_thien_tan_so FLOAT, 
    cao_do_trung_binh FLOAT,    
    do_bien_thien_cao_do FLOAT
);

