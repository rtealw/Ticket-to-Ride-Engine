import simulate

def simulate_iterations(iterations=100, output="output/games.txt", agent_names = ["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"], point_table={1:1, 2:2, 3:4, 4:7, 5:10, 6:15}):
    wins = {"total" : 0, "LongRouteJunkie" : 0}
    output_file = open(output, "a")
    for iteration in range(iterations):
        reload(simulate)
        results = simulate.run_game(agent_names=agent_names, point_table=point_table)
        output_file.write(str(results) + '\n')
        for winner in results['winners']:
            winner_name = agent_names[winner]
            if winner_name not in wins:
                wins[winner_name] = 0
            wins[winner_name] += 1
            wins["total"] += 1
        current_prop = float(wins['LongRouteJunkie'])/wins["total"]
        print "Iteration:", iteration, "Long Route Proportion", current_prop
    output_file.close()
    print(wins)

simulate_iterations(iterations=20)