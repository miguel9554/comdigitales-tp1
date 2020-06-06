import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random
from QAM import QAM
from PAM import PAM
from PSK import PSK
from FSK import FSK

def generate_plot(constellation, Nsamples, SNRmax, Ms):

    for M in Ms:

        constellation_class = type(constellation)
        Mconstellation = constellation_class(M, 1)

        SNRs_estimacion, pe_estimada = Mconstellation.montecarlo_pe_vs_snr(SNRmax, Nsamples)
        SNRs_teoricas, pe_teorica = Mconstellation.theorical_pe_vs_snr(SNRmax)

        plt.plot(SNRs_teoricas, pe_teorica, label='Teórica M= %d' %M,color='r',zorder=1)
        plt.scatter(SNRs_estimacion, pe_estimada, label='Estimación M = %d' %M,zorder=2)
        
    plt.title(f'Probabilidad de error para {Mconstellation.name}')
    plt.yscale('log')
    plt.xlabel('SNR [dB]')
    plt.ylabel('log(Probabilidad de error)')
    plt.legend()
    plt.grid()
    plt.savefig(f'results/{Mconstellation.name}.png')
    plt.show()

def main():

    Nsamples = int(1e4)
    SNRmax = 10
    pulse_energy = 1
    varios_M = [2,4,8,16]
    #generate_plt(PAM(4,1), Nsamples, SNRmax, varios_M)
    #generate_plot(PSK(4,1), Nsamples, SNRmax, varios_M)
    generate_plot(FSK(4,1), Nsamples, SNRmax, varios_M)
    varios_M = [4,8,16]
    #generate_plot(QAM(4,1), Nsamples, SNRmax, varios_M)

if __name__ == "__main__":
    main()
