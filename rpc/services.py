import json
import logging

from nameko.rpc import rpc
from nameko_redis import Redis

import arithmetic
from constants import (
    SUM_OPERATION_NAME,
    SUBTRACT_OPERATION_NAME,
    MULTIPLY_OPERATION_NAME,
    DIVIDE_OPERATION_NAME,
    PROCEDURE_STATUS_DONE,
)

_OPERATION_FUNCTION = {
    SUM_OPERATION_NAME: arithmetic.sum_,
    SUBTRACT_OPERATION_NAME: arithmetic.subtract,
    MULTIPLY_OPERATION_NAME: arithmetic.multiply,
    DIVIDE_OPERATION_NAME: arithmetic.divide,
}


class ArithmeticService:
    name = 'arithmetic'
    redis = Redis('newton')

    @rpc
    def calculate(self, procedure_uuid: str):
        arithmetic_procedure = json.loads(self.redis.get(procedure_uuid))
        status = None

        if not arithmetic_procedure:
            logging.error('Couldnt find procedure with uuid %s to calculate', procedure_uuid)

        try:
            operation_function = _OPERATION_FUNCTION[arithmetic_procedure['operation']]
            arithmetic_procedure['result'] = operation_function(*arithmetic_procedure['arguments'])
            status = PROCEDURE_STATUS_DONE

        except Exception as exception:
            logging.error(exception)
            status = str(exception)

        finally:
            logging.info('Procedure with uuid %s calculation finished', procedure_uuid)
            arithmetic_procedure['status'] = status
            self.redis.set(procedure_uuid, json.dumps(arithmetic_procedure))
