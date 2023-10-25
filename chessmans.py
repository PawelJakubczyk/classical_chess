from utilities import type_validator


class Chessman:
    possibility_moves_list: list = []
    color_dict: dict = {'b': 'black', 'w': 'white'}
    move_count: int = 0
    move_memory_dict: dict = {}
    fields_status = [[[None, None, None] for _ in range(8)] for _ in range(8)]

    def __init__(self, row: int, column: int, colour: str) -> None:
        type_validator(row, 'int', 'Chessman')
        type_validator(column, 'int', 'Chessman')
        type_validator(colour, 'str', 'Chessman')
        if colour not in ['w', 'b']:
            raise ValueError('Class: Chessman - arg colour must be "w"(white) or "b"(black)')
        self.row = row
        self.column = column
        self.colour = colour
        self.enemy_colour = 'b' if colour == 'w' else 'w' if colour == 'b' else None

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.color_dict[self.colour]}'

    def calculate_moves(self, for_inheritance: bool = False) -> None:
        pass

    def print_possibility_move(self):
        chessboard = [['-' for _ in range(8)] for _ in range(8)]
        for field in self.possibility_moves_list:
            mark_row = field[0]
            mark_column = field[1]
            chessboard[mark_row][mark_column] = 'X'

        chessboard[self.row][self.column] = self.__class__.__name__[0]

        print("    " + " ".join([chr(65 + i) for i in range(8)]))
        for i in range(8):
            print(f"{8 - i}  " + " ".join(chessboard[i]))

    def print_all_statistic(self):
        print(f"""
        name:                   {self.__str__()}
        row:                    {self.row}
        column:                 {self.column}
        colour:                 {self.colour}
        move_count:             {self.move_count}
        move_memory_dict:       {self.move_memory_dict}
        fields_status:          {self.fields_status}
        possibility_moves_list: {self.possibility_moves_list}
        """)
        self.print_possibility_move()


class PawnTail(Chessman):
    def __str__(self) -> str:
        return ''


class Pawn(Chessman):

    def calculate_moves(self, for_inheritance: bool = False) -> None:
        self.possibility_moves_list = []

        match self.colour:
            case 'w':
                starting_row = 6
                step = -1
            case 'b':
                starting_row = 1
                step = 1
            case _:
                raise ValueError('Class: Chessman - arg colour must be "w"(white) or "b"(black)')

        # first move give 2 field move possibility
        if (self.row == starting_row
                and self.fields_status[self.row + 2 * step][self.column][0] is None
                and self.fields_status[self.row + step][self.column][0] is None):
            self.possibility_moves_list.append([self.row + 2 * step, self.column + 0])
        # normal move one step forward
        if self.fields_status[self.row + step][self.column][0] is None:
            self.possibility_moves_list.append([self.row + step, self.column + 0])
        # paws beats left and right side
        for side in [-1, 1]:
            # We make sure we have possibility moves inside board
            if (self.column + side in range(0, 8)
                    and (self.fields_status[self.row + step][self.column + side][0] == 'Enemy'
                         or self.fields_status[self.row + step][self.column + side][1] == 'Enemy_Tail')):
                self.possibility_moves_list.append([self.row + step, self.column + side])


class Knight(Chessman):
    chessman_range = [[-1, 2], [1, 2], [1, -2], [-1, -2], [-2, 1], [2, 1], [2, -1], [-2, -1]]

    def calculate_moves(self, for_inheritance: bool = True) -> list:
        if not for_inheritance:
            self.possibility_moves_list = []
        for move_row, move_col in self.chessman_range:
            # We make sure we have possibility moves inside board
            if (self.row + move_row in range(0, 8)
                    and self.column + move_col in range(0, 8)
                    # We make sure Ally block possibility to move
                    and self.fields_status[self.row + move_row][self.column + move_col][0] != 'Ally'):
                self.possibility_moves_list.append([self.row + move_row, self.column + move_col])
        return self.possibility_moves_list


class Bishop(Chessman):

    def calculate_moves(self, for_inheritance: bool = False) -> None:
        if not for_inheritance:
            self.possibility_moves_list = []

        to_up = self.row
        to_left = self.column
        to_down = 7 - self.row
        to_right = 7 - self.column

        directions = [
            (1, 1, min(to_right, to_down)),
            (-1, -1, min(to_left, to_up)),
            (-1, 1, min(to_right, to_up)),
            (1, -1, min(to_left, to_down))
        ]

        for hor_dir, vert_dir, limit_to_move in directions:
            for fields in range(1, limit_to_move + 1):
                fields_to_check = [self.row + fields * hor_dir, self.column + fields * vert_dir]
                match self.fields_status[self.row + fields * hor_dir][self.column + fields * vert_dir][0]:
                    case 'Ally':
                        break
                    case 'Enemy':
                        self.possibility_moves_list.append(fields_to_check)
                        break
                    case None:
                        self.possibility_moves_list.append(fields_to_check)


class Rock(Chessman):

    def calculate_moves(self, for_inheritance: bool = False) -> None:
        if not for_inheritance:
            self.possibility_moves_list = []

        directions = [
            (-1, 0, self.row),
            (0, -1, self.column),
            (1, 0, 7 - self.row),
            (0, 1, 7 - self.column)
        ]

        for hor_dir, vert_dir, limit_to_move in directions:
            for fields in range(1, limit_to_move + 1):
                fields_to_check = [self.row + fields * hor_dir, self.column + fields * vert_dir]
                match self.fields_status[self.row + fields * hor_dir][self.column + fields * vert_dir][0]:
                    case 'Ally':
                        break
                    case 'Enemy':
                        self.possibility_moves_list.append(fields_to_check)
                        break
                    case None:
                        self.possibility_moves_list.append(fields_to_check)


class Queen(Bishop, Rock):

    def calculate_moves(self, for_inheritance: bool = False) -> None:
        self.possibility_moves_list = []
        super(Queen, self).calculate_moves()
        super(Bishop, self).calculate_moves(True)
        super(Rock, self).calculate_moves(True)


class King(Knight):
    chessman_range = [[1, -1], [-1, 1], [1, 1], [-1, -1], [0, 1], [0, -1], [-1, 0], [1, 0]]

    def calculate_moves(self, for_inheritance: bool = True) -> None:
        super(King, self).calculate_moves()
        super(Knight, self).calculate_moves(True)
        if self.move_count == 0:
            if self.colour == 'w':
                print()
                if (self.fields_status[7][7][2] == 0
                        and self.fields_status[7][6][0] is None
                        and self.fields_status[7][5][0] is None):
                    pass
