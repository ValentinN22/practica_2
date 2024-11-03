import generate
import draw
import check
import copy

TARGET = 10_000
games = generate.games()

def _crush_group(game, groups, key, points_to_add, simulation = 0):
    points = 0
    for group in groups[key]:
        if _validate_group(group, game):
            points += points_to_add
            if simulation == 0:
                for i in range(len(group)):
                    game[group[i][0]][group[i][1]] = 0
    return points
def _validate_group(group, game):
    for i in range(len(group)):
        if game[group[i][0]][group[i][1]] == 0:
            return False
    return True
def _initial_groups(game, simulation = 0):
    points = 0
    groups = check.for_groups(game)
    for key in groups:
        if key == 'linie_5':
            points += _crush_group(game, groups, key, 50, simulation)
        elif key == 'T':
            points += _crush_group(game, groups, key, 30, simulation)
        elif key == 'L':
            points += _crush_group(game, groups, key, 20, simulation)
        elif key == 'linie_4':
            points += _crush_group(game, groups, key, 10, simulation)
        elif key == 'linie_3':
            points += _crush_group(game, groups, key, 5, simulation)
        else:
            pass
    return points
def _gravity(game):
    for i in range(len(game)):
        write_row = len(game) - 1
        for j in range(len(game) - 1, -1, -1):
            if game[j][i] != 0:
                game[write_row][i] = game[j][i]
                write_row -= 1
        while write_row >= 0:
            game[write_row][i] = 0
            write_row -= 1
def _shuffle(game):
    while True:
        linie_1 = generate.random.randint(0,10)
        linie_2 = generate.random.randint(0,10)
        if linie_1 != linie_2: break
    game[linie_1], game[linie_2] = game[linie_2], game[linie_1]
    print(game)
    for i in range(len(game)):
        game[i][linie_1], game[i][linie_2] = game[i][linie_2], game[i][linie_1]
    print(game)
def _best_move(game):
    max_points = 0
    best_move = []
    # incercam fiecare schimbare posibila si cautam cea mai buna schimbare
    for i in range(len(game)):
        for j in range(len(game)):
            # schimbare la dreapta
            if j < len(game) - 1:
                game[i][j], game[i][j+1] = game[i][j+1], game[i][j]
                points = _initial_groups(game, 1)
                #print(points, f"[{i}][{j}] <-> [{i}][{j+1}]")
                if points > max_points:
                    best_move = [(i,j),(i,j+1)] 
                    max_points = points
                # se revine la forma initiala        
                game[i][j], game[i][j+1] = game[i][j+1], game[i][j]

            # schimbare in jos
            if i < len(game) - 1:
                game[i][j], game[i+1][j] = game[i+1][j], game[i][j]
                points = _initial_groups(game, 1)
                #print(points, f"[{i}][{j}] <-> [{i+1}][{j}]")
                if points > max_points:
                    best_move = [(i,j),(i+1,j)] 
                    max_points = points
                # se revine la forma initiala        
                game[i][j], game[i+1][j] = game[i+1][j], game[i][j]
    return max_points, best_move


def crush_candies(c, game, debug = 0):
    points = 0
    moves = 0
    while True:
        if points >= TARGET: break

        # Pasul 1: Cat timp exista formatiuni le eliminam
        while True:
            if debug:
                c.drawString(300, 750, f"Puncte:{points}, Mutari:{moves}")
                draw.games_2_pdf(c,game,"Joc initial sau joc dupa mutare")
            initial_points = _initial_groups(game)
            if initial_points == 0: break
            else:
                points += initial_points
                print(f"Puncte:{points}, Mutari:{moves}")
                if debug:
                    draw.games_2_pdf(c, game, "Eliminare toate formatiuni initiale")
                _gravity(game)
                if debug: 
                    draw.games_2_pdf(c, game, "Joc dupa gravitatie")
                game = generate.new_elements(game)
                if debug: 
                    draw.games_2_pdf(c, game, "Joc dupa generare elemente noi")
        # Pasul 2: Cautam cea mai buna mutare
        while True:
            # Pasul 2.1: Daca nu avem mutare facem shuffle jocului pana avem mutare
            points_from_move, best_move = _best_move(game)
            if points_from_move == 0:
                print("Shuffle")
                _shuffle(game)
            else:
                # se produce mutarea
                game[best_move[0][0]][best_move[0][1]], game[best_move[1][0]][best_move[1][1]] = game[best_move[1][0]][best_move[1][1]], game[best_move[0][0]][best_move[0][1]]
                # se incrementeaza mutarea
                moves += 1
                break
    return moves


if __name__ == '__main__':
    moves = 0
    for i in range(1, len(games) + 1):
        print('\n','\n',f"Jocul {i}")
        debug = 0
        if i < 5:
            # genereaza fisierul pdf pentru jocul initial
            path = f'games/game{i}.pdf'
            c = draw.canvas.Canvas(path, pagesize=draw.letter)
            draw.games_2_pdf(c, games[i],f"Jocul {i}")
            debug = 1
        moves += crush_candies(c, games[i], debug)
        if i < 5:
            c.save()
    print(f"Rezultat final: {moves} / 100 = {moves / 100}")
        
