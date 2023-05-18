#!/usr/bin/env python
# coding: utf-8

# In[24]:


import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from IPython.display import HTML

delta = 0.5; w_0 = 2*np.pi/5

length = 10

def f(u, t):
    return np.array([
        u[1],
        - 2 * delta * u[1] - w_0 ** 2 * np.sin(u[0])
    ])

t_0 = 0; t_final = 50

M = 1000

tau = (t_final - t_0)/M
t = np.linspace(t_0, t_final, M + 1)

phi = np.zeros((M + 1, 2))

phi[0] = [5*np.pi/6, 0]

for n in range(M):
    k1 = f(phi[n], t[n])
    k2 = f(phi[n] + tau * k1/2, t[n]  + tau/2)
    k3 = f(phi[n] + tau * k2/2, t[n] + tau/2)
    k4 = f(phi[n] + tau * k3, t[n] + tau)
    phi[n + 1] = phi[n] + tau / 6 * (k1 + 2*k2 + 2*k3 + k4)

X = -length * np.sin(phi)
X = X[:, 0]

Y = -length * np.cos(phi)
Y = Y[:, 0]

circle_r = np.linspace(- np.pi * 50, 0, 50 * 50)
circle_l = np.linspace(0, np.pi * 50, 50 * 50)

fig, axs = plt.subplots(figsize=(8, 8), ncols=2, nrows=2, layout='tight')

axs[0][0].set_xlim((-11, 11))
axs[0][0].set_ylim((-11, 11))

camera = Camera(fig)
for i in range(0, phi.shape[0], 5):
    axs[0][0].plot([0, X[i]], [0, Y[i]], c='red')
    axs[0][0].scatter([X[i]], [Y[i]], c='red')
    axs[0][1].scatter(t[i], phi[i, 0], c='red')
    axs[1][0].scatter(t[i], phi[i, 1], c='red')
    axs[1][1].scatter(phi[i, 0], phi[i, 1], c='red')
    camera.snap()
anim = camera.animate()
HTML(anim.to_html5_video())

#axs[0][0].scatter([0], [0], c='black')
#axs[0][0].plot([0, 0], [-10, 0], 'b--')
axs[0][1].plot(t, phi[:, 0], c='blue')
axs[1][0].plot(t, phi[:, 1], c='red')
axs[1][1].plot(phi[:, 0], phi[:, 1], c='green')

HTML(anim.to_html5_video())


# In[ ]:




