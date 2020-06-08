import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random
from constellation import constellation
from utils import Q

class FSK(constellation):
    def __init__(self, M: int, pulse_energy: float):
        self.M = M
        # Cantidades asociadas a la energía
        self.pulse_energy = pulse_energy
        self.average_energy = pulse_energy
        self.bit_energy = pulse_energy/np.log2(M)
        self.min_distance = np.sqrt(2*pulse_energy)
        # Construimos los símbolos
        # Representamos los símbolos con una matriz cuyas filas son las coordenadas de cada símbolo
        # Es de MxN (M órden de la constelación, N dimensión)

        self.symbols = np.matrix(np.diag([np.sqrt(pulse_energy) for _ in range(M)]))
        self.symbols_energy = np.matrix([ [x] for x in np.linalg.norm(self.symbols, axis=-1)**2])
        self.N = M
        self.name = "FSK"

    def theorical_pe(self, SNR):
        return (self.M-1)*Q(np.sqrt(np.log2(self.M)*10**(SNR/10)))

    def symbol_to_code(self, symbol):
        if type(symbol) == np.matrix:
            symbol = np.asarray(symbol).reshape(-1)
        index = np.argmax(symbol)
        code = f"{index:0{int(np.log2(self.M))}b}" 
        return code

    def theorical_pb(self, SNR):
        return self.theorical_pe(SNR)*self.M/(2*(self.M-1))
