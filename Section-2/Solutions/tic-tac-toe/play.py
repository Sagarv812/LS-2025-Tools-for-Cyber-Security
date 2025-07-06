import subprocess
import numpy as np

def parse_grid(output: str) -> np.ndarray:
    lines = output.strip().splitlines()
    grid_lines = [line.strip() for line in lines if line.strip().count(' ') == 2]

    grid = np.zeros((3, 3), dtype=int)
    for i, line in enumerate(grid_lines):
        symbols = line.split()
        for j, symbol in enumerate(symbols):
            if symbol == 'o':
                grid[i][j] = 1
            elif symbol == 'x':
                grid[i][j] = -1
    return grid

edges = [(0,1),(1,2),(2,1),(1,0)]
corners = [(0,0),(0,2),(2,0),(2,2)]
edge_corner_rel = [
    [2,3],
    [0,2],
    [0,1],
    [1,3]
]

def fill_row(board,row_num):
    col = list(board[row_num]).index(0)
    return (row_num, col)

def find_win_or_lose(board, win):
    num = 2 if win is True else -2
    row_sums = np.sum(board, axis=1)
    if num in row_sums:
        row_num = list(row_sums).index(num)
        return fill_row(board,row_num)
    
    col_sums = np.sum(board, axis=0)

    if num in col_sums:
        col_num = list(col_sums).index(num)
        for i in range(3):
            if (board[i][col_num] == 0):
                return (i,col_num)

    diag_sum = np.trace(board)
    if (diag_sum==num):
        diag = np.diag(board)
        idx = np.where(diag==0)[0][0]
        return (idx,idx)

    anti_diag = np.diag(np.fliplr(board))
    anti_diag_sum = np.sum(anti_diag)
    if anti_diag_sum==num:
        idx = np.where(anti_diag==0)[0][0]
        return (idx, 2-idx)

    return None


def strategy(board: np.ndarray) -> tuple[int, int]:
    print("My board is: ", board)
    if (board[1,1]==0):
        return (1,1)
    else:
        win = find_win_or_lose(board, True)
        lose = find_win_or_lose(board, False)
        if win is not None:
            return win
        elif lose is not None:
            return lose
        else:
            if_edges = [board[pos[0]][pos[1]] for pos in edges]
            if -1 in if_edges:
                idx = if_edges.index(-1)
                return corners[edge_corner_rel[idx][0]]

            if_corners = [board[pos[0]][pos[1]] for pos in corners]
            if -1 in if_corners:
                idx = if_corners.index(-1)
                for i in range(4):
                    if idx in edge_corner_rel[i]:
                        return edges[i]

            i, j = np.where(board == 0)
            return(i[0], j[0])



def run_game():
    # Start the executable process
    proc = subprocess.Popen(["./ttt"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1)

    board = np.zeros((3, 3), dtype=int)
    output = ""
    
    while True:
        line = proc.stdout.readline()
        if not line:
            break 

        output += line
        print(line, end="")  

        # Detect prompt for move
        if "Enter the block you want to mark" in line:
            board = parse_grid(output)
            move = strategy(board)
            if move is None:
                print("Game finished or board full.")
                break
            move_str = f"{move[0]},{move[1]}\n"
            print(f">>> Playing: {move_str.strip()}")
            proc.stdin.write(move_str)
            proc.stdin.flush()
            output = ""  

    proc.wait()

if __name__ == "__main__":
    run_game()
