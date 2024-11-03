import random

def games(no_of_games = 100):
    id = 1
    games = {i:0 for i in range(1,101)}
    while True:
        if id == 101:
            return games
        game = [[random.randint(1,4) for _ in range(11)] for _ in range (11)]
        games[id] = game
        id += 1
    return games

def new_elements(game):
    for i in range(len(game)):
        for j in range(len(game)):
            if game[i][j] == 0:
                game[i][j] = random.randint(1,4)
    return game

if __name__ == '__main__':
    test = games()
    print(test[1])

