import sys
sys.path.insert(0, 'scripts/')

from loadDestinationDeck import *
from loadMap import *
from ttrengine import *
from pathAgent import *
from hungryAgent import *
from oneStepThinkerAgent import *
from longRouteJunkieAgent import *

import time
import random
import copy

# board = pointer to object of class Board
# point_table = dict that maps the number of trains used to how many points are awarded to the player (it sometimes changes between maps) (the table that is usually printed on the edge of the map)
# destination_deck = Dict of all destination cards in the game (cards should be of class DestinationCard)
# train_deck = list of all train cards in the game (use function make_train_deck)
# players => list of all players (objects of class Player) in the game
# current_player => index of the player in the list of players who should make the next move (it gets randomized on game setup)
# variants = List of values that change details in the game to be able to simulate different maps:
#	position 0, 1, 2, 3 => Rules for drawing from the destination deck
#			position 0: number of destination cards drawn at the setup
#			position 1: minumum number of destination cards players have to keep during the setup
# 			position 2: number of destination cards drawn when taking the action during the match
#			position 3: minumum number of destination cards players have to keep during the match when taking the action above
#	position 4  => Boolean / does longest route score points at the end of the game?
#	position 5  => Boolean / does globetrotter rule get scored at the end of the game? (See rules for TTR USA 1910)
#	position 6  => Boolean / use europe variant extra rules?
#	position 7  => Boolean / ALWAYS KEEP IT FALSE (meant for switzerland_variant rules, never finished implementation)
#	position 8  => Boolean / use nordic countries variant rules?
#	position 9  => Boolean / use india variant rules?
#	position 10 => number of train cards players start with during setup (Usually 4)
# 	position 11 => number of face up train cards during the game (Usually 5)
# 	position 12 => limit of wild cards face up at the same time (Usually 2 - it means that on the 3rd face up wild it will reshuffle)
#	position 13 => number of cards drawn for underground rule (TTR Europe) (Usually 3)
#	position 14 => number of leftover trains to trigger end of the game (Usually 2)
#	position 15 => amount of points won with longest route (Usually 10)
#	position 16	=> amount of points won with globetrotter (Usually 15)
#	position 17 => number of train cards draw on action (Usually 2)
#	position 18 => Boolean / use asia variant rules?
# Values for USA 1910 Variant with longest route and no globetrotter

def simulate_once(player_agents, agent_names):
	board = Board(loadgraphfromfile("gameContent/usa.txt"))
	dest_deck_dict = destinationdeckdict(dest_list=loaddestinationdeckfromfile("gameContent/usa_destinations.txt"), board="usa")

	player_list = [Player(hand=emptyCardDict(), number_of_trains=45, points=0) for i in range(len(player_agents))]
	game_object = Game(board=board.copy(), point_table=point_table(), destination_deck=dest_deck_dict.copy(), train_deck=make_train_deck(number_of_color_cards=12, number_of_wildcards=14), players=player_list, current_player=0, variants=[3, 2, 3, 1, True, False, False, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2, False])
	game_object.setup()

	# game = object of class
	# agents = list of agents that will play
	# filename = name of the file where you want to save the game logs
	gh = GameHandler(game=game_object, agents=player_agents, filename="test")

	# runnum = integer that gets appended to the log filename (useful if you are running multiple games in a loop)
	# save = boolean that chooses to save (True), or not (False), the game logs
	gh.play(runnum=0, save=False)

	game_result = {}

	for i in range(len(player_agents)):
	#	print("Player ", i, ":")
		player_result = gh.game.printScoring(i)
		game_result[agent_names[i]] = player_result
	#	print(player_result)	
	game_result['winners'] = [agent_names[i] for i in gh.game.winner()]

	#print("WINNER : ", gh.game.winner())
	#print("Unclaimed Routes: ", gh.game.getUnclaimedRoutes())
	return game_result

def simulate_wrapper(player_agents, agent_names):
	has_passed = False
	while not has_passed:
		try:
			return simulate_once(player_agents, agent_names)
		except:
			print("exception :(")

def simulate(iterations, starting_time, filename):
	four_agents = [HungryAgent(), PathAgent(), OneStepThinkerAgent(), LongRouteJunkieAgent()]
	four_names = ['Hungry', 'Path', 'OneStepThinker', 'LongRouteJunkie']
	results_product = {'completed' : {}, 'uncompleted' : {}, 'routes' : {}, 'players' : {}}
	results_outcome = {'winning' : copy.deepcopy(results_product), 'losing' : copy.deepcopy(results_product) }
	results = { '4-player' : copy.deepcopy(results_outcome), '2-player' : copy.deepcopy(results_outcome)}

	game_file = open("output/{}.txt".format(filename), "a")

	for i in range(iterations):
		one_game  = simulate_wrapper(player_agents = four_agents, agent_names = four_names)
		one_game["players"] = four_names
		print("Iteration: " + str(i) + ", Time Elapsed: " + str(round(time.time() - starting_time, 2)))
		game_file.write(str(one_game) + '\n')

	for i in range(iterations):
		two_names, two_agents = get2Agents(four_agents=four_agents, four_names=four_names, i=i)
		one_game = simulate_wrapper(player_agents = two_agents, agent_names = two_names)
		one_game["players"] = two_names
		print("Iteration: " + str(i+iterations) + ", Time Elapsed: " + str(round(time.time() - starting_time, 2)))
		game_file.write(str(one_game) + '\n')

	game_file.close()

	return results

def get2Agents(four_agents, four_names, i):
	first_index = i//3 % 4
	valid_choices = four_names[:first_index] + four_names[first_index + 1:]
	two_names = [four_names[first_index], valid_choices[i % 3]]
	two_agents = []
	for name in two_names:
		if name == 'Hungry':
			two_agents.append(HungryAgent())
		if name == 'Path':
			two_agents.append(PathAgent())
		if name == 'OneStepThinker':
			two_agents.append(OneStepThinkerAgent())
		if name == 'LongRouteJunkie':
			two_agents.append(LongRouteJunkieAgent())
	if len(two_agents) != 2:
		raise "Two agent list does not have two agents"
	return two_names, two_agents


starting_time = time.time()
simulate(iterations=2, starting_time=starting_time, filename="games4")