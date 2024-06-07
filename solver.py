import numpy as np


def get_remained(data):
    """
    找到当前数组的反数字（即数组中不存在的数字）
    """
    return np.arange(1, 10)[~np.in1d(np.arange(1, 10), data)]


def get_sudoku(data, guess=False):
    """
    求解数独
    Args:
        data (np.array): 二维数组，其中每一个数组代表的是一个宫格，而不是一行数据
        guess (bool): 是否启用猜测模式：中低难度的数独每次遍历都能找到一个可以精准填入的数字，此时不用猜测算法效率更高，高难度的数独初始待填入的数字很多没法精确填入数字，此时需要猜测算法

    Returns:
        2D numpy array | None: 解出的数独矩阵
    """
    # 这里判断整个矩阵中是否有0，如果有，则进入填充模式，如果没有0了则说明已经填充完毕，返回结果矩阵
    if data.min() > 0:
        return data
    i = 9  # i代表第几宫格
    while i > 0:
        i -= 1
        if data[i].min() == 0:
            # np.arange(9)[data[i] == 0]获取当前宫格中的所有需要填充数字的位置的数组。j则是需要填充数字的位置
            for j in np.arange(9)[data[i] == 0]:
                useful_data = get_remained(data[i])  # 先找到当前宫格内还能填哪些数字
                if len(useful_data) == 1:
                    # 如果当前宫格内只有一个数字可以填，则直接填入
                    data[i][j] = useful_data[0]
                    i = 9  # 精准填充后回到最开始处
                    break
                # 如果当前宫格的数字会影响到其他宫格的可用数字，则在这些宫格中找到可用的数字
                unuseful = np.append(data[i // 3 * 3:i // 3 * 3 + 3, j // 3 * 3:j // 3 * 3 + 3],
                                     data[i % 3::3, j % 3::3]).flatten()
                useful_data = useful_data[np.in1d(useful_data, get_remained(unuseful))]
                if len(useful_data) == 1:
                    data[i][j] = useful_data[0]
                    i = 9
                    break
                elif len(useful_data) == 0:
                    return
                else:
                    if guess:
                        for t in useful_data:
                            data[i][j] = t
                            temp = get_sudoku(data.copy(), ~guess)  # 将多种可能性都带入进去，递归的查找,错的中途死
                            if temp is not None:
                                return temp
    if not guess:
        # 没有启用猜测模式，没算出来解的话自动用猜测算法重试
        return get_sudoku(data, ~guess)
