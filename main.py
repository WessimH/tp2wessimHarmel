import json

import pandas as pd


# Fonction pour récupérer les garnitures uniques du fichier menu.json
def get_garnitures():
    # Lecture du fichier JSON
    menu = pd.read_json("menu.json")

    unique_garnitures = []


    for pizza in menu.get("pizzas", []):
        if "garnitures" in pizza:
            for garniture in pizza["garnitures"]:
                if garniture not in unique_garnitures:
                    unique_garnitures.append(garniture)

    return unique_garnitures


# Fonction pour récupérer le menu complet depuis menu.json
def get_menu():
    return pd.read_json("menu.json")


# Classe Pizza
class Pizza:
    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price
        self.ingredients = []  # Liste pour stocker les ingrédients
        self.available_garnitures = get_garnitures()

    def add_ingredient(self, ingredient):
        if ingredient not in self.available_garnitures:
            raise ValueError(f"L'ingrédient '{ingredient}' n'existe pas dans le menu.")
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)

    def __str__(self):
        return f"{self.name} ({self.size}) - {self.price}€, Ingrédients: {', '.join(self.ingredients)}"


# Classe Drink
class Drink:
    def __init__(self, name, volume, price):
        self.name = name
        self.volume = volume
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.volume} ml) - {self.price}€"


# Classe Order
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.products = []  # Liste pour stocker les produits

    def add_product(self, product):
        self.products.append(product)

    def total_price(self):
        total = sum(product.price for product in self.products)
        return total

    def generate_receipt(self):
        receipt_data = []
        for product in self.products:
            if isinstance(product, Pizza):
                receipt_data.append({
                    "Nom du produit": product.name,
                    "Taille": product.size,
                    "Prix": product.price
                })
            elif isinstance(product, Drink):
                receipt_data.append({
                    "Nom du produit": product.name,
                    "Taille": f"{product.volume} ml",
                    "Prix": product.price
                })
        df = pd.DataFrame(receipt_data)
        print(f"Commande {self.order_id} :\n{df}\nPrix total : {self.total_price()}€")
        return df


# Fonction pour traiter les commandes depuis commandes.json
def process_orders(commands_file):
    menu = get_menu()
    with open(commands_file, "r") as file:
        commandes = json.load(file)

    for commande in commandes:
        order = Order(commande["commande_id"])
        for item in commande["items"]:
            # Vérification si l'item est une pizza
            pizza_info = menu[menu['pizzas'].apply(lambda x: x['nom']) == item]
            if not pizza_info.empty:
                pizza_data = pizza_info['pizzas'].values[0]
                pizza = Pizza(pizza_data['nom'], pizza_data['taille'], pizza_data['prix'])
                order.add_product(pizza)
            else:
                # Vérification si l'item est une boisson
                drink_info = menu[menu['boissons'].apply(lambda x: x['nom']) == item]
                if not drink_info.empty:
                    drink_data = drink_info['boissons'].values[0]
                    drink = Drink(drink_data['nom'], drink_data['volume'], drink_data['prix'])
                    order.add_product(drink)
                else:
                    print(f"L'item '{item}' n'est ni une pizza ni une boisson dans le menu.")
        order.generate_receipt()


# Exemple d'utilisation pour traiter les commandes
process_orders("commandes.json")
