"""
1. Генерация (загрузка) данных
2. Примение к данным математической модели
3. Оформление итогов вычислений
"""
from typing import Tuple
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
import yaml
import addict


def load_config(config_path: str) -> addict.Dict:
    with open(config_path, 'r') as f:
        config = addict.Dict(yaml.unsafe_load(f.read()))
    return config


def get_data(config: addict.Dict) -> Tuple[np.ndarray, np.ndarray]:
    conf = config.model
    X = np.arange(conf.N)
    Y = conf.K * X + conf.B + np.random.normal(
        conf.NoiseMean, conf.NoiseScale, size=conf.N)  # kx + b
    return X, Y


def calc(X: np.ndarray, Y: np.ndarray, config: addict.Dict) -> Polynomial:
    return Polynomial.fit(X, Y, config.calc.PolyfitDegree, rcond=None)


def save_data(path: str, X: np.ndarray, Y: np.ndarray) -> None:
    np.savez_compressed(path, np.vstack((X, Y)).T)


def plot_results(X: np.ndarray, Y: np.ndarray, poly: Polynomial) -> None:
    plt.scatter(X, Y)
    plt.plot(X, poly(X), color='r')
    plt.show()


# 1. Генерация (загрузка) данных
config_path = 'test0.yaml'
config = load_config(config_path)
X, Y = get_data(config)
save_data('test_data0.bin', X, Y)
# 2. Примение к данным математической модели
poly = calc(X, Y, config)
# 3. Оформление итогов вычислений
plot_results(X, Y, poly)
