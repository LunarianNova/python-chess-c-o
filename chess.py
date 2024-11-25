import random

LETTERS = ["a", "b", "c", "d", "e", "f", "h", "i"]

class Location:
    __slots__ = ["row", "column"]
    
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def __repr__(self) -> str:
        return str((self.row, self.column))

    def __str__(self) -> str:
        return LETTERS[self.row].upper() + str(self.column+1)
    
    def __lt__(self, other) -> bool:
        if type(self) != type(other):
            raise TypeError("Cannot compare Location and " + str(type(other)) + " types!")
        return self.row < other.row and self.column < other.column

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            raise TypeError("Cannot compare Location and " + str(type(other)) + " types!")
        return self.row == other.row and self.column == other.column
    
    def __sub__(self, other):
        if type(self) != type(other):
            raise TypeError("Cannot subtract Location and " + str(type(other)) + " types!")
        return Location(self.row - other.row, self.column - other.column)
    
    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Cannot add Location and " + str(type(other)) + " types!")
        return Location(self.row + other.row, self.column + other.column)
    
    def __mul__(self, other):
        if type(other) != int:
            raise TypeError("Cannot multiply Location and " + str(type(other)) + " types!")
        return Location(self.row * other, self.column * other)
    
    def __hash__(self) -> int:
        return hash((self.row, self.column))

class Piece:
    __slots__ = ["__name", "__shorthand", "__moves", "__position", "__owner"]

    def __init__(self, name: str, shorthand: str, moves: list, position: Location, owner: str) -> None:
        self.__name = name
        self.__shorthand = shorthand
        self.__moves = moves
        if owner == "White":
            self.__moves = []
            for move in moves:
                if type(move) == Location:
                    self.__moves.append(move*-1)
                elif type(move) == list:
                    self.__moves.append([x*-1 for x in move])
        self.__position = position
        self.__owner = owner

    def __str__(self) -> str:
        return self.__shorthand + str(self.__position)
    
    def __repr__(self) -> str:
        return self.__shorthand + str(self.__position)

    def get_name(self) -> str:
        return self.__name
    
    def get_shorthand(self) -> str:
        return self.__shorthand
    
    def get_moves(self) -> list:
        return [x for x in self.__moves]
    
    def get_position(self) -> Location:
        return Location(self.__position.row, self.__position.column)
    
    def get_owner(self) -> str:
        return self.__owner
    
    def move(self, new_location: Location) -> None:
        self.__position = new_location

class Rook(Piece):
    def __init__(self, row: int, column: int, owner: str) -> None:
        moves = [[Location(0, x) for x in range(1, 8)]]
        moves.append([Location(0, -x) for x in range(1, 8)])
        moves.append([Location(x, 0) for x in range(1, 8)])
        moves.append([Location(-x, 0) for x in range(1, 8)])
        super().__init__("Rook", "R", moves, Location(row, column), owner)

class Knight(Piece):
    def __init__(self, row: int, column: int, owner: str) -> None:
        super().__init__("Knight", "N", [Location(2, 1), Location(2, -1), Location(-2, 1), Location(-2, -1), Location(1, 2), Location(1, -2), Location(-1, 2), Location(-1, -2)], Location(row, column), owner)

class Bishop(Piece):
    def __init__(self, row: int, column: int, owner: str) -> None:
        moves = [[Location(x, x) for x in range(1, 8)]]
        moves.append([Location(x, -x) for x in range(1, 8)])
        moves.append([Location(-x, x) for x in range(1, 8)])
        moves.append([Location(-x, -x) for x in range(1, 8)])
        super().__init__("Bishop", "B", moves, Location(row, column), owner)

class Queen(Piece):
    def __init__(self, row: int, column: int, owner: str) -> None:
        moves = [Location(0, x) for x in range(1, 8)]
        moves.append([Location(0, -x) for x in range(1, 8)])
        moves.append([Location(x, 0) for x in range(1, 8)])
        moves.append([Location(-x, 0) for x in range(1, 8)])
        moves.append([Location(x, x) for x in range(1, 8)])
        moves.append([Location(x, -x) for x in range(1, 8)])
        moves.append([Location(-x, x) for x in range(1, 8)])
        moves.append([Location(-x, -x) for x in range(1, 8)])
        super().__init__("Queen", "Q", moves, Location(row, column), owner)

