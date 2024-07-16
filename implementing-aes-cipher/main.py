#am ramas la vid #3

def key_expansion(key):
    pass

def state_from_bytes(data):
    state = [data[i*4:(i+1)*4] for i in range(len(data)//4)]
    return state

def add_round_key(state,key_schedule,round):
    pass

def sub_bytes(state):
    pass 

def shift_rows(state):
    pass 

def mix_columns(state):
    pass

def bytes_from_state(state)->bytes:
    cipher = bytes(state[0]+state[1]+state[2]+state[3])
    return cipher

def aes_encryption(data:bytes,key:bytes)->bytes:
    state = state_from_bytes(data)

    key_schedule = key_expansion(key) 
    add_round_key(state,key_schedule,round=0)

    key_bit_length = len(key) * 8
    if key_bit_length == 128:
        nr = 10 
    if key_bit_length == 192:
        nr = 12 
    if key_bit_length == 256:
        nr = 14
    for round in range(1,nr):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state,key_schedule,round)

    sub_bytes(state)
    shift_rows(state)
    mix_columns(state)
    add_round_key(state,key_schedule,round=nr)

    cipher = bytes_from_state(state)
    return cipher




if __name__ == "__main__":
    #NIST AES-128 test vector appendix c.1
    plaintext = bytearray.fromhex('00112233445566778899aabbccddeeff')
    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f')
    expected_ciphertext = bytearray.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
    ciphertext = aes_encryption(plaintext,key)
    print(ciphertext)
    #assert(ciphertext == expected_ciphertext)

    #NIST AES-192 test vector appendix c.2 
    plaintext = bytearray.fromhex('00112233445566778899aabbccddeeff')
    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f1011121314151617')
    expected_ciphertext = bytearray.fromhex('dda97ca4864cdfe06eaf70a0ec0d7191')
    ciphertext = aes_encryption(plaintext,key)
    #assert(ciphertext == expected_ciphertext)

    #NIST AES-256 test vector appendix c.3 
    plaintext = bytearray.fromhex('00112233445566778899aabbccddeeff')
    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')
    expected_ciphertext = bytearray.fromhex('8ea2b7ca516745bfeafc49904b496089')
    ciphertext = aes_encryption(plaintext,key)
    #assert(ciphertext == expected_ciphertext)
