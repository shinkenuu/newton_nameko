import json
import logging
from uuid import uuid4

from marshmallow import ValidationError
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from nameko_redis import Redis

from constants import (
    SUM_OPERATION_NAME,
    SUBTRACT_OPERATION_NAME,
    MULTIPLY_OPERATION_NAME,
    DIVIDE_OPERATION_NAME,
    PROCEDURE_STATUS_SCHEDULED,
)
from schemas import (
    ArithmeticProcedureSchema,
    ArithmeticProcedureRequestSchema,
)


class WebService:
    name = 'web'
    redis = Redis('newton')

    arithmetic_rpc = RpcProxy('arithmetic')

    arithmetic_schema = ArithmeticProcedureSchema()
    arithmetic_request_schema = ArithmeticProcedureRequestSchema()

    @http('POST', '/arithmetic/sum')
    def sum(self, request):
        return self.handle_arithmetic_request(request, SUM_OPERATION_NAME)

    @http('POST', '/arithmetic/subtract')
    def subtract(self, request):
        return self.handle_arithmetic_request(request, SUBTRACT_OPERATION_NAME)

    @http('POST', '/arithmetic/multiply')
    def multiply(self, request):
        return self.handle_arithmetic_request(request, MULTIPLY_OPERATION_NAME)

    @http('POST', '/arithmetic/divide')
    def divide(self, request):
        return self.handle_arithmetic_request(request, DIVIDE_OPERATION_NAME)

    @http('GET', '/arithmetic/<string:procedure_uuid>')
    def result(self, request, procedure_uuid):
        procedure = json.loads(self.redis.get(procedure_uuid))

        if not procedure:
            return 404, ''

        serialized_procedure = self.arithmetic_schema.dump(procedure)
        return 200, json.dumps(serialized_procedure)

    def handle_arithmetic_request(self, request, operation: str):
        try:
            payload = self.arithmetic_request_schema.loads(request.get_data(as_text=True))
            procedure_uuid = self._schedule_arithmetic_procedure(
                operation, payload['arguments'])

            return 202, json.dumps({'uuid': procedure_uuid})

        except ValidationError as error:
            return 400, json.dumps({'error': str(error)})

        except Exception as exception:
            logging.error(exception)
            return 500, json.dumps({'error': 'internal error'})

    def _schedule_arithmetic_procedure(self, operation: str, arguments: list):
        procedure_uuid = uuid4().hex

        procedure = self.arithmetic_schema.load({
            'operation': operation,
            'arguments': arguments,
            'result': None,
            'status': PROCEDURE_STATUS_SCHEDULED,
        })

        self.redis.set(procedure_uuid, json.dumps(procedure))
        self.arithmetic_rpc.calculate.call_async(procedure_uuid)

        return procedure_uuid
