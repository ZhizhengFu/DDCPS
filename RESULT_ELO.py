import os
import csv
import matplotlib.pyplot as plt

# Elo评分计算公式
def update_elo(player_elo, opponent_elo, result, K=40):
    # 计算期望得分
    expected_score = 1 / (1 + 10 ** ((opponent_elo - player_elo) / 400))

    # 计算新Elo
    new_elo = player_elo + K * (result - expected_score)

    return int(new_elo)


def result_old_elo(folder_path, file, player_elo, elo_dict):
    with open(os.path.join(folder_path, file), mode='r') as f:
        player_name = file.split('_')[1].replace('.pgn', '')
        reader = csv.DictReader(f)

        # 初始化棋手的初始Elo
        player_elo = 1000

        # 保存该棋手每局后的Elo评分
        elo_history = [player_elo]

        # 遍历每一行比赛数据
        for row in reader:
            opponent_elo = int(row['oponent_elo'])

            # 修改此行代码来处理 '1/2' 的情况
            result = 0.5 if row['player_result'] == '1/2' else float(row['player_result'])

            # 更新棋手的Elo
            player_elo = update_elo(player_elo, opponent_elo, result)

            # 将新Elo保存到历史中
            elo_history.append(player_elo)

        # 将棋手的Elo历史保存到字典中
        elo_dict[player_name] = elo_history
        return elo_dict

#
# # 初始化字典保存每个棋手的Elo变化记录
# elo_dict = {}
# files_all = []
# folder_path_all = ["lower_elo", "equal_elo", "higher_elo"]
# for i in folder_path_all:
#     files_all.append(os.listdir(i))
#
# for i in range(len(files_all)):
#     files = files_all[i]
#     folder_path = folder_path_all[i]
#     # 遍历所有文件
#     for file in files:
#         # 提取棋手的名字（文件名中的第一部分）
#         player_name = file
#         # 读取每个文件
#         with open(os.path.join(folder_path, file), mode='r') as f:
#             reader = csv.DictReader(f)
#
#             # 初始化棋手的初始Elo
#             player_elo = 1000
#
#             # 保存该棋手每局后的Elo评分
#             elo_history = [player_elo]
#
#             # 遍历每一行比赛数据
#             for row in reader:
#                 opponent_elo = int(row['oponent_elo'])
#
#                 # 修改此行代码来处理 '1/2' 的情况
#                 result = 0.5 if row['player_result'] == '1/2' else float(row['player_result'])
#
#                 # 更新棋手的Elo
#                 player_elo = update_elo(player_elo, opponent_elo, result)
#
#                 # 将新Elo保存到历史中
#                 elo_history.append(player_elo)
#
#             # 将棋手的Elo历史保存到字典中
#             elo_dict[player_name] = elo_history
#
# # 输出结果
# print(elo_dict)
#
#
#
#
# fig, ax = plt.subplots(figsize=(10, 6))
#
# linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 10))]
# markers = ['o', 'v', '^', '<', '>', 's']
#
# i=0
# for player_name, elo_history in elo_dict.items():
#
#
#     color = 'blue' if 'lower' in player_name else ('red' if 'higher' in player_name else 'green')
#     linestyle = linestyles[i % len(linestyles)]
#     marker = markers[i % len(markers)]
#     label = player_name
#
#     ax.plot(elo_history, label=label, color=color, linestyle=linestyle, marker=marker)
#     ax.set_title('calculating elo')
#     ax.set_xlabel('Time/Game Number')
#     ax.set_ylabel('ELO')
#     ax.legend(loc='best')
#     ax.grid(True)
#     i+=1
# ax.axhline(y=1200, color='red', linestyle='--')
# ax.axhline(y=1300, color='red', linestyle='--')
# ax.axhline(y=1500, color='red', linestyle='--')
# ax.axhline(y=1800, color='red', linestyle='--')
# ax.axhline(y=1900, color='red', linestyle='--')
# plt.tight_layout()
#
#
# plt.savefig('trajectory_plot.png')
#
#
#

