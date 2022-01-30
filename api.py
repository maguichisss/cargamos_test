import csv
from datetime import datetime
import cargamos

def validate(row):
    """Validate the fields in row to create Order and Address"""
    # remove empty fields from row dict
    keys = [k for k in row.keys()]
    for k in keys:
        if not row.get(k):
            row.pop(k)

    return validate_order(row) and validate_address(row)

def validate_order(order):
    """Check fields for order

        Args:
            order: dict with order fields
        Return:
            boolean if all the field are valid
    """
    # validate created at
    if order.get("created_at"):
        if valid_date(order["created_at"]):
            order["created_at"] = valid_date(order["created_at"])
        else:
            return False
    # validate expired at
    if order.get("expired_at"):
        if valid_date(order["expired_at"]):
            order["expired_at"] = valid_date(order["expired_at"])
        else:
            return False

    return True

def validate_address(address):
    """Check fields for address

        Args:
            address: dict with address fields
        Return:
            boolean if all the field are valid
    """
    required_fields = ["address_line_1","postal_code","locality","city","state","country"]
    for k in required_fields:
        try:
            _ = address[k]
        except KeyError as e:
            return False
    return True

def valid_date(date):
    """Check valid format date

        Args:
            date: string to check the date
        Return:
            datetime with the date or None if not matched any format
    """
    dateFormats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
    ]
    for form in dateFormats:
        try:
            return datetime.strptime(date, form)
        except ValueError as ve:
            pass

def main(pathfile, sort=True, skus_delivered=[]):
    # process file with and valid data
    with open(pathfile, "r") as f:
        orders = {}
        for row in csv.DictReader(f):
            if validate(row):
                o = cargamos.Order(**row)
                orders[o.SKU] = o
    # sort orders by alive_time
    orders = orders.values()
    if sort:
        orders = sorted(orders, key=lambda x: x.alive_time, reverse=True)
    # mark orders as delivered
    for o in orders:
        if o.SKU in skus_delivered:
            try:
                o.mark_as_delivered()
            except Exception as e:
                # TODO: log this exception
                print(e, o.SKU)
                pass

    return orders


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Process orders from a csv file")
    parser.add_argument('file', help="Path to the file with the orders")
    parser.add_argument('--skus', help="SKUs to mark as delivered separated by comas", default="")
    args = parser.parse_args()

    skus = args.skus.split(",")

    orders = main(args.file, skus_delivered=skus)
    for o in orders:
        print(o)
