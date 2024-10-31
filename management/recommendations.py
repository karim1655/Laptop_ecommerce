import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import Laptop, LaptopReview

def get_recommendations(user):
    # Estrae tutte le recensioni e crea un DataFrame
    reviews = LaptopReview.objects.all()
    data = {
        "user_id": [review.user.id for review in reviews],
        "laptop_id": [review.laptop.id for review in reviews],
        "rating": [review.rating for review in reviews]
    }
    df = pd.DataFrame(data)

    # Crea la matrice utente-laptop
    user_laptop_matrix = df.pivot_table(index="user_id", columns="laptop_id", values="rating").fillna(0)
    print(user_laptop_matrix)

    #Controllo per far sì che non cerchi di generare le recommendations per un
    # utente non loggato: il server dà l'errore "KeyError at /", perché nella home cerca la chiave dell'utente,
    # ma un utente non loggato non ne ha una
    if user.id not in user_laptop_matrix.index:
        return Laptop.objects.none()


    # Recupera i rating dell'utente specifico dalla matrice di rating.
    # Rimuove i valori nulli (NaN) dai rating dell'utente.
    user_ratings = user_laptop_matrix.loc[user.id].dropna()
    print(user_ratings)

    # Inizializza la lista delle raccomandazioni
    recommendations = []

    # Loop su ogni laptop e rating nella matrice
    for laptop_id, rating in user_ratings.items():
        laptop = Laptop.objects.get(id=laptop_id)
        if rating >= 4:  # Solo laptop con rating >= 4
            similar_laptops = Laptop.objects.filter(
                category=laptop.category,
                laptopreview__rating__gte=4
            ).exclude(id__in=user_ratings[user_ratings >= 4].index).distinct()
            recommendations.extend(similar_laptops)

    # Rimuove i duplicati
    final_laptops_recommendations = list(set(recommendations))

    # Restituisce le prime 6 raccomandazioni
    return final_laptops_recommendations[:6]