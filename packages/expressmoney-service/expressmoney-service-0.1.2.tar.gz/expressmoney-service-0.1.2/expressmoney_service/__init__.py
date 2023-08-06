from expressmoney_service.api import *

SERVICE = 'services'


class IdIDXCreateContract(Contract):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_date = serializers.DateField()
    passport_code = serializers.CharField(max_length=16)


class IdIDXResponseContract(IdIDXCreateContract):
    pass


class IdIDXID(ID):
    _service = SERVICE
    _app = 'id_idx'
    _view_set = 'id_idx'


class IdIDXPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = IdIDXID()
    _create_contract = IdIDXCreateContract
    _response_contract = IdIDXResponseContract
