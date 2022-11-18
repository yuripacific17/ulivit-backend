from fastapi.responses import JSONResponse

from .squarespace_gateway import SquarespaceGateway
from crud.climate_measure_crud import get_climate_measure_by_sku
from crud.affiliate_crud import get_associated_affiliate_promo_code_from_list
from crud.affiliate_climate_change_impact_crud import get_affiliate_climate_change_impact_by_promo_code
from schemas import AffiliateClimateChangeImpactCreate
from .webhook_schemas import WebhookRequest


def get_order_from_webhook_response(webHookSchema: WebhookRequest, gateway):
    """
    Get order id from the webhook order create response
    Retrieve order information through squarespace gateway

    :param webHookSchema:
    :param gateway:
    :return:
    """
    return gateway.get_order_by_id(webHookSchema.data.orderId)


def calculate_climate_impact(order, db):
    """
    calculate the climate impact per order

    :param order:
    :param db:
    :return:
    """
    affiliate_promo_code = get_associated_affiliate_promo_code_from_list(db=db, promo_codes=order.promo_list)

    if affiliate_promo_code is None:
        return JSONResponse(status_code=418, content={"ErrorType": "PromoCodeNotFound",
                                                      "Description": "Climate Change Calculator Promo Code Not "
                                                                     "Found From This Order"})

    impact = get_affiliate_climate_change_impact_by_promo_code(db=db, promoCode=affiliate_promo_code)

    if impact is not None:
        cars_off_road = impact.totalCarsOffRoad
        fighting_food_waste = impact.totalFightingFoodWaste
        water_saved = impact.totalWaterSaved
        land_use = impact.totalLandUse
        cholesterol_saved = impact.totalCholesterolSaved
    else:
        cars_off_road = 0.0
        fighting_food_waste = 0.0
        water_saved = 0.0
        land_use = 0.0
        cholesterol_saved = 0.0

    # TODO: Check if the order has already been processed

    for product in order.product_list:
        climate_measure_response = get_climate_measure_by_sku(db=db, sku=product.sku)
        if climate_measure_response is None:
            return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                          "Description": "Climate Measure With Given SKU Not Found"})

        cars_off_road += float(climate_measure_response.carsOffRoad) * int(product.quantity)
        fighting_food_waste += float(climate_measure_response.fightingFoodWaste) * int(product.quantity)
        water_saved += float(climate_measure_response.waterSaved) * int(product.quantity)
        land_use += float(climate_measure_response.landUse) * int(product.quantity)
        cholesterol_saved += float(climate_measure_response.cholesterolSaved) * int(product.quantity)

    return AffiliateClimateChangeImpactCreate(promoCode=affiliate_promo_code, totalCarsOffRoad=cars_off_road,
                                              totalFightingFoodWaste=fighting_food_waste,
                                              totalWaterSaved=water_saved,
                                              totalLandUse=land_use, totalCholesterolSaved=cholesterol_saved)


def calculator_create(webHookSchema: WebhookRequest, db):
    """
    Provide interface for the order create api

    :param webHookSchema:
    :param db:
    :return:
    """
    gateway = SquarespaceGateway()
    order = get_order_from_webhook_response(webHookSchema, gateway)
    return calculate_climate_impact(order, db)


# TODO: update climate change impact by looking up orders from the climate change impact audit table
# TODO: the climate change impact audit table needs to be first implemented
def calculator_update(webHookSchema: WebhookRequest, db):
    pass
