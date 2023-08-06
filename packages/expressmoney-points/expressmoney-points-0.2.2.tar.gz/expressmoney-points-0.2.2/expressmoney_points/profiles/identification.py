__all__ = ('IdentificationProcessPoint', 'AutoIdentificationTaskPoint')

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


class AutoIdentificationTaskReadContract(Contract):
    EMPTY = status.EMPTY
    SUCCESS = status.SUCCESS
    FAILURE = status.FAILURE
    RESULT_CHOICES = (
        (EMPTY, EMPTY),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
    )
    RU = 'RU'
    COUNTRY_CHOICES = (
        (RU, RU),
    )
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    comment = serializers.CharField(max_length=1024, allow_blank=True)


class IdentificationProcessID(ID):
    _service = SERVICE
    _app = 'identification'
    _view_set = 'identification_process'


class AutoIdentificationTaskID(ID):
    _service = SERVICE
    _app = 'identification'
    _view_set = 'auto_identification_task'


class IdentificationProcessPoint(ListPointMixin, ContractPoint):
    _point_id = IdentificationProcessID()
    _read_contract = IdentificationProcessReadContract


class AutoIdentificationTaskPoint(ListPointMixin, ContractPoint):
    _point_id = AutoIdentificationTaskID()
    _read_contract = AutoIdentificationTaskReadContract
