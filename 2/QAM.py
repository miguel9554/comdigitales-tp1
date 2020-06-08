import numpy as np
import matplotlib.pyplot as plt
import random
from constellation import constellation
from utils import Q
from gray import gray_coding_qam

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
        self.symbol_to_code_table = self.create_symbol_to_code_table()

    def theorical_pe(self, SNR):
        return 4*(1-1/np.sqrt(self.M))*Q(np.sqrt(3*np.log2(self.M)*10**(SNR/10)/(self.M-1))) 

    def create_symbol_to_code_table(self):

        if self.M == 4:
            i_bits = 1
            q_bits = 1
        elif self.M == 8:
            i_bits = 2
            q_bits = 1
        elif self.M == 16:
            i_bits = 2
            q_bits = 2

        table = {}
        for code in [f"{m:0{int(np.log2(self.M))}b}" for m in range(self.M)]:
            symbol = [amplitude*np.sqrt(self.pulse_energy) for amplitude in gray_coding_qam(code, i_bits, q_bits)]
            table[tuple(symbol)] = code
        return table

    def symbol_to_code(self, symbol):
        if type(symbol) == np.matrix:
            symbol = np.asarray(symbol).reshape(-1)
        return self.symbol_to_code_table[tuple(symbol)]

    def theorical_pb(self, SNR):
        return self.theorical_pe(SNR)/np.log2(self.M)
