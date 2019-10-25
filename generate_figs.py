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
    text_file.close()

def combineDicts(dict1, dict2):
    new_dict = {}
    for key in np.unique(dict1.keys() + dict2.keys()):
        new_dict[key] = dict1[key] + dict2[key]
    return new_dict

def capAllWords(cities):
    result = ""
    for city in cities.split("/"):
        result_city = ""
        for word in city.split(" "):
            result_city += word.lower().capitalize() + " "
        result += result_city[:-1] + "/"
    return result[:-1]

def getProportions(won, lost):
    win_prop = []
    keys = []
    for key in won.keys():
        win_prop.append(float(won[key])/(lost[key] + won[key]))
        keys.append(capAllWords(key))
    return win_prop, keys

def ticketsFigure(summary, limit, num_games):
    # Destination Tickets
    combined_two_won = combineDicts(summary['2-player']['winning']['uncompleted'], summary['2-player']['winning']['completed'])
    combined_two_lost = combineDicts(summary['2-player']['losing']['uncompleted'], summary['2-player']['losing']['completed'])
    combined_four_won = combineDicts(summary['4-player']['winning']['uncompleted'], summary['4-player']['winning']['completed'])
    combined_four_lost= combineDicts(summary['4-player']['losing']['uncompleted'], summary['4-player']['losing']['completed'])
    prop_two, keys_two = getProportions(won=combined_two_won, lost=combined_two_lost)
    prop_four, keys_four = getProportions(won=combined_four_won, lost=combined_four_lost)
    if keys_two != keys_four:
        raise "keys_two and keys_four not equal"
    generateFigure(
        keys=orderXbyY(keys_two, prop_two),
        freq2=orderXbyY(prop_two, prop_two),
        freq4=orderXbyY(prop_four, prop_two),
        title="Destination Tickets",
        filename = "destination_tickets.eps",
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
    prop_two = [float(combined_two[key])/num_games for key in combined_two.keys()]
    prop_four = [float(combined_four[key])/num_games for key in combined_four.keys()]
    keys = [capAllWords(key) for key in combined_two.keys()]
    if combined_two.keys() != combined_four.keys():
        raise "keys not equal!"
    generateFigure(
        keys=orderXbyY(keys, prop_four)[:limit],
        freq2=orderXbyY(prop_two, prop_four)[:limit],
        freq4=orderXbyY(prop_four, prop_four)[:limit],
        title="Routes",
        filename = "routes.eps",
        colors = ['black', 'gold'],
        xlabel = "Claims per Game",
        include_lines = False
    )

readAndGenerate(filename='summary', limit=5, num_games=1000)