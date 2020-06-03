import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist

def estimate_pe(M, SNRdb, Nsamples):

    d = 2
    # Generamos los símbolos
    M = 8
    if M == 4:
        X = [d*(n-1/2) for n in np.random.randint(0, 2, int(Nsamples))]
        Y = [d*(n-1/2) for n in np.random.randint(0, 2, int(Nsamples))]
        x_edge_value = [-d/2, d/2]
        y_edge_value = [-d/2, d/2]
    elif M == 8:
        X = [d*(2*n-3)/2 for n in np.random.randint(0, 4, int(Nsamples))]
        Y = [d*(n-1/2) for n in np.random.randint(0, 2, int(Nsamples))]
        x_edge_value = [-d*3/2, d*3/2]
        y_edge_value = [-d/2, d/2]
    elif M == 16:
        X = [d*(2*n-3)/2 for n in np.random.randint(0, 4, int(Nsamples))]
        Y = [d*(2*n-3)/2 for n in np.random.randint(0, 4, int(Nsamples))]
        x_edge_value = [-d*3/2, d*3/2]
        y_edge_value = [-d*3/2, d*3/2]

    # Obtenemos N0
    SNRveces = 10**(SNRdb/10)
    Eb = d**2*(M-1)/(6*np.log2(M))
    N0 = Eb/SNRveces

    # Le agregamos ruido a los símbolos y nos fijamos si caen dentro de la frontera de decisión
    errors = 0
    for idx in len(X):

        x_sent = X[idx]
        y_sent = Y[idx]

        x_noise = np.random.normal(0, np.sqrt(N0/2), 1)
        y_noise = np.random.normal(0, np.sqrt(N0/2), 1)

        x_received = x_sent + x_noise
        y_received = y_sent + y_noise

        if x_sent in x_edge_value and y_sent in y_edge_value:
            # Caso esquina
            if x_sent == x_edge_value[0] and y_sent == y_edge_value[1]:
                if x_received > x_sent + d/2 or y_received < y_sent - d/2:
                    errors += 1
            pass
        elif (x_sent in x_edge_value and y_sent not in y_edge_value) or (y_sent in y_edge_value and x_sent not in x_edge_value):
            # Caso lateral
            pass
        else:
            # Caso interior
            pass


    return errors/Nsamples
    

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
