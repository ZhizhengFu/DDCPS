import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm
import math
a = 120000        # Threshold
z = 1000         # Start point bias
sigma = 0      # Noise level
max_time = 120000  # Maximum time
dt = 1           # Time step
k = 1          # ELO's K
father_path = "../name_cpl/"
father_path2 = "../name_cpl_lw/"
file_path = []
iteration = 0
file_path2 = []

def f(t):
    x = abs(t)
    signal = 1 if t > 0 else -1
    if x == 0:
        return 10 * signal
    elif x >=1 and x <=4:
        return 9 * signal
    elif x >=5 and x <=15:
        return 8 * signal
    elif x >=16 and x <=60:
        return 6 * signal
    elif x >=61 and x <=100:
        return 4 * signal
    elif x >=101 and x <=200:
        return 2 * signal
    elif x >=201 and x <=1000:
        return 1 * signal
    else:
        return 0

def drift_diffusion_model(v, a=1200, z=1000, sigma=0.1, max_time=1000, dt=1, k=1.0, signal=[]):
    x = z
    time = 0
    trajectory = [x]
    with tqdm(total=min(max_time, len(v)), desc="Simulation Progress") as pbar:
        while x < a and time < max_time and time < len(v):
            noise = np.random.normal(0, sigma)
            dr = -1*v[time]*20 + noise
            x += dr
            trajectory.append(x)
            time += dt
            pbar.update(dt)

    return trajectory


for root, dirs, files in os.walk(father_path):
    for file in files:
        if file.endswith(".csv"):
            file_path.append(os.path.join(root, file))
for root, dirs, files in os.walk(father_path2):
    for file in files:
        if file.endswith(".csv"):
            file_path.append(os.path.join(root, file))

fig, ax = plt.subplots(figsize=(10, 6))

linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 10))]
markers = ['o', 'v', '^', '<', '>', 's']

for i, path in enumerate(file_path):
    
    df = pd.read_csv(path)
    iteration += 1
    cur_num = 0
    begin = 0
    cpl_calcu_win = 0
    cpl_calcu_loss = 0
    elo_win = 0
    elo_loss = 0
    is_high_win = False
    cpl_list = []
    elo_list = []

    for index, row in df.iterrows():
        if row['game_num'] != cur_num:
            if begin != 0:
                cpl_list.append((cpl_calcu_win - cpl_calcu_loss)/begin)
                elo_list.append(abs(elo_win - elo_loss))
            cur_num = row['game_num']
            begin = 0
            cpl_calcu_win = 0
            cpl_calcu_loss = 0
            elo_win = 0
            elo_loss = 0
            if row['object'] == 1:
                elo_win = row['elo']
            else:
                elo_loss = row['elo']
            continue
        begin += 1
        if begin == 1:
            if row['object'] == 1:
                elo_win = row['elo']
            else:
                elo_loss = row['elo']
        if row['CPL'] > 1000:
            continue
        if row['object'] == 1:
            cpl_calcu_win += f(row['CPL'])
        else:
            cpl_calcu_loss += f(row['CPL'])

    cpl_list = [x for x in cpl_list if isinstance(x, (int, float)) and not math.isnan(x)]
    trajectory = drift_diffusion_model(cpl_list, a, z, sigma, max_time, dt, k)

    color = 'blue' if 'lw' in path else 'green'
    linestyle = linestyles[i % len(linestyles)]
    marker = markers[i % len(markers)]
    label = path.replace('../name_cpl_lw/', '').replace('../name_cpl/', '')

    ax.plot(trajectory, label=label, color=color, linestyle=linestyle, marker=marker)
    ax.set_title('Drift-Diffusion Model: Decision Variable Trajectory')
    ax.set_xlabel('Time/Game Number')
    ax.set_ylabel('CPL')
    ax.legend(loc='best')
    ax.grid(True)

ax.axhline(y=1050, color='red', linestyle='--', label='Threshold 1050')

plt.tight_layout()
plt.savefig('trajectory_plot.png')