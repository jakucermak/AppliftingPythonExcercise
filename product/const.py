from enum import Enum

class ProductError(Enum):
    prod_name_err = 'You has to provide product name, buddy.'
    prod_desc_err = 'You has to provide product description, mate.'
    prod_no_field_err = 'Did you forget to give me some info about your product? 🙂'