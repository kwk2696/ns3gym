import zmq, json
import numpy as np
from struct import *

class Server():
    def __init__(self, port, obsize):
        self.m_port = port
        self.m_context = zmq.Context ()
        self.m_socket = self. m_context.socket(zmq.REP)
		
        self.m_obsize = obsize
        self.m_socket.bind ("tcp://*:5050")
	
    def _recv (self):
        recv = self.m_socket.recv ()
        return recv 
        
    def _communicate (self):
        recv = self._recv ()
        dict = json.loads (recv)
        
        obs = np.zeros ((1, self.m_obsize))
        reward = 0
        # iter = 0
        for key in dict:
            if key == 'reward' :
                reward = dict[key]
                break
                
            if key == 'state0':
                obs[0][0] = dict[key]
            if key == 'state1':
                obs[0][1] = dict[key]
            if key == 'state2':
                obs[0][2] = dict[key]
            # obs[0][iter] = dict[key]
            # iter += 1
        
        self.m_socket.send(b"1")
        return obs, reward
    
    def _obs (self):
        obs = np.zeros ((1, self.m_obsize))
        for i in range(self.m_obsize):
            recv = self._recv ()
            
            result = 0
            index = 1
            for byte in recv:
                result = result + int(byte) * index
                index = index * 256
            
            obs[0][i] = result
            
            self.m_socket.send(b"1")
            
        return obs
        
    def _action (self, action):
        recv = self._recv ()
        snd = str(action).encode ()
        self.m_socket.send (snd)
    
    def _reward (self):
        recv = self._recv ()
        reward = self.byteToint (recv)
        
        if reward == 255.0:
            reward = -1.0
        
        self.m_socket.send(b"1")
        
        return reward 
    def _end (self):
        recv = self._recv ()
        end = self.byteToint (recv)
        self.m_socket.send(b"1")
        
        if end == 1: 
            return True
            
        return False
      
    def byteToint (self, byte):
       result = int.from_bytes (byte, byteorder = 'big', signed=True)
       return result
    
    # def byteTouint (self, byte):
        # result = int.from_bytes (byte, byteorder = 'big')
        # return result