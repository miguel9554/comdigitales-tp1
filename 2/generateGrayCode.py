#import math as mt 
import numpy as np
  
# This function generates all n bit Gray  
# codes and prints the generated codes 
def generateGrayarr(n): 
  
    # base case 
    if (n <= 0): 
        return
  
    # 'arr' will store all generated codes 
    arr = list() 
  
    # start with one-bit pattern 
    arr.append("0") 
    arr.append("1") 
  
    # Every iteration of this loop generates  
    # 2*i codes from previously generated i codes. 
    i = 2
    j = 0
    while(True): 
  
        if np.uint64(i) >= np.uint64(1) << np.uint64(n): 
            break
      
        # Enter the prviously generated codes  
        # again in arr[] in reverse order.  
        # Nor arr[] has double number of codes. 
        for j in range(i - 1, -1, -1): 
            arr.append(arr[j]) 
  
        # append 0 to the first half 
        for j in range(i): 
            arr[j] = "0" + arr[j] 
  
        # append 1 to the second half 
        for j in range(i, 2 * i): 
            arr[j] = "1" + arr[j] 
        i = i << 1
  
    return arr
    # prcontents of arr[] 
    #for i in range(len(arr)): 
    #    print(arr[i])


M = 8;
codes = generateGrayarr(np.log2(M)) # lista ['0', '1']
G = []

for m in range(M): # indice del simbolo
    G.append(codes[m]) # entra un simbolo, sale el codigo
