from copy import deepcopy
from typing import List, Optional
from utilities import type_validator, range_validator
from chess_pieces import (
    Chessman,
    Pawn as Pw,
    Knight as Kt,
    Bishop as Bp,
    Rock as Rk,
    Queen as Qn,
    King as Kg
)


# Definition of the ChessBoard class
class ChessBoard:
    # Initialization of the empty chess board
    board: List[List[Optional[Chessman]]] = [[None for _ in range(8)] for _ in range(8)]
    king_position_dict = {'b': [0, 4], 'w': [7, 4]}

    def __init__(self):
        """Constructor of the class"""
        self.create_board()

    def __str__(self) -> str:
        """Special method returning the string representation of the object"""

        def sp(num):
            return " " * num

        # Define the alphabetical header
        alphabet = f'{sp(7)}|{sp(6)}'.join(chr(65 + i) for i in range(8))
        alphabet_string = f'{sp(3)}|{sp(6)}{alphabet}{sp(7)}|\n'
        # Define the line vertical graduation
        vertical_graduation = '-' * 124
        # Define the board string
        board_string = alphabet_string + vertical_graduation

        for board_row in range(8):
            board_string += f'\n {board_row + 1} |'
            for column in range(8):
                chessman = self.board[board_row][column]
                if chessman is None:
                    board_string += f'{sp(14)}|'
                else:
                    board_string += f' {str(chessman).ljust(12)} |'
            board_string += f'\n{vertical_graduation}'
        return board_string

    def create_board(self) -> None:
        """Method for creating the initial chessboard and restart board"""
        w = 'w'
        b = 'b'

        self.board: List[List[Chessman | None]] = [
            [Rk(0, 0, b), Kt(0, 1, b), Bp(0, 2, b), Qn(0, 3, b), Kg(0, 4, b), Bp(0, 5, b), Kt(0, 6, b), Rk(0, 7, b)],
            [Pw(1, 0, b), Pw(1, 1, b), Pw(1, 2, b), Pw(1, 3, b), Pw(1, 4, b), Pw(1, 5, b), Pw(1, 6, b), Pw(1, 7, b)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pw(6, 0, w), Pw(6, 1, w), Pw(6, 2, w), Pw(6, 3, w), Pw(6, 4, w), Pw(6, 5, w), Pw(6, 6, w), Pw(6, 7, w)],
            [Rk(7, 0, w), Kt(7, 1, w), Bp(7, 2, w), Qn(7, 3, w), Kg(7, 4, w), Bp(7, 5, w), Kt(7, 6, w), Rk(7, 7, w)],
        ]

    def generate_fields_statuses(self, board: Optional[List[List[Optional[Chessman]]]] = None) -> dict:
        """
        Generates information about the status of fields on the chessboard.

        Returns a dictionary containing information about each square on the chessboard, including
        the location of the piece, its ownership, and the number of moves made for both colour.
        """
        if board is None:
            board = self.board

        black_fields_update = []
        white_fields_update = []
        for board_row in board:
            black_row_fields_update = []
            white_row_fields_update = []
            for field in board_row:
                if field is None:
                    white_row_fields_update.append([None, None, None])
                    black_row_fields_update.append([None, None, None])
                elif field.colour == 'w':
                    white_row_fields_update.append(['Ally', field.__class__.__name__, field.move_count])
                    black_row_fields_update.append(['Enemy', field.__class__.__name__, field.move_count])
                    if field.__class__.__name__ == 'King':
                        self.king_position_dict['w'] = [field.row, field.column]
                else:
                    white_row_fields_update.append(['Enemy', field.__class__.__name__, field.move_count])
                    black_row_fields_update.append(['Ally', field.__class__.__name__, field.move_count])
                    if field.__class__.__name__ == 'King':
                        self.king_position_dict['b'] = [field.row, field.column]

            black_fields_update.append(black_row_fields_update)
            white_fields_update.append(white_row_fields_update)

        return {'b': black_fields_update, 'w': white_fields_update}

    def update_fields_statuses_for_all_chess_pieces(self, board: List[List[Optional[Chessman]]] | None = None) -> None:
        """Use generate_fields_statuses method to update all fields_statuses list for all chess pieces"""

        if board is None:
            board = self.board
        update_dict = self.generate_fields_statuses(board=board)
        for board_row in self.board:
            for field in board_row:
                if field is not None:
                    field.fields_statuses = update_dict[field.colour]

    def get_all_chess_pieces_moves_for_colour(
            self, colour: str, board: List[List[Optional[Chessman]]] | None = None) -> list:
        """This function retrieves all possible moves for a specific color of chess pieces on the board.
        return a list containing all possible moves for the specified color of chess pieces."""
        if board is None:
            board = self.board
        all_moves: list = []
        for board_row in board:
            for field in board_row:
                if field is not None:
                    if field.colour == colour:
                        field.calculate_moves()
                        all_moves.extend(field.possibility_moves_list)
        return all_moves

    def classify_move_possibility_for_chess_pieces(self, pieces_colour: str) -> None:
        """Method for Chess Piece Movement Classification: Each class of chess pieces is equipped with the knowledge of
        available moves based class properties and on the king's vulnerability to checks."""

        def is_king_in_check(king_colour: str, board: List[List[Optional[Chessman]]] | None = None) -> bool:
            if board is None:
                board = self.board
            opponent_colour = 'b' if king_colour == 'w' else 'w' if king_colour == 'b' else None
            # Update chess piece field statuses
            self.update_fields_statuses_for_all_chess_pieces(board=board)
            # Collect all opponent moves to ensure the check condition is accurate
            enemy_move_list: list = self.get_all_chess_pieces_moves_for_colour(opponent_colour, board=board)
            # Check if the king is in check
            if self.king_position_dict[king_colour] in enemy_move_list:
                return True
            else:
                return False

        self.update_fields_statuses_for_all_chess_pieces()

        for board_row in self.board:
            for chessman in board_row:
                if chessman is not None:
                    if chessman.colour == pieces_colour:
                        chessman_row = chessman.row
                        chessman_column = chessman.column
                        chessman.calculate_moves()

                        # To ensure the safety of the King's moves, always verify if it is under threat before
                        # proceeding, either by repositioning the King or shielding it with other chess pieces.
                        for possibility_row, possibility_column in chessman.possibility_moves_list[:]:
                            temporary_board = deepcopy(self.board)
                            temporary_board[possibility_row][possibility_column] = chessman
                            temporary_board[chessman_row][chessman_column] = None
                            if is_king_in_check(chessman.colour, temporary_board):
                                chessman.possibility_moves_list.remove([possibility_row, possibility_column])
                            del temporary_board

    def move_chessman(self, from_row: int, from_col: int, to_row: int, to_col: int) -> None:

        # Argument Validations
        for arg in [from_row, from_col, to_row, to_col]:
            type_validator(arg, int, 'move_chessman')
            range_validator(arg, range(0, 8), 'move_chessman')

        chessman = self.board[from_row][from_col]
        if chessman is None:
            return

        self.classify_move_possibility_for_chess_pieces(chessman.colour)
        if [to_row, to_col] in chessman.possibility_moves_list:
            self.board[to_row][to_col] = deepcopy(chessman)
            self.board[to_row][to_col].move_count += 1
            self.board[to_row][to_col].row, chessman.column = to_row, to_col
            self.board[to_row][to_col].move_memory_dict[
                chessman.move_count] = f'{from_row}:{from_col}-{to_row}:{to_col}'
            self.board[from_row][from_col] = None
