import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random
from constellation import constellation
from utils import Q
from gray import psk_table

class PSK(constellation):
    def __init__(self, M: int, pulse_energy: float):
        self.M = M
        # Cantidades asociadas a la energía
        self.pulse_energy = pulse_energy
        self.average_energy = pulse_energy
        self.bit_energy = pulse_energy/np.log2(M)
        self.min_distance = 2*np.sqrt(np.log2(M)*np.sin(np.pi/M)**2*self.bit_energy)
        # Construimos los símbolos
        # Representamos los símbolos con una matriz cuyas filas son las coordenadas de cada símbolo
        # Es de MxN (M órden de la constelación, N dimensión)

        self.symbols = np.matrix([[np.sqrt(pulse_energy)*np.cos(2*np.pi*(m-1)/M), np.sqrt(pulse_energy)*np.sin(2*np.pi*(m-1)/M)] \
                for m in range(1,self.M+1)])
        self.symbols_energy = np.matrix([ [x] for x in np.linalg.norm(self.symbols, axis=-1)**2])
        self.N = 2
        self.name = "PSK"
        self.symbol_to_code_table = psk_table(np.log2(M))

    def theorical_pe(self, SNR):
        
        if self.M == 2:
            return 1*Q(np.sqrt(2*np.log2(self.M)*np.sin(np.pi/self.M)**2*10**(SNR/10)))
        else:
            return 2*Q(np.sqrt(2*np.log2(self.M)*np.sin(np.pi/self.M)**2*10**(SNR/10)))

    def symbol_to_code(self, symbol):
        if type(symbol) == np.matrix:
            symbol = np.asarray(symbol).reshape(-1)
        theta = np.arctan2(symbol[1], symbol[0])
        # Pasamos de -pi, pi a 0, 2pi
        theta = (2*np.pi + theta) * (theta < 0) + theta*(theta >= 0)
        index = int(theta*self.M/(2*np.pi))
        return self.symbol_to_code_table[index]

    def theorical_pb(self, SNR):
        return self.theorical_pe(SNR)/np.log2(self.M)
