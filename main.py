import os
import chess.pgn
import chess.engine
import csv
# from tqdm import tqdm
from PGN_to_FEN import pgn_fen
from PGN_ELO import pgn_elo
from CPL_fig import draw_fig

# 使用Stockfish引擎路径（根据你的安装位置调整）
stockfish_path = "/home/aquila/Stockfish/src/stockfish"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
# 路径设定
fen_folder_lower = "/home/aquila/nurohw/dataset/test_lw_fen"
fen_folder_higher = "/home/aquila/nurohw/dataset/test_hi_fen"
dataset_path = "/home/aquila/nurohw/dataset/name_pgn"
max_game_num = 1000



if __name__ == "__main__":
    # 获取dataset_path下所有pgn文件
    pgn_files = [f for f in os.listdir(dataset_path) if f.endswith(".pgn")]
    print(pgn_files)
    elo_dict = {}
    # 处理每个pgn文件
    for pgn_file in pgn_files:
        base_name = os.path.basename(pgn_file)
        player_name = base_name.split('_')[1].replace('.pgn', '')
        player_elo_init = int(base_name.split('_')[0].replace('.pgn', ''))  # 标准elo
        with open(os.path.join(dataset_path, pgn_file), "r") as f:
            player_elo_history = [player_elo_init]
            pgn_iterator = iter(lambda: chess.pgn.read_game(f), None)
            game_num = 1
            for pgn_game in pgn_iterator:   # 每一局
                if game_num > max_game_num:
                    continue
                player_elo_history.append(pgn_elo(pgn_game, player_name, player_elo_history[-1]))
                # player_elo_history[-1] += pgn_fen(pgn_game, fen_folder_lower, fen_folder_higher, player_name, game_num)
                # 在这里通过new_elo进行修正，使用已经读出来的cpl数据
                game_num += 1
            elo_dict[player_name] = player_elo_history

    draw_fig(elo_dict)
    # 关闭Stockfish引擎
    engine.quit()

    print(f"所有PGN文件已经处理完毕。")