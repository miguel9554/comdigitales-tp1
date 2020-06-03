import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist

def estimate_pe(M, SNRdb, Nsamples):

    d = 2
    # Generamos los símbolos
    symbols = [d*(n-(M-1)/2) for n in np.random.randint(0, M, int(Nsamples))]

    # Obtenemos N0
    SNRveces = 10**(SNRdb/10)
    Eb = d**2*(M**2-1)/(12*np.log2(M))
    N0 = Eb/SNRveces

    errors = 0

    for symbol in symbols:
        noise = np.random.normal(0, np.sqrt(N0/2), 1)
        received = symbol + noise
        if received > symbol + d/2 or received < symbol - d/2:
            errors += 1

    return errors/Nsamples

def montecarlo_pe_vs_snr(M, SNRmax, Nsamples):

    SNRs = range(SNRmax+1)
    pe_vec = []

    for SNR in SNRs:
        pe_vec.append(estimate_pe(M, SNR, Nsamples))

    return SNRs, pe_vec

def theorical_pe_vs_snr(M, SNRmax):
    
    SNRs = list(range(SNRmax+1))

    return SNRs, [2*(1-1/M)*Q(np.sqrt(6*np.log2(M)*(10**(SNR/10))/(M**2-1))) for SNR in SNRs]

def Q(q):
    return 2*(1 - NormalDist(mu=0, sigma=1).cdf(q))


Nsamples = 10e3
M = 16
SNRmax = 10

SNRs_montecarlo, pe_montecarlo = montecarlo_pe_vs_snr(M, SNRmax, Nsamples)
SNRs_theorical, pe_theorical = theorical_pe_vs_snr(M, SNRmax)

plt.plot(SNRs_montecarlo, np.log(pe_montecarlo), label='Estimación')
plt.plot(SNRs_theorical, np.log(pe_theorical), label='Teórica')
plt.title(f'Probabilidad de error para {M}-PAM')
plt.xlabel('SNR [dB]')
plt.ylabel('log(Probabilidad de error)')
plt.legend()
plt.grid()
plt.savefig('results/PAM.png')
plt.show()
