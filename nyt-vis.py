import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# Individual, filtered data frames

# Gender of authors on list
year_gender_df = pd.DataFrame(overall_gender_year_count,
                              columns=["year", "male_count",
                                       "female_count",
                                       "unknown_count"])
year_gender_df.set_index('year', inplace=True)

# Gender of authors that had a w/ first ranking
first_rank_df = pd.DataFrame(overall_first_rank_count,
                             columns=["year", "male_count",
                                      "female_count",
                                      "unknown_count"])
first_rank_df.set_index("year", inplace=True)

# Gender of authors that debuted w/ first ranking
debut_first_df = pd.DataFrame(overall_debut_first_count,
                              columns=["year", "male_count",
                                       "female_count",
                                       "unknown_count"])
debut_first_df.set_index("year", inplace=True)

# Collection of top ten titles on list in each year
# Top ten measured by: most time on the list, grabbed first ten for
# Each year

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

# Gender of authors in top ten
top_ten_gender_df = pd.DataFrame(top_ten_gender_counts,
                                 columns=["year", "male_count",
                                          "female_count", "unknown_count"])
print(top_ten_gender_df)

# Plots

# Gender of authors on the list (overall)
sns.set_theme(style="darkgrid")
sns.lineplot(data=year_gender_df)
plt.title("Percieved gender of hardcover fiction bestseller authors \
          (1931-2020)")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# Gender of authors that reached first ranking
sns.lineplot(data=first_rank_df)
plt.title("Percieved gender of #1 hardcover fiction bestseller authors \
          (1931-2020)")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# Gender of authors that debuted w/ first ranking
sns.lineplot(data=debut_first_df)
plt.title("Percieved gender of debut #1 hardcover fiction bestseller authors \
          (1931-2020)")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# Gender of authors of top ten books over time
male_bar = sns.barplot(x="year", y="male_count", data=top_ten_gender_df, color="darkblue")
female_bar = sns.barplot(x="year", y="female_count", data=top_ten_gender_df, color="lightblue")
unknown_bar = sns.barplot(x="year", y="unknown_count", data=top_ten_gender_df, color="green")

top_bar = mpatches.Patch(color='darkblue', label='male')
middle_bar = mpatches.Patch(color='lightblue', label='female')
bottom_bar = mpatches.Patch(color="green", label="unknown")
plt.legend(handles=[top_bar, middle_bar, bottom_bar])

plt.title("Percieved gender of top ten hardcover fiction bestseller authors \
          (1931-2020)")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()
