import csv
import shutil
from enum import IntEnum
from tempfile import NamedTemporaryFile

CSV_HEADER = ['phone_number', 'user_address', 'contract_address',
              'current_balance', 'send_amount', 'timestamp']


class CSV_Column(IntEnum):
    Phone = 0,
    Address = 1,
    ContractAddress = 2
    CurrentBalance = 3,
    SendAmount = 4,
    Timestamp = 5
