import logging
import os

import grpc

from apeman_model_client import apemanModelClient_pb2
from apeman_model_client import apemanModelClient_pb2_grpc
from apeman_model.modelInstanceTaskStatus_pb2 import ModelInstanceTaskStatus
from apeman_model_client.model_instance_task_status import TaskStatus

logging.basicConfig(level=logging.DEBUG)


class ApemanModelServiceClient(object):

    def __init__(self):
        apeman_meta_server_addr = os.getenv("apeman_meta_server_addr")
        if apeman_meta_server_addr is None:
            raise RuntimeError('Invalid value of apeman_meta_server_addr')

        logging.debug('Connect to APEMAN meta server %s', apeman_meta_server_addr)
        channel = grpc.insecure_channel(apeman_meta_server_addr)
        self.__stub = apemanModelClient_pb2_grpc.ApemanModelClientStub(channel)

    def report(self, task_id='', status=TaskStatus.NONE, progress=0.0, message='', token=''):
        print('report....')
        model_instance_task_status = ModelInstanceTaskStatus.Value(status.value)
        request = apemanModelClient_pb2.TaskStatusReportRequest(modelInstanceTaskId=task_id,
                                                                status=model_instance_task_status,
                                                                progress=progress,
                                                                token=token,
                                                                message=message)
        self.__stub.Report(request)

    def get_endpoint(self, model_id=''):
        request = apemanModelClient_pb2.GetModelEndpointRequest(modelId=model_id)
        response = self.__stub.GetModelEndpoint(request)
        return response.endpoint
