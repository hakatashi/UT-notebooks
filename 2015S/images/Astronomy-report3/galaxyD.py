# -*- coding: UTF-8 -*-

from rk4 import rk4

import numpy as np
from numpy import random, sin, cos

from scipy.constants import *

from matplotlib import pyplot as plot, animation

Npar = 500
N2par = 500
Rh = 1.
Rb = 5. / 30.
Rd = Rb * 3
Rh2 = 1.
Rb2 = 5. / 30.
Rd2 = Rb2 * 3
mu = 0.5

particles = []
particles2 = []

galaxy2 = np.array([2., -1., 1., 0.])

# Step of calculation
N = 400
dt = 2. / N

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

def gravforce2(particle):
    global galaxy2
    (x, y) = particle
    sx = x - galaxy2[0]
    sy = y - galaxy2[2]
    r = np.sqrt(sx ** 2 + sy ** 2)

    if r <= Rb2:
        F = mu * r / (Rh2 * Rb2 ** 2)
    elif Rb2 <= r <= Rh2:
        F = mu / (r * Rh2)
    else:
        F = mu / (r ** 2)

    return [
        - F * (sx / r),
        - F * (sy / r),
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

for i in range(N2par):
    [gx, gvx, gy, gvy] = galaxy2
    theta = random.uniform(0, pi * 2)
    r = random.uniform(Rb2, Rd2)
    x = r * cos(theta) + gx
    y = r * sin(theta) + gy
    [Fx, Fy] = gravforce2((x, y))
    v = np.sqrt(r * np.sqrt(Fx ** 2 + Fy ** 2))
    particles2.append(np.array([x, - (y - gy) / r * v + gvx, y, (x - gx) / r * v + gvy]))

# Differentiation function
def F(t, status):
    global galaxy2, mu
    (x, vx, y, vy) = status
    [Fx, Fy] = gravforce((x, y))
    [Fx2, Fy2] = gravforce2((x, y))
    dvxdt = Fx + Fx2
    dxdt = vx
    dvydt = Fy + Fy2
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
image3 = None
count = 0

def update_plot(i):
    global image, image2, image3, particles, particles2, galaxy2, count
    t = i * dt
    particles_x = np.array([])
    particles_y = np.array([])
    for i, particle in enumerate(particles):
        particles[i] = rk4(t, particle, F, dt)
        particles_x = np.append(particles_x, [particle[0]])
        particles_y = np.append(particles_y, [particle[2]])
    particles2_x = np.array([])
    particles2_y = np.array([])
    for i, particle in enumerate(particles2):
        particles2[i] = rk4(t, particle, F, dt)
        particles2_x = np.append(particles2_x, [particle[0]])
        particles2_y = np.append(particles2_y, [particle[2]])
    galaxy2 = rk4(t, galaxy2, F2, dt)

    if image is not None:
        image.remove()
    if image2 is not None:
        image2.remove()
    if image3 is not None:
        image3.remove()
    image = plot.scatter(particles_x, particles_y)
    image2 = plot.scatter(galaxy2[0], galaxy2[2], s=200, c='r')
    image3 = plot.scatter(particles2_x, particles2_y, c='g')

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
ax.set_xlim([-2., 2.])
ax.set_ylim([-2., 2.])

animate = animation.FuncAnimation(
    figure, update_plot,
    frames = N,
    interval = 1
)

plot.show();
