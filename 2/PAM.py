import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random

class PAM:
    def __init__(self, M: int, pulse_energy: float):
        self.M = M
        self.pulse_energy = pulse_energy
        self.average_energy = (M**2-1)*pulse_energy/3
        self.bit_energy = self.average_energy/np.log2(M)
        self.min_distance = 2*np.sqrt(pulse_energy)
        amplitudes = [2*m+1-M for m in range(M)]
        # Matriz cuyas filas son las coordenadas de cada símbolo
        # Es de MxN (M órden de la constelación, N dimensión)
        self.symbols = np.matrix([[amplitude*np.sqrt(pulse_energy)] for amplitude in amplitudes])
        self.symbols_energy = np.matrix([[amplitude**2*pulse_energy] for amplitude in amplitudes])

    def estimate_pe(self, SNRdb, iterations):

        # Obtenemos N0
        SNRveces = 10**(SNRdb/10)
        N0 = self.bit_energy/SNRveces

        # Envíamos símbolos al azar y les agregamos ruido, detectamos lo recibido
        # y contamos los errores
        errors = 0
        for sent in random.choices(self.symbols, k=iterations):
            noise = np.random.normal(0, np.sqrt(N0/2), 1)
            received = sent + noise

            # Detectamos
            correlator_output = self.symbols*received
            bias = N0/2*np.log(1/self.M)-self.symbols_energy/2
            detected = self.symbols[np.argmax(correlator_output+bias)]
            if detected != sent:
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

        return SNRs, [2*(1-1/self.M)*Q(np.sqrt(6*np.log2(self.M)*(10**(SNR/10))/(self.M**2-1))) for SNR in SNRs]

def Q(q): # corrijo factor de la Q

    return 1 - NormalDist(mu=0, sigma=1).cdf(q)


def main():

    Nsamples = int(1e3)
    SNRmax = 10
    pulse_energy = 1
    varios_M = [2,4,8,16]

    for M in varios_M:
        constelation = PAM(M, pulse_energy)
        SNRs_estimacion, pe_estimada = constelation.montecarlo_pe_vs_snr(SNRmax, Nsamples)
        SNRs_teoricas, pe_teorica = constelation.theorical_pe_vs_snr(SNRmax)

        plt.plot(SNRs_teoricas, pe_teorica, label='Teórica M= %d' %M,color='r',zorder=1)
        plt.scatter(SNRs_estimacion, pe_estimada, label='Estimación M = %d' %M,zorder=2)
        
    plt.title('Probabilidad de error para PAM')
    plt.yscale('log')
    plt.xlabel('SNR [dB]')
    plt.ylabel('log(Probabilidad de error)')
    plt.legend()
    plt.grid()
    plt.savefig('results/PAM.png')
    plt.show()

if __name__ == "__main__":
    main()
