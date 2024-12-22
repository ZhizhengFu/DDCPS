import chess
import chess.engine
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
import os

# 定义引擎路径和加载引擎
STOCKFISH_PATH = "./stockfish-ubuntu-x86-64-avx2"

def evaluate_fen(previous_fen, current_fen):
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        
        # 评估上一局面
        previous_board = chess.Board(previous_fen)
        previous_info = engine.analyse(previous_board, chess.engine.Limit(depth=10))
        previous_evaluation = previous_info["score"].white().score(mate_score=10000)

        # 评估当前局面
        current_board = chess.Board(current_fen)
        current_info = engine.analyse(current_board, chess.engine.Limit(depth=10))
        current_evaluation = current_info["score"].white().score(mate_score=10000)

        # 如果任一局面已结束，返回 CPL 为 0
        if previous_evaluation is None or current_evaluation is None:
            engine.quit()
            return 0

        # 找到上一局面的最佳走法
        best_move = previous_info["pv"][0]
        previous_board.push(best_move)  # 应用最佳走法

        # 重新评估上一局面走一步后的局面
        best_previous_info = engine.analyse(previous_board, chess.engine.Limit(depth=10))
        best_previous_evaluation = best_previous_info["score"].white().score(mate_score=10000)

        # 计算 CPL
        cpl = abs(current_evaluation - best_previous_evaluation)
        engine.quit()
        return cpl
    except Exception as e:
        print(f"Error processing FEN: {previous_fen}, {current_fen}, {e}")
        return None

# 读取 CSV 文件
# file_path = []
# file_path_1 = []
# father_path = "name_csv/higher"
# for root, dirs, files in os.walk(father_path):
#     for file in files:
#         if file.endswith(".csv"):
#             file_path.append(os.path.join(root, file))
#             file_path_1.append(file)
# # for (path, path1) in zip(file_path,file_path_1):
path = "/home/test/fuzz/code/stockfish/name_csv/lower/1500_asbharath2.csv"
data = pd.read_csv(path)

# 分批处理数据
batch_size = 1000
num_batches = len(data) // batch_size + (1 if len(data) % batch_size != 0 else 0)

for i in range(num_batches):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, len(data))
    batch_data = data.iloc[start_idx:end_idx]

    # 初始化上一行的 FEN
    previous_fen = None

    # 使用多进程池并行处理，并显示进度条
    with Pool() as pool:
        cpl_values = []
        for idx, row in tqdm(batch_data.iterrows(), total=len(batch_data)):
            current_fen = row["FEN"]
            if previous_fen is not None:
                # 计算当前行和上一行的 CPL
                cpl_value = evaluate_fen(previous_fen, current_fen)
                cpl_values.append(cpl_value)
            else:
                cpl_values.append(None)  # 第一行没有上一局面
                
            # 更新上一行的 FEN
            previous_fen = current_fen

    # 将 CPL 列加入批处理数据
    batch_data["CPL"] = cpl_values

    # 写入文件
    if i == 0:
        batch_data.to_csv(f"name_cpl_lw/1500_asbharath2.csv", index=False, mode='w')
    else:
        batch_data.to_csv(f"name_cpl_lw/1500_asbharath2.csv", index=False, mode='a', header=False)
    break
