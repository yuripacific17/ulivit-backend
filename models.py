from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, MetaData
from sqlalchemy.orm import relationship, declarative_base
from uuid import uuid4

metadate_obj = MetaData(schema="CCC")

Base = declarative_base(metadata=metadate_obj)


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    emailAddress = Column(String)
    username = Column(String)
    password = Column(String)


class ClimateMeasure(Base):
    __tablename__ = "climate_measure"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    carsOffRoad = Column(Float, nullable=True)
    fightingFoodWaste = Column(Float, nullable=True)
    waterSaved = Column(Float, nullable=True)
    landUse = Column(Float, nullable=True)
    cholesterolSaved = Column(Float, nullable=True)


class ClimateMeasureAudit(Base):
    __tablename__ = "climate_measure_audit"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    createdDateTime = Column(DateTime)
    createdBy = Column(String)
    lastModifiedDateTime = Column(DateTime, nullable=True)
    lastModifiedBy = Column(DateTime, nullable=True)


class AffiliateStatus(Base):
    __tablename__ = "affiliate_status"

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True, default=uuid4)
    status =Column(String, nullable=False, unique=True)


class Affiliate(Base):
    __tablename__ = "affiliate"

    id = Column(Integer, primary_key=True)
    promoCode = Column(String, nullable=True, unique=True)
    statusId = Column(UUID(as_uuid=True), ForeignKey("affiliate_status.id"), default=uuid4)
    organizationName = Column(String)
    emailAddress = Column(String, nullable=False, unique=True)

    affiliateStatus = relationship("AffiliateStatus")
    affiliateClimateChangeImpact = relationship("AffiliateClimateChangeImpact", back_populates="affiliate", uselist=False)


class AffiliateClimateChangeImpact(Base):
    __tablename__ = "affiliate_climate_change_impact"

    id = Column(Integer, primary_key=True)
    promoCode = Column(String, ForeignKey("affiliate.promoCode"), nullable=False, unique=True)
    totalCarsOffRoad = Column(Float, nullable=True)
    totalFightingFoodWaste = Column(Float, nullable=True)
    totalWaterSaved = Column(Float, nullable=True)
    totalLandUse = Column(Float, nullable=True)
    totalCholesterolSaved = Column(Float, nullable=True)

    affiliate = relationship("Affiliate", back_populates="affiliateClimateChangeImpact")
