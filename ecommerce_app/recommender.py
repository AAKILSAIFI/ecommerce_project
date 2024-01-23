# ecommerce_app/recommender.py
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.db.models import Count
from .models import Product

class ProductRecommender:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

        X, y = make_classification(n_samples=100, n_features=20, n_informative=10, n_clusters_per_class=2, random_state=42)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.train()

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def recommend(self, user_id, liked_products, disliked_products):
        # Adjust your recommendation logic based on user likes and dislikes
        # For simplicity, let's assume recommendations are based on popular products
        all_products = Product.objects.annotate(num_likes=Count('liked_by')).order_by('-num_likes')
        recommended_products = [product.name for product in all_products]

        return recommended_products
