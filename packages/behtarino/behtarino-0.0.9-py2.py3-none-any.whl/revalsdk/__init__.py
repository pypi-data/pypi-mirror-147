"""The Python implementation of the gRPC Reval client."""

import grpc
from .notification_pb2 import *
from .notification_pb2_grpc import *
from .authentication_pb2 import *
from .authentication_pb2_grpc import *
from .internal_pb2 import *
from .internal_pb2_grpc import *


def create_notification_stub(channel: grpc.Channel) -> NotificationStub:
    return NotificationStub(channel)

def create_internal_stub(channel: grpc.Channel) -> InternalStub:
    return InternalStub(channel)


def create_authentication_stub(channel: grpc.Channel) -> AuthenticationStub:
    return AuthenticationStub(channel)


def create_grpc_client(server: str) -> grpc.Channel:
    return grpc.secure_channel(server, grpc.ssl_channel_credentials())
