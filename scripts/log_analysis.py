#!/usr/bin/env python3
import re
import operator
import csv
from collections import defaultdict

def parse_log_file(logfile_path):
    """Parse the syslog file and return error counts and per-user statistics."""
    errors = defaultdict(int)
    per_user = defaultdict(lambda: {"INFO": 0, "ERROR": 0})

    pattern = r"ticky: ([\w+]*):? ([\w' ]*)[\[[#0-9]*\]?]? ?\((.*)\)$"
    # we can also use: r"ticky: (INFO|ERROR)[:]? (.+) \(([\w\.]+)\)$"



    with open(logfile_path, "r") as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                code, message, user = match.groups()

                # Count errors by message
                if code == "ERROR":
                    errors[message] += 1

                # Count per-user INFO/ERROR
                per_user[user][code] += 1

    return errors, per_user


def write_error_csv(errors, output_path):
    """Write error messages and counts to CSV, sorted by frequency."""
    sorted_errors = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Error", "Count"])
        writer.writerows(sorted_errors)


def write_user_csv(per_user, output_path):
    """Write per-user INFO/ERROR counts to CSV, sorted by username."""
    sorted_users = sorted(per_user.items())
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "INFO", "ERROR"])
        for user, stats in sorted_users:
            writer.writerow([user, stats["INFO"], stats["ERROR"]])


def main():
    errors, per_user = parse_log_file("data/syslog.log")
    write_error_csv(errors, "output/error_message.csv")
    write_user_csv(per_user, "output/user_statistics.csv")
    print("Reports generated in 'output/' folder.")


if __name__ == "__main__":
    main()
