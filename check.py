import numpy as np
import draw
import generate

def _check_group(game, formation):
    return (game[formation[0][0]][formation[0][1]] ==  game[formation[1][0]][formation[1][1]] == 
            game[formation[2][0]][formation[2][1]] == game[formation[3][0]][formation[3][1]] ==
            game[formation[4][0]][formation[4][1]] )

def _complex_groups(game):
    T_groups = []
    L_groups = []
    for i in range(len(game) - 2):
        for j in range(len(game) - 2):
            l_groups = [
                # L normal
                [(i, j), (i+1, j), (i+2, j), (i+2, j+1), (i+2, j+2)],
                # L rotit 90°
                [(i, j), (i, j+1), (i, j+2), (i+1, j), (i+2, j)],
                # L rotit 180°
                [(i, j), (i, j+1), (i, j+2), (i+1, j+2), (i+2, j+2)],
                # L rotit 270°
                [(i+2, j), (i+2, j+1), (i+2, j+2), (i+1, j+2), (i, j+2)]
            ]
            t_groups = [
                # T normal
                [(i, j), (i, j+1), (i, j+2), (i+1, j+1), (i+2, j+1)],
                # T rotit 90°
                [(i,j+2),(i+1,j+2),(i+2,j+2),(i+1,j+1),(i+1,j)],
                # T rotit 180°
                [(i,j+1),(i+1,j+1),(i+2,j+1),(i+2,j),(i+2,j+2)],
                # T rotit 270°
                [(i,j),(i+1,j),(i+2,j),(i+1,j+1),(i+1,j+2)]
            ]
            for L in l_groups:
                if _check_group(game,L):
                    L_groups.append(L)
            for T in t_groups:
                if _check_group(game, T):
                    T_groups.append(T)
    return T_groups, L_groups

def _lines_groups(game):
    lines_of_3 = []
    lines_of_4 = []
    lines_of_5 = []
    # linii orizontale
    for i in range(len(game)):
        j = 0
        while True:
            if j >= (len(game) - 2):
                break
            else:
                if game[i][j] and game[i][j] == game[i][j+1] == game[i][j+2]:
                    line = [(i,j),(i,j+1),(i,j+2)]
                    if j + 3 < len(game) and game[i][j] == game[i][j+3]:
                        line.append((i, j+3))
                        if j + 4 < len(game) and game[i][j] == game[i][j+4]: 
                            line.append((i, j+4))
                            lines_of_5.append(line)
                            j = j + 4
                        else:
                            lines_of_4.append(line) 
                            j = j + 3
                    else:
                        lines_of_3.append(line)
                        j = j + 2
                else: j+=1
    

    # # linii verticale
    for j in range(len(game)):
        i = 0
        while True:
            if i >= (len(game) - 2):
                break
            else:
                if game[i][j] and game[i][j] == game[i+1][j] == game[i+2][j]:
                    line = [(i,j),(i+1,j),(i+2,j)]
                    if i + 3 < len(game) and game[i][j] == game[i+3][j]:
                        line.append((i+3, j))
                        if i + 4 < len(game) and game[i][j] == game[i+4][j]: 
                            line.append((i+4, j))
                            lines_of_5.append(line)
                            i = i + 4
                        else:
                            lines_of_4.append(line) 
                            i = i + 3
                    else:
                        lines_of_3.append(line)
                        i = i + 2
                else: i+=1

    return lines_of_3, lines_of_4, lines_of_5


def for_groups(game):
    groups = {"linie_5":[], "T":[], 'L':[], 'linie_4':[], 'linie_3':[]}
    # Formatiuni de tip T si L
    complex_groups = _complex_groups(game)
    groups['T'] = complex_groups[0]
    groups['L'] = complex_groups[1]
    
    # Linii
    lines = _lines_groups(game)
    groups['linie_3'] = lines[0]
    groups['linie_4'] = lines[1]
    groups['linie_5'] = lines[2]
    return groups

if __name__ == '__main__':
    test = [[3,3,3,3,1,3,2,3,3,3,4],
            [4,4,4,4,4,1,2,2,2,3,2],
            [1,1,1,1,1,4,1,1,1,3,2],
            [1,4,2,4,0,3,2,1,2,1,1],
            [3,2,4,4,2,3,1,1,2,1,3],
            [3,2,4,3,1,1,2,2,2,1,3],
            [3,3,3,4,4,2,3,1,1,1,4],
            [1,4,3,3,4,3,4,4,1,1,4],
            [1,1,1,4,1,4,1,2,3,4,2],
            [1,4,2,1,2,1,2,3,4,4,4],
            [2,3,2,2,2,4,3,1,4,1,1]]
    groups = for_groups(test)
    for key in groups.keys():
        print(key)
        print(groups[key])
        print('\n\n')