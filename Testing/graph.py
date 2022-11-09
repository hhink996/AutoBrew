
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import psutil
import collections

from mpu6050 import mpu6050
import time
mpu = mpu6050(0x68)

# function to update the data
def my_function():
    # get data
    cpu.popleft()
    accel_data = mpu.get_accel_data()
    cpu.append(accel_data['x'])
#    ram.popleft()
#    ram.append(psutil.virtual_memory().percent)

    # clear axis
    ax.cla()
#    ax1.cla()

    # plot cpu
    ax.plot(cpu)
    ax.scatter(len(cpu)-1, cpu[-1])
 #   ax.text(len(cpu)-1, cpu[-1]+2, "{}%".format(cpu[-1]))
    ax.set_ylim(0,100)

    # plot memory
#    ax1.plot(ram)
#    ax1.scatter(len(ram)-1, ram[-1])
#    ax1.text(len(ram)-1, ram[-1]+2, "{}%".format(ram[-1]))
#    ax1.set_ylim(0,100)

# start collections with zeros
cpu = collections.deque(np.zeros(10))
#accel_data = mpu.get_accel_data()
#ram = collections.deque(np.zeros(10))

# define and adjust figure
fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
ax = plt.subplot()
#ax1 = plt.subplot(122)
ax.set_facecolor('#DEDEDE')
#ax1.set_facecolor('#DEDEDE')

# animate
anim = FuncAnimation(fig, my_function(), interval=1000)
plt.show()
