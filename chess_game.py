import chess, sys

def handle_turn(board, player):
    while True:
        print(player + "'s turn")
        cmd = input("Enter a command: ")
        tokens = cmd.split(" ")
        if tokens[0].lower() == "h" or tokens[0].lower() == "help":
            print("h(elp) - prints this message")
            print("m(ove) <from> <to> - moves a piece to destination")
            print("l(ist) <location> - prints possible moves for a piece")
            print("q(uit) - exits the program")
        elif tokens[0].lower() == "m" or tokens[0].lower() == "move":
            if len(tokens) != 3:
                print("Invalid number of arguments!")
                continue
            piece_location = board.human_to_location(tokens[1])
            new_location = board.human_to_location(tokens[2])
            if board.get_piece(piece_location).get_owner() != player:
                print("Invalid move!")
                continue
            if not board.move(piece_location, new_location):
                print("Invalid move!")
                continue
            else:
                print(board)
                break
        elif tokens[0].lower() == "l" or tokens[0].lower() == "list":
            if len(tokens) != 2:
                print("Invalid number of arguments!")
                continue
            location = board.human_to_location(tokens[1])
            print(board.get_validated_board(location.row, location.column))
        elif tokens[0].lower() == "q" or tokens[0].lower() == "quit":
            sys.exit()
        else:
            print("Invalid command! Use h for help")

def two_player():
    board = chess.Board()
    player = "White"
    print(board)
    while True:
        handle_turn(board, player)
        player = "White" if player == "Black" else "Black"

def one_player():
    board = chess.Board()
    player = "White"
    print(board)
    while True:
        handle_turn(board, player)
        board.get_best_move("Black")
        print(board)

def main():
    mode = input("Enter a mode: ")
    if mode == "1":
        one_player()
    elif mode == "2":
        two_player()
    else:
        print("Invalid mode! Use 1 for one player and 2 for two player")
    
    

if __name__ == "__main__":
    main()