import fileinput
from dataclasses import dataclass


@dataclass
class BoardCell:
    num: int
    marked: bool = False


def play_bingo(nums_to_draw, boards):
    for drawn_num in nums_to_draw:
        mark_boards(boards, drawn_num)
        winner = get_winner(boards)
        if winner:
            return winner, drawn_num


def play_bingo_until_last_wins(nums_to_draw, boards):
    nboards = len(boards)
    winners = []
    while len(winners) < nboards:
        for drawn_num in nums_to_draw:
            mark_boards(boards, drawn_num)
            round_winners = get_round_winners(boards)
            if round_winners:
                remove_winning_boards(round_winners, boards)
                winners.extend([(winner, drawn_num) for _, winner in round_winners])
    return winners[-1]


def remove_winning_boards(winners, boards):
    for i, _ in sorted(winners, reverse=True):
        del boards[i]


def mark_boards(boards, drawn_num):
    for board in boards:
        for row in board:
            for board_cell in row:
                if board_cell.num == drawn_num:
                    board_cell.marked = True


def get_round_winners(boards):
    winners = []
    for i, board in enumerate(boards):
        if has_winner_row(board) or has_winner_column(board):
            winners.append((i, board))
    if not winners:
        return None
    return winners


def get_winner(boards):
    for board in boards:
        if has_winner_row(board) or has_winner_column(board):
            return board
    return None


def has_winner_row(board):
    return any(is_winner_sequence(row) for row in board)


def has_winner_column(board):
    ncols = len(board[0])
    cols = [[row[i] for row in board] for i in range(ncols)]
    return any(is_winner_sequence(col) for col in cols)


def is_winner_sequence(sequence):
    return all(board_cell.marked for board_cell in sequence)


def parse():
    def create_board(rows):
        return [[BoardCell(num=int(n)) for n in row] for row in rows]

    file = fileinput.input()
    nums_to_draw = [int(n) for n in file.readline().strip().split(",")]
    file.readline()

    boards = []

    new_board_rows = []
    for line in file:
        if line == "\n":
            boards.append(create_board(new_board_rows))
            new_board_rows = []
        else:
            new_board_rows.append(line.strip().split())
    boards.append(create_board(new_board_rows))

    return nums_to_draw, boards


def main():
    nums_to_draw, boards = parse()
    winner, winning_num = play_bingo(nums_to_draw, boards)
    print("winner:")
    print_board(winner)
    score = compute_score(winner, winning_num)
    print(f"Part 1: {score}\n")

    nums_to_draw, boards = parse()
    last_winner, winning_num = play_bingo_until_last_wins(nums_to_draw, boards)
    print("last winner:")
    print_board(last_winner)
    score = compute_score(last_winner, winning_num)
    print(f"Part 2: {score}")


def print_board(board):
    print("\n".join(" ".join(str(x.num) for x in row) for row in board))
    print()


def compute_score(winner, winning_num):
    unmarked = (
        board_cell.num for row in winner for board_cell in row if not board_cell.marked
    )
    return sum(unmarked) * winning_num


if __name__ == "__main__":
    main()
