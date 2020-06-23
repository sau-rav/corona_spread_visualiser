import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from person import *

class Population:
    def __init__(self, population_size, infected_percentage, recovery_time, random_recovery_time, quarantine_limit, transmission_radius, transmission_probab, length, width):
        self.pop_size = population_size
        self.inf_per = infected_percentage
        self.recov_time = recovery_time
        self.rand_recov = random_recovery_time
        self.quar_limit = quarantine_limit
        self.trans_rad = transmission_radius
        self.trans_probab = transmission_probab
        self.grid_len = length
        self.grid_width = width
        self.infected_num = 0
        self.recovered_num = 0
        self.quartine_number = 0
        self.reached_tolerence = False
        self.persons = self.initiatePopulation()

    def initiatePopulation(self):
        persons = []
        for i in range(self.pop_size):
            p = None
            if not self.rand_recov:
                p = Person(i, np.random.random() * (self.grid_len + self.grid_width) * 2, self.grid_len, self.grid_width, self.inf_per, self.recov_time)
            else:
                p = Person(i, np.random.random() * (self.grid_len + self.grid_width) * 2, self.grid_len, self.grid_width, self.inf_per, np.random.randint(100, 200))
            if p.get_state() == 'inf':
                self.infected_num += 1
            persons.append(p)
        return persons

    def update(self, frame):
        self.infected_num = 0
        self.recovered_num = 0
        for p in self.persons:
            status = p.check_recovery(frame)
            if status:
                self.quartine_number -= 1
            p.update_location()
            if p.get_state() == 'rec':
                self.recovered_num += 1 
            if p.get_state() == 'inf':
                self.infected_num = self.infected_num + 1
                for q in self.persons:
                    if q.ID == p.ID or q.get_state() == 'inf' or p.quarantined or p.get_state() == 'rec':
                        pass
                    else:
                        dist = p.distanceTo(q.x_pos, q.y_pos)
                        if dist < self.trans_rad:
                            if q.get_state() == 'sus':
                                if np.random.random() < self.trans_probab / 100:
                                    q.infect()
                                    if np.random.random() < 0.0012 and self.quartine_number / self.pop_size < self.quar_limit:
                                        q.quarantined = True
                                        q.quarantine_start_idx = frame
                                        self.quartine_number += 1
                if np.random.random() < 0.0012 and self.quartine_number / self.pop_size < self.quar_limit and not p.quarantined:
                    p.quarantined = True
                    p.quarantine_start_idx = frame
                    self.quartine_number += 1

        offsets = np.array([[p.x_pos for p in self.persons], [p.y_pos for p in self.persons]])
        color_list = [p.get_color() for p in self.persons]
        size_list = [7 for p in self.persons]
        return offsets, color_list, size_list

        
