import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import pandas as pd
from scipy.interpolate import make_interp_spline

data_file = open("assets/associated_nyt_titles.csv", "r")
df = pd.read_csv(data_file)

years = range(1931, 2021)
overall_gender_year_count = []
overall_first_rank_count = []
overall_debut_first_count = []

for year in years:
    year_by_gender_df = df[df["year"] == year]["author_gender"]
    gender_bs_df = df[(df["year"] == year) &
                      (df["best_rank"] == 1)]["author_gender"]
    first_df = df[(df["year"] == year) &
                  (df["debut_rank"] == 1)]["author_gender"]

    all_counts = [year, 0, 0, 0]
    for entry in year_by_gender_df:
        if "M" in entry:
            all_counts[1] += 1
        elif "F" in entry:
            all_counts[2] += 1
        elif "None" in entry:
            all_counts[3] += 1

    first_rank_counts = [year, 0, 0, 0]
    for entry in gender_bs_df:
        if "M" in entry:
            first_rank_counts[1] += 1
        elif "F" in entry:
            first_rank_counts[2] += 1
        elif "None" in entry:
            first_rank_counts[3] += 1

    debut_first_counts = [year, 0, 0, 0]
    for entry in first_df:
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
first_rank_long_df = pd.melt(first_rank_df, id_vars=["year"],
                             value_vars=["male_count", "female_count",
                                         "unknown_count"])

# Gender of authors that debuted w/ first ranking
debut_first_df = pd.DataFrame(overall_debut_first_count,
                              columns=["year", "male_count",
                                       "female_count",
                                       "unknown_count"])
# debut_first_df.set_index("year", inplace=True)

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
    top_ten_by_yr_df = top_ten_df[top_ten_df["year"] == year]["author_gender"]
    gender_counts = [year, 0, 0, 0]
    for entry in top_ten_by_yr_df:
        if "M" in entry:
            gender_counts[1] += 1
        elif "F" in entry:
            gender_counts[2] += 1
        elif "None" in entry:
            gender_counts[3] += 1
    top_ten_gender_counts.append(gender_counts)

# Gender of authors in top ten
tt_gender_df = pd.DataFrame(top_ten_gender_counts,
                            columns=["year", "male_count",
                                     "female_count", "unknown_count"])
tt_gender_df.set_index("year", inplace=True)

# Plots

plt.rcParams["font.family"] = "monospace"
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.left'] = False

# Gender of authors on the list (overall)
# Line chart: male_count on bottom (pink), female_count (blue)
# in middle, unknown_count on top (green)

male_counts = year_gender_df['male_count'].values
female_counts = year_gender_df['female_count'].values
unknown_counts = year_gender_df['unknown_count'].values

custom_colors = ["#DE95BA", "#0C359E", "#416D19"]

x_smooth = np.linspace(year_gender_df.index.min(),
                       year_gender_df.index.max(),
                       300)
df_smooth = pd.DataFrame({
    'male_count': make_interp_spline(year_gender_df.index,
                                     male_counts)(x_smooth),
    'female_count': make_interp_spline(year_gender_df.index,
                                       female_counts)(x_smooth),
    'unknown_count': make_interp_spline(year_gender_df.index,
                                        unknown_counts)(x_smooth)
})

# Creating the stacked plot with Plotly
fig = go.Figure()

# Add traces for each gender category
fig.add_trace(go.Scatter(x=x_smooth, y=df_smooth["male_count"],
                         mode="lines", fill="tozeroy", name="Male",
                         line=dict(color=custom_colors[0])))
fig.add_trace(go.Scatter(x=x_smooth, y=df_smooth["female_count"],
                         mode="lines", fill="tozeroy", name="Female",
                         line=dict(color=custom_colors[1])))
fig.add_trace(go.Scatter(x=x_smooth, y=df_smooth["unknown_count"],
                         mode="lines", fill="tozeroy", name="Unknown",
                         line=dict(color=custom_colors[2])))

# Customize plot layout
fig.update_layout(font_family="Courier New",
                  title="Perceived gender of bestseller authors (1931-2020)",
                  xaxis_title="Year",
                  yaxis_title="Count",
                  title_font=dict(size=20,
                                  family="Courier New"),
                  title_x=0.5,
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                  hovermode="x unified",
                  plot_bgcolor="#FFF3C7",
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  xaxis=dict(tickvals=[1940, 1960, 1980, 2000, 2020],
                             tickmode="array",
                             tickformat="d")
                  )

