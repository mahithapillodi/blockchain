#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 01:44:47 2023

@author: miaweaver
"""

from hashlib import sha256
from datetime import datetime as dt


block_hash = 4795886727471279181
nonce = 1  # We don't know what y should be yet...
difficulty = -7
difficulty_keys = { -5 : "ffffd", -6 : "fffffd", -7 : "ffffffd"}

start = dt.now()
while sha256(f'{block_hash*nonce}'.encode()).hexdigest()[difficulty:] < difficulty_keys[difficulty]: #or [-5:] < ffffd for quicker
    #print(f'{block_hash*nonce}')
    #print(sha256(f'{block_hash*nonce}'.encode()).hexdigest()[-5:]) 
    nonce += 1
end = dt.now()
print(f'The solution is nonce = {nonce}')
print("Successful hash:", sha256(f'{block_hash*nonce}'.encode()).hexdigest()[difficulty:])
print("Time to compute:", end - start)
