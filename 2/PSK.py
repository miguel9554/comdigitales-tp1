import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random

class PSK(constelation):
    def __init__(self, M: int, pulse_energy: float):
        self.M = M
        # Cantidades asociadas a la energía
        self.pulse_energy = pulse_energy
        self.average_energy = pulse_energy
        self.bit_energy = pulse_energy/np.log2(M)
        self.min_distance = 2*np.sqrt(np.pi**2*np.log2(self.M)*np.sin(np.pi/M)**2*self.bit_energy)
        # Construimos los símbolos
        # Representamos los símbolos con una matriz cuyas filas son las coordenadas de cada símbolo
        # Es de MxN (M órden de la constelación, N dimensión)

        self.symbols = np.matrix([[pulse_energy*np.cos(2*np.pi*(m-1)/M), pulse_energy*np.cos(2*np.pi*(m-1)/M)] \
                for m in range(1,self.M+1)])
        self.symbols_energy = np.matrix([ [x] for x in np.linalg.norm(self.symbols, axis=-1)**2])

    def theorical_pe_vs_snr(self, SNRmax):
        
        SNRs = list(range(SNRmax+1))
        if self.M ==2:
            return SNRs, [ 1*Q(np.sqrt(2*np.log2(M)*np.sin(np.pi/M)**2*10**(SNR/10))) for SNR in SNRs]
        else:
            return SNRs, [ 2*Q(np.sqrt(2*np.log2(M)*np.sin(np.pi/M)**2*10**(SNR/10))) for SNR in SNRs]

