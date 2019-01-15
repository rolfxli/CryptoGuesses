from pwn import *

from string import lowercase

alphabet = lowercase + '_'

# r = process('./serv-distribute.py')
r = remote('crypto.chal.csaw.io', 8040)

guesses = ['']
max_len = 0

while max_len < 40:
  new_guesses = []
  for guess in guesses:
    for char in alphabet:
      pat = char + guess
      this = pat * max(int(20/len(pat)) + 1, 4)
      r.recvline()
      r.sendline(this)
      length = ord(r.recvline()[-2])
      new_guesses.append((pat, length))
  best_len = min(new_guesses, key=lambda x: x[1])[1]
  guesses += [x[0] for x in filter(lambda x: x[1] == best_len, new_guesses)]
  max_len = max(map(len, guesses))
  guesses = list(filter(lambda x: len(x) == max_len, guesses))
  print(guesses, best_len)
