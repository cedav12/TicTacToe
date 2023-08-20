def minimax(board, depth, is_maximizing):
    winner = evaluate(board)

    if winner == 'X':
        return {'score': 10 - depth, 'position': None}
    elif winner == 'O':
        return {'score': depth - 10, 'position': None}

    if is_maximizing:
        best_score = {'score': float('-inf'), 'position': None}
        for i in range(15):
            for j in range(15):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    if score['score'] > best_score['score']:
                        best_score = {'score': score['score'], 'position': (i, j)}
        return best_score
    else:
        best_score = {'score': float('inf'), 'position': None}
        for i in range(15):
            for j in range(15):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    if score['score'] < best_score['score']:
                        best_score = {'score': score['score'], 'position': (i, j)}
        return best_score


def evaluate():
    pass
