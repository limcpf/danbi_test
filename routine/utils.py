from rest_framework import exceptions, status
from rest_framework.response import Response

from routine.enums import ResponseEnum


def get_response(data, res_enum):
    if not isinstance(res_enum, ResponseEnum):
        raise exceptions.APIException(detail="res_enum 은 ResponseEnum 타입이여야 합니다.", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(
        {
            "data": data,
            "message": {
                "msg": res_enum.value[0],
                "status": res_enum.name
            }
        },
        status=res_enum.value[1]
    )