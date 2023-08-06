import logging
import math
import os
import pathlib
import subprocess
import sys
from typing import List

import click

from cic_helper.Person import Person, load_people_from_csv, save_people_to_csv

log = logging.getLogger(__name__)

log_format = '%(message)s'


def set_log_level(level: int = 1):
    # ERROR, WARN, INFO, DEBUG
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    if (level == 1):
        logging.basicConfig(format=log_format, level=logging.INFO)
    else:
        logging.basicConfig(format=log_format, level=logging.DEBUG)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv)')
@click.option('-t', '--token', type=str, nargs=1, default=False, help='Token address')
def get_balances(filename, verbose, token):
    set_log_level(verbose)
    people = load_people_from_csv(filename)
    errored = False
    for person in people:
        err = person.verify(user_address=True)
        if(err):
            raise Exception(err)
    for person in people:
        balance = person.get_balance(token)
    save_people_to_csv(filename, people)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv)')
def verify_amount(filename, verbose, user, token, balance, all):
    set_log_level(verbose)
    if user or token or balance or all:
        people = load_people_from_csv(filename)
        errored = False
        for person in people:
            err = person.verify(user_address=True,
                                balance=True, contract_address=True)
            if(err):
                errored = True
                log.error(err)


@cli.command()
@click.option('-c', '--config', type=str, help='Path to Kitabu Config Folder')
def run(config):
    base = pathlib.Path(__file__).parent.resolve()
    kitabu_path = config or base.joinpath('kitabu')
    result = subprocess.run(
        ['bash', 'run.sh'], stdout=subprocess.PIPE, cwd=kitabu_path)
    log.info(result)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv)')
@click.option('-f', '--force', is_flag=True, help='Updates the users address even if it is present')
def get_addresses(filename, verbose, force):
    set_log_level(verbose)
    people = load_people_from_csv(filename)
    log.info(f"Fetching Address for {len(people)} People")
    for idx, person in enumerate(people):
        log.info(
            f"[{idx}/{len(people)}] Fetching address for: {person.phone_number}")
        address = person.get_address()
        if person.user_address is None:
            log.error(
                f"Failed to get address for {person.phone_number}, so skipping")

    log.info(f"Saving to {filename}                     ", end='\r')
    save_people_to_csv(filename, people)
    log.info(f"Saved to {filename}                      ")


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('contract_address', type=str)
@click.option('--fee-limit', nargs=1, type=str, default='80000', show_default=True, help='Fee limit for each tx')
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv)')
@click.option('--check', is_flag=True, help='Dont send if users balance is within send_amount-1')
@click.option('-y', '--signer', type=str, required=True, help='Signer Keyfile Location (e.g "/home/sarafu//wor-deployer-wallet-keyfile")')
@click.option('-f', '--force', is_flag=True, help='Send the requrested amount even if the users balance is ~=send_amount')
def send(filename, contract_address, check, fee_limit, signer, verbose, force):
    set_log_level(verbose)
    people = load_people_from_csv(filename)
    errors = []
    for person in people:
        person.contract_address = contract_address
        err = person.verify(user_address=True, contract_address=True)
        if (err):
            errors.append(err)
    if len(errors) > 0:
        log.error(errors)
        sys.exit(1)

    save_people_to_csv(filename=filename, people=people)
    for person in people:
        person.send(contract_address, signer,
                    fee_limit=fee_limit, check_balance=check)


def print_help_msg(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == '__main__':
    cli()
