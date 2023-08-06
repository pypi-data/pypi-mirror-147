import csv
import logging
import re
import shutil
import subprocess
from tempfile import NamedTemporaryFile
from typing import List

from chainlib.eth.address import is_address

from cic_helper.constants import CSV_HEADER, CSV_Column

log = logging.getLogger(__name__)


class Person:
    def __init__(self, phone_number: str, user_address: str, contract_address: str, current_balance: str, send_amount: str, timestamp: str):
        self.phone_number = phone_number if phone_number.startswith(
            '+') else f"+{phone_number}"
        self.user_address = user_address
        self.contract_address = contract_address
        self.current_balance = current_balance
        self.send_amount = int(send_amount)
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.phone_number} {self.user_address} {self.send_amount}"

    def has_corrent_amount(self):
        self.current_balance = self.get_balance(self.contract_address)
        #  -1 from expected amount to account for demurrage
        return self.current_balance and self.current_balance >= (self.send_amount - 1)

    def get_address(self, force=False, failHard=False):
        if(self.user_address and not force):
            log.debug("Skipping fetch as user already has address")
            return self.user_address
        result = subprocess.run(
            ['clicada', 'u', self.phone_number], capture_output=True, text=True)
        output = result.stdout
        regex = re.search("Network address: (0x[a-fA-F0-9]{40})", output)
        try:
            self.user_address = regex.group(1)
        except Exception as e:
            log.debug(e)
            log.error(f"Failed to get address for {self.phone_number}")
            pass
        finally:
            if (self.user_address is None and failHard):
                raise Exception(
                    f"Failed to get address for {self.phone_number}\n STDOUT: {result.stdout}\n STDERR:{result.stderr}")
        return self.user_address

    def get_balance(self, tokenAddress: str):
        result = subprocess.run(['erc20-balance', '--fee-limit', '1000000000', '-p', 'http://127.0.0.1:8545',
                                 '-i', 'evm:kitabu:5050:sarafu', '-u', '-e', tokenAddress, self.user_address], capture_output=True, text=True)
        try:
            self.current_balance = float(result.stdout.strip())
        except Exception as e:
            self.current_balance = None
            pass
        return self.current_balance

    def verify(self, user_address=False, balance=False, contract_address=False):
        errors = []
        if user_address:
            if not is_address(self.user_address):
                errors.append('  - No Valid User Address')
        if contract_address:
            if not is_address(self.contract_address):
                errors.append('  - No Valid Token Address')
        if balance and not self.has_corrent_amount():
            errors.append(
                f'  - Incorrect balance. Expected Current Balance {self.current_balance} > {self.send_amount} - 1')
        if len(errors) > 0:
            errors.insert(0, f"{self.phone_number}")
            return "\n".join(errors)
        else:
            return None

    def transfer(self, checkBalance=True):
        if(checkBalance and self.has_corrent_amount()):
            print(f"Skipping {self.phone_number} as balance is within range")
            print(
                f"  Network: {self.current_balance}, Requested: {self.send_amount}")
            return
        else:
            print(
                f"  Sending {self.send_amount} to {self.phone_number} ({self.user_address}) from {self.contract_address}")
            # result = subprocess.run([
            #     "erc20-transfer", "-p", "https://rpc.kitabu.grassecon.org", "-i", "evm:kitabu:5050:sarafu", "-u", "-e", tokenAddress, "--fee-limit", "10000000", "-y", "/home/sarafu/keystore/wor-deployer-wallet-keyfile", "-a", self.address, "10000000000", "-s"], capture_output=True,
            #     text=True)
            # txHash = result.stdout
            print(f"  Sent: ")

    def to_row(self) -> List[str]:
        return [self.phone_number, self.user_address, self.contract_address, self.current_balance, self.send_amount, self.timestamp]


def person_from_row(row: List[str]) -> Person:
    return Person(*row)


def load_people_from_csv(filename: str) -> List[Person]:
    people = []
    with open(filename) as file:
        csvreader = csv.reader(file, delimiter=',')
        for idx, row in enumerate(csvreader):
            if idx == 0:
                if row != CSV_HEADER:
                    raise Exception(
                        f'Seems you are using the wrong csv format. Expected the header to be: \n\t {", ".join(CSV_HEADER)}')
                continue
            people.append(person_from_row(row))
    return people


def save_people_to_csv(filename: str, people: List[Person]):
    with NamedTemporaryFile('w+t', newline='', delete=False) as tempfile:
        csvwriter = csv.writer(tempfile, delimiter=',', quotechar='"')
        csvwriter.writerow(CSV_HEADER)
        csvwriter.writerows([person.to_row() for person in people])
        shutil.move(tempfile.name, filename)
