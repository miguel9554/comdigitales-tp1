from typing import Tuple, List

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

def gray_coding_qam(code: str, bits_i: int, bits_q: int) -> Tuple[int, int]:
    i_value = gray_coding_pam(code[:bits_i], bits_i)
    q_value = gray_coding_pam(code[bits_i:], bits_q)
    return (i_value, q_value)

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

