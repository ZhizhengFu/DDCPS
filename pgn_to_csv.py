import chess.pgn
import pandas as pd

# 读取 PGN 文件
pgn_file = "/home/test/fuzz/code/stockfish/ficsgamesdb_202006_standard_nomovetimes_403950.pgn"  # 替换为你的PGN文件路径
output_csv = "202006.csv"

# 初始化结果存储
data = []
batch_size = 1000  # 每批次写入的条数

# 解析 PGN 文件
with open(pgn_file) as pgn:
    game_num = 0
    game = chess.pgn.read_game(pgn)  # 读取第一局
    while game:
        # 获取 Elo 信息
        white_elo = game.headers.get("WhiteElo", "N/A")
        black_elo = game.headers.get("BlackElo", "N/A")

        if abs(int(white_elo) - int(black_elo)) < 300:
            continue
        game_num += 1
        board = game.board()
        
        
        # 获取选手名字
        white_player = game.headers.get("White", "")
        black_player = game.headers.get("Black", "")

        # 谁赢了比赛
        result = game.headers.get("Result", "N/A")
        if result == "1-0":
            win_value = 1
        elif result == "0-1":
            win_value = 0
        else:
            win_value = 0.5
        
        # 遍历每一步
        move_num = 0
        for move in game.mainline_moves():
            move_num += 1
            board.push(move)
            
            # 判断当前棋手的 Elo
            current_elo = white_elo if move_num % 2 == 1 else black_elo
            
            current_player = white_player if move_num % 2 == 1 else black_player
            if current_player == white_player and win_value == 1:
                win = 1
            elif current_player == black_player and win_value == 0:
                win = 1
            else:
                win = 0
            
            if current_elo >= white_elo and current_elo >= black_elo:
                object_value = 1
            else:
                object_value = 0
            
            # 保存当前 FEN 和相关信息
            data.append({
                "FEN": board.fen(),
                "elo": current_elo,
                "game_num": game_num,
                "win": win,
                "object": object_value
            })
            
            # 每生成1000条数据写入一次CSV文件
            if len(data) >= batch_size:
                df = pd.DataFrame(data)
                df.to_csv(output_csv, mode='a', header=not pd.io.common.file_exists(output_csv), index=False)
                data = []  # 清空数据列表
                print(f"已处理 {game_num} 局")
        
        # 读取下一局
        game = chess.pgn.read_game(pgn)

# 将剩余数据保存到 CSV 文件
if data:
    df = pd.DataFrame(data)
    df.to_csv(output_csv, mode='a', header=not pd.io.common.file_exists(output_csv), index=False)

print(f"数据提取完成，结果已保存到 {output_csv}")