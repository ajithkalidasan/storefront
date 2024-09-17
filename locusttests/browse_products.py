from locust import HttpUser, task, between
from random import randint


class StoreUser(HttpUser):
    wait_time = between(1, 10)

    @task(2)
    def view_products(self):
        print( "viewing products")
        collecton_id = randint(0, 2)
        self.client.get(
            f"/store/products/?collecton_id = {collecton_id}", name="/store/products"
        )

    @task(4)
    def view_product(self):
        print ("viewing product details")
        product_id = randint(1, 10)
        self.client.get(
            f"/store/products/{product_id}",
            
            name = '/store/products/:id'
        )

    @task(1)
    def add_to_cart(self):
        print ("adding to cart")
        product_id = randint(1, 10)
        self.client.post(
            f"/store/cart/{self.cart_id}/items/",
            name="/store/cart/items",
            json={"product_id": product_id, "quantity": 1},
        )

    def on_start(self) -> None:
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
