import uuid
import models

# hardcoded UUID for affiliate_status id
AFFILIATE_STATUS_ID_PENDING = uuid.UUID('079434f9-732e-425b-981e-82157f6e0801')
AFFILIATE_STATUS_ID_APPROVED = uuid.UUID('f36a54a2-cf5d-4b20-b379-09a938120685')


class Wellknown:
    def __init__(self):
        self.affiliate_status_id_pending = AFFILIATE_STATUS_ID_PENDING
        self.affiliate_status_id_approved = AFFILIATE_STATUS_ID_APPROVED
        # these data will always be the same and always populated once the app starts
        self.WELLKNOWN_DATA = {
            'affiliate_status': [
                {
                    'id': self.affiliate_status_id_pending,
                    'status': 'pending'
                },
                {
                    'id': self.affiliate_status_id_approved,
                    'status': 'approved'
                }
            ]
        }

    def affiliate_status_wellknown_mapper_to_orm(self):
        """
            map affiliate status wellknown data from the json structure to orm model
            :param: self
            :return: an array of affiliate status models
        """
        orm_arr = []
        for record in self.WELLKNOWN_DATA.get('affiliate_status'):
            orm_arr.append(models.AffiliateStatus(id=record.get('id'), status=record.get('status')))

        return orm_arr
