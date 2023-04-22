#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 19:26:11 2023

@author: miaweaver
"""
import sys

import grpc
from concurrent import futures

import blockchain_pb2
import blockchain_pb2_grpc

from blockchain_obj import blockchain_obj


#RPC STATE UPDATE HANDLERS
def hanlde_issuedTX(tx_msg):
    global PENDING_TX_POOL
    PENDING_TX_POOL.append(tx_msg)
    return

def handle_block_prop(chain_length, prev_hash, new_block):
    global BLOCKCHAIN
    if chain_length < len(BLOCKCHAIN.blocks):
        block_status = False
    elif prev_hash != BLOCKCHAIN.blocks[-1]:
        block_status = False
    else:
        block_status = True
        ##TODO: append block
    return block_status

def get_hash(block_index):
    last_block_index = len(BLOCKCHAIN.blocks) - 1
    global BLOCKCHAIN
    if block_index < len(BLOCKCHAIN.blocks):
        return BLOCKCHAIN.blocks[block_index].block_hash, last_block_index
    else:
        return "", last_block_index 

#/////////////////////////////////////////////////////////////////////////////

##INITIALIZE STATE
def init_servers():
    global SERVERS, LOCAL_ID
    
    with open("config.conf", "r") as f:
        for line in f:
            SERVERS[int(line.split(" ")[0])] = f'{line.split(" ")[1]}:{line.split(" ")[2].rstrip()}'
            
    LOCAL_ID = SERVERS[int(sys.argv[1])]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blockchain_pb2_grpc.add_blockchainServicer_to_server(blockchainServices(), server)
    server.add_insecure_port(LOCAL_ID)
    server.start()
    return

##INITIALIZE STATE
def init_state():
    global PENDING_TX_POOL, STAKERS, BLOCKCHAIN
    
    PENDING_TX_POOL = [] #will contain list of rpc "issue_tx" messages
    STAKERS = {}
    BLOCKCHAIN = blockchain_obj() #init blockchain to populate later

            
##EVENT LOOP COORDINATING OUT-GOING RPC
def event_loop():
    return

#/////////////////////////////////////////////////////////////////////////////
##HANDLE INCOMING RPC
class blockchainServices(blockchain_pb2_grpc.blockchainServicer):
    ##HANDLE RPC CALLS....
    ##handles incoming RPC and changes state accordingly
    
    def checkHashes(block_index):
        
        return
    
    def VoteRequest(source_node, dst_node, term):
        if term > replica_term and replica_state == "F":
            outcome = handle_vote_request()
            vote_4_me_reply = raft_pb2.voted_4_u(source_node = resp_src_node, dst_node = resp_dst_node,
                                                 term = replica_term, outcome = outcome)
        else:
            vote_4_me_reply = raft_pb2.voted_4_u(source_node = resp_src_node, dst_node = resp_dst_node,
                                                 term = replica_term, outcome = False)
        return vote_4_me_reply

    
    ##END HANDLE RPC CALLS....
    

if __name__ == "__main__":
    init_servers()    
    init_state()

