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
from math import sqrt
from bahiart_gym.server.comms import Comms
from bahiart_gym.server.ball import Ball
from bahiart_gym.server.singleton import Singleton
from bahiart_gym.server.trainer import Trainer

class World(Singleton):
    
    net = Comms()
    ball = Ball()
    parser = net.serverParser
    trainer = Trainer()
    
    def __init__(self):
        
        #DYNAMIC
        self.time = 0.0
        self.playMode = 0
        self.scoreLeft = 0
        self.scoreRight = 0

        #STATIC
        self.fieldLength = 0.0
        self.fieldHeight = 0.0
        self.fieldwidth = 0.0
        self.goalWidth = 0.0
        self.goalDepth = 0.0
        self.goalHeight = 0.0

        #BALL
        self.ballRadius = 0.0
        self.ballMass = 0.0
        self.ballIndex = None
        self.ballNode = None
        self.ballGraph = None

        #BALL SPEED
        self.ballFinalPos = []
        self.ballInitPos = []
        self.ballSpeed = 0
        self.ballInitTime = 0
        self.count = 0
    
    def dynamicUpdate(self):
        
        serverExp = []
        try:
            self.net.updateSExp()
            serverExp = self.net.serverExp            
        except Exception as e:
            pass
            #print("-----SERVER S-EXPRESSION UPDATE ERROR-----:")
            #print(e)
        #DEBUG
        #print("SERVER EXPRESSION BEGIN")
        #print(serverExp)
        #print("SERVER EXPRESSION END")
        
        #ENVIRONMENT
        try:
            self.time = float(self.parser.getValue('time', serverExp, self.time))
            self.playMode = int(self.parser.getValue('play_mode', serverExp, self.playMode))
            self.scoreLeft = int(self.parser.getValue('score_left', serverExp, self.scoreLeft))
            self.scoreRight = int(self.parser.getValue('score_right', serverExp, self.scoreRight))
        except Exception as e:
            pass
            #print("-----ENVIRONMENT EXCEPTION-----: ")
            #print(e)

        #BALLPOS
        try:
            self.ballNode = self.parser.getBallNd(serverExp, self.ballIndex)
            self.ballGraph = self.parser.getBallGraph(self.ballNode, self.ballGraph)
            self.ballFinalPos = self.parser.getBallPos(self.ballGraph, self.ballFinalPos)       
        except Exception as e:
            pass
            #print("-----BALLPOSS EXCEPTION-----:")
            #print(e)

        #BALL SPEED
        try:
            if(self.count == 0):
                self.ballInitPos = self.ballFinalPos
                self.ballInitTime = self.time
            if(self.count == 9):
                if(len(self.ballInitPos) > 0):
                    self.ballSpeed = sqrt(((self.ballFinalPos[0] - self.ballInitPos[0])**2) + ((self.ballFinalPos[1] - self.ballInitPos[1])**2)) / (self.time - self.ballInitTime)
                self.count = -1
            self.count = self.count + 1
        except Exception as e:
            pass
            # print("------EXCEPTION SPEED---------")
            # print(e)
            # print("---------END EXCEPTION-------")

        #DEBUG
        #print("Game Time: " + self.time)
        #print("score right: " + self.scoreRight)
        #print("score left: " + self.scoreLeft)
        #print("PlayMode: " + self.playMode)
    
    def staticUpdate(self):
        while(self.ballIndex is None):    
            try:
                self.trainer.reqFullState()
                self.net.updateSExp()
                serverExp = self.net.serverExp
                self.ballIndex = self.parser.getBallIndex(serverExp, self.ballIndex) #The ball should be initiated along with the server so if the ball is up, everything else should be ready as well.
            except Exception as e:
                pass
                #print("-----BALLPOSS EXCEPTION-----:")
                #print(e)
        
        try:
            self.net.updateSExp()
            serverExp = self.net.serverExp
            self.ballIndex = self.parser.getBallIndex(serverExp, self.ballIndex) #The ball should be initiated along with the server so if the ball is up, everything else should be ready as well.
        except Exception as e:
            pass
            #print("-----BALLPOSS EXCEPTION-----:")
            #print(e)

        try:
            #FIELD
            self.fieldLength = float(self.parser.getValue('FieldLength', serverExp, self.fieldLength))
            self.fieldHeight = float(self.parser.getValue('FieldHeight', serverExp, self.fieldHeight))
            self.fieldwidth = float(self.parser.getValue('FieldWidth', serverExp, self.fieldwidth))
            self.goalWidth = float(self.parser.getValue('GoalWidth', serverExp, self.goalWidth))
            self.goalDepth = float(self.parser.getValue('GoalDepth', serverExp, self.goalDepth))
            self.goalHeight = float(self.parser.getValue('GoalHeight', serverExp, self.goalHeight))

            #BALL
            self.ballRadius = float(self.parser.getValue('BallRadius', serverExp, self.ballRadius))
            self.ballMass = float(self.parser.getValue('BallMass', serverExp, self.ballMass))
        except Exception as e:
            pass
            #print("-----BALLPOSS EXCEPTION-----:")
            #print(e)