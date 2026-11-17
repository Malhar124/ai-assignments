## Time Complexity :- O(N) for row and O(N) for column traversal
## Space Complexity:- O(1) {Constant Space}

def check_tic_tac_toe(board):
   
    for i in range(3):
        ## Check column
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return board[i][0]
        ## Check row
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return board[0][i]

        ## Check diagonls
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    for row in board:
        if ' ' in row:
            return "Unfinished"

    return "Draw"

grid = [
    ['X', 'O', 'X'],
    ['O', 'X', ' '],
    ['O', ' ', 'X']
]

print("Game Result:", check_tic_tac_toe(grid))