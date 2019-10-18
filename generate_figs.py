import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict

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

def shortenEdge(long_descriptions):
    result = []
    for edge in long_descriptions:
        result.append("/".join([city.replace(" ", "")[:4] for city in edge.split("/")]))
    #return long_descriptions
    return result

def generateFigure(keys, freq2, freq4, title, limit):
    df = pd.DataFrame(np.vstack((freq2, freq4)).T, index = keys)
    df.plot.barh(color = ['black', 'gold'])
    plt.title(title)
    plt.xlabel("Frequency (1000 Simulations)")
    plt.legend(
        ['Two', 'Four'],
        loc=0,
        title="Players"
    )
    plt.show()

desirables = [['losing', 'uncompleted'], ['winning', 'routes'], ['winning', 'completed']]
desirable_titles = [
    "Most Common Uncompleted Destination Tickets in Losers' Hands",
    "Most Common Routes in Winners' Hands",
    "Most Common Completed Destination Tickets in Winners' Hands"
]

def generateFigures(filename, limit):
    file_name = 'output/{}.txt'.format(filename)
    text_file = open(file_name, 'r')
    summary = eval(text_file.read())
    text_file.close()

    for i in range(len(desirables)):
        desirable = desirables[i]
        freq_dict2 = summary['2-player'][desirable[0]][desirable[1]]
        freq_dict4 = summary['4-player'][desirable[0]][desirable[1]]
        keys2 = getTopXMostFrequent(freq_dict2, limit)
        keys4 = getTopXMostFrequent(freq_dict4, limit)
        unique_keys = list(set(keys2 + keys4))
        shortened_keys = shortenEdge(unique_keys)
        freq2 = np.array([freq_dict2[key] for key in unique_keys])   
        freq4 = np.array([freq_dict4[key] for key in unique_keys])
        sum_freq = np.array([x + y for x,y in zip(freq2, freq4)])
        ordered_keys = orderXbyY(shortened_keys, sum_freq)
        ordered_freq2 = orderXbyY(freq2, sum_freq)
        ordered_freq4 = orderXbyY(freq4, sum_freq)
        title = desirable_titles[i]

        generateFigure(
            keys=ordered_keys,
            freq2=ordered_freq2,
            freq4=ordered_freq4,
            title=title,
            limit = limit
        )

generateFigures(filename='summary', limit=5)