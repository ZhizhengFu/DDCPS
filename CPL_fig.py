import pandas as pd
import matplotlib.pyplot as plt

def draw_fig(elo_dict):
    fig, ax = plt.subplots(figsize=(10, 6))

    # linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 10))]
    # markers = ['o', 'v', '^', '<', '>', 's']

    i=0
    for player_name, elo_history in elo_dict.items():


        # color = 'blue' if 'lower' in player_name else ('red' if 'higher' in player_name else 'green')
        # linestyle = linestyles[i % len(linestyles)]
        # marker = markers[i % len(markers)]
        label = player_name

        ax.plot(elo_history, label=label)
        ax.set_title('calculating elo')
        ax.set_xlabel('Time/Game Number')
        ax.set_ylabel('ELO')
        ax.legend(loc='best')
        ax.grid(True)
        i+=1
    # ax.axhline(y=1200, color='red', linestyle='--')
    # ax.axhline(y=1300, color='red', linestyle='--')
    # ax.axhline(y=1500, color='red', linestyle='--')
    # ax.axhline(y=1800, color='red', linestyle='--')
    # ax.axhline(y=1900, color='red', linestyle='--')
    plt.tight_layout()


    plt.savefig('trajectory_plot.png')
