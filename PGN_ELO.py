# import os
# import chess.pgn
# import chess.engine
# import csv
# # from tqdm import tqdm
#
# # 使用Stockfish引擎路径（根据你的安装位置调整）
# stockfish_path = "/home/aquila/Stockfish/src/stockfish"
#
# # 输出文件夹路径
# # output_folder = "equal_elo"
#
# # # 创建输出文件夹（如果不存在）
# # if not os.path.exists(output_folder):
# #     os.makedirs(output_folder)
#
# # 加载Stockfish引擎
# engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
#
#
def update_elo(player_elo, opponent_elo, result, K=40):
    # 计算期望得分
    expected_score = 1 / (1 + 10 ** ((opponent_elo - player_elo) / 400))

    # 计算新Elo
    new_elo = player_elo + K * (result - expected_score)

    return int(new_elo)
#
# # 判定条件
# def calculate_diff(object_elo, opponent_elo):
#     return True if abs(int(object_elo) - int(opponent_elo)) <= 50 else False
#
#
# def get_fen_for_move(board, move):
#     """
#     获取每步棋的FEN表示，增加合法性检查。
#     """
#     if board.is_legal(move):  # 只执行合法的棋步
#         board.push(move)
#         return board.fen()
#     else:
#         return None  # 如果棋步不合法，则返回None
#
#
# def process_pgn_file(pgn_file, player_name, output_folder):
#     """
#     处理PGN文件，转换为CSV格式。
#     """
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#     # 获取文件名中的关注棋手名字
#     base_name = os.path.basename(pgn_file)
#     name_part = base_name.split('_')[1].replace('.pgn', '')
#     elo_part = base_name.split('_')[0].replace('.pgn', '')  # 标准elo
#
#     # 输出CSV文件路径
#     output_file = os.path.join(output_folder, f"{base_name.replace('.pgn', '.csv')}")
#
#     with open(pgn_file, "r") as f, open(output_file, "w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#
#         # 写入表头
#         writer.writerow(["oponent_elo", "player_result"])
#
#         game_num = 1  # 当前游戏编号
#         total_games = 0  # 计数总游戏数
#
#         # 使用 tqdm 显示进度条
#         pgn_iterator = iter(lambda: chess.pgn.read_game(f), None)
#
#         for pgn_game in pgn_iterator:
#             if pgn_game is None:  # 处理文件中的空内容（防止文件末尾有空数据）
#                 continue
#
#             white_elo = int(pgn_game.headers["WhiteElo"])
#             black_elo = int(pgn_game.headers["BlackElo"])
#             board = chess.Board()
#             moves = list(pgn_game.mainline_moves())
#
#             # if (calculate_diff(elo_part, white_elo) and calculate_diff(elo_part, black_elo)) == False:  # 判定
#             #     continue
#
#             # else:
#             result = pgn_game.headers["Result"].split('-')  # 分割结果
#             oponent_elo = black_elo if pgn_game.headers["White"] == player_name else white_elo
#             player_result = result[0] if pgn_game.headers["White"] == player_name else result[1]
#             #  # 棋手是白棋
#             print(f"对手elo: {black_elo}, 结果为：{result[0]}") if pgn_game.headers["White"] == player_name else print(f"对手elo: {white_elo}, 结果为：{result[1]}")
#
#             writer.writerow([oponent_elo, player_result])
#
#
#             game_num += 1
#             total_games += 1
#
#         print(f"棋手 {player_name} 处理完毕，总计 {total_games} 局棋。")
#         print("-----------------------------------")
#         # 把oponent_elo和player_result存成数组并且导入到{output_folder}/{player_name}.csv中
#         # 搞定


def pgn_elo(pgn_game, player_name, player_elo):
    result = pgn_game.headers["Result"].split('-')  # 分割结果
    white_elo = int(pgn_game.headers["WhiteElo"])
    black_elo = int(pgn_game.headers["BlackElo"])
    oponent_elo = black_elo if pgn_game.headers["White"] == player_name else white_elo
    result = result[0] if pgn_game.headers["White"] == player_name else result[1]
    result = 0.5 if result == '1/2' else float(result)
    return update_elo(player_elo, oponent_elo, result, K=20)


# # 获取当前目录下所有pgn文件
# pgn_files = [f for f in os.listdir() if f.endswith(".pgn")]
#
# # 处理每个pgn文件
# for pgn_file in pgn_files:
#     # 提取文件名中的棋手名字
#     player_name = pgn_file.split('_')[1].replace('.pgn', '')
#     process_pgn_file(pgn_file, player_name)
#
# # 关闭Stockfish引擎
# engine.quit()
#
# print(f"所有PGN文件已经处理完毕。")
#
