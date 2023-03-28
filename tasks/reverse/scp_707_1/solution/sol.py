#!/usr/bin/env python

from functools import partial
import hashlib

CIPHER_TEXT = "lvl1_ct"
PLAIN_TEXT  = "lvl1_decrypted"
SIGNATURE   = b'\xff'

def gen_hash_table():
  table = {}

  for i in range(2**16):
    data = i.to_bytes(2, 'little')
    table[hashlib.sha1(data).hexdigest()] = data

  return table


if __name__ == "__main__":
  table = gen_hash_table()

  with open(CIPHER_TEXT, "rb") as cipher_text, open(PLAIN_TEXT, "wb") as plain_text:
    byte_ctr = 0
    result = b""

    for chunk in iter(partial(cipher_text.read, 20), b''):
      byte_ctr += 2
      tmp = chunk.hex()

      result += table[tmp]

    plain_text.write(result)