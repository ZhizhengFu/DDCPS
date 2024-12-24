import chess.pgn
import pandas as pd
import os
# 读取 PGN 文件
# pgn_file = "/home/test/fuzz/code/stockfish/ficsgamesdb_202006_standard_nomovetimes_403950.pgn"  # 替换为你的PGN文件路径
# output_csv = "202006.csv"
def check_higher(object_elo, opponent_elo):
    return True if (int(object_elo) - int(opponent_elo)) >= 500 else False


def check_lower(object_elo, opponent_elo):
    return True if (int(object_elo) - int(opponent_elo)) <= -500 else False


def pgn_fen(game, fen_folder_lower, fen_folder_higher, player_name, game_num):
    # 初始化结果存储
    data = []
    if game:
        # 获取 Elo 信息
        white_elo = game.headers.get("WhiteElo", "N/A")
        black_elo = game.headers.get("BlackElo", "N/A")
        # 获取选手名字
        white_player = game.headers.get("White", "")
        black_player = game.headers.get("Black", "")
        if white_player == player_name:
            object_elo = white_elo
            opponent_elo = black_elo
        else:
            object_elo = black_elo
            opponent_elo = white_elo
        output_folder = " "
        if check_higher(object_elo, opponent_elo):
            output_folder = fen_folder_higher
        if check_lower(object_elo, opponent_elo):
            output_folder = fen_folder_lower
        if output_folder != " ":    #触发存储条件
            board = game.board()
            # 遍历每一步
            move_num = 0
            for move in game.mainline_moves():
                move_num += 1
                board.push(move)

                # 判断当前棋手的 Elo
                current_elo = white_elo if move_num % 2 == 1 else black_elo
                current_player = white_player if move_num % 2 == 1 else black_player

                if current_player == player_name:
                    object_value = 1
                else:
                    object_value = 0

                # 保存当前 FEN 和相关信息
                data.append({
                    "FEN": board.fen(),
                    "elo": current_elo,
                    "game_num": game_num,
                    "object": object_value
                })

            # 写入CSV文件
            df = pd.DataFrame(data)
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, player_name + ".csv")
            df.to_csv(output_path, mode='a', header=not pd.io.common.file_exists(output_path), index=False)
            data = []  # 清空数据列表
            print(f"已处理 {game_num} 局")
            if len(game.mainline_moves)>1000:   #结束决策
                pass
    return 0