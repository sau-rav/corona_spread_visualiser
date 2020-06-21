from person import *
from population import *

population_size = 300 # toatal population
init_infected_percentage = 1 # percentage of population initially infected
recovery_time = 10 # or fix randomly for every person
quarantine_limit = 50 # max population that can be quarantined
transmission_radius = 4 # radius under which infection if probable
transmission_probab = 3 # probability of infecting if in transmission radius
frame_len = 200 # size of frame
frame_wid = 200 # size of frame

# parameters to be passed in model
# population size, infected_percentage_initially, recovery time, whether recovery time is random or not, quarantime_limit, transmission probability, lenght of frame, width of frame
model = Population(population_size, init_infected_percentage, recovery_time, False, quarantine_limit, transmission_radius, transmission_probab, frame_len, frame_wid)

fig = plt.figure(figsize = (18, 9))
movement_fig = fig.add_subplot(1, 2, 1)
count_fig = fig.add_subplot(1, 2, 2)

count_fig.axis([0, 5000, 0, population_size])
scat_plot = movement_fig.scatter([p.x_pos for p in model.persons], [p.y_pos for p in model.persons], color = 'blue', s = 7)
movement_fig_boundary = plt.Rectangle((0, 0), frame_len, frame_wid, fill = False)
movement_fig.add_patch(movement_fig_boundary)

count_fig.set_xlabel('Time')
count_fig.set_ylabel('Number of People')
infected_population, = count_fig.plot(model.infected_num, color = 'red', label = 'Infected Count')
recovered_population, = count_fig.plot(model.infected_num, color = 'gray', label = 'Recovered Count')
count_fig.legend(handles = [recovered_population, infected_population])

infected = [model.infected_num]
recovered = [0]
timestamp = [0]

def animate(frame, recovered, infected, timestamp):
    model.update(frame)
    infected.append(model.infected_num)
    recovered.append(model.recovered_num)
    timestamp.append(frame)

    color_list = [p.get_color() for p in model.persons]
    size_list = [7 for p in model.persons]

    offsets = np.array([[p.x_pos for p in model.persons], [p.y_pos for p in model.persons]])
    scat_plot.set_offsets(np.ndarray.transpose(offsets))
    scat_plot.set_color(color_list)
    scat_plot.set_sizes(size_list)
    infected_population.set_data(timestamp, infected)
    recovered_population.set_data(timestamp, recovered)
    return scat_plot, infected_population, recovered_population

anim = FuncAnimation(fig, animate, interval = 5, fargs = (infected, recovered, timestamp), blit = True)
plt.show()


