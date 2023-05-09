#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 19:26:11 2023

@author: miaweaver
"""
import sys

import time
import signal
from random import choice, sample

import grpc
from concurrent import futures

import blockchain_pb2
import blockchain_pb2_grpc

from blockchain import Blockchain, Transaction

#RPC STATE UPDATE HANDLERS
##handle issued_tx msg
#   Add transaction to pending pool.
def handle_issuedTX(src, dst, amnt, reward, timestamp):
    global PENDING_POOL
    print("Adding transaction to pending pool...")
    print("src: %d; dst: %s; amnt: %s; reward: %s, timestamp: %s" % (src, dst, amnt, reward, timestamp))
    
    tx_str = str(src) + " " + str(dst) + " " + str(amnt) + " " + str(reward) + " " + str(timestamp)
    PENDING_POOL.append(tx_str)
    print("NUM PENDING TXS:", len(PENDING_POOL))
    return hash( ((hash((src, dst)), hash((reward, amnt))), timestamp) ) 

##handle append_block_request
#   If block valid, append to chain. Else, update or do nothing.
def handle_block_append_request(chain_length, block_dict):
    global BLOCKCHAIN
    print("Receiving block_append_request")
    block_status = False
    #print(block_dict["prev_hash"],  BLOCKCHAIN.blocks[-1].block_hash)
    #print(chain_length, len(BLOCKCHAIN.blocks) + 1)
    if chain_length == len(BLOCKCHAIN.blocks) + 1 and block_dict["prev_hash"] == BLOCKCHAIN.blocks[-1].block_hash:
        try:
            BLOCKCHAIN.add_block(block_dict["LOCAL_ID"], block_dict["txs"],
                                 block_dict["prev_hash"], block_dict["nonce"])
            block_status = True
            print("Valid block appended to chain...")
        except Exception as e:
            print("Append failure; block invalid...", e)
    else:
        print("Append failure; Chains don't match...")
        
    print("CURRENT BLOCKCHAIN:")
    for block in BLOCKCHAIN.blocks:
        print("**************************************************")
        print("BLOCK with hash %s and prev hash %s" % (block.block_hash, block.prev_hash if block.prev_hash != "" else "NULL") )
        if len(block.txs) == 0:
            print("No transactions in block...")
        else:
            print("%d transactions:" % len(block.txs))
            for tx in block.txs:
                print(tx)
        print(f'The solution is nonce = {block.nonce}')
        # print("Successful hash:", hashlib.sha256(f'{self.block_hash*nonce}'.encode()).hexdigest()[difficulty:])
        print("**************************************************")
        print("\n")

    return block_status

##handle hash_request
#   Send last block hash to requester; used so replicas can update one another
def get_hash(block_index):
    global BLOCKCHAIN
    last_block_index = len(BLOCKCHAIN.blocks) - 1
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
    global SERVERS, LOCAL_ID, SERVER_NUM
    SERVERS = {}
    print("Reading from [config.conf] and initializing server...")
    with open("config.conf", "r") as f:
        for line in f:
            SERVERS[int(line.split(" ")[0])] = f'{line.split(" ")[1]}:{line.split(" ")[2].rstrip()}'
            
    SERVER_NUM = int(sys.argv[1])
    LOCAL_ID = SERVERS[SERVER_NUM]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blockchain_pb2_grpc.add_blockchainServicer_to_server(blockchainServices(), server)
    server.add_insecure_port(LOCAL_ID)
    server.start()
    print("Server started successfully. Local ID is", LOCAL_ID)
    return server

##INITIALIZE STATE
def init_state():
    global PENDING_POOL, BLOCKCHAIN, WALLET, SUSPENDED, LOCAL_ID
    
    WALLET = 10000
    print("Initializing state... init [WALLET] amnt is %d" % WALLET)
    
    SUSPENDED = False
    PENDING_POOL = [] #will contain list of rpc "issue_tx" messages & tx's waiting to be committed
    BLOCKCHAIN = Blockchain(SERVER_NUM) #init blockchain to populate later
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

def check_if_replica_needs_updated(original_response, id_):
    global BLOCKCHAIN, SERVERS

    if original_response.status == False:
        if original_response.chain_len < len(BLOCKCHAIN.blocks):
            print("REPLICA CHAIN SHORTER:", original_response.chain_len, "blocks.")
            for i in range(1, len(BLOCKCHAIN.blocks[:original_response.chain_len])):
                print("Requesting block #", len(BLOCKCHAIN.blocks[:original_response.chain_len]) - i)
                channel = grpc.insecure_channel(SERVERS[id_])
                stub = blockchain_pb2_grpc.blockchainStub(channel)
                params = blockchain_pb2.request_hash(block_index = -i)
                response = stub.return_hash(params)
                print("HASH IS:", response.block_hash)
                if response.block_hash == BLOCKCHAIN.blocks[:original_response.chain_len-i]:
                    print("FOUND LAST COMMON BLOCK...")
                    print("**************************************************")
                    print("BLOCK with hash %s and prev hash %s" % (BLOCKCHAIN.blocks[:original_response.chain_len-i].block_hash, BLOCKCHAIN.blocks[:original_response.chain_len-i].prev_hash if BLOCKCHAIN.blocks[:original_response.chain_len-i].prev_hash != "" else "NULL") )
                    if len(BLOCKCHAIN.blocks[:original_response.chain_len-i].txs) == 0:
                        print("No transactions in block...")
                    else:
                        print("%d transactions:" % len(BLOCKCHAIN.blocks[:original_response.chain_len-i].txs))
                        for tx in BLOCKCHAIN.blocks[:original_response.chain_len-i].txs:
                            print(tx)
                    print(f'The solution is nonce = {BLOCKCHAIN.blocks[:original_response.chain_len-i].nonce}')
                    print("**************************************************")
                    break
    return


def prop_block():
    global BLOCKCHAIN, SERVERS, LOCAL_ID, SERVER_NUM, PENDING_POOL
    #responses = []
    for id_ in SERVERS.keys():
        if SERVER_NUM == id_:
            continue
        else:            
            channel = grpc.insecure_channel(SERVERS[id_])
            stub = blockchain_pb2_grpc.blockchainStub(channel)
            
            tx_list = str([tx.str for tx in BLOCKCHAIN.blocks[-1].txs])[1:-1]
            params = blockchain_pb2.append_block_request(chain_length = len(BLOCKCHAIN.blocks),
                                                         transactions = tx_list,
                                                         block_hash = BLOCKCHAIN.blocks[-1].block_hash,
                                                         prev_hash = BLOCKCHAIN.blocks[-1].prev_hash,
                                                         nonce = BLOCKCHAIN.blocks[-1].nonce,
                                                         src_server = SERVER_NUM
                                                         )
            response = stub.propBlock(params)
            #check_if_replica_needs_updated(response, id_)
    return response

def batch_txs():
    global PENDING_POOL
    print("Batching transactions... PENDING POOL LEN: ", len(PENDING_POOL))
    tx_list = []
    
    if len(PENDING_POOL) > 10:
        num_txs = 10
    else:
        num_txs = len(PENDING_POOL)
        
    tx_str_list = sample(PENDING_POOL, num_txs)
    for tx_str in tx_str_list:
        print("Adding [%s] to block..." % tx_str)
        tx_list.append( Transaction(tx_str) )
        
    NEW_PENDING = []
    for tx_str in PENDING_POOL:
        if tx_str not in tx_str_list:
            NEW_PENDING.append(tx_str)
    PENDING_POOL = NEW_PENDING
    print("PENDING POOL LEN IS NOW:", len(PENDING_POOL))
    return tx_list

def create_block(signum, frame):
    global BLOCKCHAIN, LOCAL_ID, SERVER_NUM
    stop_timer() ##stop the timer...
    
    if len(PENDING_POOL) == 0:
        set_timer(create_block)
        return
    #try:
    print("\n")
    print("Creating block...")
    tx_list = batch_txs()
    print("Appending new block to chain...")
    BLOCKCHAIN.add_block(SERVER_NUM, tx_list, BLOCKCHAIN.blocks[-1].block_hash)
    print("Propagating...")
    prop_block()
    print("\n")
    #except Exception as e:
    #    print("Batching and propagating transactions fail...\nError msg:")
    #    print(e)
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
                time.sleep(15)
                server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
                blockchain_pb2_grpc.add_blockchainServicer_to_server(blockchainServices(), server)
                server.add_insecure_port(LOCAL_ID)
                server.start()
                SUSPENDED = False
                print("Server re-started...")
            print("waiting...")
            time.sleep(5)
        ##TODO: check if 5th back block committed yet... if not, commit it
    except Exception as e:
        print(e)
    return

#/////////////////////////////////////////////////////////////////////////////
##DIRECT INCOMING RPC
class blockchainServices(blockchain_pb2_grpc.blockchainServicer):
    ##HANDLE RPC CALLS....
    ##handles incoming RPC and changes state accordingly
    def issueTX(self, request, context):
        print("handling transaction...")
        tx_hash = handle_issuedTX(request.src, request.dst, request.amnt, request.reward, request.timestamp)
        resp = blockchain_pb2.tx_hash(hash = str(tx_hash))
        return resp

    def checkHashes(self, request, context):
        block_hash, last_block_index = get_hash(request.block_index)
        resp = blockchain_pb2.return_hash(block_hash = block_hash, last_block_index = last_block_index)
        return resp
    
    def propBlock(self, request, context):#chain_length, prev_hash, new_block):
        block_dict = {"LOCAL_ID"    : request.src_server,
                      "block_hash"  : request.block_hash,
                      "prev_hash"   : request.prev_hash,
                      "nonce"       : request.nonce,
                      "txs"         : request.transactions.split(",")}
        
        block_status = handle_block_append_request(request.chain_length, block_dict)
        resp = blockchain_pb2.block_status(status = block_status)
        return resp

    def suspend(self, request, context):
        handle_suspend()
        return
    ##TODO: handle incoming updateReplica, printChain
    ##END HANDLE RPC CALLS....
    

if __name__ == "__main__":
    server = init_servers()    
    init_state()
    event_loop(server)

