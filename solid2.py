"""
1. Генерация (загрузка) данных
2. Примение к данным математической модели
3. Оформление итогов вычислений
"""
from __future__ import annotations
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
import yaml
import addict
from pathlib import Path
from loguru import logger


@logger.catch(reraise=True)
def log_exception(exception: type[Exception], msg: str):
    # logger.error(msg)
    raise exception(msg)


def load_config(config_path: str | Path) -> addict.Dict:
    if isinstance(config_path, str):
        config_path = Path(config_path)
    if not config_path.exists():
        log_exception(FileNotFoundError, f'Config {config_path} is not exists')
    if config_path.is_dir():
        log_exception(EnvironmentError,
                      f'Path {config_path} is a directory, not file')
    with config_path.open() as f:
        config = addict.Dict(yaml.unsafe_load(f.read()))
    if config == {}:
        log_exception(EnvironmentError, f'Config {config_path} is empty')
    logger.success(f'Config {config_path} is loaded')
    return config


def get_data(config: addict.Dict) -> tuple[np.ndarray, np.ndarray]:
    conf = config.model
    if conf == {}:
        log_exception(ValueError, f'Section `model` is empty: {config}')
    X = np.arange(conf.N)
    Y = conf.K * X + conf.B + np.random.normal(
        conf.NoiseMean, conf.NoiseScale, size=conf.N)  # kx + b
    return X, Y


def calc(X: np.ndarray, Y: np.ndarray, config: addict.Dict) -> Polynomial:
    if not X.size or not Y.size:
        log_exception(
            ValueError, f'Zero-size data detected: X({X.size} bytes), Y({Y.size} bytes)')
    if X.shape != Y.shape:
        log_exception(
            ValueError, f'X and Y have different shapes: X{X.shape}, Y{Y.size}')
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
