import re
import csv

# Loading and converting data
with open("assets/nyt_titles.tsv", 'r') as myfile:
    with open("assets/nyt_titles.csv", 'w') as csv_file:
        for line in myfile:
            file_content = re.sub(",", "%%%%", line)
            file_content = re.sub("\t", ",", file_content)
            csv_file.write(file_content)

nyt_data = open("assets/nyt_titles.csv", "r")
nyt_data_csv = csv.DictReader(nyt_data)
nyt_data_rows = [row for row in nyt_data_csv]
nyt_data.close()

for row in nyt_data_rows:
    for key in row.keys():
        row[key] = re.sub("%%%%", ",", row[key])

    int_cols = ["year", "total_weeks", "debut_rank", "best_rank"]
    for col in int_cols:
        row[col] = int(row[col])

names_gender_data = open("assets/name_gender_dataset.csv", "r")
names_gender_csv = csv.DictReader(names_gender_data)
names_gender_rows = [row for row in names_gender_csv]
names_gender_data.close()

for row in names_gender_rows:
    row["Count"] = int(row["Count"])
    row["Probability"] = float(row["Probability"])

surnames_race_data = open("assets/surnames-race.csv", "r")
surnames_race_csv = csv.DictReader(surnames_race_data)
surnames_race_rows = [row for row in surnames_race_csv]
surnames_race_data.close()

for row in surnames_race_rows:
    for key in row.keys():
        if row[key] == "(S)":
            row[key] = 0

    int_cols = ["rank", "count"]
    float_cols = ["prop100k", "cum_prop100k", "pctwhite", "pctblack", "pctapi",
                  "pctaian", "pct2prace", "pcthispanic"]

    for col in int_cols:
        row[col] = int(row[col])

    for col in float_cols:
        row[col] = float(row[col])


def parse(string):
    """
    Takes in a string (author name)
    Parses and returns list of names in the string

    Does not account for "edited and illustrated by"
    """
    if ", " in string:
        names = string.split(", ")
        list = []
        for name in names:
            list.extend(parse(name))
        return list
    elif " and " in string:
        names = string.split(" and ")
        list = []
        for name in names:
            list.extend(parse(name))
        return list
    else:
        return [string]


assert parse("Trevanian") == ['Trevanian']
assert parse("Clive Cussler and Jack Du Brul") == ['Clive Cussler', 'Jack Du Brul']
assert parse("""Newt Gingrich, William R. Forstchen and Albert S. Hanser""") == ['Newt Gingrich', 'William R. Forstchen', 'Albert S. Hanser']
assert parse("James Patterson and Frank Constantini, Emily Raymond and Brian Sitts") == ['James Patterson', 'Frank Constantini', 'Emily Raymond', 'Brian Sitts']
assert parse("W.E.B. Griffin and William E. Butterworth") == ['W.E.B. Griffin', 'William E. Butterworth']


# Figuring out first names
def parse_author_names(data):
    """
    Takes NYT bestseller data (parsed through CSV dictreader) as list of
    entries
    For each entry, figures out first and last names for authors

    If there are multiple authors: "first_name" and "last_name" cols
    for the entry will contain a tuple where each index will correspond
    to the author name. Ex. "first_name": ("Josh", "Ben") and "last_name":
    ("Jackson", "Anderson").

    Adds col w/ # of authors

    Creates and returns copy of data with first and last names as seperated
    cols in the row and col w/ count of authors
    """
    parsed_nyt_data = []
    for row in data:
        author_entry = row["author"]
        list_of_authors = parse(author_entry)

        author_count = len(list_of_authors)
        row["author_count"] = author_count

        # If one author
        if author_count == 1:
            name_segments = list_of_authors[0].split()
            num_name_seg = len(name_segments)
            # Only first name
            if num_name_seg == 1:
                first = name_segments[0]
                last = "N/A"
            # First last, first middle last
            elif num_name_seg > 1:
                first = name_segments[0]
                last = name_segments[num_name_seg - 1]
            row["author_first_name"] = [first]
            row["author_last_name"] = [last]

        # If multiple authors
        else:
            first_list = []
            last_list = []
            for i in range(len(list_of_authors)):
                name_segments = list_of_authors[i].split()
                num_name_seg = len(name_segments)
                if num_name_seg == 1:
                    first = name_segments[0]
                    last = "N/A"
                else:
                    first = name_segments[0]
                    last = name_segments[num_name_seg - 1]
                first_list.append(first)
                last_list.append(last)
            row["author_first_name"] = first_list
            row["author_last_name"] = last_list
        parsed_nyt_data.append(row)
    return parsed_nyt_data


parsed_authors_data = parse_author_names(nyt_data_rows)

