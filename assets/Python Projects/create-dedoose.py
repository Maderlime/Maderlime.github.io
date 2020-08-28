#!/usr/bin/python

import sys
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input CSV file to read from")
parser.add_argument("output", help="base name of CSV files to generate")
parser.add_argument("first", default=0, nargs="?")
parser.add_argument("last", default=-1, nargs="?")
parser.add_argument("DeID", default=-1, nargs="?")
parser.add_argument("--full", action="store_true", help="whether to output every row")
args = parser.parse_args()

# ID, DeID, data, source file, question #
# ID = unique ID for this response (incorporates DeID and question information)
# DeID = deidentified student ID

args.DeID = int(args.DeID)

rows = list()

with open(args.input, "r", newline="") as f:
    reader = csv.reader(f)

    count = 0
    last_row = []

    for row in reader:
        # skip duplicates
        if last_row != [] and row[args.DeID] == last_row[args.DeID]:
            continue

        if args.full or (count >= 41) or count == 0:
            rows.append(row)
        count += 1

        last_row = row

first = int(args.first)
last = int(args.last)
last = last if last > 0 else len(rows[0]) + last

for q_num in range(first, last):
    adj_q_num = q_num + 1

    with open(f"{args.output}-q{adj_q_num}.csv", 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(["ID", "DeID", rows[0][q_num], "Source", "Question ID"])

        for row in rows[1:]:
            source = sys.argv[1][5:-4]
            # 5:-4; for filenames like "DeID F20 Initial Responses.csv", removes "DeID" and ".csv"

            writer.writerow([f"{args.output}-{row[args.DeID]}-{adj_q_num}", row[args.DeID],
                             row[q_num], source, f"{source}-{adj_q_num}"])
