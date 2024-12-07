#!/usr/bin/env python3
import csv
import os

out_dir = os.environ["OUT_DIR"]

with open(f"{out_dir}/sample.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["foo", "bar"])
    writer.writeheader()
    writer.writerows([{"foo": "hello", "bar": "world"}, {"foo": "goodbye", "bar": "friend"}])
