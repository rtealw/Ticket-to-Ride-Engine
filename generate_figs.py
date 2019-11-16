import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def orderXbyY(X, Y):
    ordered_X = [x for _, x in sorted(zip(Y,X), key = lambda pair: pair[0])]
    ordered_X.reverse()
    return ordered_X

def generateFigure(keys, freq2, freq4, title, filename, colors, xlabel, include_lines):
    df = pd.DataFrame(np.vstack((freq2, freq4)).T, index = keys)
    df.plot.barh(color = colors)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.legend(
        ['Two', 'Four'],
        loc=0,
        title="Players"
    )
    # set up for my file system
    directory = "{}/../Ticket-to-Ride/paper/figures/".format(os.getcwd())
    plt.tight_layout()
    plt.xlim(0, max(freq2 + freq4) * 1.1)
    if include_lines:
        plt.axvline(x=.25,color='red', linestyle='--')
        plt.axvline(x=.5,color='red', linestyle='--')
    plt.savefig(directory + filename)

def capAllWords(cities):
    result = ""
    for city in cities.split("/"):
        result_city = ""
        for word in city.split(" "):
            result_city += word.lower().capitalize() + " "
        result += result_city[:-1] + "/"
    return result[:-1]

def addToTickets(tickets, game):
    num_player = '2-player' if len(game['players']) == 2 else '4-player'
    for player in game['players']:
        count = 'win_count' if player in game['winners'] else 'lose_count'
        for ticket in game[player]['completed'] + game[player]['uncompleted']:
            if ticket not in tickets[num_player][count]:
                tickets[num_player][count][ticket] = 0
            tickets[num_player][count][ticket] += 1
    return tickets

def addToRoutes(routes, game):
    num_player = '2-player' if len(game['players']) == 2 else '4-player'
    for player in game['players']:
        player_routes = game[player]['routes']
        for route in player_routes:
            if route not in routes[num_player]:
                routes[num_player][route] = 0
            routes[num_player][route] += 1
    return routes

def postProcessTickets(dictionary, keys):
    prop_win = []
    for key in keys:
        win_count = 0 if key not in dictionary['win_count'] else dictionary['win_count'][key]
        lose_count = 0 if key not in dictionary['lose_count'] else dictionary['lose_count'][key]
        ratio = 0 if win_count + lose_count == 0 else float(win_count) / (win_count + lose_count)
        prop_win.append(ratio)
    return prop_win

def postProcessRoutes(dictionary, keys, num_games):
    array = []
    for key in keys:
        appeared = 0 if key not in dictionary else float(dictionary[key])/num_games
        array.append(appeared)
    return array

def saveProportions(keys, props, filename):
    directory = "{}/../Ticket-to-Ride/scripts/input/".format(os.getcwd())
    file = open(directory + filename, 'w')
    file.write(str(list(keys)) + '\n')
    file.write(str(props) + '\n')
    file.close()

def anyRepeats(game):
    repeats = False
    for player in game['players']:
        routes = game[player]['routes']
        for route in routes:
            if routes.count(route) > 1:
                repeats = True
                print("player", player)
                print("route", route)
    if repeats:
        return True
    return False

def readGamesAndGenerateFigures(filename, limit):
    tickets = {
        '2-player' : {'win_count': {}, 'lose_count': {}},
        '4-player' : {'win_count': {}, 'lose_count': {}}
    }
    routes = {
        '2-player' : {},
        '4-player' : {} 
    }
    num_games_two = num_games_four = 0
    games_file1 = open("output/{}1.txt".format(filename), 'r')
    games_file2 = open("output/{}2.txt".format(filename), 'r')
    games_file3 = open("output/{}3.txt".format(filename), 'r')
    games_file4 = open("output/{}4.txt".format(filename), 'r')
    for game in games_file1.readlines() + games_file2.readlines() + games_file3.readlines() + games_file4.readlines():
        game = eval(game)
        if anyRepeats(game):
            print("game", game)
            raise "Player owns both double routes!"
        if len(game['players']) == 2:
            num_games_two += 1
        else:
            num_games_four += 1
        tickets = addToTickets(tickets=tickets, game=game)
        routes = addToRoutes(routes=routes, game=game)
    games_file1.close()
    games_file2.close()
    games_file3.close()
    games_file4.close()

    print("Number of games with two players: {}".format(num_games_two))
    print("Number of games with four players: {}".format(num_games_four))

    # Ticket Processing
    two_tickets = tickets['2-player']
    four_tickets = tickets['4-player']
    tickets_keys = np.unique(
        two_tickets['win_count'].keys() + two_tickets['lose_count'].keys() + four_tickets['win_count'].keys() + four_tickets['lose_count'].keys()
    )
    tickets_two = postProcessTickets(two_tickets, tickets_keys)
    tickets_four = postProcessTickets(four_tickets, tickets_keys)

    # Route Processing
    routes_keys = np.unique(routes['2-player'].keys() + routes['4-player'].keys())
    routes_two = postProcessRoutes(dictionary=routes['2-player'], keys = routes_keys, num_games=num_games_two)
    routes_four = postProcessRoutes(dictionary=routes['4-player'], keys = routes_keys, num_games=num_games_four)

    # Save Proportions
    saveProportions(keys=tickets_keys, props=tickets_two, filename="tickets_two.txt")
    saveProportions(keys=tickets_keys, props=tickets_four, filename="tickets_four.txt")
    saveProportions(keys=routes_keys, props=routes_two, filename="routes_two.txt")
    saveProportions(keys=routes_keys, props=routes_four, filename="routes_four.txt")

    generateFigure(
        keys=[capAllWords(key) for key in orderXbyY(tickets_keys, tickets_two)],
        freq2=orderXbyY(tickets_two,tickets_two),
        freq4=orderXbyY(tickets_four,tickets_two),
        title="Destination Tickets",
        filename = "destination_tickets.eps",
        colors = ['gold', 'black'],
        xlabel = "Proportion of Wins",
        include_lines = True
    )

    generateFigure(
        keys=[capAllWords(key) for key in orderXbyY(routes_keys, routes_four)[:limit]],
        freq2=orderXbyY(routes_two, routes_four)[:limit],
        freq4=orderXbyY(routes_four, routes_four)[:limit],
        title="Routes",
        filename = "routes.eps",
        colors = ['black', 'gold'],
        xlabel = "Claims per Game",
        include_lines = False
    )

readGamesAndGenerateFigures("games", limit = 30)