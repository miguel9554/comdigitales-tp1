import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random

class constellation:

    def estimate_pe(self, SNRdb, iterations):

        # Obtenemos N0
        SNRveces = 10**(SNRdb/10)
        N0 = self.bit_energy/SNRveces

        # Envíamos símbolos al azar y les agregamos ruido, detectamos lo recibido
        # y contamos los errores
        errors = 0
        for sent in random.choices(self.symbols, k=iterations):
            noise = np.random.multivariate_normal(np.zeros(self.N), np.diag([N0/2 for _ in range(self.N)]), 1)
            received = np.transpose(sent + noise)

            # Detectamos
            correlator_output = self.symbols*received
            bias = N0/2*np.log(1/self.M)-self.symbols_energy/2
            detected = self.symbols[np.argmax(correlator_output+bias)]
            if not np.array_equal(sent, detected):
                errors += 1

        return errors/iterations

    def montecarlo_pe_vs_snr(self, SNRmax, iterations):

        SNRs = range(SNRmax+1)
        pe_vec = []

        for SNR in SNRs:
            pe_vec.append(self.estimate_pe(SNR, iterations))

        return SNRs, pe_vec

    def theorical_pe_vs_snr(self, SNRmax):
        
        SNRs = list(range(SNRmax+1))
        
        return SNRs, [ self.theorical_pe(SNR) for SNR in SNRs]

