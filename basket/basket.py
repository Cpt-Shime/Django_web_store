from decimal import Decimal

from store.models import Product

class Basket():
   
    # funckija koja se pozve i stvara session i stvara session key
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    #dodaj u kosaricu proslijedemo 
    def add(self, product, qty):
        
        product_id = str(product.id)
        # ako product je u kosarici 
        if product_id in self.basket:
            #ako je u kosarici onda qt
            self.basket[product_id]['qty'] = qty
        else:
            #ako nije u kosarici napravi i proslijedi cijenu i kolicinu
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()


    
    def __iter__(self):
       
        #iteratiraj po kljucevima koje smo dodali u kosaricu
        # tj. prodi kroz sve što je u kosarici

        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()


        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            # vrati item
            yield item


    # funckija za zbrajanje qty basketa (suma qty itema u basketu )
    def __len__(self):
        
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    # zbroji totalnu cijena svih itema i svih qunatitya
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())


    #pborisi iz kosarice
    def delete(self, product):
        
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()

    #spremi session
    def save(self):
        self.session.modified = True