import csv
import json
import sys

def json_to_csv():
    writer = csv.writer(sys.stdout)
    for l in sys.stdin:
        j = json.loads(l)
        writer.writerow(j.values())


def csv_to_json():
    reader = csv.reader(sys.stdin)
    for x in reader:
        print(json.dumps(x))


def main():
    command = sys.argv[1]
    f = globals()[command]
    f()

if __name__=='__main__':
    main()
