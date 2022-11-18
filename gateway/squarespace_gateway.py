from .squarespace_api_key import api_key
from .transaction_records import OrderRecord, ProductRecord, InventoryRecord
import requests


class SquarespaceGateway:
    """
    A gateway for communicating with the SquareSpace commerce API
    """

    def __init__(self):
        self.api_version_order = 1.0
        self.api_version_inventory = 1.0
        self.headers = {'Authorization': f"Bearer {api_key}",
                        'User-Agent': "ULIVIT Climate Change Calculator Gateway/1.0"}

    def get_all_orders(self) -> list[OrderRecord]:
        """
        Get all orders using the SquareSpace API

        :return: a list of OrderRecords corresponding to all orders
        """
        url = f"https://api.squarespace.com/{self.api_version_order}/commerce/orders/"

        r = requests.get(url, headers=self.headers)

        # TODO: Check if successful
        order_list = self.__parse_order_list(r)

        return order_list

    def get_all_inventories(self) -> list[InventoryRecord]:
        """
        Get all inventories using the SquareSpace API

        :return: a list of InventoryRecords corresponding to all inventories
        """
        url = f"https://api.squarespace.com/{self.api_version_inventory}/commerce/inventory/"

        r = requests.get(url, headers=self.headers)

        inventory_list = self.__parse_inventory_list(r)

        return inventory_list

    def get_order_by_id(self, order_id) -> OrderRecord:
        """
        Get an order using the SquareSpace API

        :param order_id: The SquareSpace order id of the order to be retrived
        :return: an OrderRecord object of the order
        """
        url = f"https://api.squarespace.com/{self.api_version_order}/commerce/orders/{order_id}"

        r = requests.get(url, headers=self.headers)

        return self.__parse_order(r)

    def get_inventory_by_id(self, variantId) -> InventoryRecord:
        """
        Get an item inventory using the SquareSpace API.

        :param variantId: The SquareSpace InventoryItem id of the inventory to be retrived
        :return: an InventoryRecord object of the inventory
        """
        url = f"https://api.squarespace.com/{self.api_version_inventory}/commerce/inventory/{variantId}"

        r = requests.get(url, headers=self.headers)

        return self.__parse_inventory(r)

    def __parse_order_list(self, r: requests.Response):
        orders_parsed = r.json()
        order_list = []
        for order in orders_parsed['result']:
            order_list.append(self.__parse_order(order, isJSON=False))

        return order_list

    def __parse_inventory_list(self, r: requests.Response):
        inventories_parsed = r.json()
        inventory_list = []
        for inventory in inventories_parsed['inventory']:
            inventory_list.append(self.__parse_inventory(inventory, isJSON=False))

        return inventory_list

    @staticmethod
    def __parse_order(order: dict | requests.Response, isJSON=True):
        if isJSON:
            order = order.json()

        product_list = []
        for product in order["lineItems"]:
            product_list.append(ProductRecord(product["sku"],
                                              product["quantity"],
                                              product["productName"]))

        # All promo codes are retrieved here, they can be filtered out later
        promo_list = []
        for promo in order["discountLines"]:
            promo_list.append(promo["promoCode"])

        return OrderRecord(order["id"],
                           order["customerEmail"],
                           product_list,
                           promo_list,
                           order["testmode"])

    @staticmethod
    def __parse_inventory(inventory, isJSON=True):
        if isJSON:
            inventory = inventory.json()

        return InventoryRecord(inventory["variantId"],
                               inventory["sku"],
                               inventory["descriptor"],
                               inventory["quantity"],
                               inventory["isUnlimited"])


if __name__ == "__main__":
    gateway = SquarespaceGateway()
    # ret = gateway.get_all_orders()
    ret = gateway.get_order_by_id('635a09ba3051bd1bdaadf09e')
    # ret1 = gateway.get_all_inventories()
    print(ret.promo_code)
    # print(ret.product_list[0].sku)
    # print(ret.product_list[0].quantity)
    # print(ret1)
