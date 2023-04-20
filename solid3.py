"""
1. Генерация (загрузка) данных
2. Примение к данным математической модели
3. Оформление итогов вычислений
"""
from __future__ import annotations
from datetime import datetime
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
import yaml
import addict
from pathlib import Path
from loguru import logger
from dataclasses import dataclass
import pickle


# @logger.catch(reraise=True)
def log_exception(exception: type[Exception], msg: str):
    # logger.error(msg)
    raise exception(msg)


def check_path(path: str | Path) -> Path:
    assert isinstance(path, (str, Path)), f'Path has a wrong type {type(path)}'
    if not path:
        log_exception(ValueError, 'Path is an empty string')
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        log_exception(FileNotFoundError, f'Config {path} is not exists')
    if path.is_dir():
        log_exception(EnvironmentError,
                      f'Path {path} is a directory, not file')
    return path


@dataclass
class DataFrame:
    X: np.ndarray
    Y: np.ndarray
    timestamp: float = 0
    path: str = ''

    def __post_init__(self):
        self.timestamp = datetime.now().timestamp()

    def save(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        self.path = str(path.resolve())
        with path.open('wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str | Path):
        path = check_path(path)
        with path.open('rb') as f:
            return pickle.load(f)


def load_config(config_path: str | Path) -> addict.Dict:
    config_path = check_path(config_path)
    with config_path.open() as f:
        config = addict.Dict(yaml.unsafe_load(f.read()))
    if config == {}:
        log_exception(EnvironmentError, f'Config {config_path} is empty')
    logger.success(f'Config {config_path} is loaded')
    return config


def get_data(config: addict.Dict) -> DataFrame:
    if (conf := config.model) == {}:
        log_exception(ValueError, f'Section `model` is empty: {config}')
    X = np.arange(conf.N)
    Y = conf.K * X + conf.B + np.random.normal(
        conf.NoiseMean, conf.NoiseScale, size=conf.N)  # kx + b
    if X.size and Y.size:
        return DataFrame(X=X, Y=Y)
    return log_exception(RuntimeError, 'Zero-size data calculated')


def calc(frame: DataFrame, config: addict.Dict) -> Polynomial:
    if (X := frame.X).shape != (Y := frame.Y).shape:
        return log_exception(
            ValueError, f'X and Y have different shapes: X{X.shape}, Y{Y.size}')
    return Polynomial.fit(X, Y, config.calc.PolyfitDegree, rcond=None)


def plot_results(frame: DataFrame, poly: Polynomial) -> None:
    plt.scatter(X := frame.X, frame.Y)
    plt.plot(X, poly(X), color='r')
    plt.show()


if __name__ == "__main__":
    # 1. Генерация (загрузка) данных
    config_path = 'test0.yaml'
    config = load_config(config_path)
    frame = get_data(config)
    # frame = load_data('test_data0.bin')
    frame.save('test_data0.bin')
    # 2. Примение к данным математической модели
    poly = calc(frame, config)
    # 3. Оформление итогов вычислений
    plot_results(frame, poly)
