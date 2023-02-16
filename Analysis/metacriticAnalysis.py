import pandas as pd
import matplotlib.pyplot as plt
import statistics
from datetime import datetime

df = pd.read_csv('mergedMetacritic.csv')
df = df.dropna()
df['date'] = pd.to_datetime(df['date'], format="%Y/%m/%d")
df['year'] = pd.DatetimeIndex(df['date']).year

# filter out 'ratings' string
df['numberofuserreviews'] = df['numberofuserreviews'].str.extract('(\d+)').astype(int)

# convert from string
df['numberofcriticreviews'] = df['numberofcriticreviews'].astype(int)
df['userscore'] = df['userscore'].astype(float)
df['metascore'] = df['metascore'].astype(int)

# remove rows without reviews
df = df.query("numberofuserreviews >= 1 and numberofcriticreviews >= 1")


def weighted_rating(x, m, c, t):
    if t == 'user':
        v = x['numberofuserreviews']
        r = x['userscore']
        # Calculation based on the IMDB formula, x10 to make it out of 100 instead of 10 to match critic score
        return (((v/(v+m) * r) + (m/(m+v) * c)) * 10)
    elif t == 'critic':
        v = x['numberofcriticreviews']
        r = x['metascore']
        # Calculation based on the IMDB formula
        return (v/(v+m) * r) + (m/(m+v) * c)

df['userweighted'] = df.apply(weighted_rating, args=(1, df['userscore'].mean(), 'user'), axis=1)
df['criticweighted'] = df.apply(weighted_rating, args=(1, df['metascore'].mean(), 'critic'), axis=1)

df['overallweighted'] = df[['userweighted', 'criticweighted']].mean(axis=1)

df.sort_values(by=['overallweighted'], ascending=False, inplace=True)

years = sorted(df['year'].unique()) # all possible year values

overall = list(df.groupby('year')['overallweighted'].apply(list).values) # list of weighted scores by year

# iterates over overall and gets mean weighted average for each year
final = []
for list in overall:
    final.append(statistics.fmean(list))

for i, year in enumerate(years):
    years[i] = str(year)[-2:]
# converts to 2 digits instead of 4 (looks better on graph)

plt.plot(years, final)
plt.xticks(years)
plt.yticks([i for i in range(0, 101, 5)])
plt.title('Average score of a video game each year')
plt.xlabel('Years (1996-2023)')
plt.ylabel('Average score')
plt.show()

