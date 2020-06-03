import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist

def estimate_pe(M, SNRdb, Nsamples):

    d = 2
    # Generamos los símbolos
    # Si M=2, es una 2-PAM
    # Si M=4, son 2 2-PAM
    # Si M=8, son 2 4-PAM
    # Si M=16, son 4 4-PAM
    
    if (M==2):
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
    elif (M==4):
        symbols = [d*(n-(M/2-1)/2) for n in np.random.randint(0, M, int(Nsamples))]
        symbols2 = [d*(n-(M/2-1)/2) for n in np.random.randint(0, M, int(Nsamples))]
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
                
        errors2 = 0
        
        for symbol in symbols2:
            noise = np.random.normal(0, np.sqrt(N0/2), 1)
            received = symbol + noise
            if received > symbol + d/2 or received < symbol - d/2:
                errors2 += 1
        return (errors + errors2)/(int(Nsamples)^2)

def montecarlo_pe_vs_snr(M, SNRmax, Nsamples):

    SNRs = range(SNRmax+1)
    pe_vec = []

    for SNR in SNRs:
        pe_vec.append(estimate_pe(M, SNR, Nsamples))

    return SNRs, pe_vec

def theorical_pe_vs_snr(M, SNRmax):
    
    SNRs = list(range(SNRmax+1))

    return SNRs, [4*(1-1/np.sqrt(M))*Q(np.sqrt(6*np.log2(M)*(10**(SNR/10))/(M-1))) for SNR in SNRs]

def Q(q):

    return (1 - NormalDist(mu=0, sigma=1).cdf(q))


Nsamples = 1e4 # aumento para tener mayor precision
SNRmax = 10

varios_M = [2,4]

for M in varios_M:
    SNRs_estimacion, pe_estimada = montecarlo_pe_vs_snr(M, SNRmax, Nsamples)
    SNRs_teoricas, pe_teorica = theorical_pe_vs_snr(M, SNRmax)

    plt.plot(SNRs_teoricas, pe_teorica, label='Teórica M= %d' %M,color='r',zorder=1)
    plt.scatter(SNRs_estimacion, pe_estimada, label='Estimación M = %d' %M,zorder=2)
    
plt.title('Probabilidad de error para QAM')
plt.yscale('log')
plt.xlabel('SNR [dB]')
plt.ylabel('log(Probabilidad de error)')
plt.legend()
plt.grid()
#plt.savefig('results/PAM.png')
plt.show()
