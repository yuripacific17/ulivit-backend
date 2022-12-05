from typing import Union

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TopicEnum(Enum):
    CREATE = "order.create"
    UPDATE = "order.update"
    UNINSTALL = "extension.uninstall"


class UpdateEnum(Enum):
    FULFILLED = "FULFILLED"
    REFUNDED = "REFUNDED"
    CANCELED = "CANCELED"
    MARKED_PENDING = "MARKED_PENDING"
    EMAIL_UPDATED = "EMAIL_UPDATED"


class WebhookBase(BaseModel):
    id: str
    websiteId: str
    subscriptionId: str
    topic: TopicEnum
    createdOn: datetime


class WebhookData(BaseModel):
    orderId: str
    update: Union[UpdateEnum, None]


class WebhookRequest(WebhookBase):
    data: WebhookData

