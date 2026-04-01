
import sys
import math

def read_input():
    # 读取K
    K = int(sys.stdin.readline())

    # 读取K个初始聚类中心
    centers = []
    for _ in range(K):
        x, y, z = map(float, sys.stdin.readline().split())
        centers.append([x, y, z])

    # 读取迭代次数
    iterations = int(sys.stdin.readline())

    # 读取数据点个数
    m = int(sys.stdin.readline())

    # 读取m个数据点
    points = []
    for _ in range(m):
        x, y, z = map(float, sys.stdin.readline().split())
        points.append([x, y, z])

    return K, centers, iterations, points

def euclidean_distance(p1, p2):
    """计算三维欧氏距离"""
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2 +
        (p1[2] - p2[2]) ** 2
    )

def kmeans(K, initial_centers, iterations, points):
    centers = [center[:] for center in initial_centers]

    for _ in range(iterations):
        # 步骤1：分配每个点到最近的中心
        clusters = [[] for _ in range(K)]

        for point in points:
            min_dist = float('inf')
            best_cluster = 0

            for i, center in enumerate(centers):
                dist = euclidean_distance(point, center)
                if dist < min_dist:
                    min_dist = dist
                    best_cluster = i

            clusters[best_cluster].append(point)

        # 步骤2：更新聚类中心
        new_centers = []
        for index, cluster in enumerate(clusters):
            if not cluster:  # 防止空簇，保留对应的旧中心
                new_centers.append(centers[index])
            else:
                # 计算各维度的平均值
                n = len(cluster)
                avg_x = sum(p[0] for p in cluster) / n
                avg_y = sum(p[1] for p in cluster) / n
                avg_z = sum(p[2] for p in cluster) / n
                new_centers.append([avg_x, avg_y, avg_z])

        centers = new_centers

    return centers

def print_centers(centers):
    for center in centers:
        # 保留两位小数，四舍五入
        formatted = [f"{round(x, 2):.2f}" for x in center]
        print(" ".join(formatted))

def main():
    K, initial_centers, iterations, points = read_input()
    final_centers = kmeans(K, initial_centers, iterations, points)
    print_centers(final_centers)

if __name__ == "__main__":
    main()
