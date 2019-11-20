import simulate

def simulate_iterations(iterations=100, output="output/games.txt", agent_names = ["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"], point_table={1:1, 2:2, 3:4, 4:7, 5:10, 6:15}):
    output_file = open(output, "a")
    for iteration in range(iterations):
        reload(simulate)
        results = simulate.run_game(agent_names=agent_names, point_table=point_table)
        results['point_table'] = point_table
        output_file.write(str(results) + '\n')
    output_file.close()

def simulate_iterations_two_player(iterations=100, four_names=["Hungry", "Path", "OneStepThinker", "LongRouteJunkie"]):
    for i in range(iterations):
        two_names = get_two_agents(four_names, i)
        simulate_iterations(iterations=1, agent_names=two_names)

def get_two_agents(four_names, i):
	first_index = i//3 % 4
	valid_choices = four_names[:first_index] + four_names[first_index + 1:]
	two_names = [four_names[first_index], valid_choices[i % 3]]
	return two_names

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
        simulate_iterations(
            iterations=iterations, 
            output="output/point_tables.txt",
            point_table=point_table
        )

 

#simulate_iterations(iterations=10000)
simulate_iterations_two_player(iterations=10000)
#simulate_point_tables(iterations=2)