class King(Piece):
    def __init__(self, row: int, column: int, owner: str) -> None:
        super().__init__("King", "K", [Location(-1, -1), Location(-1, 0), Location(-1, 1), Location(0, -1), Location(0, 1), Location(1, -1), Location(1, 0), Location(1, 1)], Location(row, column), owner)

class Pawn(Piece):
    def __init__(self, row: int, column: int, owner: str) -> None:
        self.__moves = [Location(1, 0), Location(2, 0)] if owner == "Black" else [Location(-1, 0), Location(-2, 0)]
        super().__init__("Pawn", "P", [Location(1, 0), Location(2, 0)], Location(row, column), owner)

    def move(self, new_location: Location) -> None:
        if len(self.__moves) == 2:
            self.__moves.pop()
        return super().move(new_location)
    
    def get_moves(self) -> list:
        return [x for x in self.__moves]

class Empty(Piece):
    def __init__(self, row: int, column: int) -> None:
        super().__init__("Empty Space", "-", [], Location(row, column), "None")

class Board:
    __slots__ = ["__board", "__white_pieces", "__black_pieces", "number_string"]

    def __init__(self) -> None:
        self.__white_pieces = []
        self.__black_pieces = []
        self.__initialize_board()
        self.number_string = "      1  2  3  4  5  6  7  8"

    def __repr__(self) -> str:
        board = ""
        for i in range(8):
            line = ""
            line += LETTERS[i] + "    "
            for piece in self.__board[i]:
                if piece.get_owner() != "None":
                    line += "\033[38;5;0;48;5;15m " + piece.get_shorthand() + " \033[0m" if piece.get_owner() == "White" else "\033[38;5;15;48;5;0m " + piece.get_shorthand() + " \033[0m"
                else:
                    line += " " + piece.get_shorthand() + " "
            board += line + "\n"
        board += "\n"
        board += self.number_string
        return board

    def __initialize_board(self) -> None:
        self.__board = []
        self.__board.append([Rook(0, 0, "Black"), Knight(0, 1, "Black"), Bishop(0, 2, "Black"), Queen(0, 3, "Black"), King(0, 4, "Black"), Bishop(0, 5, "Black"), Knight(0, 6, "Black"), Rook(0, 7, "Black")])
        self.__board.append([Pawn(1, x, "Black") for x in range(8)])
        for i in range(4):
            self.__board.append([Empty(2+i, x) for x in range(8)])
        self.__board.append([Pawn(6, x, "White") for x in range(8)])
        self.__board.append([Rook(7, 0, "White"), Knight(7, 1, "White"), Bishop(7, 2, "White"), Queen(7, 3, "White"), King(7, 4, "White"), Bishop(7, 5, "White"), Knight(7, 6, "White"), Rook(7, 7, "White")])
        self.__black_pieces = [piece for piece in self.__board[0] + self.__board[1]]
        self.__white_pieces = [piece for piece in self.__board[6] + self.__board[7]]

    def __generate_moves(self, player: str) -> dict:
        moves = {"raw": [], "piece": {}}
        if player == "White":
            pieces = self.__white_pieces
        elif player == "Black":
            pieces = self.__black_pieces
        for piece in pieces:
            piece_moves = self.__validate_moves(piece.get_position().row, piece.get_position().column)
            for move in piece_moves:
                moves["raw"].append(move)
                if move not in moves["piece"].keys():
                    moves["piece"][move] = [piece]
                else:
                    moves["piece"][move].append(piece)
        return moves

    def __validate_moves(self, row: int, column: int) -> list:
        moves = []
        piece = self.get_piece(Location(row, column))
        pos = piece.get_position()
        piece_moves = piece.get_moves()
        if piece.get_name() == "Pawn":
            if piece.get_owner() == "White":
                if self.get_piece(pos + Location(-2, 0)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(-2, 0)).get_owner() != "None" and len(piece_moves) == 2:
                    piece_moves.pop()
                if self.get_piece(pos + Location(-1, 0)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(-1, 0)).get_owner() != "None":
                    piece_moves = []
                if self.get_piece(pos + Location(-1, -1)).get_owner != piece.get_owner() and self.get_piece(pos + Location(-1, -1)).get_owner() != "None":
                    piece_moves.append(Location(-1, -1))
                if self.get_piece(pos + Location(-1, 1)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(-1, 1)).get_owner() != "None":
                    piece_moves.append(Location(-1, 1))
            else:
                if self.get_piece(pos + Location(2, 0)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(2, 0)).get_owner() != "None" and len(piece_moves) == 2:
                    piece_moves.pop()
                if self.get_piece(pos + Location(1, 0)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(1, 0)).get_owner() != "None":
                    piece_moves = []
                if self.get_piece(pos + Location(1, -1)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(1, -1)).get_owner() != "None":
                    piece_moves.append(Location(1, -1))
                if self.get_piece(pos + Location(1, 1)).get_owner() != piece.get_owner() and self.get_piece(pos + Location(1, 1)).get_owner() != "None":
                    piece_moves.append(Location(1, 1))
        for move in piece_moves:
            if type(move) == Location:
                if pos + move < Location(8, 8) and pos + move > Location(-1, -1):
                    if self.get_piece(pos + move).get_owner() != piece.get_owner():
                        moves.append(pos + move)
            elif type(move) == type([]):
                for m in move:
                    if pos + m < Location(8, 8) and pos + m > Location(-1, -1):
                        if self.get_piece(pos + m).get_owner() != piece.get_owner():
                            moves.append(pos + m)
                            if self.get_piece(pos + m).get_owner() != "None":
                                break
                        else:
                            break
        return moves
    
    def get_best_move(self, player: str) -> Location:
        piece_values = {"Pawn": 1, "Knight": 3, "Bishop": 3, "Rook": 5, "Queen": 9, "King": 10}
        move_values = {}
        moves = self.__generate_moves(player)
        for move in moves["raw"]:
            piece = self.get_piece(move)
            if piece.get_name() != "Empty Space":
                move_values[move] = piece_values[piece.get_name()]
        try:
            best_move = max(move_values, key=move_values.get)
            old_pieces = list(moves["piece"][best_move])
            min = 11
            for piece in old_pieces:
                if piece_values[piece.get_name()] < min:
                    min = piece_values[piece.get_name()]
                    old_piece = piece
            print("Opponent moved " + str(old_piece) + " to " + str(best_move))
            self.move(old_piece.get_position(), best_move)
        except ValueError:
            pieces = list(moves["piece"].keys())
            new_location = random.choice(pieces)
            old_pieces = list(moves["piece"][new_location])
            old_piece = random.choice(old_pieces)
            print("Opponent moved " + old_piece.get_shorthand() + " to " + str(new_location))
            self.move(old_piece.get_position(), new_location)

    def get_piece(self, location: Location) -> Piece:
        try:
            return self.__board[location.row][location.column]
        except IndexError:
            return Empty(location.row, location.column)
        
    def human_to_location(self, location: str) -> Location:
        return Location(LETTERS.index(location.lower()[0]), int(location[1])-1)
    
    def get_validated_board(self, row: int, column: int) -> str:
        moves = self.__validate_moves(row, column)
        board = ""
        for i in range(8):
            line = ""
            line += LETTERS[i] + "    "
            for piece in self.__board[i]:
                if piece.get_position() in moves:
                    line += "\033[48;5;57m " + piece.get_shorthand() + " \033[0m"
                else:
                    if piece.get_owner() != "None":
                        line += "\033[38;5;0;48;5;15m " + piece.get_shorthand() + " \033[0m" if piece.get_owner() == "White" else "\033[38;5;15;48;5;0m " + piece.get_shorthand() + " \033[0m"
                    else:
                        line += " " + piece.get_shorthand() + " "
            board += line + "\n"
        board += "\n"
        board += self.number_string
        return board
    
    def move(self, piece_location, new_location) -> bool:
        if new_location in self.__validate_moves(piece_location.row, piece_location.column):
            piece = self.get_piece(piece_location)
            piece.move(new_location)
            if self.get_piece(new_location).get_owner() == "Black":
                self.__black_pieces.remove(self.get_piece(new_location))
            elif self.get_piece(new_location).get_owner() == "White":
                self.__white_pieces.remove(self.get_piece(new_location))
            self.__board[new_location.row][new_location.column] = piece
            self.__board[piece_location.row][piece_location.column] = Empty(piece_location.row, piece_location.column)
            return True
        return False

def main():
    board = Board()
    print(board)
    while True:
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
            if not board.move(piece_location, new_location):
                print("Invalid move!")
            else:
                print(board)
        elif tokens[0].lower() == "l" or tokens[0].lower() == "list":
            if len(tokens) != 2:
                print("Invalid number of arguments!")
                continue
            location = board.human_to_location(tokens[1])
            print(board.get_validated_board(location.row, location.column))
        elif tokens[0].lower() == "q" or tokens[0].lower() == "quit":
            break
        else:
            print("Invalid command! Use h for help")
        

if __name__ == "__main__":
    main()