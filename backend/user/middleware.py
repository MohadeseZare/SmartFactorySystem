from factory import models as facmodels
from factory.api import serializers as facserializers
from device import models as devmodel
from django.utils.deprecation import MiddlewareMixin


class FilterOtherFactory(MiddlewareMixin):
    def process_request(self, request):
        try:
            device = request.query_params('device_id')
            product_line = facmodels.ProductLinePart.objects.get(
                id=devmodel.Device.objects.get(id=device).prodeuct_line_part)
            product_line_ser = facserializers.ProductLineSerializer(product_line)
            factory_member = facmodels.FactoryMember.objects.get(member=request.user.id)
            factory_member_ser = facserializers.FactoryMemberSerializer(factory_member)
            if product_line_ser['id'].value in factory_member_ser['product_line'].value:
                return True
            else:
                if product_line_ser['factory'].value in factory_member_ser['factory'].value and 'ALL' in \
                        factory_member_ser['product_line'].value:
                    return True
                else:
                    return False
        except:
            return True
