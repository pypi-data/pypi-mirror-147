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
import socket
from socket import timeout
import threading
import re
from bahiart_gym.server.player import Player


class AgentProxy:

    def __init__(self,agentSock,server_port=3100,server_host='localhost'):
        self.SERVER_HOST = server_host
        self.SERVER_PORT = server_port
        self.agentSock = agentSock
        self.MAX_WAIT_TIME = 0.15
        self.isConnected = True
        self.agentNumber = '0'
        self.listOfMessages = []
        self.player = None
        
    def connectToServer(self):
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.connect((self.SERVER_HOST, self.SERVER_PORT))
        return serverSock

    def closeConnection(self):
        try:
            try:
                self.serverSock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.agentSock.shutdown(socket.SHUT_RDWR)
            except:
                pass
        except:
            pass
        finally:
            print("Closed connection")
            self.isConnected = False
            return
        

    def connectionManager(self):
        self.serverSock = self.connectToServer()
        threading._start_new_thread(self.serverToAgent,())
        threading._start_new_thread(self.agentToServer,())

    def serverToAgent(self):
        self.serverSock.settimeout(self.MAX_WAIT_TIME)
        length = ''.encode()
        message = ''.encode()
        splitMessage = re.split("\s",message.decode())
        while True:
            try:
                length = self.serverSock.recv(4)          
                sockLen = int.from_bytes(length, 'little')          
                sockIntLen = socket.ntohl(sockLen)
                message = self.serverSock.recv(sockIntLen)
                fullmessage = length + message
                
                if not message:
                    if self.isConnected:
                        self.closeConnection()
                    else:
                        return

                try:
                    self.agentSock.sendall(fullmessage)
                except:
                    if self.isConnected:
                        self.closeConnection()
                    else:
                        return

            except timeout:
                message = '(syn)'.encode()
                sockLen = socket.htonl(len(message))
                length = sockLen.to_bytes(4,'little')
                fullmessage = length + message

                try:
                    self.serverSock.sendall(fullmessage)
                except:
                    if self.isConnected:
                        self.closeConnection()
                    else:
                        return
            
            # Searching agent number
            if self.agentNumber == '0':    
                # If the proxy doesn't know the agent, 
                # it keeps searching in the messages for the number of the agent.
                splitMessage = re.split("\s",message.decode())
                for x in range(len(splitMessage)):
                    if 'unum' in splitMessage[x]:
                        self.agentNumber = str(splitMessage[x+1].split(')',1)[0])
                        # # # # # # # # # # # # # # # # 
                        # Instance of player created  #
                        self.player = Player(self.agentNumber)
                        # # # # # # # # # # # # # # # #
                
            if not message.decode() == "(syn)":
                if self.getIsConnected:
                    self.listOfMessages.append(message.decode())
                    if self.player is not None:
                        try:
                            self.player.updateStats(message.decode())
                        except Exception as e:
                            print(e)


                        
    def agentToServer(self):
        while True:
            try:
                length = self.agentSock.recv(4)
                sockLen = int.from_bytes(length, 'little')          
                sockIntLen = socket.ntohl(sockLen)
                message = self.agentSock.recv(sockIntLen)
                fullmessage = length + message
            except Exception as e:
                print("[PROXY]!!!!!!EXCEPTION HERE!!!!!!")
                print(repr(e))
                #pass

            if not message:
                if self.isConnected:
                    self.closeConnection
                else:
                    return

            try:
                self.serverSock.sendall(fullmessage)
            except:
                if self.isConnected:
                    self.closeConnection()
                else:
                    return
    
    def getAgentNumber(self):
        return self.agentNumber
    
    def getAgentMessages(self):
        # Return list of messages and clear it
        messages = self.listOfMessages.copy()
        self.listOfMessages = []

        return messages

    def getIsConnected(self):
        return self.isConnected

    def getPlayerObj(self):
        return self.player