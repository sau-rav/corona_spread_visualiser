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
        self.persons = self.initiatePopulation()

    def initiatePopulation(self):
        persons = []
        for i in range(self.pop_size):
            p = None
            if not self.rand_recov:
                p = Person(i, np.random.random() * (self.grid_len + self.grid_width) / 2, self.grid_len, self.grid_width, self.inf_per, self.recov_time)
            else:
                p = Person(i, np.random.random() * (self.grid_len + self.grid_width) / 2, self.grid_len, self.grid_width, self.inf_per, np.random.randint(10, 100))
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
                    if q.ID == p.ID or q.get_state() == 'inf' or p.quarantined:
                        pass
                    else:
                        dist = p.get_dist(q.x_pos, q.y_pos)
                        if dist < self.trans_rad:
                            if q.get_state() == 'sus':
                                if np.random.random() < self.trans_probab / 100:
                                    q.infect()
                                    if np.random.random() < 0.4 and self.quartine_number / self.pop_size < self.quar_limit:
                                        q.quarantined = True
                                        q.quarantine_start_idx = frame
                            elif q.get_state() == 'rec':
                                if np.random.random() < self.trans_probab / (100 * self.infected_num):
                                    q.infect()
                                    if q.get_state() == 'inf' and np.random.random() < 0.4 and self.quartine_number / self.pop_size < self.quar_limit:
                                        q.quarantined = True
                                        q.quarantine_start_idx = frame
                if self.infected_num > self.pop_size / 2 and np.random.random() < 0.5 and self.quartine_number / self.pop_size < self.quar_limit:
                    p.quarantined = True
                    p.quarantine_start_idx = frame

        
