import pandas as pd
import matplotlib.pyplot as plt
import statistics

df = pd.read_csv('mergedMetacritic.csv')
df = df.dropna()
df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y")
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


plt.plot(years, final)
plt.title('Title')
plt.xlabel('Years')
plt.ylabel('Avg score')
plt.show()