fig.update_traces(hovertemplate='%{x}: %{y:.0f}')

# Show the interactive plot
# fig.show()
with open('overall.html', 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn'))

# Gender of authors that reached first ranking
# Stacked barplot: male_count on bottom (pink), female_count (blue)
# in middle, unknown_count on top (green)

years_list = list(years)
fig, ax = plt.subplots()
fig.set_size_inches(10, 10)

ax.bar(years_list, first_rank_df["male_count"], color="#DE95BA",
       alpha=1, label="Male")
ax.bar(years_list, first_rank_df["female_count"],
       bottom=first_rank_df["male_count"], color="#0C359E",
       alpha=1, label="Female")
ax.bar(years_list, first_rank_df["unknown_count"],
       bottom=np.add(first_rank_df["male_count"],
                     first_rank_df["female_count"]),
       color="#416D19", alpha=1, label="Unknown")

ax.set_facecolor("#FFF3C7")
ax.legend()

plt.title("Percieved gender of #1 bestseller authors (1931-2020)",
          y=1.05, fontsize=15)
plt.xlabel("Year")
plt.ylabel("Count")

# plt.show()
plt.savefig("first_rank.png")
plt.close()

# Gender of authors that debuted w/ first ranking
# Stacked barplot: male_count on bottom (pink), female_count (blue)
# in middle, unknown_count on top (green)

print(debut_first_df.to_string())

fig, ax = plt.subplots()
fig.set_size_inches(10, 10)

ax.bar(years_list, debut_first_df["male_count"], color="#DE95BA", alpha=1,
       label="Male")
ax.bar(years_list, debut_first_df["female_count"],
       bottom=debut_first_df["male_count"], color="#0C359E", alpha=1,
       label="Female")
ax.bar(years_list, debut_first_df["unknown_count"],
       bottom=np.add(debut_first_df["male_count"],
                     debut_first_df["female_count"]),
       color="#416D19", alpha=1, label="Unknown")

ax.set_facecolor("#FFF3C7")
ax.legend()

plt.title("Percieved gender of debut #1 bestseller authors (1931-2020)",
          y=1.05, fontsize=15)
plt.xlabel("Year")
plt.ylabel("Count")

# plt.show()
plt.savefig("debut_first_rank.png")
plt.close()

# Gender of authors of top ten books over time
# Stacked area chart: male_count on bottom (pink), female_count (blue)
# in middle, unknown_count on top (green)

fig, ax = plt.subplots()
fig.set_size_inches(10, 10)

tt_gender_df = tt_gender_df[["male_count", "female_count", "unknown_count"]]

top_ten_male_ct = tt_gender_df["male_count"]
top_ten_female_ct = tt_gender_df["female_count"]
top_ten_unknown_ct = tt_gender_df["unknown_count"]

tt_colors = ["#0C359E", "#416D19", "#DE95BA"]

x_smooth = np.linspace(tt_gender_df.index.min(),
                       tt_gender_df.index.max(),
                       300)
top_smooth = pd.DataFrame({
    count: make_interp_spline(tt_gender_df.index,
                              tt_gender_df[count])(x_smooth)
    for count in tt_gender_df.columns
    })

plt.stackplot(x_smooth,
              top_smooth["female_count"],
              top_smooth["unknown_count"],
              top_smooth["male_count"],
              labels=["Female", "Unknown", "Male"],
              colors=tt_colors)

ax.set_facecolor("#FFFFFF")

handles, labels = ax.get_legend_handles_labels()
new_order = [2, 0, 1]
ax.legend([handles[idx] for idx in new_order],
          [labels[idx] for idx in new_order],
          loc="upper right")
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.xaxis.limit_range_for_scale(1931, 2020)

plt.title("Percieved gender of top ten bestseller authors (1931-2020)",
          y=1.05, fontsize=15)
plt.xlabel("Year")
plt.ylabel("Count")

# plt.show()
plt.savefig("top_ten.png")
plt.close()
