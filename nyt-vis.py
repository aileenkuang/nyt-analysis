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
overall_first_rank_count = []
overall_debut_first_count = []

for year in years:
    year_by_gender_df = df[df["year"] == year]["author_gender"]
    gender_and_bestseller_df = df[(df["year"] == year) & (df["best_rank"] == 1)]["author_gender"]
    debut_first_df = df[(df["year"] == year) & (df["debut_rank"] == 1)]["author_gender"]

    all_counts = [year, 0, 0, 0]
    for entry in year_by_gender_df:
        if "M" in entry:
            all_counts[1] += 1
        elif "F" in entry:
            all_counts[2] += 1
        elif "None" in entry:
            all_counts[3] += 1

    first_rank_counts = [year, 0, 0, 0]
    for entry in gender_and_bestseller_df:
        if "M" in entry:
            first_rank_counts[1] += 1
        elif "F" in entry:
            first_rank_counts[2] += 1
        elif "None" in entry:
            first_rank_counts[3] += 1

    debut_first_counts = [year, 0, 0, 0]
    for entry in debut_first_df:
        if "M" in entry:
            debut_first_counts[1] += 1
        elif "F" in entry:
            debut_first_counts[2] += 1
        elif "None" in entry:
            debut_first_counts[3] += 1

    overall_gender_year_count.append(all_counts)
    overall_first_rank_count.append(first_rank_counts)
    overall_debut_first_count.append(debut_first_counts)

# Gender of authors on list
year_gender_df = pd.DataFrame(overall_gender_year_count,
                              columns=["year", "male_count",
                                       "female_count",
                                       "unknown_count"])
print(year_gender_df)

# Gender of authors that had a w/ first ranking
first_rank_df = pd.DataFrame(overall_first_rank_count,
                             columns=["year", "male_count",
                                      "female_count",
                                      "unknown_count"])
print(first_rank_df)

# Gender of authors that debuted w/ first ranking
debut_first_df = pd.DataFrame(overall_debut_first_count,
                              columns=["year", "male_count",
                                       "female_count",
                                       "unknown_count"])
print(debut_first_df)

titles_in_yearly_top_ten = []
for year in years:
    year_df = df[df["year"] == year]
    sorted_year_df = year_df.sort_values(by="total_weeks", ascending=False)
    top_ten_titles_df = sorted_year_df.iloc[:10]

    for index, entry in top_ten_titles_df.iterrows():
        entry_as_list = [entry["year"], entry["title"], entry["author"],
                         entry["total_weeks"], entry["author_gender"],
                         entry["author_race"]]
        titles_in_yearly_top_ten.append(entry_as_list)

# Collection of top ten titles on list in each year
# Top ten measured by: most time on the list, grabbed first ten for
# Each year
top_ten_df = pd.DataFrame(titles_in_yearly_top_ten,
                          columns=["year", "title", "author",
                                   "total_weeks", "author_gender",
                                   "author_race"])

top_ten_gender_counts = []
for year in years:
    top_ten_by_year_df = top_ten_df[top_ten_df["year"] == year]["author_gender"]
    gender_counts = [year, 0, 0, 0]
    for entry in top_ten_by_year_df:
        if "M" in entry:
            gender_counts[1] += 1
        elif "F" in entry:
            gender_counts[2] += 1
        elif "None" in entry:
            gender_counts[3] += 1
    top_ten_gender_counts.append(gender_counts)

top_ten_gender_df = pd.DataFrame(top_ten_gender_counts,
                                 columns=["year", "male_count",
                                          "female_count", "unknown_count"])
print(top_ten_gender_df)

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

# Print statements
print()
print("Number of male authors: ", male_count)
print("Number of female authors: ", female_count)
print("Number of authors with unknown gender: ", unknown_count)
print()
print("Number of white authors: ", white_count)
print("Number of Black authors: ", black_count)
print("Number of API authors: ", api_count)
print("Number of AIAN authors: ", aian_count)
print("Number of 2prace authors: ", twoprace_count)
print("Number of Hispanic authors: ", hispanic_count)
print("Number of authors w/ unknown race: ", unknown_count)
