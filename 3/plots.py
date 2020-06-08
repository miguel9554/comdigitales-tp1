import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random
from PAM import PAM

def generate_plot(constellation, Nsamples, SNRmax, Ms, probabilites, plot_type):

    for M in Ms:

        print(f"Estimando para M={M}...")

        constellation_class = type(constellation)
        Mconstellation = constellation_class(M, 1, probabilites)

        if plot_type == "pe":
            SNRs_estimacion, pe_estimada = Mconstellation.montecarlo_pe_vs_snr(SNRmax, Nsamples)
            SNRs_teoricas, pe_teorica = Mconstellation.theorical_pe_vs_snr(SNRmax)
        elif plot_type == "pb":
            SNRs_estimacion, pe_estimada = Mconstellation.montecarlo_pb_vs_snr(SNRmax, Nsamples)
            SNRs_teoricas, pe_teorica = Mconstellation.theorical_pb_vs_snr(SNRmax)

        plt.plot(SNRs_teoricas, pe_teorica, label='Teórica M= %d' %M,color='r',zorder=1)
        plt.scatter(SNRs_estimacion, pe_estimada, label='Estimación M = %d' %M,zorder=2)
    
    if plot_type == "pe":
        plt.title(f'Probabilidad de error para {Mconstellation.name}')
    elif plot_type == "pb":
        plt.title(f'Probabilidad de error de bit para {Mconstellation.name}')
    plt.yscale('log')
    plt.xlabel('SNR [dB]')
    plt.ylabel('log(Probabilidad de error)')
    plt.legend()
    plt.grid()
    plt.savefig(f'results/{Mconstellation.name}_{plot_type}.png')
    plt.show()

def generate_pe_plot(constellation, Nsamples, SNRmax, Ms, probabilites):
    return generate_plot(constellation, Nsamples, SNRmax, Ms, probabilites, "pe")

def generate_pb_plot(constellation, Nsamples, SNRmax, Ms, probabilites):
    return generate_plot(constellation, Nsamples, SNRmax, Ms, probabilites, "pb")

def main():

    Nsamples = int(1e4)
    SNRmax = 10
    pulse_energy = 1
    varios_M = [2]
    p = 3/4
    probabilites = [p, 1-p]
    generate_pe_plot(PAM(4,1, probabilites), Nsamples, SNRmax, varios_M, probabilites)

if __name__ == "__main__":
    main()
