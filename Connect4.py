def gameboard(col=7, row=6):
    '''gameboard([col=7, row=6]) -> list
    returns a start gameboard for the game'''
    # create a column
    column = ["." for i in range(row)]

    # create the board
    return [column[:] for i in range(col)]


def show_board(board):
    '''show_board(board) -> None
    converts board to string and prints it'''
    # print the column numbers
    for i in range(len(board)):
        print(i, end=" ")
    print()

    # print the board
    for i in range(len(board[0])-1, -1, -1):
        for col in board:
            print(col[i], end=" ")
        print()
    print()


def get_move_position(board, col):
    '''move(board, col, piece) -> (int, int) or None
    returns the gameboard with a move on it'''
    # check for the first occurence of "." and return the position
    for row in range(len(board[0])):
        if board[col][row] == ".":
            return (col, row)

    return None


def positive_slope_diagonal(board, pos):
    '''positive_slope_diagonal(board, pos) -> list
    returns a list of the positions of the right diagonal 
    with pos on board'''
    # set up pos
    (col, row) = pos

    # find the distance to the endpoints
    delta_start = min(col, row)
    delta_end = min(6-col, 5-row)

    # find the positions of the endpoints
    start = (col-delta_start, row-delta_start)
    end = (col+delta_end, row+delta_end)

    # put the diagonal positions into a list
    diagonal_list = [board[i][j] 
        for i, j in zip(range(start[0], end[0]+1), range(start[1], end[1]+1))]

    return diagonal_list


def negative_slope_diagonal(board, pos):
    '''negative_slope_diagonal(board, pos) -> list
    returns a list of the positions of the left diagonal 
    with pos on board'''
    # set up pos
    (col, row) = pos

    # find the distance to the endpoints
    delta_start = min(col, 5-row)
    delta_end = min(6-col, row)

    # find the positions of the endpoints
    start = (col-delta_start, row+delta_start)
    end = (col+delta_end, row-delta_end)

    # put the diagonal positions into a list
    diagonal_list = [board[i][j] 
        for i, j in zip(range(start[0], end[0]+1), range(start[1], end[1]-1, -1))]

    return diagonal_list


def get_max_repeat(string_list, ch):
    '''get_max_repeat(string_list, ch) -> int
    returns the frequency of the largest consecutive 
    occurence of ch in string_list'''
    # initialize the values for counting the frequencies
    max_frequency = 0
    frequency = 0
    
    for i in range(len(string_list)):
        # check if the next element is ch and increse frequency
        if string_list[i] == ch:
            frequency += 1
            max_frequency = max(max_frequency, frequency)
        # restart the count of frequency
        else:
            frequency = 0

    return max_frequency


def check_win(board, pos, piece, in_a_row=4):
    '''check_win(board, pos, piece[, in_a_row=4]) -> str, bool
    checks if a winning combination is achieved'''
    # set up pos
    (col, row) = pos

    # find a winning combination in the columns and rows
    win = get_max_repeat(board[col], piece) >= in_a_row
    row_list = [board[i][row] for i in range(len(board))]
    win = win or (get_max_repeat(row_list, piece) >= in_a_row)

    # find a winning combination in the diagonals
    right_diagonal = positive_slope_diagonal(board, pos)
    win = win or (get_max_repeat(right_diagonal, piece) >= in_a_row)
    left_diagonal = negative_slope_diagonal(board, pos)
    win = win or (get_max_repeat(left_diagonal, piece) >= in_a_row)

    return piece, win


def get_player(player_number):
    '''get_player(player_number) -> str
    returns the name of the player_number
    player'''
    # initialize player_name
    player_name = ""

    # check if player_name is just space
    while player_name.strip() == "":
        player_name = input("Player {}, please enter your name: ".format(player_number))

    return player_name


def get_player_move(player):
    '''get_player_move(player) -> int
    returns the column number which player 
    put his/her piece in'''
    while True:
        col = input("{}, in which column do you want to play? ".format(player))
        # make sure col is a valid input
        if col.strip() == "":
            print("Please enter a column number.\n")
        elif not col.isdigit():
            print("{} is not a nonnegative integer.\n".format(col))
        elif int(col) > 6:
            print("{} is not between 0 and 6.\n".format(col))
        else:
            return int(col)


def play_connect_4():
    '''play_connect_4() -> None
    plays a game of Connect 4'''
    # set up the players
    players = ["", ""]
    players[0] = get_player(1)
    print()
    players[1] = get_player(2)

    # set up the game pieces
    player_pieces = ["X", "O"]
    print()
    for i, j in zip(players, player_pieces):
        print("{}, you are piece {}.".format(i, j)) 
    print()

    # print the start gameboard
    board = gameboard()
    show_board(board)

    # initialize the first player
    current_player = 0
    player = players[current_player]
    player_piece = player_pieces[current_player]

    # play until someone will win or tie
    winner = False
    move_count = 0
    while not winner and move_count < 42:
        # check col
        while True:
            # get the column number and position
            col = get_player_move(player)
            pos = get_move_position(board, col)
            
            # check if column is full
            if pos is None:
                print("Column {} is already full. Please select another one.\n".format(col))
            # replace "." with player_piece
            else:
                (col, row) = pos
                board[col][row] = player_piece
                break

        # print the modified board
        print()
        show_board(board)

        # check if the current player won
        piece, winner = check_win(board, (col, row), player_piece)
        if winner:
            print("Congratulations {}, you have won!".format(player))
        # continue to the next player
        else:
            current_player += 1
            player = players[current_player % 2]
            player_piece = player_pieces[current_player % 2]
            move_count += 1
            
        # check for a tie
        if move_count == 42:
            print("Game Over! It is a tie.")


# play the game
play_connect_4()