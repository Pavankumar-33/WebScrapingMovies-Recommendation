import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


# Read the DataFrame from the pickle file
df = pd.read_pickle('.\\data.pkl')

#Read actual csv files
df1 = pd.read_csv('.\\credits.csv')
df2 = pd.read_csv('.\\movies.csv')
#print(df2.head())

final_df = df2.merge(df1, on = 'title')
print(final_df.shape)

