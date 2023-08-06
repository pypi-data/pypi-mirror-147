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
from bahiart_gym.server.sexpr import str2sexpr
from bahiart_gym.server.singleton import Singleton
from multiprocessing import Lock
import numpy as np
#from bahiart_gym.server.parsr import Parser

class AgentParser(Singleton):
    """
    Class to retrieve and parse the S-Expression sent by the server to the agents
    """

    def __init__(self):
        super().__init__()
        self.mutex = Lock()

    def parse(self, string:str):
        parsedString = []       
        with self.mutex:
            parsedString = str2sexpr(string)    
        return parsedString

    def getHinjePos(self, word: str, lst: list, old):
        value = old
        for i in range(0,len(lst)):
            if value == None or value == old:
                if lst[i] == 'HJ':
                    hingeName = lst[i+1]
                    if hingeName[1] == word:
                        ax = lst[i+2]
                        value = ax[1]
                        return float(value)
                    else:
                        continue
                elif type(lst[i]) is list:
                    value = self.getHinjePos(word, lst[i], old)
                else:
                    continue
                if value == None or value == old:
                    continue
            else:
                return value
        if value is None:
            value = old
        return value

    #Can be used for ACC too. Just send 'ACC' as the word instead of 'GYR'
    def getGyr(self, word: str, lst: list, old):
        value = old
        for i in range(0,len(lst)):
            if value == [] or value == old:
                if lst[i] == word:
                    valuesList = lst[i+2]
                    x = float(valuesList[1])
                    y = float(valuesList[2])
                    z = float(valuesList[3])
                    value = [x, y, z]
                    return value
                elif type(lst[i]) is list:
                    value = self.getGyr(word, lst[i], old)
                else:
                    continue
                if value == None or value == old:
                    continue
            else:
                return value
        if value is None:
            value = old
        return value

    def getTime(self, lst: list, old, word='GS'):
        try:
            value = old.copy()
        except:
            value = old
        time = None
        for i in range(0,len(lst)):
            if value == [] or value == old:
                if lst[i] == word:
                    time = self.getValue('t', lst, old)
                    value = float(time)
                    return value
                elif type(lst[i]) is list:
                    value = self.getTime(lst[i], old)
                else:
                    continue
                if value == None or value == old:
                    continue
            else:
                return value
        if value is None:
            value = old
        return value


    def getBallVision(self, lst: list, old):
        value = old
        for i in range(0,len(lst)):
            if value == [] or value == old:
                if lst[i] == 'B':
                    valuesList = lst[i+1]
                    distance = float(valuesList[1])
                    angle1 = float(valuesList[2])
                    angle2 = float(valuesList[3])
                    value = [distance, angle1, angle2]
                    return value
                elif type(lst[i]) is list:
                    value = self.getBallVision(lst[i], old)
                else:
                    continue
                if value == None or value == old:
                    continue
            else:
                return value
        if value is None:
            value = old
        return value

    def getFootResistance(self, word: str, lst: list, old):
        value = old
        for i in range(0,len(lst)):
            if value == [] or value == old:
                if lst[i] == 'FRP':
                    foot = lst[i+1]
                    if foot[1] == word:
                        coordList = lst[i+2]
                        forceList = lst[i+3]
                        x1 = float(coordList[1])
                        y1 = float(coordList[2])
                        z1 = float(coordList[3])
                        x2 = float(forceList[1])
                        y2 = float(forceList[2])
                        z2 = float(forceList[3])
                        value = [[x1, y1, z1], [x2, y2, z2]]
                        return value
                elif type(lst[i]) is list:
                    value = self.getFootResistance(word, lst[i], old)
                else:
                    continue
                if value == None or value == old:
                    continue
            else:
                return value
        if value == None or value == []:
            value = old
        return value

    def search(self, word: str, lst: list):
        for i in range(0,len(lst)):
            if type(lst[i]) is list:
                self.search(word, lst[i])
            elif lst[i] == word:
                print(word, '=', lst[i+1])
            continue
        return

    def getValue(self, word: str, lst: list, old):
        value = old
        for i in range(0,len(lst)):
            if value == None or value == old:
                if lst[i] == word:
                    value = lst[i+1]
                    return value
                elif type(lst[i]) is list:
                    value = self.getValue(word, lst[i], old)
                else:
                    continue
                if value == None or value == old:
                    continue
            else:
                return value
        if value is None:
            value = old
        return value