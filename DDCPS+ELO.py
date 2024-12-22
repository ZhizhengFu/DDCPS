import chess.pgn
import chess.engine
import pandas as pd
import os
from tqdm import tqdm
import numpy as np
import math
import matplotlib.pyplot as plt
a = 250        # Threshold
z = 1000         # Start point bias
sigma = 0      # Noise level
max_time = 120000  # Maximum time
dt = 1           # Time step
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

def drift_diffusion_model(v, a=1200, z=1000, sigma=0.1, max_time=1000, dt=1):
    x = z
    time = 0
    trajectory = [x]
    with tqdm(total=min(max_time, len(v)), desc="Simulation Progress") as pbar:
        while x < a and time < max_time and time < len(v):
            noise = np.random.normal(0, sigma)
            dr = v[time]*20 + noise
            x += dr
            trajectory.append(x)
            time += dt
            pbar.update(dt)
    if x >= 1000+a:
        decision = 1
    elif x <= 1000-a:
        decision = -1
    else:
        decision = 0
    return decision, trajectory

def ddm_model(path):
    df = pd.read_csv(path)
    if len(df) > 1000:
        open(path, 'w').close()
    cur_num = 0
    begin = 0
    cpl_calcu_win = 0
    cpl_calcu_loss = 0
    cpl_list = []

    for _, row in df.iterrows():
        if row['game_num'] != cur_num:
            if begin != 0:
                cpl_list.append((cpl_calcu_win - cpl_calcu_loss)/begin)
            cur_num = row['game_num']
            begin = 0
            cpl_calcu_win = 0
            cpl_calcu_loss = 0
            continue
        begin += 1
        if row['object'] == 1:
            cpl_calcu_win += f(row['CPL'])
        else:
            cpl_calcu_loss += f(row['CPL'])

    cpl_list = [x for x in cpl_list if isinstance(x, (int, float)) and not math.isnan(x)]
    decision, trajectory = drift_diffusion_model(cpl_list, a, z, sigma, max_time, dt)
    return decision, trajectory

def CPL(path):
    if os.path.getsize(path) == 0:
        print(f"File {path} is empty.")
        return

    data = pd.read_csv(path)
    batch_size = 1000
    num_batches = len(data) // batch_size + (1 if len(data) % batch_size != 0 else 0)

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(data))
        batch_data = data.iloc[start_idx:end_idx]

        previous_fen = None

        cpl_values = []
        for idx, row in tqdm(batch_data.iterrows(), total=len(batch_data)):
            current_fen = row["FEN"]
            if previous_fen is not None:
                cpl_value = evaluate_fen(previous_fen, current_fen)
                cpl_values.append(cpl_value)
            else:
                cpl_values.append(None)
                
            previous_fen = current_fen

        batch_data["CPL"] = cpl_values

        if i == 0:
            batch_data.to_csv(path, index=False, mode='w')
        else:
            batch_data.to_csv(path, index=False, mode='a', header=False)

def f(t):
    x = float(t)
    if x == 0:
        return 10
    elif x >=1 and x <=4:
        return 9
    elif x >=5 and x <=15:
        return 8
    elif x >=16 and x <=50:
        return 4
    elif x >=51 and x <=100:
        return 0
    elif x >=101 and x <=200:
        return -2
    elif x >=201 and x <=1000:
        return -4
    elif x > 1001:
        return -8
    else:
        return 0

def update_elo(player_elo, opponent_elo, result, K=20):
    expected_score = 1 / (1 + 10 ** ((opponent_elo - player_elo) / 400))
    new_elo = player_elo + K * (result - expected_score)
    return int(new_elo)

father_path = "./temp100"
file_path = []
output_csv = "data100.csv"
high_csv = "high100.csv"
low_csv = "low100.csv"
for root, dirs, files in os.walk(father_path):
    for file in files:
        if file.endswith(".pgn"):
            file_path.append(os.path.join(root, file))
name_list = ["asmena", "AmyPeng", "Matinkurdistan", "asbharath", "Gschach", "MishaMolotok", "kenzaburo", "exeComp", "lczero"]
fig, ax = plt.subplots(figsize=(10, 6))
for i, path in enumerate(file_path):
    current_elo = 0
    component_elo = 0
    data = []
    elo_list = []
    game_num = 0
    with open(path) as pgn:
        print("--------------------")
        print(path)
        game = chess.pgn.read_game(pgn)
        game_num = 0
        while game:
            game_num += 1
            data = []
            white_elo = game.headers.get("WhiteElo", "N/A")
            black_elo = game.headers.get("BlackElo", "N/A")
            white_player = game.headers.get("White", "")
            black_player = game.headers.get("Black", "")
            board = game.board()
            if white_player in name_list:
                current_elo = white_elo
                component_elo = black_elo
            elif black_player in name_list:
                current_elo = black_elo
                component_elo = white_elo
            else:
                print("Error")
                import pdb; pdb.set_trace()
            result = game.headers.get("Result", "N/A")
            if result == "1-0":
                win_value = 1
            elif result == "0-1":
                win_value = 0
            else:
                win_value = 0.5
            print(f"Game {game_num}: {white_player} ({white_elo}) vs. {black_player} ({black_elo}) win_value: {win_value}, current_elo: {current_elo}, component_elo: {component_elo}")
            move_num = 0
            for move in game.mainline_moves():
                move_num += 1
                board.push(move)
                now_elo = white_elo if move_num % 2 == 1 else black_elo
                
                if current_elo == now_elo:
                    object_value = 1
                else:
                    object_value = 0
                
                data.append({
                    "FEN": board.fen(),
                    "elo": current_elo,
                    "game_num": game_num,
                    "object": object_value
                })
            
            if game_num == 1:
                elo_list.append(int(current_elo))
            else:
                current_elo = update_elo(elo_list[-1], int(component_elo), win_value)
                elo_list.append(int(current_elo))
            df = pd.DataFrame(data)
            if df.empty:
                game = chess.pgn.read_game(pgn)
                continue
            if int(current_elo) - int(component_elo) >= 500:
                df.to_csv(output_csv, mode='w', header=True, index=False)
                if os.path.getsize(output_csv) > 0:
                    CPL(output_csv)
                    df = pd.read_csv(output_csv) 
                    df.to_csv(high_csv, mode='a', header=True, index=False)
                    decision, trajectory = ddm_model(high_csv)
                    if decision == 1:
                        elo_list[-1] += 200
                        open(high_csv, 'w').close()
            elif int(component_elo) - int(current_elo) >= 500:
                df.to_csv(output_csv, mode='w', header=True, index=False)
                if os.path.getsize(output_csv) > 0:
                    CPL(output_csv)
                    df = pd.read_csv(output_csv)
                    df.to_csv(low_csv, mode='a', header=True, index=False)
                    decision, trajectory = ddm_model(low_csv)
                    if decision == -1:
                        elo_list[-1] -= 200
                        open(low_csv, 'w').close()
            # elif abs(int(component_elo)-int(current_elo)) < 50:
            #     #todo
            #     continue

            game = chess.pgn.read_game(pgn)
            if game_num > 100:
                break
    elo_list = [x for x in elo_list if isinstance(x, (int, float)) and not math.isnan(x)]
    label = path.split("/")[-1].split(".")[0]
    plt.plot(elo_list, label=label)
    plt.legend()
    ax.set_xlabel('Time/Game Number')
    ax.set_ylabel('CPL')
    ax.set_title('Drift-Diffusion Model: Decision Variable Trajectory')
plt.show()
plt.savefig("CPL.png")