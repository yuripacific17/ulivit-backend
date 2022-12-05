import os
from dotenv import load_dotenv

from fastapi.responses import JSONResponse

from .squarespace_gateway import SquarespaceGateway
from crud.climate_measure_crud import get_climate_measure_by_sku
from crud.climate_measure_crud import get_all_climate_measures
from crud.affiliate_crud import get_associated_affiliate_promo_code_from_list
from crud.affiliate_climate_change_impact_crud import get_affiliate_climate_change_impact_by_promo_code
from schemas import AffiliateClimateChangeImpactCreate
from .webhook_schemas import WebhookRequest
import models

# TODO: delete after testing
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


load_dotenv()
MC_API_KEY = os.environ.get('MC_API_KEY')


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


def send_email():
    try:
        mailchimp = MailchimpTransactional.Client(MC_API_KEY)
        print(mailchimp.messages)

        response = mailchimp.messages.send_template(
            {"template_name": "template_name", "template_content": [{}], "message": {}})
        print(response)
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


def fetch_sku_for_admin(db,skip:int = 0, limit: int = 100):
    gateway = SquarespaceGateway()
    # brings back all ivnentory records from sqaurespace # sku = 28
    inventory = gateway.get_all_inventories()

    # bring back all climate measure from our database
    climate_measure = get_all_climate_measures(db=db, skip=skip, limit=limit)

    #extra sku number list 
    extra_sku=[]

    for i in inventory:
        extra_sku.append(i.sku)

    for j in climate_measure:
        if j.sku in extra_sku:
            extra_sku.remove(j.sku)
    
    for num in extra_sku:
        db_climateMeasure = models.ClimateMeasure(sku=num, carsOffRoad='',
                                              fightingFoodWaste='',
                                              waterSaved='', landUse='',
                                              cholesterolSaved='')
        db.add(db_climateMeasure)
        db.commit()
        db.refresh(db_climateMeasure)
    return


