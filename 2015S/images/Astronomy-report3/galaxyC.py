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

    if r <= Rb:
        F = r / (Rh * Rb ** 2)
    elif Rb <= r <= Rh:
        F = 1. / (r * Rh)
    else:
        F = 1. / (r ** 2)

    return [
        - F * (x / r),
        - F * (y / r),
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

galaxy2 = np.array([1., -1., 1., -0.2])

# Step of calculation
N = 400
dt = 2. / N

# Differentiation function
def F(t, status):
    global galaxy2, mu
    (x, vx, y, vy) = status
    [Fx, Fy] = gravforce((x, y))
    # Distance to the galaxy2
    xdist = x - galaxy2[0]
    ydist = y - galaxy2[2]
    dist = np.sqrt(xdist ** 2 + ydist ** 2)
    dvxdt = Fx - (mu * xdist / dist ** 3)
    dxdt = vx
    dvydt = Fy - (mu * ydist / dist ** 3)
    dydt = vy
    return np.array([dxdt, dvxdt, dydt, dvydt])

# Differentiation function of galaxy2
def F2(t, status):
    (x, vx, y, vy) = status
    [Fx, Fy] = gravforce((x, y))
    dvxdt = Fx
    dxdt = vx
    dvydt = Fy
    dydt = vy
    return np.array([dxdt, dvxdt, dydt, dvydt])

image = None
image2 = None
count = 0

def update_plot(i):
    global image, image2, particles, galaxy2, count
    t = i * dt
    particles_x = np.array([])
    particles_y = np.array([])
    for i, particle in enumerate(particles):
        particles[i] = rk4(t, particle, F, dt)
        particles_x = np.append(particles_x, [particle[0]])
        particles_y = np.append(particles_y, [particle[2]])
    galaxy2 = rk4(t, galaxy2, F2, dt)

    if image is not None:
        image.remove()
    if image2 is not None:
        image2.remove()
    image = plot.scatter(particles_x, particles_y)
    image2 = plot.scatter(galaxy2[0], galaxy2[2], s=200, c='r')

    count += 1

    if count == N - 1:
        count_d = 0
        count_h = 0
        for i, particle in enumerate(particles):
            (x, vx, y, vy) = particle
            r = np.sqrt(x ** 2 + y ** 2)
            if r < Rd:
                count_d += 1
            if r < Rh:
                count_h += 1
        print('Stars inside disk: %d' % count_d)
        print('Stars inside halo: %d' % count_h)

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
