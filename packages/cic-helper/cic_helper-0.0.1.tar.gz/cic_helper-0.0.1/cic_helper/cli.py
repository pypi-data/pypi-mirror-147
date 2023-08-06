import os
import subprocess
import sys
from typing import List

import click

from cic_helper.Person import Person, load_people_from_csv, save_people_to_csv


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv, -vvv)')
@click.option('-u', '--user', is_flag=True, default=False, help='Check that all users have a valid address')
@click.option('-t', '--token', is_flag=True, default=False, help='Check that all users have a valid token address')
@click.option('-b', '--balance', is_flag=True, default=False, help='Check that all user balances are > send_amount - 1')
@click.option('-a', '--all', is_flag=True, default=False, help='Check All')
def verify(filename, verbose, user, token, balance, all):
    if user or token or balance or all:
        people = load_people_from_csv(filename)
        errored = False
        for person in people:
            err = person.verify(
                balance=balance or all, contract_address=token or all, user_address=user or all)
            if(err):
                errored = True
                print(err)

        userAddressSuccess = "- Have a valid wallet address\n" if user else ""
        tokenAddressSuccess = "- Have a valid token address\n" if token else ""
        balanceSuccess = "- Have balances that are > send_amount - 1\n" if balance else ""

        if errored:
            click.echo("FAILED")
        else:
            click.echo(
                f"Verified that {len(people)} Perople :\n{userAddressSuccess}{tokenAddressSuccess}{balanceSuccess}")
        save_people_to_csv(filename, people)
    else:
        click.echo("You need to select somthing to verify")
        print_help_msg(verify)
        sys.exit(1)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('token_address', type=str)
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv, -vvv)')
@click.option('-f', '--force', is_flag=True, help='Send the requrested amount even if the users balance is ~=send_amount')
def send(filename, token_address, verbose, force):
    people = load_people_from_csv(filename)
    errors = []
    for person in people:
        person.contract_address = tokenAddress
        err = person.verify(user_address=True, contract_address=True)
        if (err):
            errors.append(err)
    if len(errors) > 0:
        print(errors)
        sys.exit(1)

    save_people_to_csv(filename=filename, people=people)
    for person in people:
        person.transfer(tokenAddress)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', count=True, help='Verbosity Level (-v,-vv, -vvv)')
@click.option('-f', '--force', is_flag=True, help='Updates the users address even if it is present')
def get_addresses(filename, verbose, force):
    people = load_people_from_csv(filename)
    print(f"Fetching Address for {len(people)} People")
    for idx, person in enumerate(people):
        percent_complete = math.floor((idx/len(people)) * 100)
        print(
            f"[{percent_complete}%] Fetching address for: {person.phone_number}", end="\r")
        address = person.get_address()
        if person.user_address is None:
            print(
                f"Failed to get address for {person.phone_number}, so skipping")

    print(f"Saving to {filename}                     ", end='\r')
    save_people_to_csv(filename, people)
    print(f"Saved to {filename}                      ")


def print_help_msg(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == '__main__':
    cli()
