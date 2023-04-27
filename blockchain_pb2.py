# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: blockchain.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x62lockchain.proto\"\x0e\n\x0c\x45mptyMessage\"U\n\x08issue_tx\x12\x0b\n\x03src\x18\x01 \x01(\x05\x12\x0b\n\x03\x64st\x18\x02 \x01(\x05\x12\x0c\n\x04\x61mnt\x18\x03 \x01(\x02\x12\x0e\n\x06reward\x18\x04 \x01(\x02\x12\x11\n\ttimestamp\x18\x05 \x01(\x02\"\x17\n\x07tx_hash\x12\x0c\n\x04hash\x18\x01 \x01(\t\")\n\rprint_request\x12\x0b\n\x03src\x18\x01 \x01(\x05\x12\x0b\n\x03\x64st\x18\x02 \x01(\x05\"x\n\x14\x61ppend_block_request\x12\x14\n\x0c\x63hain_length\x18\x01 \x01(\x05\x12\x14\n\x0ctransactions\x18\x02 \x03(\t\x12\x12\n\nblock_hash\x18\x03 \x01(\t\x12\x11\n\tprev_hash\x18\x04 \x01(\t\x12\r\n\x05nonce\x18\x05 \x01(\x05\"\x1e\n\x0c\x62lock_status\x12\x0e\n\x06status\x18\x01 \x01(\x08\"#\n\x0crequest_hash\x12\x13\n\x0b\x62lock_index\x18\x01 \x01(\x05\"7\n\x0breturn_hash\x12\x12\n\nblock_hash\x18\x01 \x01(\t\x12\x14\n\x0c\x63hain_length\x18\x02 \x01(\x05\"\x9d\x01\n\x0eupdate_replica\x12\x1f\n\x17last_common_block_index\x18\x01 \x01(\x05\x12\x1e\n\x16last_common_block_hash\x18\x02 \x01(\t\x12\x14\n\x0ctransactions\x18\x03 \x03(\t\x12\x12\n\nblock_hash\x18\x04 \x01(\t\x12\x11\n\tprev_hash\x18\x05 \x01(\t\x12\r\n\x05nonce\x18\x06 \x01(\x05\")\n\x0ereplica_status\x12\x17\n\x0flast_block_hash\x18\x01 \x01(\t\"\x1f\n\x0fsuspend_request\x12\x0c\n\x04temp\x18\x01 \x01(\x05\x32\xa8\x02\n\nblockchain\x12 \n\x07issueTX\x12\t.issue_tx\x1a\x08.tx_hash\"\x00\x12\x32\n\x0fprintBlockchain\x12\x0e.print_request\x1a\r.EmptyMessage\"\x00\x12\x33\n\tpropBlock\x12\x15.append_block_request\x1a\r.block_status\"\x00\x12,\n\x0b\x63heckHashes\x12\r.request_hash\x1a\x0c.return_hash\"\x00\x12\x33\n\rupdateReplica\x12\x0f.update_replica\x1a\x0f.replica_status\"\x00\x12,\n\x07suspend\x12\x10.suspend_request\x1a\r.EmptyMessage\"\x00\x62\x06proto3')



_EMPTYMESSAGE = DESCRIPTOR.message_types_by_name['EmptyMessage']
_ISSUE_TX = DESCRIPTOR.message_types_by_name['issue_tx']
_TX_HASH = DESCRIPTOR.message_types_by_name['tx_hash']
_PRINT_REQUEST = DESCRIPTOR.message_types_by_name['print_request']
_APPEND_BLOCK_REQUEST = DESCRIPTOR.message_types_by_name['append_block_request']
_BLOCK_STATUS = DESCRIPTOR.message_types_by_name['block_status']
_REQUEST_HASH = DESCRIPTOR.message_types_by_name['request_hash']
_RETURN_HASH = DESCRIPTOR.message_types_by_name['return_hash']
_UPDATE_REPLICA = DESCRIPTOR.message_types_by_name['update_replica']
_REPLICA_STATUS = DESCRIPTOR.message_types_by_name['replica_status']
_SUSPEND_REQUEST = DESCRIPTOR.message_types_by_name['suspend_request']
EmptyMessage = _reflection.GeneratedProtocolMessageType('EmptyMessage', (_message.Message,), {
  'DESCRIPTOR' : _EMPTYMESSAGE,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:EmptyMessage)
  })
