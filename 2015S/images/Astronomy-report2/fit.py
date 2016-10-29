import numpy as np
from scipy import optimize
from numpy import cos

data = np.recfromcsv('sgrA.csv')

xdata = np.array([row[6] for row in data])
ydata = np.array([row[5] for row in data])

def fitf(parameter, x, y):
    A = parameter[0]
    B = parameter[1]
    C = parameter[2]
    return y - B / (1.0 + A * cos(x + C))

result = optimize.leastsq(fitf, [0.0, 0.0, 0.0], args=(xdata, ydata))
print(result)

