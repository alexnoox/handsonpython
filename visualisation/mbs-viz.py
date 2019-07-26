#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

#%%
data = [
    {'t': 1, 'lpt': 1.32, 'b':['9866|1.32', '9097|1.31', '19696|1.3', '20953|1.29'], 'l':['5230|1.33', '3751|1.34', '1183|1.35']},
    {'t': 2, 'lpt': 1.32, 'b':['9866|1.32', '9097|1.31', '19696|1.3', '20953|1.29'], 'l':['5230|1.33', '3751|1.34', '1183|1.35']},
    {'t': 3, 'lpt': 1.32, 'b':['9866|1.32', '9097|1.31', '19696|1.3', '20953|1.29'], 'l':['5230|1.33', '3751|1.34', '1183|1.35']}
]

t_x = [item['t'] for item in data]
b_y = [[b.split('|')[1] for b in item['b']] for item in data]
b_size = [[b.split('|')[0] for b in item['b']] for item in data]
l_y = [[l.split('|')[1] for l in item['l']] for item in data]
l_size = [[l.split('|')[0] for l in item['l']] for item in data]
print(len(t_x))
print(len(b_y))

#%%
fig, ax = plt.subplots()

for xe, ye in zip(t_x, b_y):
    plt.scatter([xe] * len(ye), ye, color=mcd.XKCD_COLORS['xkcd:lightblue'])
# print(zip(t_x, b_y))
for xe, ye in zip(t_x, l_y):
    plt.scatter([xe] * len(ye), ye, color=mcd.XKCD_COLORS['xkcd:salmon'])

plt.xlabel("Time (s)")
plt.ylabel("o")
plt.show()


#%%
