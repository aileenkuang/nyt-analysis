import pandas as pd

data_file = open("assets/associated_nyt_titles.csv", "r")
df = pd.read_csv(data_file)

# Author gender
male_count = 0
female_count = 0
unknown_count = 0
for entry in df["author_gender"]:
    if "M" in entry:
        male_count += 1
    elif "F" in entry:
        female_count += 1
    elif "None" in entry:
        unknown_count += 1

years = range(1931, 2021)
overall_gender_year_count = []
for year in years:
    year_df = df[df["year"] == year]["author_gender"]
    year_male_ct = 0
    year_female_ct = 0
    year_unknown_ct = 0
    for entry in year_df:
        if "M" in entry:
            year_male_ct += 1
        elif "F" in entry:
            year_female_ct += 1
        elif "None" in entry:
            year_unknown_ct += 1
    all_counts = [year, year_male_ct, year_female_ct, year_unknown_ct]
    overall_gender_year_count.append(all_counts)

year_gender_df = pd.DataFrame(overall_gender_year_count,
                              columns=["Year", "Male Authors",
                                       "Female Authors",
                                       "Authors w/ Unknown Gender"])

print("Number of male authors: ", male_count)
print("Number of female authors: ", female_count)
print("Number of authors with unknown gender: ", unknown_count)
print()

# Author race
white_count = 0
black_count = 0
api_count = 0
aian_count = 0
twoprace_count = 0
hispanic_count = 0
unknown_count = 0
for entry in df["author_race"]:
    if "white" in entry:
        white_count += 1
    elif "black" in entry:
        black_count += 1
    elif "api" in entry:
        api_count += 1
    elif "aian" in entry:
        aian_count += 1
    elif "2prace" in entry:
        twoprace_count += 1
    elif "hispanic" in entry:
        hispanic_count += 1
    elif "None" in entry:
        unknown_count += 1

print("Number of white authors: ", white_count)
print("Number of Black authors: ", black_count)
print("Number of API authors: ", api_count)
print("Number of AIAN authors: ", aian_count)
print("Number of 2prace authors: ", twoprace_count)
print("Number of Hispanic authors: ", hispanic_count)
print("Number of authors w/ unknown race: ", unknown_count)
