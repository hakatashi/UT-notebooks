unset polar
set parametric
set dummy t
set trange [0:2*pi]

plot 'sgrA.dat' using 2:4:3:5 with xyerrorbars,\
     (2.91e-2 / (1 - 8.62e-1 * cos(t + 1.10))) * cos(t),\
     (2.91e-2 / (1 - 8.62e-1 * cos(t + 1.10))) * sin(t),
