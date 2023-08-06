__all__ = ('SmsMTSPoint',)

from ...api import *

PROJECT = 'expressmoney-service'
SERVICE = 'services'


class SmsMTSCreateContract(Contract):
    message = serializers.CharField(max_length=60)


class SmsMTSResponseContract(SmsMTSCreateContract):
    pass


class SmsMTSID(ID):
    _project = PROJECT
    _service = SERVICE
    _app = 'sms_mts'
    _view_set = 'sms_mts'


class SmsMTSPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = SmsMTSID()
    _create_contract = SmsMTSCreateContract
    _response_contract = SmsMTSResponseContract
