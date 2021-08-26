from phonenumbers import carrier
from phonenumbers import parse

from phonenumbers.phonenumberutil import number_type

number = "+4915    \n730418142"
if carrier._is_mobile(number_type(parse(number))):
    print('ff')