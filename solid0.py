"""
1. Генерация (загрузка) данных
2. Примение к данным математической модели
3. Оформление итогов вычислений
"""
import numpy as np
import matplotlib.pyplot as plt
import yaml
import addict

# 1. Генерация (загрузка) данных
config_path = 'test0.yaml'
with open(config_path, 'r') as f:
    config = addict.Dict(yaml.unsafe_load(f.read()))

X = np.arange(config.model.N)
Y = config.model.K * X + config.model.B + np.random.normal(
    config.model.NoiseMean, config.model.NoiseScale, size=config.model.N)  # kx + b
# 2. Примение к данным математической модели
k, b = np.polyfit(X, Y, config.calc.PolyfitDegree, rcond=None)
# 3. Оформление итогов вычислений
plt.scatter(X, Y)
plt.plot(X, k * X + b, color='r')
plt.show()
