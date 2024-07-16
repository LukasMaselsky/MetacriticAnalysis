import pandas as pd
import matplotlib.pyplot as plt
import statistics
from datetime import datetime
from textwrap import wrap
import os

# path of the given file
print(os.path.dirname(os.path.abspath("mergedMetacritic.csv")))


df = pd.read_csv(r'Analysis/mergedMetacritic.csv')
df = df.dropna()

df['date'] = pd.to_datetime(df['date'], format="ISO8601")
df['year'] = pd.DatetimeIndex(df['date']).year

print(df['year'].value_counts()) # shows 96-99 are outliers due to the low amount of games those years
print(df['developer'].value_counts()) # most common developers
print(df['rating'].value_counts())
print(df['platform'].value_counts())
print(df['genres'].str.split(',\s+', expand=True).stack().value_counts()) 
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
overallYears = list(df.groupby('year')['overallweighted'].apply(list).values) # list of weighted scores by year

# iterates over overall and gets mean weighted average for each year
final = []
for l in overallYears:
    final.append(statistics.fmean(l))

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



developers = sorted(df['developer'].unique())
overallDevelopers = list(df.groupby('developer')['overallweighted'].apply(list).values)


final = []
for l in overallDevelopers:
    final.append(statistics.fmean(l))

topDevs = list(df['developer'].value_counts().index[:20]) # top 20 developers by COUNT
topDevsDict = {}

for dev in topDevs:
    index = developers.index(dev)
    topDevsDict[dev] = final[index] 
    #changed.append(final[index])


topDevsDict = {k: v for k, v in reversed(sorted(topDevsDict.items(), key=lambda item: item[1]))} # sort 
topDevs = ["\n".join(wrap(dev, 5)) for dev in topDevsDict.keys()]

plt.bar(topDevs, topDevsDict.values()) #! fix label issue/legend      
plt.show()