manual_parse = []
for row in parsed_authors_data:
    parsed_first = row["author_first_name"]
    parsed_last = row["author_last_name"]
    for i in range(len(parsed_first)):
        if "illustrated" in parsed_first[i] or "illustrated" in parsed_last[i]:
            manual_parse.append(row["id"])
        elif " and " in parsed_first[i] or " and " in parsed_last[i]:
            manual_parse.append(row["id"])
        elif " edited " in parsed_first[i] or " edited " in parsed_last[i]:
            manual_parse.append(row["id"])

for id in manual_parse:
    for row in parsed_authors_data:
        if row["id"] == id:
            author_entry = row["author"]
            author_name = author_entry.split(" by ")[1]

            name_segments = author_name.split()
            num_name_seg = len(name_segments)

            if num_name_seg == 1:
                first = name_segments[0]
                last = "N/A"
            elif num_name_seg > 1:
                first = name_segments[0]
                last = name_segments[num_name_seg - 1]
            row["author_first_name"] = [first]
            row["author_last_name"] = [last]
            row["author_count"] = 1

for row in parsed_authors_data:
    if row["id"] == "5511":
        row["author_count"] = 2
        row["author_first_name"] = ["Janet", "Allan"]
        row["author_last_name"] = ["Ahlberg", "Ahlberg"]

for row in parsed_authors_data:
    if row["id"] == "7236":
        row["author_first_name"] = ["Jimmy"]
        row["author_last_name"] = ["Buffett"]

for row in parsed_authors_data:
    if row["id"] == "7260":
        row["author_first_name"] = ["Clive, Paul"]
        row["author_last_name"] = ["Cussler, Kemprecos"]

for row in parsed_authors_data:
    if row["id"] == "7278":
        row["author_first_name"] = ["Bill, Thomas"]
        row["author_last_name"] = ["Adler, Chastain"]


# Associating race and gender with names
def associate_titles_gender(data):
    """
    Takes NYT bestseller data (parsed through CSV dictreader)
    and associates authors w/ race + gender

    Returns copy of data w/ associations
    """
    associated_gender_data = []
    for row in data:
        row["author_gender"] = []
        first_name = row["author_first_name"]
        for name in first_name:
            gender = None
            gender_count = 0
            for name_row in names_gender_rows:
                if name == name_row["\ufeffName"]:
                    if name_row["Count"] > gender_count:
                        gender = name_row["Gender"]
                        gender_count = name_row["Count"]
            row["author_gender"].append(gender)
        associated_gender_data.append(row)
    return associated_gender_data


def associate_titles_race(data):
    """
    Takes NYT bestseller data (parsed through CSV dictreader)
    and associates authors w/ race

    Returns copy of data w/ associations
    """
    associated_race_data = []
    for row in data:
        # Initialize empty column for race data
        row["author_race"] = []

        # Get last names
        last_name = row["author_last_name"]

        for name in last_name:
            max_race = None
            for surname_row in surnames_race_rows:
                if name.strip(".").upper() == surname_row["name"]:
                    name_race_perc = {"white": surname_row["pctwhite"],
                                      "black": surname_row["pctblack"],
                                      "api": surname_row["pctapi"],
                                      "aian": surname_row["pctaian"],
                                      "2prace": surname_row["pct2prace"],
                                      "hispanic": surname_row["pcthispanic"]}
                    max_race = max(name_race_perc, key=name_race_perc.get)
            row["author_race"].append(max_race)
        associated_race_data.append(row)
    return associated_race_data


associated_gender_nyt_rows = associate_titles_gender(parsed_authors_data)
associated_race_nyt_rows = associate_titles_race(associated_gender_nyt_rows)

with open("assets/associated_nyt_titles.csv", "w") as associated_csv:
    for row in associated_race_nyt_rows:
        associated_csv.write(row)

# Count rows w/ an unassociated gender
unassociated_gender_rows_count = 0
unassociated_gender_names = []
for row in associated_gender_nyt_rows:
    if None in row["author_gender"]:
        unassociated_gender_rows_count += 1
        unassociated_gender_names.append(row["author_first_name"])

print(unassociated_gender_names)

# Count rows w/ an unassociated race
unassociated_race_rows_count = 0
unassociated_race_surnames = []
for row in associated_race_nyt_rows:
    if None in row["author_race"]:
        unassociated_race_rows_count += 1
        unassociated_race_surnames.append(row["author_last_name"])

print("Count of titles w/ unassociated gender: ",
      unassociated_gender_rows_count)
print("Count of titles w/ unassociated race: ",
      unassociated_race_rows_count)

print(associated_race_nyt_rows)
