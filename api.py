import pickle
from sklearn.metrics.pairwise import linear_kernel
from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional

with open('tfidf_matrix.pkl', 'rb') as file:
    tfidf_matrix = pickle.load(file)

popularite = pd.read_csv("data.csv", sep="\t")

anime = pd.read_csv("anime2.csv", low_memory=False, sep="\t")

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(anime.index, index=anime['name'])


def get_recommendations(name, cosine_sim=cosine_sim):
    try:
        idx = indices[name]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        return anime['name'].iloc[movie_indices].values.tolist()
    except:
        return []


def get_recs_by_genres(genre):
    return anime[anime['genre'].str.contains(genre)].sort_values('rating', ascending=False).head(10)


def get_popular_recs():
    return popularite.sort_values('rating_y', ascending=False).head(10)


def filter_by_type(type):
    return anime[anime['type'].str == type]


app = FastAPI()


class ContentRecs(BaseModel):
    name: str


@app.post("/content")
async def predict_cluster(item: ContentRecs):
    return {'anime': get_recommendations(item.name)}


class GenreRecs(BaseModel):
    genre: str



@app.post("/genre")
async def predict_cluster(item: GenreRecs):
    result =  get_recs_by_genres(item.genre)
    return {
            'names': result['name'].values.tolist(),
            'anime': result['genre'].values.tolist()
        }


@app.get("/popular")
async def predict_cluster():
    return {'anime': get_popular_recs()['name'].values.tolist()}


class AnimeItem(BaseModel):
    type: str
    name: str


@app.get("/anime/", response_model=List[AnimeItem])
async def get_anime(type: Optional[str] = Query(None, description="Тип аниме для фильтрации")):
    if type is None:
        result_df = anime
    else:
        result_df = anime[anime['type'] == type]

    return result_df.head(10).to_dict(orient="records")

