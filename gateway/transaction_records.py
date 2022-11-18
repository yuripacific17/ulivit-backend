class ProductRecord:

    def __init__(self, sku: str, quantity: int, product_name=""):
        self.sku = sku
        self.quantity = quantity
        self.product_name = product_name


class OrderRecord:

    def __init__(self, order_id: str, customer_email: str, product_list: list[ProductRecord], promo_list: list[str], test_mode=False):
        self.order_id = order_id
        self.customer_email = customer_email
        self.product_list = product_list
        self.promo_list = promo_list
        self.test_mode = test_mode

class InventoryRecord:
    
    def __init__(self, variantId: str, sku: str, descriptor: str,  quantity: int, isUnlimited = False):
        self.variantId = variantId
        self.sku = sku
        self.descriptor = descriptor
        self.quantity = quantity
        self.isUnlimited = isUnlimited