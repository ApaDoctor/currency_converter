#!/usr/bin/env python3
import argparse
import requests
import sys

API_SERVER = "http://localhost:8000"


def parse_args():
    parser = argparse.ArgumentParser(description='Converts one currency to other', prog='currency_converter')
    parser.add_argument('--amount',
                        type=float,
                        help='Amount to convert',
                        dest='amount',
                        required=True
                        )
    parser.add_argument('--input_currency',
                        type=str,
                        help="Currency to convert from",
                        dest="input_currency",
                        required=True)
    parser.add_argument("--output_currency",
                        type=str,
                        help="Currency to convert to")

    return parser.parse_args()


def make_request(amount, input_currency, output_currency):
    data = {
        "amount": amount,
        "input_currency": input_currency,
    }
    if output_currency is not None:
        data["output_currency"] = output_currency
    return requests.get("{}/currency_converter".format(API_SERVER), params=data)


def main():
    args = parse_args()
    try:
        print(make_request(args.amount, args.input_currency, args.output_currency).content.decode('UTF-8'))
    except requests.exceptions.ConnectionError:
        print("There are connection problems. Please change host or make sure that server runs at {}".format(
            API_SERVER
        ), file=sys.stderr)


if __name__ == '__main__':
    main()