_sym_db.RegisterMessage(EmptyMessage)

issue_tx = _reflection.GeneratedProtocolMessageType('issue_tx', (_message.Message,), {
  'DESCRIPTOR' : _ISSUE_TX,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:issue_tx)
  })
_sym_db.RegisterMessage(issue_tx)

tx_hash = _reflection.GeneratedProtocolMessageType('tx_hash', (_message.Message,), {
  'DESCRIPTOR' : _TX_HASH,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:tx_hash)
  })
_sym_db.RegisterMessage(tx_hash)

print_request = _reflection.GeneratedProtocolMessageType('print_request', (_message.Message,), {
  'DESCRIPTOR' : _PRINT_REQUEST,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:print_request)
  })
_sym_db.RegisterMessage(print_request)

append_block_request = _reflection.GeneratedProtocolMessageType('append_block_request', (_message.Message,), {
  'DESCRIPTOR' : _APPEND_BLOCK_REQUEST,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:append_block_request)
  })
_sym_db.RegisterMessage(append_block_request)

block_status = _reflection.GeneratedProtocolMessageType('block_status', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK_STATUS,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:block_status)
  })
_sym_db.RegisterMessage(block_status)

request_hash = _reflection.GeneratedProtocolMessageType('request_hash', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST_HASH,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:request_hash)
  })
_sym_db.RegisterMessage(request_hash)

return_hash = _reflection.GeneratedProtocolMessageType('return_hash', (_message.Message,), {
  'DESCRIPTOR' : _RETURN_HASH,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:return_hash)
  })
_sym_db.RegisterMessage(return_hash)

update_replica = _reflection.GeneratedProtocolMessageType('update_replica', (_message.Message,), {
  'DESCRIPTOR' : _UPDATE_REPLICA,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:update_replica)
  })
_sym_db.RegisterMessage(update_replica)

replica_status = _reflection.GeneratedProtocolMessageType('replica_status', (_message.Message,), {
  'DESCRIPTOR' : _REPLICA_STATUS,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:replica_status)
  })
_sym_db.RegisterMessage(replica_status)

suspend_request = _reflection.GeneratedProtocolMessageType('suspend_request', (_message.Message,), {
  'DESCRIPTOR' : _SUSPEND_REQUEST,
  '__module__' : 'blockchain_pb2'
  # @@protoc_insertion_point(class_scope:suspend_request)
  })
_sym_db.RegisterMessage(suspend_request)

_BLOCKCHAIN = DESCRIPTOR.services_by_name['blockchain']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTYMESSAGE._serialized_start=20
  _EMPTYMESSAGE._serialized_end=34
  _ISSUE_TX._serialized_start=36
  _ISSUE_TX._serialized_end=121
  _TX_HASH._serialized_start=123
  _TX_HASH._serialized_end=146
  _PRINT_REQUEST._serialized_start=148
  _PRINT_REQUEST._serialized_end=189
  _APPEND_BLOCK_REQUEST._serialized_start=191
  _APPEND_BLOCK_REQUEST._serialized_end=311
  _BLOCK_STATUS._serialized_start=313
  _BLOCK_STATUS._serialized_end=343
  _REQUEST_HASH._serialized_start=345
  _REQUEST_HASH._serialized_end=380
  _RETURN_HASH._serialized_start=382
  _RETURN_HASH._serialized_end=437
  _UPDATE_REPLICA._serialized_start=440
  _UPDATE_REPLICA._serialized_end=597
  _REPLICA_STATUS._serialized_start=599
  _REPLICA_STATUS._serialized_end=640
  _SUSPEND_REQUEST._serialized_start=642
  _SUSPEND_REQUEST._serialized_end=673
  _BLOCKCHAIN._serialized_start=676
  _BLOCKCHAIN._serialized_end=972
# @@protoc_insertion_point(module_scope)
