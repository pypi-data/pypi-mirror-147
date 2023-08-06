"""
        Copyright (C) 2022  Salvador, Bahia
        Gabriel Mascarenhas, Marco A. C. Simões, Rafael Fonseca

        This file is part of BahiaRT GYM.
        
        BahiaRT GYM is free software: you can redistribute it and/or modify
        it under the terms of the GNU Affero General Public License as
        published by the Free Software Foundation, either version 3 of the
        License, or (at your option) any later version.

        BahiaRT GYM is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.

        You should have received a copy of the GNU Affero General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
import numpy as np
from bahiart_gym.server.singleton import Singleton

class Ball(Singleton):

    def __init__(self):
        super().__init__()
        self.latestServerPos = None
        self.currentServerPos = None

    # Update ballSpeed based on server perception
    def updateServer(self, ballPos, time):
        if(not self.latestServerPos):
            self.latestServerPos = ballPos
            self.currentServerPos = ballPos
            self.latestServerTime = time
            self.currentServerTime = time

            self.speedBallServer = 0.0
        else:
            self.latestServerPos = self.currentServerPos
            self.currentServerPos = ballPos
            self.latestServerTime = self.currentServerTime
            self.currentServerTime = time

            a = np.array((self.latestServerPos[0], self.latestServerPos[1], self.latestServerPos[2]))
            b = np.array((self.currentServerPos[0], self.currentServerPos[1], self.currentServerPos[2]))

            dist = np.linalg.norm(b-a)
            
            if((self.currentServerTime - self.latestServerTime) < 0.000000000000001):
                self.speedBallServer = 0.0
            else:
                self.speedBallServer = dist / (self.currentServerTime - self.latestServerTime)        

    #TODO: Update ballSpeed based on player perception
    def updatePlayer(self, ballPos, time):
        self.speedBallPlayer
        pass