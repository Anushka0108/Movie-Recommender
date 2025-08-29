import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_excel("imdb_movies.xlsx")
df['Genre'] = df['Genre'].fillna("")

vectorizer = TfidfVectorizer(stop_words="english")
genre_matrix = vectorizer.fit_transform(df['Genre'])
cosine_sim = cosine_similarity(genre_matrix, genre_matrix)

def recommend_movies(title, n=5):
    if title not in df['Title'].values:
        return f"Movie '{title}' not found in dataset"
    
    idx = df.index[df['Title'] == title][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    top_movies = [df.iloc[i[0]]['Title'] for i in sim_scores[1:n+1]]
    recommend_df = df[df['Title'].isin(top_movies)][
        ["Title", "Year", "Duration", "Rating", "Genre", "Link"]
    ]
    
    recommend_df.to_excel("recommended.xlsx", index=False)
    return recommend_df

movie_title = input("Enter a movie title: ")
print(f"Recommendations for {movie_title}:")
result_df = recommend_movies(movie_title, n=5)
print(result_df)                             
