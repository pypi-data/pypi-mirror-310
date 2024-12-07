# pasir
granular-based simulation and related systems


## install
```batch
pip install pasir
```

## datasets

### binary and plot2
```py
from pasir.datasets.clasdata import binary
from pasir.datasets.dataviz import plot2

r1 = [0, 1.05, 0.05]
r2 = [0, 1.05, 0.05]
coeffs = [[0.41], [-1, -1], [1, 0, 1]]
x, y, z = binary(coeffs, r1=r1, r2=r2)

plot2(x, y, z)
```

With

$$\tag{1}
f(z) = \left\{
\begin{array}{lcr}
1, & z > 0, \newline
0, & z \le 0,
\end{array}
\right.
$$

and

$$\tag{2}
z = (x - 0.5)^2 + (y - 0.5)^2 - 0.3^2,
$$

which is the decision boundary.


## motion examples

### parabolic motion
```py
from pasir.butiran.color2 import Color2
from pasir.butiran.math.vect3 import Vect3
from pasir.butiran.grain import Grain
from pasir.butiran.force.gravitational import Gravitational

# define grain with initial position and velocity
grain = Grain(id="0002", m = 1)
grain.r = Vect3(0, 0, 0)
grain.v = Vect3(30, 40, 0)

# define gravitational field and force
g = Vect3(0, -10, 0)
gravitational = Gravitational(field=g)

import numpy as np

# define iteration
tbeg = 0
tend = 8
N = 100
dt = (tend - tbeg) / N

# define lists
data_t = []
data_x = []
data_y = []
data_vx = []
data_vy = []

# perform iteration
#print("#t x y vx vy")
print("Calculate position and velocity.")
for i in range(N + 1):
  t = i
  
  m = grain.m
  v = grain.v
  r = grain.r
  
  data_t.append(t)
  data_x.append(r.x)
  data_y.append(r.y)
  data_vx.append(v.x)
  data_vy.append(v.y)

  fg = gravitational.force(grain)
  a = fg / m
  v += a * dt
  r += v * dt
  
  grain.v = v
  grain.r = r
  
  #print(t, ' ', end='')
  #print(r.x, ' ', r.y, ' ', end='')
  #print(v.x, ' ', v.y)
  
print("Plot data.")
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

figure(figsize=(5,3.5), dpi=80)

plt.plot(data_x, data_y, c='r')
plt.xlabel('x')
plt.ylabel('y')

plt.grid()
plt.xlim([0, 240])
plt.ylim([0, 80])
plt.xticks(np.arange(0, 240+0.01, 40))
plt.yticks(np.arange(0, 80+0.01, 20))

plt.text(60, 39, "$v_x = 30$, $v_y = 40$, $m = 1$", fontsize=12)
plt.text(98, 30, "$g = -10$", fontsize=12)

print("Save figure.")
plt.savefig('parabolic_gravitational_euler.png', bbox_inches='tight')
```

### circular motion
```py
from butiran.color2 import Color2
from butiran.math.vect3 import Vect3
from butiran.grain import Grain
from butiran.force.magnetic import Magnetic

# define grain with initial position and velocity
grain = Grain(id="0001", m = 1, q = 1)
grain.r = Vect3(1, 0, 0)
grain.v = Vect3(0, 1, 0)

# define magnetic field and force
B = Vect3(0, 0, -1)
magnetic = Magnetic(field=B)

import numpy as np

# define iteration
tbeg = 0
tend = 2 * np.pi
N = 10000
dt = (tend - tbeg) / N

# define lists
data_t = []
data_x = []
data_y = []
data_vx = []
data_vy = []

# perform iteration
#print("#t x y vx vy")
print("Calculate position and velocity.")
for i in range(N + 1):
  t = i
  
  m = grain.m
  v = grain.v
  r = grain.r
  
  data_t.append(t)
  data_x.append(r.x)
  data_y.append(r.y)
  data_vx.append(v.x)
  data_vy.append(v.y)

  fB = magnetic.force(grain)
  a = fB / m
  v += a * dt
  r += v * dt
  
  grain.v = v
  grain.r = r
  
  #print(t, ' ', end='')
  #print(r.x, ' ', r.y, ' ', end='')
  #print(v.x, ' ', v.y)
  
print("Plot data.")
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

figure(figsize=(5,5), dpi=80)

plt.plot(data_x, data_y, c='r')
plt.xlabel('x')
plt.ylabel('y')

plt.grid()
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])
plt.xticks(np.arange(-1.5, 1.5+0.01, 0.5))
plt.yticks(np.arange(-1.5, 1.5+0.01, 0.5))

plt.text(-0.5, 0.2, "$B = 1, m = 1, q = 1$", fontsize=12)
plt.text(-0.4, -0.05, "$\Delta t = 2 \pi \ / \ 10^4$", fontsize=12)
plt.text(-0.3, -0.3, "$T \in [0, 2\pi]$", fontsize=12)

print("Save figure.")
plt.savefig('circular_magnetic_euler.png', bbox_inches='tight')
```
