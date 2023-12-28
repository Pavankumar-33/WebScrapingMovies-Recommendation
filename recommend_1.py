import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import ast


# Read the DataFrame from the pickle file
df = pd.read_pickle('.\\data.pkl')

#Read actual csv files
df1 = pd.read_csv('.\\credits.csv')
df2 = pd.read_csv('.\\movies.csv')
#print(df2.head())

final_df = df2.merge(df1, on = 'title')
#print(final_df.shape)

#print(final_df.isnull().sum())

final_df.dropna(inplace=True)

# print("HI")
# print(final_df.isnull().sum())
#print(final_df.duplicated().sum())

#literal obj to arry
def convert(obj):
    array = []
    for i in ast.literal_eval(obj):
        array.append(i['name'])
    return array

final_df['genres'] = final_df['genres'].apply(convert)
final_df['keywords'] = final_df['keywords'].apply(convert)
#print(final_df.head())

#noe cast and crew colmn
def casrCrew(obj):
    array = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            array.append(i['name'])
            counter += 1
        else:
            break

    return array
    
final_df['cast'] = final_df['cast'].apply(casrCrew)
#print(final_df.head())

#for directors clmn
def fetchDirecter(obj):
    array = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            array.append(i['name'])
            break
    return array

final_df['crew'] = final_df['crew'].apply(fetchDirecter)
#print(final_df.head())

#print(final_df['overview'][0])
final_df['overview'] = final_df['overview'].apply(lambda x:x.split())
#print(final_df['overview'][0])

#for other clmns to remove spaces
final_df['genres'] = final_df['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
final_df['keywords'] = final_df['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
final_df['crew'] = final_df['crew'].apply(lambda x:[i.replace(" ", "") for i in x])
final_df['cast'] = final_df['cast'].apply(lambda x:[i.replace(" ", "") for i in x])

#create tags
final_df['tags'] = final_df['overview'] + final_df['keywords'] + final_df['crew'] + final_df['cast']

new_df = final_df[['movie_id', 'title', 'tags']]
#print(new_df)

new_df['tags'] = new_df['tags'].apply(lambda x : ' '.join(x))
new_df['tags'] = new_df['tags'].apply(lambda x : x.lower())
#print(new_df['tags'][0])

#--------------------------------------------------------------------

cv = CountVectorizer(max_features = 5000, stop_words = 'english')
cv.fit_transform(new_df['tags']).toarray().shape

#convert count vector to array
vector = cv.fit_transform(new_df['tags']).toarray()
print(vector[0])
