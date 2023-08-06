__all__ = ('IdentificationProcessPoint',)

from expressmoney.api import *
from expressmoney.viewflow import status

SERVICE = 'profiles'


class IdentificationProcessReadContract(Contract):
    EMPTY = status.EMPTY
    SUCCESS = status.SUCCESS
    FAILURE = status.FAILURE

    RESULT_CHOICES = (
        (EMPTY, EMPTY),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
    )
    id = serializers.IntegerField(min_value=1)
    updated = serializers.DateField()
    user_id = serializers.IntegerField(min_value=1)
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    comment = serializers.CharField(max_length=1024, allow_blank=True)
    status = serializers.CharField(max_length=50)


class IdentificationProcessID(ID):
    _service = SERVICE
    _app = 'identification'
    _view_set = 'identification_process'


class IdentificationProcessPoint(ListPointMixin, ContractPoint):
    _point_id = IdentificationProcessID()
    _read_contract = IdentificationProcessReadContract
