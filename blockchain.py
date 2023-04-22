#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 22:25:36 2023

@author: miaweaver
"""
#from datetime import datetime as dt

#NOTE: 
    #referenced this link for merkle tree implementation reference:
#http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
    #reference this link for POW
#https://dev.to/envoy_/learn-blockchains-by-building-one-in-python-2kb3#:~:text=A%20Proof%20of%20Work%20algorithm,idea%20behind%20Proof%20of%20Work.

##########################################################################
import hashlib
from datetime import datetime as dt


class Blockchain:
    class Block:
        def __init__(self, server_id, tx_list = [], prev_hash = ""):
            self.server_id = server_id
            self.prev_hash = prev_hash
            self.txs = tx_list
            self.merkle_root = self.get_merkle_root( self.get_tx_hashes(tx_list) )
            self.block_hash = self.get_block_hash()
            self.nonce = self.get_nonce()
            
        def get_tx_hashes(self, tx_list):
            tx_hashes = []
            for tx in tx_list:
                tx_hashes.append( hash( ((hash((tx.src, tx.dst)), hash((tx.reward, tx.amnt))), tx.ts) ) )
            return tx_hashes

        def get_merkle_root(self, tx_hashes): ##recursive func
            if len(tx_hashes) == 0:
                return "root_block"
            if len(tx_hashes) == 1: ##base case; list len == 1 aka all pairs have been hashed
                return tx_hashes[0]
            new_tx_hashes = []
            # Process pairs. For odd length, the last is skipped
            for i in range(0, len(tx_hashes)-1, 2): ##iterate through list, increment by two as pairing together hash i with hash i + 1
                new_tx_hashes.append(hash( (tx_hashes[i], tx_hashes[i+1]) ))
            if len(tx_hashes) % 2 == 1: # odd, hash last item twice
                new_tx_hashes.append(hash( (tx_hashes[-1], tx_hashes[-1]) ))
            return self.get_merkle_root(new_tx_hashes) ##after hashing pairs, call self to hash new pairs
        
        def get_block_hash(self):
            if self.prev_hash == "":
                return hash( (self.merkle_root, self.server_id) )
            return hash( (hash( (self.merkle_root, self.prev_hash) ), self.server_id) )
    
        def get_nonce(self):
            print("Mining block...")
            nonce = 0
            difficulty_keys = { -5 : "ffffd", -6 : "fffffd", -7 : "ffffffd"}
            difficulty = -6
            start = dt.now()
            while hashlib.sha256(f'{self.block_hash*nonce}'.encode()).hexdigest()[difficulty:] < difficulty_keys[difficulty]: #or [-5:] < ffffd for quicker
                #print(f'{block_hash*nonce}')
                #print(sha256(f'{block_hash*nonce}'.encode()).hexdigest()[-5:]) 
                nonce += 1
            end = dt.now()
            print(f'The solution is nonce = {nonce}')
            print("Successful hash:", hashlib.sha256(f'{self.block_hash*nonce}'.encode()).hexdigest()[difficulty:])
            print("Time to compute:", end - start)
            return nonce
    
        def __str__(self):
            return "server_id: %d; prev_hash: %s; merkle_root: %s; block_hash: %s" % (self.server_id, self.prev_hash, self.merkle_root, self.block_hash)


    def __init__(self, server_id):
        self.blocks = [ self.Block(server_id) ]
        
    def add_block(self, server_id, tx_list, prev_hash):
        if prev_hash == self.blocks[-1].block_hash:
            new_block = self.Block(server_id, tx_list, prev_hash)
            self.blocks.append(new_block)
        return


#FOR TESTING:
class TX:
    def __init__(self, src, dst, amnt, reward, ts):
        self.src = src
        self.dst = dst
        self.amnt = amnt
        self.reward = reward
        self.ts = ts
        
     
ts = dt.now().timestamp()
ts = 4386663582533938045
tx_list = []
#dt.now().timestamp()
tx_list.append( TX( 1, 2, 3000, 10, dt.now().timestamp() ) )
tx_list.append( TX( 1, 3, 110, 40, dt.now().timestamp() ) )
tx_list.append( TX( 1, 4, 10, 33, dt.now().timestamp() ) )
tx_list.append( TX( 1, 2, 1000, 2, dt.now().timestamp() ) )
tx_list.append( TX( 1, 5, 100, 120, dt.now().timestamp() ) )

blockchain = Blockchain(0)
print(blockchain.blocks[-1])
print("ROOT BLOCK INITIALIZED\n")

blockchain.add_block(0, tx_list, hash( ("root_block", 0) ))
print(blockchain.blocks[1])
print("TXS IN LAST BLOCK:")
for tx in blockchain.blocks[-1].txs:
    print("SRC:", tx.src, "DST:", tx.dst, 
          "AMNT:", tx.amnt, "REWARD:", tx.reward, "ISSUED AT:", tx.ts)
print("\n")

blockchain.add_block(0, tx_list[4:], blockchain.blocks[-1].block_hash)
print(blockchain.blocks[-1])
print("TXS IN LAST BLOCK:")
for tx in blockchain.blocks[-1].txs:
    print("SRC:", tx.src, "DST:", tx.dst, 
          "AMNT:", tx.amnt, "REWARD:", tx.reward, "ISSUED AT:", tx.ts)
print("\n")

blockchain.add_block(0, tx_list[1:3], blockchain.blocks[-1].block_hash)
print(blockchain.blocks[-1])
print("TXS IN LAST BLOCK:")
for tx in blockchain.blocks[-1].txs:
    print("SRC:", tx.src, "DST:", tx.dst, 
          "AMNT:", tx.amnt, "REWARD:", tx.reward, "ISSUED AT:", tx.ts)
print("\n")

