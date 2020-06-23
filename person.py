import math
import numpy as np

class Person:
    def __init__(self, index, speed, frame_len, frame_wid, init_infection_per, recovery_time):
        self.ID = index
        self.speed = speed
        self.lenght = frame_len
        self.width = frame_wid
        self.x_pos = np.random.random() * frame_len
        self.y_pos = np.random.random() * frame_wid
        self.x_target = np.random.random() * frame_len
        self.y_target = np.random.random() * frame_wid
        self.quarantined = False
        self.recovery_time = recovery_time
        self.infected_count = 0
        self.quarantine_start_idx = -1
        self.states = ['inf', 'sus', 'rec']
        if np.random.random() < init_infection_per / 100:
            self.stateIdx = 0
            self.infected_count += 1
        else:
            self.stateIdx = 1
        self.colors = ['red', 'blue', 'gray']
        if np.random.random() < 0.5:
            self.dx_pos = 0
            self.dy_pos = 0
        else:
            self.dx_pos = (self.x_target - self.x_pos) / self.speed
            self.dy_pos = (self.y_target - self.y_pos) / self.speed

    def get_state(self):
        return self.states[self.stateIdx]
    
    def infect(self):
        self.stateIdx = 0
    
    def recover(self):
        self.stateIdx = 2

    def get_random_target(self):
        self.x_target = np.random.random() * self.lenght
        self.y_target = np.random.random() * self.width
        if self.quarantined:
            self.dx_pos = 0
            self.dy_pos = 0
        else:
            self.dx_pos = (self.x_target - self.x_pos) / self.speed
            self.dy_pos = (self.y_target - self.y_pos) / self.speed

    def check_recovery(self, index):
        if self.quarantine_start_idx != -1:
            if index - self.quarantine_start_idx >= self.recovery_time:
                self.recover()
                self.quarantined = False
                self.quarantine_start_idx = -1
                self.get_random_target()
                return True

    def update_location(self):
        if self.quarantined:
            return
        self.x_pos = self.x_pos + self.dx_pos
        self.y_pos = self.y_pos + self.dy_pos

        if self.get_dist(self.x_target, self.y_target) < 4:
            self.get_random_target()

    def get_color(self):
        return self.colors[self.stateIdx]

    def get_pos(self):
        return (self.x_pos, self.y_pos)

    def get_dist(self, x_pos, y_pos):
        return np.sqrt((self.x_pos - x_pos)**2 + (self.y_pos - y_pos)**2)