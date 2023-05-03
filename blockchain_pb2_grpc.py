# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import blockchain_pb2 as blockchain__pb2


class blockchainStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.issueTX = channel.unary_unary(
                '/blockchain/issueTX',
                request_serializer=blockchain__pb2.issue_tx.SerializeToString,
                response_deserializer=blockchain__pb2.tx_hash.FromString,
                )
        self.printBlockchain = channel.unary_unary(
                '/blockchain/printBlockchain',
                request_serializer=blockchain__pb2.print_request.SerializeToString,
                response_deserializer=blockchain__pb2.EmptyMessage.FromString,
                )
        self.propBlock = channel.unary_unary(
                '/blockchain/propBlock',
                request_serializer=blockchain__pb2.append_block_request.SerializeToString,
                response_deserializer=blockchain__pb2.block_status.FromString,
                )
        self.checkHashes = channel.unary_unary(
                '/blockchain/checkHashes',
                request_serializer=blockchain__pb2.request_hash.SerializeToString,
                response_deserializer=blockchain__pb2.return_hash.FromString,
                )
        self.updateReplica = channel.unary_unary(
                '/blockchain/updateReplica',
                request_serializer=blockchain__pb2.update_replica.SerializeToString,
                response_deserializer=blockchain__pb2.replica_status.FromString,
                )
        self.suspend = channel.unary_unary(
                '/blockchain/suspend',
                request_serializer=blockchain__pb2.suspend_request.SerializeToString,
                response_deserializer=blockchain__pb2.EmptyMessage.FromString,
                )


class blockchainServicer(object):
    """Missing associated documentation comment in .proto file."""

    def issueTX(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def printBlockchain(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def propBlock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkHashes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateReplica(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def suspend(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_blockchainServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'issueTX': grpc.unary_unary_rpc_method_handler(
                    servicer.issueTX,
                    request_deserializer=blockchain__pb2.issue_tx.FromString,
                    response_serializer=blockchain__pb2.tx_hash.SerializeToString,
            ),
            'printBlockchain': grpc.unary_unary_rpc_method_handler(
                    servicer.printBlockchain,
                    request_deserializer=blockchain__pb2.print_request.FromString,
                    response_serializer=blockchain__pb2.EmptyMessage.SerializeToString,
            ),
            'propBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.propBlock,
                    request_deserializer=blockchain__pb2.append_block_request.FromString,
                    response_serializer=blockchain__pb2.block_status.SerializeToString,
            ),
            'checkHashes': grpc.unary_unary_rpc_method_handler(
                    servicer.checkHashes,
                    request_deserializer=blockchain__pb2.request_hash.FromString,
                    response_serializer=blockchain__pb2.return_hash.SerializeToString,
            ),
            'updateReplica': grpc.unary_unary_rpc_method_handler(
                    servicer.updateReplica,
                    request_deserializer=blockchain__pb2.update_replica.FromString,
                    response_serializer=blockchain__pb2.replica_status.SerializeToString,
            ),
            'suspend': grpc.unary_unary_rpc_method_handler(
                    servicer.suspend,
                    request_deserializer=blockchain__pb2.suspend_request.FromString,
                    response_serializer=blockchain__pb2.EmptyMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'blockchain', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class blockchain(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def issueTX(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blockchain/issueTX',
            blockchain__pb2.issue_tx.SerializeToString,
            blockchain__pb2.tx_hash.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def printBlockchain(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blockchain/printBlockchain',
            blockchain__pb2.print_request.SerializeToString,
            blockchain__pb2.EmptyMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def propBlock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blockchain/propBlock',
            blockchain__pb2.append_block_request.SerializeToString,
            blockchain__pb2.block_status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkHashes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blockchain/checkHashes',
            blockchain__pb2.request_hash.SerializeToString,
            blockchain__pb2.return_hash.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateReplica(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blockchain/updateReplica',
            blockchain__pb2.update_replica.SerializeToString,
            blockchain__pb2.replica_status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def suspend(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blockchain/suspend',
            blockchain__pb2.suspend_request.SerializeToString,
            blockchain__pb2.EmptyMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
