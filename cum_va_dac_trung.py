class Cum:  # Cluster
    def __init__(self, tam=None, dac_trung=None):
        """
        Lớp đại diện cho một cụm (Cluster)
        :param tam: Tâm của cụm
        :param dac_trung: Danh sách các đặc trưng thuộc cụm
        """
        self.tam = tam              # center
        self.dac_trung = dac_trung  # features (list các ĐặcTrung)

class DacTrung:  # Feature
    def __init__(self, lien_ket=None, dac_trung=None):
        """
        Lớp đại diện cho một đặc trưng (Feature)
        :param lien_ket: Đường dẫn hoặc thông tin liên kết đến dữ liệu gốc
        :param dac_trung: Giá trị đặc trưng (có thể là vector, mảng số...)
        """
        self.lien_ket = lien_ket      # link
        self.dac_trung = dac_trung    # feature (dữ liệu đặc trưng)
