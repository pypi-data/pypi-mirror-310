import csv
import json


def json_deserialize(stream):
    for line in stream:
        j = json.loads(line)
        yield j


def json_serialize(it, stream):
    for x in it:
        json.dump(x, stream)
        stream.write('\n')


def csv_deserialize(stream):
    reader = csv.DictReader(stream)
    for x in reader:
        yield x


def csv_serialize(it, stream):
    first = next(it)
    if type(first) == dict:
        fieldnames = list(first.keys())
        writer = csv.DictWriter(stream, fieldnames)
        writer.writeheader()
        writer.writerow(first)
    elif type(first) == list:
        writer = csv.writer()

    for x in it:
        writer.writerow(x)


