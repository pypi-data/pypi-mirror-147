from datetime import datetime
import numpy as np

seed = int(datetime.now().date().strftime('%y%m%d'))
np.random.seed(seed)

a = np.arange(26)
np.random.shuffle(a)

alphabets = [chr(x) for x in range(ord('a'), ord('z')+1)]

alpha_to_pos = {}
pos_to_alpha = {}
for i in range(26):
    alpha_to_pos[alphabets[i]] = i
    pos_to_alpha[i] = alphabets[i]

encoder = {}
decoder = {}
for i, alp in enumerate(alphabets):
    encoder[alp] = pos_to_alpha[a[i]]
    decoder[pos_to_alpha[a[i]]] = alp

def encode_():
    print('TYPE IN THE MESSAGE!')
    text = input()
    encoded=[]
    for ch in text.lower():
        if not ch.isalpha():
            encoded.append(ch)
        else:
            encoded.append(encoder[ch])
    print(('✪ '*45).center(120))
    print('\n'*5)
    print(('-'*7).center(120))
    print('ENCODED'.center(120))
    print(('-'*7).center(120))
    print('✪CLASSIFIED'.center(120))
    print()
    print(''.join(encoded).upper().center(120))
    print('\n'*5)
    print(('✪ '*45).center(120))

def decode_(text):
    print('TYPE IN THE ENIGMA!')
    text = input()
    decoded=[]
    for ch in text.lower():
        if not ch.isalpha():
            decoded.append(ch)
        else:
            decoded.append(decoder[ch])
    print(('✪ '*45).center(120))
    print('\n'*5)
    print(('-'*7).center(120))
    print('ENCODED'.center(120))
    print(('-'*7).center(120))
    print('✪CLASSIFIED'.center(120))
    print()
    print(''.join(decoded).upper().center(120))
    print('\n'*5)
    print(('✪ '*45).center(120))