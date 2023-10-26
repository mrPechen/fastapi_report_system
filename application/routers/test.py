def get_max_sheep_timestamp(data: list[list[int]]) -> int:
    count = 0
    index = []
    time = 0
    if len(data) == 1:
        return data[0][0]
    for i in range(len(data)):
        if data[i][2] == 1:
            if count < count + data[i][1]:
                count += data[i][1]
                time = data[i][0]
                index.append([time, count])
        elif data[i][2] == 0:
            count -= data[i][1]
            if data[i][0] == time:
                if len(index) != 0:
                    index.pop()
                    try:
                        time = min(map(max, index))
                    except Exception:
                        pass
    sorted(index)
    for j in range(1, len(index)):
        if index[j][1] == index[j-1][1]:
            time = index[0][0]
        else:
            time = index[-1][0]
    return time




data1 = [
    [1487799426, 21, 1]
]
assert get_max_sheep_timestamp(data1) == 1487799426

data2 = [
    [1487799425, 21, 1],
    [1487799427, 12, 1],
    [1487901318, 7, 0]
]
assert get_max_sheep_timestamp(data2) == 1487799427

data3 = [
    [1487799425, 21, 1],
    [1487799425, 21, 0],
    [1487901318, 7, 1]
]
assert get_max_sheep_timestamp(data3) == 1487901318

data4 = [
    [1487799425, 5, 1],
    [1487901318, 8, 1],
    [1487901318, 8, 0]
]
assert get_max_sheep_timestamp(data4) == 1487799425

data5 = [
    [1487799425, 14, 1],
    [1487799425, 4, 0],
    [1487799425, 2, 0],
    [1487800378, 10, 1],
    [1487801478, 18, 0],
    [1487801478, 18, 1],
    [1487901013, 1, 0],
    [1487901211, 7, 1],
    [1487901211, 7, 0]
]
assert get_max_sheep_timestamp(data5) == 1487800378

data6 = [
    [1487799425, 14, 1],
    [1487799425, 4, 1],
    [1487799425, 2, 1],
    [1487800378, 10, 1],
    [1487801478, 18, 1],
    [1487901013, 1, 1],
    [1487901211, 7, 1],
    [1487901211, 7, 1]
]
assert get_max_sheep_timestamp(data6) == 1487901211

data7 = [
    [1487799425, 14, 1], [1487799425, 4, 0], [1487799425, 2, 0],
    [1487800378, 10, 1], [1487801478, 18, 0], [1487801478, 19, 1],
    [1487801478, 1, 0], [1487801478, 1, 1], [1487901013, 1, 0],
    [1487901211, 7, 1], [1487901211, 8, 0]
]
assert get_max_sheep_timestamp(data7) == 1487801478

print('Completed!')