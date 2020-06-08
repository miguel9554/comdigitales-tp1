import numpy as np
import matplotlib.pyplot as plt
import random
from constellation import constellation
from utils import Q
from gray import gray_coding_pam

class PAM(constellation):
    def __init__(self, M: int, pulse_energy: float):
        self.M = M
        # Cantidades asociadas a la energía
        self.pulse_energy = pulse_energy
        self.average_energy = (M**2-1)*pulse_energy/3
        self.bit_energy = self.average_energy/np.log2(M)
        self.min_distance = 2*np.sqrt(pulse_energy)
        # Construimos los símbolos
        # Representamos los símbolos con una matriz cuyas filas son las coordenadas de cada símbolo
        # Es de MxN (M órden de la constelación, N dimensión)
        amplitudes = [2*m+1-M for m in range(M)]
        self.symbols = np.matrix([[amplitude*np.sqrt(pulse_energy)] for amplitude in amplitudes])
        self.symbols_energy = np.matrix([ [x] for x in np.linalg.norm(self.symbols, axis=-1)**2])
        self.N = 1
        self.name = "PAM"
        self.symbol_to_code_table = self.create_symbol_to_code_table()

    def create_symbol_to_code_table(self):
        table = {}
        for code in [f"{m:0{int(np.log2(self.M))}b}" for m in range(self.M)]:
            symbol = [amplitude*np.sqrt(self.pulse_energy) for amplitude in gray_coding_pam(code, np.log2(self.M))]
            table[tuple(symbol)] = code
        return table

    def symbol_to_code(self, symbol):
        if type(symbol) == np.matrix:
            symbol = np.asarray(symbol).reshape(-1)
        return self.symbol_to_code_table[tuple(symbol)]

    def theorical_pe(self, SNR):
        return 2*(1-1/self.M)*Q(np.sqrt(6*np.log2(self.M)*(10**(SNR/10))/(self.M**2-1)))

    def theorical_pb(self, SNR):
        return self.theorical_pe(SNR)/np.log2(self.M)

