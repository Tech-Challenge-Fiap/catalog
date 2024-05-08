from enum import Enum


class ProductTypeEnum(str, Enum):
    SNACK = "SNACK"
    SIDE = "SIDE"
    BEVERAGE = "BEVERAGE"
    DESSERT = "DESSERT"
