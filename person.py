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
        if np.random.random() < 0.5:
            self.velX = 0
            self.velY = 0
        else:
            self.velX = (np.random.random() - 0.5) * frame_len / 50
            self.velY = (np.random.random() - 0.5) * frame_wid / 50
        self.quarantined = False
        self.recovery_time = recovery_time
        self.quarantine_start_idx = -1
        self.states = ['inf', 'sus', 'rec']
        if np.random.random() < init_infection_per / 100:
            self.stateIdx = 0
        else:
            self.stateIdx = 1
        self.colors = ['red', 'blue', 'gray']

    def get_state(self):
        return self.states[self.stateIdx]
    
    def infect(self):
        self.stateIdx = 0
    
    def recover(self):
        self.stateIdx = 2

    def getNewVelocities(self):
        if self.quarantined:
            self.velX = 0
            self.velY = 0
        else:
            self.velX = (np.random.random() - 0.5) * self.lenght / 50
            self.velY = (np.random.random() - 0.5) * self.width / 50

    def check_recovery(self, index):
        if self.quarantine_start_idx != -1:
            if index - self.quarantine_start_idx >= self.recovery_time:
                self.recover()
                self.quarantined = False
                self.quarantine_start_idx = -1
                self.getNewVelocities()
                return True

    def update_location(self):
        if self.quarantined:
            return
        self.x_pos = self.x_pos + self.velX
        self.y_pos = self.y_pos + self.velY

        # if abs(self.x_pos - 0) < 1 or abs(self.x_pos - self.lenght) < 1 or abs(self.y_pos - 0) < 1 or abs(self.y_pos - self.width) < 1:
        #     self.x_pos = np.random.random() * self.lenght
        #     self.y_pos = np.random.random() * self.width
        if abs(self.x_pos - 0) < 1 or abs(self.x_pos - self.lenght) < 1:
            self.velX = -self.velX
        if abs(self.y_pos - 0) < 1 or abs(self.y_pos - self.width) < 1:
            self.velY = -self.velY

    def get_color(self):
        return self.colors[self.stateIdx]

    def distanceTo(self, x_pos, y_pos):
        return np.sqrt((self.x_pos - x_pos)**2 + (self.y_pos - y_pos)**2)
