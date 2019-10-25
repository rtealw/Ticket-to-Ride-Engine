import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict
import os

def orderXbyY(X, Y):
    ordered_X = [x for _, x in sorted(zip(Y,X), key = lambda pair: pair[0])]
    ordered_X.reverse()
    return ordered_X

def getTopXMostFrequent(freq_dict, top_x):
    keys = []
    freqs = []
    for key in freq_dict.keys():
        keys.append(key)
        freqs.append(freq_dict[key])
    ordered_keys = orderXbyY(keys, freqs)
    return ordered_keys[:top_x+1]

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

desirables = [['losing', 'uncompleted'], ['winning', 'routes'], ['winning', 'completed']]
desirable_titles = [
    "Losers' Uncompleted Destination Tickets",
    "Winners' Routes",
    "Winners' Completed Destination Tickets"
]

filenames = ["uncompleted", "routes", "completed"]

def generateFigures(summary, limit, num_games):
    for i in range(len(desirables)):
        desirable = desirables[i]
        freq_dict2 = summary['2-player'][desirable[0]][desirable[1]]
        freq_dict4 = summary['4-player'][desirable[0]][desirable[1]]
        keys2 = getTopXMostFrequent(freq_dict2, limit)
        keys4 = getTopXMostFrequent(freq_dict4, limit)
        shortened_keys = list(set(keys2 + keys4))
        freq2 = np.array([float(freq_dict2[key])/num_games for key in shortened_keys])
        freq4 = np.array([float(freq_dict4[key])/num_games for key in shortened_keys])
        sum_freq = np.array([x + y for x,y in zip(freq2, freq4)])
        ordered_keys = orderXbyY(shortened_keys, sum_freq)
        ordered_freq2 = orderXbyY(freq2, sum_freq)
        ordered_freq4 = orderXbyY(freq4, sum_freq)
        title = desirable_titles[i]
        filename = "{}.eps".format(filenames[i])

        generateFigure(
            keys=ordered_keys,
            freq2=ordered_freq2,
            freq4=ordered_freq4,
            title=title,
            filename = filename
        )

def readAndGenerate(filename, limit, num_games):
    file_name = 'output/{}.txt'.format(filename)
    text_file = open(file_name, 'r')
    summaries = text_file.readlines()
    for summary in summaries:
        #generateFigures(summary = eval(summary), limit=limit, num_games=num_games)
        ticketsFigure(summary = eval(summary), limit=limit, num_games=num_games)
        routesFigure(summary = eval(summary), limit=30, num_games=num_games)
        return
    text_file.close()

def combineDicts(dict1, dict2):
    new_dict = {}
    for key in np.unique(dict1.keys() + dict2.keys()):
        in_dict1 = 0 if key not in dict1 else dict1[key]
        in_dict2 = 0 if key not in dict2 else dict2[key]
        new_dict[key] = in_dict1 + in_dict2 
    return new_dict

def capAllWords(cities):
    result = ""
    for city in cities.split("/"):
        result_city = ""
        for word in city.split(" "):
            result_city += word.lower().capitalize() + " "
        result += result_city[:-1] + "/"
    return result[:-1]

def getProportions(won, lost, keys):
    win_prop = []
    for key in keys:
        num_won = 0 if key not in won else won[key]
        num_lost = 0 if key not in lost else lost[key]
        if num_won + num_lost == 0:
            win_prop.append(0)
        else:
            win_prop.append(float(num_won)/(num_lost + num_won))
    return win_prop

def ticketsFigure(summary, limit, num_games):
    # Destination Tickets
    combined_two_won = combineDicts(summary['2-player']['winning']['uncompleted'], summary['2-player']['winning']['completed'])
    combined_two_lost = combineDicts(summary['2-player']['losing']['uncompleted'], summary['2-player']['losing']['completed'])
    combined_four_won = combineDicts(summary['4-player']['winning']['uncompleted'], summary['4-player']['winning']['completed'])
    combined_four_lost= combineDicts(summary['4-player']['losing']['uncompleted'], summary['4-player']['losing']['completed'])
    keys = np.unique(
        combined_two_won.keys() + combined_two_lost.keys() + combined_four_lost.keys() + combined_four_won.keys()
    )
    prop_two = getProportions(won=combined_two_won, lost=combined_two_lost, keys=keys)
    prop_four = getProportions(won=combined_four_won, lost=combined_four_lost, keys=keys)
    generateFigure(
        keys=orderXbyY(keys, prop_two),
        freq2=orderXbyY(prop_two, prop_two),
        freq4=orderXbyY(prop_four, prop_two),
        title="Destination Tickets",
        filename = "summary_destination_tickets.eps",
        colors = ['gold', 'black'],
        xlabel = "Proportion of Wins",
        include_lines = True
    )

def routesFigure(summary, limit, num_games):
    combined_two = combineDicts(
        summary['2-player']['winning']['routes'],
        summary['2-player']['losing']['routes']
    )
    combined_four = combineDicts(
        summary['4-player']['winning']['routes'],
        summary['4-player']['losing']['routes']
    )
    print("summary")
    print(combined_two)
    print(combined_four)
    prop_two = [float(combined_two[key])/num_games for key in combined_two.keys()]
    prop_four = [float(combined_four[key])/num_games for key in combined_four.keys()]
    keys = [capAllWords(key) for key in np.unique(combined_two.keys() + combined_four.keys())]
    generateFigure(
        keys=orderXbyY(keys, prop_four)[:limit],
        freq2=orderXbyY(prop_two, prop_four)[:limit],
        freq4=orderXbyY(prop_four, prop_four)[:limit],
        title="Routes",
        filename = "summary_routes.eps",
        colors = ['black', 'gold'],
        xlabel = "Claims per Game",
        include_lines = False
    )

readAndGenerate(filename='summary', limit=5, num_games=10)

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
        appeared = 0 if key not in dictionary else float(dictionary[key]/num_games)
        array.append(appeared)
    return array


def readGames(filename, limit):
    tickets = {
        '2-player' : {'win_count': {}, 'lose_count': {}},
        '4-player' : {'win_count': {}, 'lose_count': {}}
    }
    routes = {
        '2-player' : {},
        '4-player' : {} 
    }
    num_games = 0
    games_file = open("output/{}".format(filename), 'r')
    for game in games_file:
        num_games += .5
        tickets = addToTickets(tickets=tickets, game=eval(game))
        routes = addToRoutes(routes=routes, game=eval(game))
    games_file.close()

    print("direct")
    print(routes)

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
    routes_two = postProcessRoutes(dictionary=routes['2-player'], keys = routes_keys, num_games=num_games)
    routes_four = postProcessRoutes(dictionary=routes['4-player'], keys = routes_keys, num_games=num_games)

    generateFigure(
        keys=[capAllWords(key) for key in orderXbyY(tickets_keys, tickets_two)],
        freq2=orderXbyY(tickets_two,tickets_two),
        freq4=orderXbyY(tickets_four,tickets_two),
        title="Destination Tickets",
        filename = "direct_destination_tickets.eps",
        colors = ['gold', 'black'],
        xlabel = "Proportion of Wins",
        include_lines = True
    )

    generateFigure(
        keys=[capAllWords(key) for key in orderXbyY(routes_keys, routes_four)[:limit]],
        freq2=orderXbyY(routes_two, routes_four)[:limit],
        freq4=orderXbyY(routes_four, routes_four)[:limit],
        title="Routes",
        filename = "direct_routes.eps",
        colors = ['black', 'gold'],
        xlabel = "Claims per Game",
        include_lines = False
    )



readGames("games.txt", limit = 30)