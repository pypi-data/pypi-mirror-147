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
from numpy.core.defchararray import array
from bahiart_gym.server.ball import Ball
from bahiart_gym.server.agentParser import AgentParser
from math import fabs, sqrt
import numpy as np

class Player(object):
    """ 
    This class deals with every player instantiated on proxy
    """
    """
    Perceptor Grammar:

    Grammar = (HJ (n <joint_name>) (<angle_in_degrees>))
    Example = (HJ (n raj2) (ax -15.61))

    Joint Names: https://gitlab.com/robocup-sim/SimSpark/-/wikis/Models#physical-properties
    """

    parser = AgentParser()
    ball = Ball()

    def pol2cart(self, mag, theta):
        x = mag * np.cos(theta)
        y = mag * np.sin(theta)
        return [x, y]

    def __init__(self, unum):

        #Number/id
        self.unum = unum

        #Standing of Fallen State
        self.isFallen = False

        #ACC / GYR
        self.acc = None
        self.gyro = None

        #Force Perceptors
        self.lf = []
        self.rf = []
        #NAO TOE ONLY
        #self.lf1 = []
        #self.rf1 = []

        #ballPos
        self.ballPolarPos = [] #The returned list corresponds to [distance, horizontal angle, vertical angle] from the object.
        self.ballCartPos = []
        self.ballInitPos = []
        self.ballSpeed = 0
        self.ballCycle = 0

        #Time
        self.time = None

        #Joints
        self.neckYaw = None
        self.neckPitch = None
        self.leftShoulderPitch = None
        self.leftShoulderYaw = None
        self.leftArmRoll = None
        self.leftArmYaw = None
        self.leftHipYawPitch = None
        self.leftHipRoll = None
        self.leftHipPitch = None
        self.leftKneePitch = None
        self.leftFootPitch = None
        self.leftFootRoll = None
        self.rightHipYawPitch = None
        self.rightHipRoll = None
        self.rightHipPitch = None
        self.rightKneePitch = None
        self.rightFootPitch = None
        self.rightFootRoll = None
        self.rightShoulderPitch = None
        self.rightShoulderYaw = None
        self.rightArmRoll = None
        self.rightArmYaw = None
        #NAO TOE ONLY
        #self.leftToePitch = None
        #self.rightToePitch = None

        self.max = 0


    def getUnum(self):
        return self.unum

    def getObs(self):
        
        observation = {'joints': {
            'neckYaw': np.array([self.neckYaw]),
            'neckPitch': np.array([self.neckPitch]),
            'leftHipYawPitch': np.array([self.leftHipYawPitch]),
            'rightHipYawPitch': np.array([self.rightHipYawPitch]),
            'leftHipRoll': np.array([self.leftHipRoll]),
            'rightHipRoll': np.array([self.rightHipRoll]),
            'leftHipPitch': np.array([self.leftHipPitch]),
            'rightHipPitch': np.array([self.rightHipPitch]),
            'leftKneePitch': np.array([self.leftKneePitch]),
            'rightKneePitch': np.array([self.rightKneePitch]),
            'leftFootPitch': np.array([self.leftFootPitch]),
            'rightFootPitch': np.array([self.rightFootPitch]),
            'leftFootRoll': np.array([self.leftFootRoll]),
            'rightFootRoll': np.array([self.rightFootRoll]),
            'leftShoulderPitch': np.array([self.leftShoulderPitch]),
            'rightShoulderPitch': np.array([self.rightShoulderPitch]),
            'leftShoulderYaw': np.array([self.leftShoulderYaw]),
            'rightShoulderYaw': np.array([self.rightShoulderYaw]),
            'leftArmRoll': np.array([self.leftArmRoll]),
            'rightArmRoll': np.array([self.rightArmRoll]),
            'leftArmYaw': np.array([self.leftArmYaw]),
            'rightArmYaw': np.array([self.rightArmYaw])
        },
            'acc': np.array(self.acc),
            'gyro': np.array(self.gyro),
            'ballpos': np.array(self.ballPolarPos),
            'leftFootResistance': (np.array(self.lf[0]), np.array(self.lf[1])),
            'rightFootResistance': (np.array(self.rf[0]), np.array(self.rf[1]))
        }
        return observation

    def checkFallen(self):
        
        fallen = False

        X_ACEL = self.acc[0]
        Y_ACEL = self.acc[1]
        Z_ACEL = self.acc[2]

        if((fabs(X_ACEL) > Z_ACEL or fabs(Y_ACEL) > Z_ACEL) and Z_ACEL < 5):
            if((Y_ACEL < -6.5 and Z_ACEL < 3) or (Y_ACEL > 7.5 and Z_ACEL < 3) or (fabs(X_ACEL) > 6.5)):
                fallen = True
                #print("FALLEN: " + str([X_ACEL, Y_ACEL, Z_ACEL]) + " time: " + str(self.time))
        else:
            pass
            #print("STANDING: " + str([X_ACEL, Y_ACEL, Z_ACEL]))
        
        return fallen

    def updateStats(self, agentMsg):

        #AGENT MSG
        parsedMsg = self.parser.parse(agentMsg)
        
        #JOINTS
        self.neckYaw = self.parser.getHinjePos('hj1', parsedMsg, self.neckYaw)
        self.neckPitch = self.parser.getHinjePos('hj2', parsedMsg, self.neckPitch)
        self.leftHipYawPitch = self.parser.getHinjePos('llj1', parsedMsg, self.leftHipYawPitch)
        self.rightHipYawPitch = self.parser.getHinjePos('rlj1', parsedMsg, self.rightHipYawPitch)
        self.leftHipRoll = self.parser.getHinjePos('llj2', parsedMsg, self.leftHipRoll)
        self.rightHipRoll = self.parser.getHinjePos('rlj2', parsedMsg, self.rightHipRoll)
        self.leftHipPitch = self.parser.getHinjePos('llj3', parsedMsg, self.leftHipPitch)
        self.rightHipPitch = self.parser.getHinjePos('rlj3', parsedMsg, self.rightHipPitch)
        self.leftKneePitch = self.parser.getHinjePos('llj4', parsedMsg, self.leftKneePitch)
        self.rightKneePitch = self.parser.getHinjePos('rlj4', parsedMsg, self.rightKneePitch)
        self.leftFootPitch = self.parser.getHinjePos('llj5', parsedMsg, self.leftFootPitch)
        self.rightFootPitch = self.parser.getHinjePos('rlj5', parsedMsg, self.rightFootPitch)
        self.leftFootRoll = self.parser.getHinjePos('llj6', parsedMsg, self.leftFootRoll)
        self.rightFootRoll = self.parser.getHinjePos('rlj6', parsedMsg, self.rightFootRoll)
        self.leftShoulderPitch = self.parser.getHinjePos('laj1', parsedMsg, self.leftShoulderPitch)
        self.rightShoulderPitch = self.parser.getHinjePos('raj1', parsedMsg, self.rightShoulderPitch)
        self.leftShoulderYaw = self.parser.getHinjePos('laj2', parsedMsg, self.leftShoulderYaw)
        self.rightShoulderYaw = self.parser.getHinjePos('raj2', parsedMsg, self.rightShoulderYaw)
        self.leftArmRoll = self.parser.getHinjePos('laj3', parsedMsg, self.leftArmRoll)
        self.rightArmRoll = self.parser.getHinjePos('raj3', parsedMsg, self.rightArmRoll)
        self.leftArmYaw = self.parser.getHinjePos('laj4', parsedMsg, self.leftArmYaw)
        self.rightArmYaw = self.parser.getHinjePos('raj4', parsedMsg, self.rightArmYaw)

        #ACC/GYR
        self.acc = self.parser.getGyr('ACC', parsedMsg, self.acc)
        self.gyro = self.parser.getGyr('GYR', parsedMsg, self.gyro)
        
        #TIME
        self.time = self.parser.getTime(parsedMsg, self.time)

        #BALL
        self.ballPolarPos = self.parser.getBallVision(parsedMsg, self.ballPolarPos) # [distance, horiAngle1, vertAngle2]


        #FORCE RESISTANCE PERCEPTORS
        self.lf = self.parser.getFootResistance('lf', parsedMsg, self.lf)
        self.rf = self.parser.getFootResistance('rf', parsedMsg, self.rf)

        #CHECK IF PLAYER IS FALLEN
        self.isFallen = self.checkFallen()
        
        #NAO TOE
        #self.lf1 = self.parser.getFootResistance('lf1', parsedMsg, self.lf1)
        #self.rf1 = self.parser.getFootResistance('rf1', parsedMsg, self.rf1)
        #self.leftToePitch = self.parser.getHinjePos('llj7', parsedMsg, self.leftToePitch)
        #self.rightToePitch = self.parser.getHinjePos('rlj7', parsedMsg, self.leftToePitch)