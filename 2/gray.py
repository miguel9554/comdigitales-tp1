from typing import List
import numpy as np

def gray_coding_pam(code: str, bits: int) -> List[int]:
    if len(code) != bits:
        raise ValueError(f'El código debe tener {bits} de largo, tiene {len(code)}')
    if bits == 1:
        if code == "0":
            return [1]
        elif code == "1":
            return [-1]
    elif bits > 1:
        return [(1-2*int(code[0]))*(2**(bits-1)+gray_coding_pam(code[1:], bits-1)[0])]

def gray_coding_qam(code: str, bits_i: int, bits_q: int) -> List[int]:
    i_value = gray_coding_pam(code[:bits_i], bits_i)[0]
    q_value = gray_coding_pam(code[bits_i:], bits_q)[0]
    return [i_value, q_value]

def psk_table(n): 
  
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
def different_bits(code1: str, code2: str) -> int:
    return sum(1 for a, b in zip(code1, code2) if a != b)

def main():

    code = "1010"
    symbol = gray_coding_qam(code, 2, 2)
    #code = "11"
    #symbol = gray_coding_pam(code, len(code))
    print(type(symbol))
    print(f"El código {code} se corresponde al símbolo {symbol}")

if __name__ == "__main__":
    main()

