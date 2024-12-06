import numpy as np

def generate_random_array(shape, distribution="uniform", params=None, seed=None):
    """
    生成随机数组的工具方法。

    :param shape: tuple，指定数组的形状，例如 (3, 4) 表示 3 行 4 列。
    :param distribution: str，指定随机数分布类型，可选值：
        - "uniform"：均匀分布（默认）。
        - "normal"：正态分布。
        - "integer"：随机整数。
    :param params: dict，分布的参数配置：
        - 均匀分布：{"low": 最小值, "high": 最大值}，默认 low=0, high=1。
        - 正态分布：{"mean": 均值, "std": 标准差}，默认 mean=0, std=1。
        - 随机整数：{"low": 最小值, "high": 最大值, "dtype": 类型}，默认 low=0, high=10。
    :param seed: int，随机数种子（可选），用于结果可复现。
    :return: np.ndarray，生成的随机数组。
    """
    if seed is not None:
        np.random.seed(seed)

    if params is None:
        params = {}

    if distribution == "uniform":
        low = params.get("low", 0)
        high = params.get("high", 1)
        return np.random.uniform(low, high, size=shape)
    
    elif distribution == "normal":
        mean = params.get("mean", 0)
        std = params.get("std", 1)
        return np.random.normal(mean, std, size=shape)
    
    elif distribution == "integer":
        low = params.get("low", 0)
        high = params.get("high", 10)
        dtype = params.get("dtype", int)
        return np.random.randint(low, high, size=shape, dtype=dtype)
    
    else:
        raise ValueError("不支持的分布类型！可选值为 'uniform', 'normal', 'integer'。")

# 示例用法
if __name__ == "__main__":
    array_uniform = generate_random_array((3, 4), distribution="uniform", params={"low": 1, "high": 10})
    array_normal = generate_random_array((2, 3), distribution="normal", params={"mean": 0, "std": 1}, seed=42)
    array_integer = generate_random_array((4, 5), distribution="integer", params={"low": 0, "high": 20})

    print("均匀分布随机数组：\n", array_uniform)
    print("正态分布随机数组：\n", array_normal)
    print("随机整数数组：\n", array_integer)

