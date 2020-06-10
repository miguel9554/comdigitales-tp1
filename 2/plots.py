import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist
import random
from QAM import QAM
from PAM import PAM
from PSK import PSK
from FSK import FSK

def generate_plot(constellation, Nsamples, SNRmax, Ms, show_plot, plot_type):

    map_constellation_name = {"QAM": QAM, "PAM": PAM, "PSK": PSK, "FSK": FSK}

    for M in Ms:

        print(f"Estimando para M={M}...")

        Mconstellation = map_constellation_name[constellation](M, 1)

        if plot_type == "pe":
            SNRs_estimacion, pe_estimada = Mconstellation.montecarlo_pe_vs_snr(SNRmax, Nsamples)
            SNRs_teoricas, pe_teorica = Mconstellation.theorical_pe_vs_snr(SNRmax)
        elif plot_type == "pb":
            SNRs_estimacion, pe_estimada = Mconstellation.montecarlo_pb_vs_snr(SNRmax, Nsamples)
            SNRs_teoricas, pe_teorica = Mconstellation.theorical_pb_vs_snr(SNRmax)

        plt.plot(SNRs_teoricas, pe_teorica, label='Teórica M= %d' %M,zorder=1)
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
    if show_plot:
        plt.show()
    plt.close()
    plt.clf()

def generate_pe_plot(constellation, Nsamples, SNRmax, Ms, show_plot):
    return generate_plot(constellation, Nsamples, SNRmax, Ms, show_plot, "pe")

def generate_pb_plot(constellation, Nsamples, SNRmax, Ms, show_plot):
    return generate_plot(constellation, Nsamples, SNRmax, Ms, show_plot, "pb")

def plot_all_pb(Nsamples, SNRmax, show_plot):

    modulations = {}
    modulations["QAM"] = QAM(16, 1)
    modulations["PAM"] = PAM(16, 1)
    modulations["PSK"] = PSK(16, 1)
    modulations["FSK"] = FSK(16, 1)
    for modulation_name in modulations:
        SNRs_estimacion, pe_estimada = modulations[modulation_name].montecarlo_pb_vs_snr(SNRmax, Nsamples)
        SNRs_teoricas, pe_teorica = modulations[modulation_name].theorical_pb_vs_snr(SNRmax)
        plt.plot(SNRs_teoricas, pe_teorica, label=f"{modulation_name} teórica",zorder=1)
        plt.scatter(SNRs_estimacion, pe_estimada, label=f"{modulation_name} estimada",zorder=2)

    plt.title('Probabilidades de error de bit para M=16')
    plt.yscale('log')
    plt.xlabel('SNR [dB]')
    plt.ylabel('log(Probabilidad de error)')
    plt.legend()
    plt.grid()
    plt.savefig(f'results/all_modulations.png')
    if show_plot:
        plt.show()
    plt.close()
    plt.clf()

def main():

    Nsamples = int(1e4)
    SNRmax = 10
    pulse_energy = 1
    varios_M = [2,4,8,16]

    # Graficos de prob de error
    generate_pe_plot("PAM", Nsamples, SNRmax, varios_M, False)
    generate_pe_plot("PSK", Nsamples, SNRmax, varios_M, False)
    generate_pe_plot("FSK", Nsamples, SNRmax, varios_M, False)
    varios_M = [4,8,16]
    generate_pe_plot("QAM", Nsamples, SNRmax, varios_M, False)

    varios_M = [2,4,8,16]
    # Graficos de prob de error de bit
    generate_pb_plot("PAM", Nsamples, SNRmax, varios_M, False)
    generate_pb_plot("PSK", Nsamples, SNRmax, varios_M, False)
    generate_pb_plot("FSK", Nsamples, SNRmax, varios_M, False)
    varios_M = [4,8,16]
    generate_pb_plot("QAM", Nsamples, SNRmax, varios_M, False)

    # Graficamos pb para todas
    plot_all_pb(Nsamples, SNRmax, False)


if __name__ == "__main__":
    main()
