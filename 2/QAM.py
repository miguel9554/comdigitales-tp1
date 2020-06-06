import numpy as np
import matplotlib.pyplot as plt
import random
from constellation import constellation
from utils import Q

class QAM(constellation):
    def __init__(self, M: int, pulse_energy: float):
        self.M = M
        # Cantidades asociadas a la energía
        self.pulse_energy = pulse_energy
        self.average_energy = (M-1)*2*pulse_energy/3
        self.bit_energy = (M-1)*2*pulse_energy/(3*np.log2(M))
        self.min_distance = np.sqrt(4*pulse_energy)
        # Construimos los símbolos
        # Representamos los símbolos con una matriz cuyas filas son las coordenadas de cada símbolo
        # Es de MxN (M órden de la constelación, N dimensión)
        if M == 4:
            Ami = [-1, 1]
            Amq = [-1, 1]
        elif M == 8:
            Ami = [-3, -1, 1, 3]
            Amq = [-1, 1]
        elif M == 16:
            Ami = [-3, -1, 1, 3]
            Amq = [-3, -1, 1, 3]
        self.symbols = np.matrix([[ami*np.sqrt(pulse_energy), amq*np.sqrt(pulse_energy)] \
                for ami in Ami for amq in Amq])
        self.symbols_energy = np.matrix([ [x] for x in np.linalg.norm(self.symbols, axis=-1)**2])
        self.N = 2
        self.name = "QAM"

    def theorical_pe(self, SNR):
        return 4*(1-1/np.sqrt(self.M))*Q(np.sqrt(3*np.log2(self.M)*10**(SNR/10)/(self.M-1))) 
