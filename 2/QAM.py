import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random

class QAM:
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

    def estimate_pe(self, SNRdb, iterations):

        # Obtenemos N0
        SNRveces = 10**(SNRdb/10)
        N0 = self.bit_energy/SNRveces

        # Envíamos símbolos al azar y les agregamos ruido, detectamos lo recibido
        # y contamos los errores
        errors = 0
        for sent in random.choices(self.symbols, k=iterations):
            noise = np.random.multivariate_normal(np.zeros(2), np.diag([N0/2, N0/2]), 1)
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
        
        return SNRs, [ 4*(1-1/np.sqrt(self.M))*Q(np.sqrt(3*np.log2(self.M)*10**(SNR/10)/(self.M-1))) for SNR in SNRs]

def Q(q):

    return 1 - NormalDist(mu=0, sigma=1).cdf(q)


def main():

    Nsamples = int(1e3)
    SNRmax = 10
    pulse_energy = 1
    varios_M = [4,8,16]

    for M in varios_M:
        constelation = QAM(M, pulse_energy)
        SNRs_estimacion, pe_estimada = constelation.montecarlo_pe_vs_snr(SNRmax, Nsamples)
        SNRs_teoricas, pe_teorica = constelation.theorical_pe_vs_snr(SNRmax)

        plt.plot(SNRs_teoricas, pe_teorica, label='Teórica M= %d' %M,color='r',zorder=1)
        plt.scatter(SNRs_estimacion, pe_estimada, label='Estimación M = %d' %M,zorder=2)
        
    plt.title('Probabilidad de error para QAM')
    plt.yscale('log')
    plt.xlabel('SNR [dB]')
    plt.ylabel('log(Probabilidad de error)')
    plt.legend()
    plt.grid()
    plt.savefig('results/QAM.png')
    plt.show()

if __name__ == "__main__":
    main()
