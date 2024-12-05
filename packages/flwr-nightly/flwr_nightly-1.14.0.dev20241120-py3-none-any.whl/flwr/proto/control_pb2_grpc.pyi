"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import flwr.proto.run_pb2
import grpc

class ControlStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    CreateRun: grpc.UnaryUnaryMultiCallable[
        flwr.proto.run_pb2.CreateRunRequest,
        flwr.proto.run_pb2.CreateRunResponse]
    """Request to create a new run"""

    GetRunStatus: grpc.UnaryUnaryMultiCallable[
        flwr.proto.run_pb2.GetRunStatusRequest,
        flwr.proto.run_pb2.GetRunStatusResponse]
    """Get the status of a given run"""

    UpdateRunStatus: grpc.UnaryUnaryMultiCallable[
        flwr.proto.run_pb2.UpdateRunStatusRequest,
        flwr.proto.run_pb2.UpdateRunStatusResponse]
    """Update the status of a given run"""


class ControlServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def CreateRun(self,
        request: flwr.proto.run_pb2.CreateRunRequest,
        context: grpc.ServicerContext,
    ) -> flwr.proto.run_pb2.CreateRunResponse:
        """Request to create a new run"""
        pass

    @abc.abstractmethod
    def GetRunStatus(self,
        request: flwr.proto.run_pb2.GetRunStatusRequest,
        context: grpc.ServicerContext,
    ) -> flwr.proto.run_pb2.GetRunStatusResponse:
        """Get the status of a given run"""
        pass

    @abc.abstractmethod
    def UpdateRunStatus(self,
        request: flwr.proto.run_pb2.UpdateRunStatusRequest,
        context: grpc.ServicerContext,
    ) -> flwr.proto.run_pb2.UpdateRunStatusResponse:
        """Update the status of a given run"""
        pass


def add_ControlServicer_to_server(servicer: ControlServicer, server: grpc.Server) -> None: ...
