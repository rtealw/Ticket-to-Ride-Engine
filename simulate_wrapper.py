import simulate

def simulate_iterations(iterations=100, output="output/games.txt", agent_names = ["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"], point_table={1:1, 2:2, 3:4, 4:7, 5:10, 6:15}):
    wins = {"total" : 0, "LongRouteJunkie" : 0}
    output_file = open(output, "a")
    for iteration in range(iterations):
        reload(simulate)
        results = simulate.run_game(agent_names=agent_names, point_table=point_table)
        results['point_table'] = point_table
        output_file.write(str(results) + '\n')
#        for winner in results['winners']:
#            winner_name = agent_names[winner]
#            if winner_name not in wins:
#                wins[winner_name] = 0
#            wins[winner_name] += 1
#            wins["total"] += 1
#        current_prop = float(wins['LongRouteJunkie'])/wins["total"]
#        print "Iteration:", iteration, "Long Route Proportion", current_prop
#    print(wins)
    output_file.close()

def get_linear_point_table(alpha):
    point_table = {}
    for k in range(1, 7):
        point_table[k] = alpha * k
    return point_table

def float_range(start, stop, step):
    result = []
    for i in range(int((stop-start+step)/step)):
        result += [start + step * i]
    return result

def simulate_point_tables(iterations):
    for alpha in float_range(start=1, stop=2.5, step=.1):
        point_table = get_linear_point_table(alpha)
        print(point_table)
        simulate_iterations(
            iterations=iterations, 
            output="output/point_tables.txt",
            point_table=point_table
        )

simulate_iterations(iterations=10000)
simulate_point_tables(iterations=1000)