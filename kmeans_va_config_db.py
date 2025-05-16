import jsonpickle as json
from sklearn.cluster import KMeans
from cum_va_dac_trung import DacTrung
from cum_va_dac_trung import Cum


def huan_luyen_kmeans(du_lieu, so_cum):
    """
    Huấn luyện mô hình K-means để phân cụm dữ liệu đặc trưng.

    Tham số:
        - du_lieu: danh sách các vector đặc trưng (list of list[float])

    Trả về:
        - labels: nhãn cụm tương ứng với từng vector đặc trưng.
        - centers: tọa độ tâm của các cụm sau khi huấn luyện.
    """
    kmeans = KMeans(n_clusters=so_cum, random_state=0, n_init=10)
    kmeans.fit(du_lieu)
    nhan_cum = kmeans.predict(du_lieu)
    tam_cum = kmeans.cluster_centers_
    return nhan_cum, tam_cum


def phan_cum_bang_kmeans(danh_sach_dac_trung, so_cum=11):
    """
    Phân cụm danh sách các đặc trưng sử dụng K-means,
    trả về danh sách các đối tượng Cluster.

    Tham số:
        - danh_sach_dac_trung: danh sách các đối tượng Feature.

    Trả về:
        - danh_sach_cum: danh sách các đối tượng Cluster, mỗi cụm chứa đặc trưng cùng loại.
    """
    du_lieu_vector = [f.dac_trung for f in danh_sach_dac_trung]
    nhan_cum, tam_cum = huan_luyen_kmeans(du_lieu_vector, so_cum)
    danh_sach_cum = []

    for i in range(len(tam_cum)):
        dac_trung_cum = []
        for j in range(len(nhan_cum)):
            if nhan_cum[j] == i:
                dac_trung_cum.append(danh_sach_dac_trung[j])
        cum = Cum(tam=tam_cum[i], dac_trung=dac_trung_cum)
        danh_sach_cum.append(cum)

    return danh_sach_cum


def luu_du_lieu(data):
    """
    Lưu dữ liệu dưới dạng JSON vào file.

    Tham số:
        - data: đối tượng bất kỳ có thể tuần tự hóa (thường là danh sách Cluster).
    """
    data_json = json.dumps(data)
    with open("sieu_du_lieu/dac_trung_am_thanh.json", "w") as file:
        file.write(data_json)
