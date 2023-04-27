#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 19:26:11 2023

@author: miaweaver
"""
import sys

import time
import signal
from random import choice

import grpc
from concurrent import futures

import blockchain_pb2
import blockchain_pb2_grpc

from blockchain import Blockchain, Transaction

#RPC STATE UPDATE HANDLERS
##handle issued_tx msg
#   Add transaction to pending pool.
def handle_issuedTX(src, dst, amnt, reward, timestamp):
    global PENDING_TX_POOL
    print("Adding transaction to pending pool...")
    print("src: %d; dst: %s; amnt: %s; reward: %s, timestamp: %s" % (src, dst, amnt, reward, timestamp))
    
    tx_str = str(src) + " " + str(dst) + " " + str(amnt) + " " + str(reward) + " " + str(timestamp)
    PENDING_TX_POOL.append(tx_str)
    return hash( ((hash((src, dst)), hash((reward, amnt))), timestamp) ) 

##handle append_block_request
#   If block valid, append to chain. Else, update or do nothing.
def handle_block_append_request(chain_length, block_dict):
    global BLOCKCHAIN
    print("Receiving block_append_request")
    block_status = False
    if chain_length == len(BLOCKCHAIN.blocks) - 1 and block_dict["prev_hash"] == BLOCKCHAIN.blocks[-1].block_hash:
        try:
            BLOCKCHAIN.add_block(block_dict["LOCAL_ID"], block_dict["txs"],
                                 block_dict["prev_hash"], block_dict["nonce"])
            block_status = True
            print("Valid block appended to chain...")
        except:
            print("Append failure; block invalid...")
    else:
        print("Append failure; Chains don't match...")
    return block_status

##handle hash_request
#   Send last block hash to requester; used so replicas can update one another
def get_hash(block_index):
    last_block_index = len(BLOCKCHAIN.blocks) - 1
    global BLOCKCHAIN
    if block_index < len(BLOCKCHAIN.blocks):
        print("Servicing get_hash request for block index %d. Returning hash %s." % (last_block_index, BLOCKCHAIN.blocks[block_index].block_hash))
        return BLOCKCHAIN.blocks[block_index].block_hash, last_block_index
    else:
        print("Index out of bounds.")
        return "", last_block_index 
    
##handle_suspend
#   Suspends replica to evaluate performance during partitions
def handle_suspend():
    global SUSPENDED
    SUSPENDED = True
    return

#/////////////////////////////////////////////////////////////////////////////
##STARTUP
##INITIALIZE STATE
def init_servers():
    global SERVERS, LOCAL_ID
    print("Reading from [config.conf] and initializing server...")
    with open("config.conf", "r") as f:
        for line in f:
            SERVERS[int(line.split(" ")[0])] = f'{line.split(" ")[1]}:{line.split(" ")[2].rstrip()}'
            
    LOCAL_ID = SERVERS[int(sys.argv[1])]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blockchain_pb2_grpc.add_blockchainServicer_to_server(blockchainServices(), server)
    server.add_insecure_port(LOCAL_ID)
    server.start()
    print("Server started successfully. Local ID is " % LOCAL_ID)
    return

##INITIALIZE STATE
def init_state():
    global PENDING_TX_POOL, BLOCKCHAIN, WALLET, SUSPENDED
    
    WALLET = 10000
    print("Initializing state... init [WALLET] amnt is %d" % WALLET)
    
    SUSPENDED = False
    PENDING_TX_POOL = [] #will contain list of rpc "issue_tx" messages
    BLOCKCHAIN = Blockchain() #init blockchain to populate later
    return

#/////////////////////////////////////////////////////////////////////////////
#EVENT_LOOP, TIMER, AND BATCH_TXS
##SET TIMER
#   When timer reaches 0, batch transactions into block
def set_timer(func): 
    heartbeat_timeout = choice(range(10, 30)) ##EDIT THIS..
    signal.signal(signal.SIGALRM, func)
    signal.alarm(heartbeat_timeout)
    return

def stop_timer():
    signal.alarm(0)
    return

def prop_block():
    global BLOCKCHAIN, SERVERS
    for id_ in SERVERS.keys():
        if LOCAL_ID == id_:
            continue
        else:
            channel = grpc.insecure_channel(SERVERS[id_])
            stub = blockchain_pb2_grpc.BlockchainStub(channel)
            
            tx_list = []
            tx_list[:] = [tx.str for tx in BLOCKCHAIN.blocks[-1].txs],
            params = blockchain_pb2.append_block_request(chain_length = len(BLOCKCHAIN.blocks),
                                                         transactions = tx_list,
                                                         block_hash = BLOCKCHAIN.blocks[-1].block_hash,
                                                         prev_hash = BLOCKCHAIN.blocks[-1].prev_hash,
                                                         nonce = BLOCKCHAIN.blocks[-1].nonce
                                                         )
            response = stub.propBlock(params)
    return response

def batch_txs():
    global PENDING_TX_POOL
    print("Batching transactions...")
    tx_list = []
    for i in range(10):
        if i == len(PENDING_TX_POOL):
            raise Exception("No transactions to batch.")
        tx_str = choice(PENDING_TX_POOL)
        print("Adding [%s] to block..." % tx_str)
        tx_list.append( Transaction(tx_str) )
    return tx_list

def create_block():
    global BLOCKCHAIN, LOCAL_ID
    print("Creating block...")
    stop_timer() ##stop the timer...
    
    if len(PENDING_TX_POOL) == 0:
        set_timer(create_block)
        return
    try:
        tx_list = batch_txs()
        print("Appending new block to chain...")
        BLOCKCHAIN.add_block(LOCAL_ID, tx_list, BLOCKCHAIN.blocks[-1].prev_hash)
        print("Propagating...")
        prop_block()
    except Exception as e:
        print("Batching and propagating transactions fail...\nError msg:")
        print(e)
    ##TODO: if not block_status, request chain_length & hash of other chain to init updating...
    set_timer(create_block)
    return 
    
##EVENT LOOP COORDINATING OUT-GOING RPC
def event_loop(server):
    global SUSPENDED, LOCAL_ID
    try:
        set_timer(create_block)
        
        while True: 
            
            if SUSPENDED: ##suspending to invoke leader re-election
                print("Suspending...")
                server.stop(0)
                time.sleep(5)
                server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
                blockchain_pb2_grpc.add_blockchainServicer_to_server(blockchainServices(), server)
                server.add_insecure_port(LOCAL_ID)
                server.start()
                SUSPENDED = False
                print("Server re-started...")
                
        ##TODO: check if 5th back block committed yet... if not, commit it
    except Exception as e:
        print(e)
    return

#/////////////////////////////////////////////////////////////////////////////
##DIRECT INCOMING RPC
class blockchainServices(blockchain_pb2_grpc.blockchainServicer):
    ##HANDLE RPC CALLS....
    ##handles incoming RPC and changes state accordingly
    def appendTransaction(request, context):
        resp = handle_issuedTX(request.src, request.dst, request.amnt, request.reward, request.timestamp)
        return resp

    def checkHashes(request, context):
        block_hash, last_block_index = get_hash(request.block_index)
        resp = blockchain_pb2.return_hash(block_hash = block_hash, last_block_index = last_block_index)
        return resp
    
    def propBlock(request, context):#chain_length, prev_hash, new_block):
        block_dict = {"block_hash"  : request.block_hash,
                      "prev_hash"   : request.prev_hash,
                      "nonce"       : request.nonce,
                      "txs"         : request.txs}
        block_status = handle_block_append_request(request.chain_length, block_dict)
        resp = blockchain_pb2.block_status(status = block_status)
        return resp

    def suspend(request, context):
        handle_suspend()
        return
    ##TODO: handle incoming updateReplica, printChain
    ##END HANDLE RPC CALLS....
    

if __name__ == "__main__":
    init_servers()    
    init_state()

