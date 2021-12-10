# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import calc_pb2
import calc_pb2_grpc
import operator


class Calculator(calc_pb2_grpc.CalculatorServicer):

    def Calc(self, request, context):

        #mapped operators
        operators = {'+': operator.add, '-' : operator.sub, '*' : operator.mul, '/' : operator.truediv}
        
        try:
            #takes the string representation of the the opreator and then operates on the terms
            calc = operators[request.oper](int(request.firstTerm), int(request.secondTerm))

            return calc_pb2.CalcReply(message = f'The calculation {request.firstTerm} {request.oper} {request.secondTerm} = {calc}\n')
        except:
            return calc_pb2.CalcReply(message = f'{request.firstTerm} or {request.secondTerm} is not an Integer or Incorect operator')
           
            
      
            

def serve():
    #server creation with the max allowed threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    
    calc_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server: calc_server.py is up and running....")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
