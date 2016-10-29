# -*- coding: UTF-8 -*-

from rk4 import rk4

import numpy as np
from numpy import random, sin, cos

from scipy.constants import *

from matplotlib import pyplot as plot, animation

Npar = 500
Rh = 1.
Rb = 5. / 30.
Rd = Rb * 3
mu = 0.05

particles = []

def gravforce(particle):
    (x, y) = particle
    r = np.sqrt(x ** 2 + y ** 2)
    return [
        - x / r ** 3,
        - y / r ** 3,
    ]

# Initialization

for i in range(Npar):
    theta = random.uniform(0, pi * 2)
    r = random.uniform(Rb, Rd)
    x = r * cos(theta)
    y = r * sin(theta)
    [Fx, Fy] = gravforce((x, y))
    v = np.sqrt(r * np.sqrt(Fx ** 2 + Fy ** 2))
    particles.append(np.array([x, - y / r * v, y, x / r * v]))

# Step of calculation
N = 400
dt = 2. / N

# Differentiation function
def F(t, status):
    (x, vx, y, vy) = status
    [Fx, Fy] = gravforce((x, y))
    dvxdt = Fx
    dxdt = vx
    dvydt = Fy
    dydt = vy
    return np.array([dxdt, dvxdt, dydt, dvydt])

image = None

def update_plot(i):
    global image, particles
    t = i * dt
    particles_x = np.array([])
    particles_y = np.array([])
    for i, particle in enumerate(particles):
        particles[i] = rk4(t, particle, F, dt)
        particles_x = np.append(particles_x, [particle[0]])
        particles_y = np.append(particles_y, [particle[2]])

    if image is not None:
        image.remove()
    image = plot.scatter(particles_x, particles_y)

figure = plot.figure()

ax = figure.add_subplot(1,1,1,aspect='equal')
ax.set_xlim([-1., 1.])
ax.set_ylim([-1., 1.])

animate = animation.FuncAnimation(
    figure, update_plot,
    frames = N,
    interval = 1
)

plot.show();
