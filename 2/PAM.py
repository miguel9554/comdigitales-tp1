import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist

def estimate_pam_pe(M, SNRdb, Nsamples):

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
    
def Q(q):
    return 1 - NormalDist(mu=0, sigma=1).cdf(q)


Nsamples = 1e4
SNRmax = 10

SNRs = range(SNRmax+1)
pe_vec = []

varios_M = [2,4,8,16]
for M in varios_M:
    pe_teorica = [2*(1-1/M)*Q(np.sqrt(6*np.log2(M)*(10**(SNR/10))/(M**2-1))) for SNR in SNRs]
    pe_vec = []
    for SNR in SNRs:
        pe_vec.append(estimate_pam_pe(M, SNR, Nsamples))
    plt.plot(SNRs, np.log(pe_teorica), label='Teórica M= %d' %M,color='r',zorder=1)
    plt.scatter(SNRs, np.log(pe_vec), label='Estimación M = %d' %M,zorder=2)
    
plt.title('Probabilidad de error para PAM')
plt.xlabel('SNR [dB]')
plt.ylabel('log(Probabilidad de error)')
plt.legend()
plt.grid()
#plt.savefig('results/PAM.png')
plt.show()
