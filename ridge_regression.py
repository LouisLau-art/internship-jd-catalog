
import sys

def matrix_transpose(matrix):
    """矩阵转置"""
    return list(map(list, zip(*matrix)))

def matrix_multiply(a, b):
    """矩阵乘法"""
    m = len(a)
    n = len(b[0])
    p = len(b)
    result = [[0.0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for k in range(p):
            if a[i][k] == 0:
                continue
            for j in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_inverse_3x3(matrix):
    """3x3矩阵求逆"""
    # 计算行列式
    det = (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
           matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
           matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

    # 伴随矩阵
    adjugate = [[0.0 for _ in range(3)] for _ in range(3)]
    adjugate[0][0] = matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]
    adjugate[0][1] = matrix[0][2] * matrix[2][0] - matrix[0][0] * matrix[2][2]
    adjugate[0][2] = matrix[0][0] * matrix[2][1] - matrix[0][1] * matrix[2][0]
    adjugate[1][0] = matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]
    adjugate[1][1] = matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]
    adjugate[1][2] = matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]
    adjugate[2][0] = matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]
    adjugate[2][1] = matrix[0][1] * matrix[2][2] - matrix[0][2] * matrix[2][1]
    adjugate[2][2] = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # 逆矩阵 = 伴随矩阵 / 行列式
    inverse = [[elem / det for elem in row] for row in adjugate]
    return inverse

def main():
    # 读取输入
    line1 = sys.stdin.readline().split()
    M, N = int(line1[0]), int(line1[1])

    data = []
    gap_positions = {}  # gap_name -> pos (1-based)

    for i in range(N):
        val = sys.stdin.readline().strip()
        if val.startswith("Gap_"):
            data.append(None)
            gap_positions[val] = i + 1  # 1-based
        else:
            data.append(float(val))

    # 按Gap_1到Gap_M的顺序处理
    sorted_gaps = sorted(gap_positions.items(), key=lambda x: int(x[0].split('_')[1]))

    lambda_val = 0.1

    for gap_name, pos in sorted_gaps:
        # 找left_start
        left_start = 1
        for i in range(pos - 2, -1, -1):  # pos-2到0（0-based）
            if data[i] is None:
                left_start = i + 2  # i是0-based，下一天是i+1，转1-based是i+2
                break

        # 找right_end
        right_end = N
        for i in range(pos, N):  # pos是0-based，从pos+1开始（即pos索引，因为pos是当前gap的位置）
            if data[i] is None:
                right_end = i  # i是0-based，前一天是i-1，转1-based是i
                break

        # 收集训练样本
        X_list = []
        y_list = []

        # 前方区间
        for day in range(left_start, pos):  # day是1-based
            idx = day - 1
            if data[idx] is not None:
                x = day
                X_list.append([x * x, x, 1.0])
                y_list.append([data[idx]])

        # 后方区间
        for day in range(pos + 1, right_end + 1):  # day是1-based
            idx = day - 1
            if data[idx] is not None:
                x = day
                X_list.append([x * x, x, 1.0])
                y_list.append([data[idx]])

        # 构建矩阵
        n_samples = len(X_list)
        X = X_list
        y = y_list

        # X^T * X
        X_T = matrix_transpose(X)
        XTX = matrix_multiply(X_T, X)

        # X^T * X + lambda * I
        I = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
        for i in range(3):
            XTX[i][i] += lambda_val

        # (X^T X + lambda I)^{-1}
        XTX_inv = matrix_inverse_3x3(XTX)

        # X^T y
        XTy = matrix_multiply(X_T, y)

        # beta = (X^T X + lambda I)^{-1} X^T y
        beta = matrix_multiply(XTX_inv, XTy)

        beta2 = beta[0][0]
        beta1 = beta[1][0]
        beta0 = beta[2][0]

        # 预测
        x_pred = pos
        y_pred = beta2 * x_pred * x_pred + beta1 * x_pred + beta0

        # 输出
        print(f"{gap_name}: {y_pred:.2f}")

if __name__ == "__main__":
    main()
