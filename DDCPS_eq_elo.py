import pandas as pd
import os

# 数据集所在的目录路径
dataset_path = '../dataset/name_cpl'

# 获取目录下所有的CSV文件
pgn_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]

# 遍历每个CSV文件
for games_file in pgn_files:
    # 构建完整的文件路径
    file_path = os.path.join(dataset_path, games_file)

    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 在这里可以继续处理df，进行后续操作
    print(f"Successfully loaded {games_file}")

    # 过滤出我们关注的棋手（object=1）
    df_filtered = df[df['object'] == 1]

    # 按照游戏编号（game_num）排序，确保按顺序处理每局
    df_filtered = df_filtered.sort_values('game_num')

    # 计算全部对局的CPL均值
    overall_cpl_mean = df_filtered['CPL'].mean()

    # 输出全部对局的CPL均值
    print(f"Overall CPL mean for {games_file}: {overall_cpl_mean}")

    # 按照游戏编号（game_num）分组，计算每局的CPL均值
    average_cpl_per_game = df_filtered.groupby('game_num')['CPL'].mean().reset_index()

    # 输出每局的CPL均值
    print(f"Average CPL per game for {games_file}:\n{average_cpl_per_game}")

    # 计算前一半对局的CPL均值
    halfway_index = len(df_filtered) // 2
    first_half = df_filtered.iloc[:halfway_index]
    second_half = df_filtered.iloc[halfway_index:]

    first_half_cpl_mean = first_half['CPL'].mean()
    second_half_cpl_mean = second_half['CPL'].mean()

    # 输出前一半和后一半的CPL均值
    print(f"First half CPL mean for {games_file}: {first_half_cpl_mean}")
    print(f"Second half CPL mean for {games_file}: {second_half_cpl_mean}")

    # 如果需要将结果保存到一个新的CSV文件
    average_cpl_per_game.to_csv(f'average_cpl_per_game_{games_file}', index=False)

    # 可以根据需要进一步处理或保存 `first_half_cpl_mean`, `second_half_cpl_mean`, 和 `overall_cpl_mean`


# import numpy as np
# import pandas as pd
# import math
#
# # 假设imported_polynomial已经加载
# imported_coefficients = np.load('/home/aquila/nurohw/dataset/coefficients.npy')
# imported_polynomial = np.poly1d(imported_coefficients)
#
# # 导入反函数，这里假设你已经有反函数 implemented
# imported_polynomial_inv = imported_polynomial  # 假设我们有反函数
#
# # 用于计算实际Elo更新的函数
# def update_elo_based_on_cpl(player_elo, game_data, K=0.001):
#     """
#     通过CPL来更新Elo评分
#
#     Parameters:
#     - player_elo: 当前棋手的Elo
#     - opponent_elo: 对手的Elo
#     - game_data: CSV数据文件路径，包含棋局步数和CPL值
#     - K: 更新因子（默认为40）
#
#     Returns:
#     - 更新后的Elo
#     """
#     # 读取游戏数据
#     df = pd.read_csv(game_data)
#
#     # 筛选出当前棋手（object == 1）
#     player_moves = df[df['object'] == 1]
#
#     # 计算实际CPL的平均值
#     avg_cpl = player_moves['CPL'].mean()
#     print(f"actual cpl: {avg_cpl}")
#
#     # 计算Elo的期望更新
#     expected_cpl = imported_polynomial(player_elo)
#     # print(f"expected cpl: {expected_cpl}")
#     # 计算新的Elo
#     new_elo = player_elo + K * (expected_cpl - avg_cpl)
#
#     return int(new_elo)
#
# # 示例：对一个棋手进行Elo更新
# player_elo = 1432
# name = ['1200_AmyPeng.csv', '1300_Matinkurdistan.csv', '1800_asmena.csv', '1900_Gschach.csv', '2200_MishaMolotok.csv', '2600_exeComp.csv', '2800_lczero.csv']
# for iter in name:
#     game_data = '/home/aquila/nurohw/dataset/name_cpl_eq/' + iter
#     print(iter)
#     new_player_elo = update_elo_based_on_cpl(player_elo, game_data)
#
#     # print(f"更新后的Elo: {new_player_elo}")
#
#
# # import numpy as np
# # import pandas as pd
# # import math
# #
# # # 假设imported_polynomial已经加载
# # imported_coefficients = np.load('/home/aquila/nurohw/dataset/coefficients.npy')
# # imported_polynomial = np.poly1d(imported_coefficients)
# #
# # # 导入反函数，这里假设你已经有反函数 implemented
# # imported_polynomial_inv = imported_polynomial  # 假设我们有反函数
# #
# # # 用于计算实际Elo更新的函数
# # def update_elo_based_on_cpl(player_elo, game_data, K=0.001):
# #     """
# #     通过CPL来更新Elo评分
# #
# #     Parameters:
# #     - player_elo: 当前棋手的Elo
# #     - opponent_elo: 对手的Elo
# #     - game_data: CSV数据文件路径，包含棋局步数和CPL值
# #     - K: 更新因子（默认为40）
# #
# #     Returns:
# #     - 更新后的Elo
# #     """
# #     # 读取游戏数据
# #     df = pd.read_csv(game_data)
# #
# #     # 筛选出当前棋手（object == 1）
# #     player_moves = df[df['object'] == 1]
# #
# #     # 计算实际CPL的平均值
# #     avg_cpl = player_moves['CPL'].mean()
# #     print(f"actual cpl: {avg_cpl}")
# #
# #     # 计算Elo的期望更新
# #     expected_cpl = imported_polynomial(player_elo)
# #     # print(f"expected cpl: {expected_cpl}")
# #     # 计算新的Elo
# #     new_elo = player_elo + K * (expected_cpl - avg_cpl)
# #
# #     return int(new_elo)
# #
# # # 示例：对一个棋手进行Elo更新
# # player_elo = 1432
# # name = ['1200_AmyPeng.csv', '1300_Matinkurdistan.csv', '1800_asmena.csv', '1900_Gschach.csv', '2200_MishaMolotok.csv', '2600_exeComp.csv', '2800_lczero.csv']
# # for iter in name:
# #     game_data = '/home/aquila/nurohw/dataset/name_cpl_eq/' + iter
# #     print(iter)
# #     new_player_elo = update_elo_based_on_cpl(player_elo, game_data)
# #
# #     # print(f"更新后的Elo: {new_player_elo}")
