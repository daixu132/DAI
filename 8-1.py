#!/usr/bin/python3
import numpy as np
from matplotlib import pyplot as plt

# Read data from text files
data_array = np.loadtxt('data.txt', dtype=float)
sampling_freq, quantization = np.loadtxt('settings.txt', dtype = float)
# --------

# Configure the graph
GRAPH_WIDTH = 16    # inches
GRAPH_HEIGHT = 10   # inches
DPI = 400           # dots per inch
figure, axes = plt.subplots(figsize=(GRAPH_WIDTH, GRAPH_HEIGHT), dpi=DPI)

axes.minorticks_on()                                    # Enable tiny ticks
axes.grid(which='major', linestyle='-', linewidth=0.5)     
plt.grid(which='minor', linestyle='--', linewidth=0.3)

font = {'fontname':'DejaVu Serif'}
axes.set_title('Процесс зарядки и разрядки конденсатора в RC-цепочке', **font)
axes.set_ylabel('Напряжение, В', **font)
axes.set_xlabel('Время, с', **font)
# --------

# Set x and y limits
y_min = data_array.min()
y_max = data_array.max()
Y_OFFSET = 5     # %
Y_OFFSET /= 100 
axes.set_ylim([(1 - Y_OFFSET) * y_min, (1 + Y_OFFSET) * y_max])

x_min = 0   # Since measurements start from t = 0
x_max = data_array.size * (1 / sampling_freq)
X_OFFSET = 1    # %
X_OFFSET /= 100
axes.set_xlim([x_min, (1 + X_OFFSET) * x_max])
measurement_times = np.linspace(x_min, x_max, data_array.size)
# --------

# Draw
DISPLAY_SPACING = 15
LINE_COLOR = '#003f5c'
MARKER_COLOR = '#ffa600'
charging_time = data_array.argmax() * (1 / sampling_freq)
discharging_time = (data_array.size - data_array.argmax()) * (1 / sampling_freq)
TEXT_CONTENTS = f'Время зарядки: {charging_time:.1f}с\n' + f'Время разрядки: {discharging_time:.1f}с'
axes.text(0.95 * x_max, 0.85 * y_max,
          TEXT_CONTENTS, fontsize=8, 
          horizontalalignment='right',
          verticalalignment='top',
          wrap=True, bbox = {'facecolor': '#ef5675', 'alpha': 1},
          **font)
axes.plot(measurement_times[::DISPLAY_SPACING], data_array[::DISPLAY_SPACING], 
        color = LINE_COLOR,
        linestyle = '--', linewidth = 1,
        marker = 'o', ms = '3.1', mfc = MARKER_COLOR, mec = MARKER_COLOR,
        label='V(t)')
# -------
figure.savefig('V(t).svg')
axes.legend()
plt.show()