from typing import Union

from pydantic import BaseModel, validator
from datetime import datetime
import uuid


# model for HTTP error, will be the response_model if api call raises error
class HTTPError(BaseModel):
    errorType: str
    description: str


class HTTPValidation(BaseModel):
    response: str


class ClimateMeasureBase(BaseModel):
    sku: str
    carsOffRoad: Union[float, None] = None
    fightingFoodWaste: Union[float, None] = None
    waterSaved: Union[float, None] = None
    landUse: Union[float, None] = None
    cholesterolSaved: Union[float, None] = None


class ClimateMeasureCreate(ClimateMeasureBase):
    pass


class ClimateMeasure(ClimateMeasureBase):
    id: int

    class Config:
        orm_mode = True


class ClimateMeasureAuditBase(BaseModel):
    sku: str
    createdDateTime: datetime
    createdBy: str


class ClimateMeasureAuditCreate(ClimateMeasureAuditBase):
    pass


class ClimateMeasureAudit(ClimateMeasureAuditBase):
    id: int
    lastModifiedDateTime: datetime
    lastModifiedBy: str

    class Config:
        orm_mode = True


class AffiliateClimateChangeImpactBase(BaseModel):
    promoCode: str
    totalCarsOffRoad: float
    totalFightingFoodWaste: float
    totalWaterSaved: float
    totalLandUse: float
    totalCholesterolSaved: float

    @validator('totalCarsOffRoad', 'totalFightingFoodWaste', 'totalWaterSaved', 'totalLandUse', 'totalCholesterolSaved')
    def result_check(cls, v):
        ...
        return round(v, 5)


class AffiliateClimateChangeImpactCreate(AffiliateClimateChangeImpactBase):
    pass


class AffiliateClimateChangeImpact(AffiliateClimateChangeImpactBase):
    id: int

    class Config:
        orm_mode = True


class AffiliateStatusBase(BaseModel):
    status: str


class AffiliateStatusCreate(AffiliateStatusBase):
    pass


class AffiliateStatus(AffiliateStatusBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class AffiliateBase(BaseModel):
    promoCode: Union[str, None] = None
    organizationName: str
    emailAddress: str


class AffiliateCreate(AffiliateBase):
    statusId: Union[uuid.UUID, None] = None


class Affiliate(AffiliateBase):
    id: int
    affiliateStatus: Union[AffiliateStatus, None] = None
    affiliateClimateChangeImpact: Union[AffiliateClimateChangeImpact, None] = None

    class Config:
        orm_mode = True


class AffiliateApprove(BaseModel):
    id: int


class AdminBase(BaseModel):
    emailAddress: str
    username: str
    password: str


class AdminCreate(AdminBase):
    pass


class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True


class AdminAuthentication(BaseModel):
    authResult: bool
