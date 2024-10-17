from store.models import Product, Profile


class Cart():
  def __init__(self, request):
    self.session = request.session
    #Get request
    self.request = request
    
    # Get the current seesion key if it exist
    cart = self.session.get('session_key')
    
    #if the user is new no session key
    if 'session_key' not in request.session:
      cart = self.session['session_key'] = {}
      
#MAKE SURE THAT CART IS AVAILABLE TO ALL PAGES OF SITE
    self.cart = cart 
  def db_add(self, product, quantity):
    product_id = str(product)
    product_qty = str(quantity)
  #LOGIC
    if product_id in self.cart:
      pass
    else:
      #self.cart[product_id] = {'price': str(product.price)}
      self.cart[product_id] = int(product_qty)
    self.session.modified = True
    # Deal withe logged in user
    if self.request.user.is_authenticated:
      #Get the current user profile
      current_user = Profile.objects.filter(user__id=self.request     .user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      #Save carty to the Profile Model
      current_user.update(old_cart=str(carty))
    
      
  def add(self, product, quantity):
    product_id = str(product.id)
    product_qty = str(quantity)
  #LOGIC
    if product_id in self.cart:
      pass
    
    else:
      #self.cart[product_id] = {'price': str(product.price)}
      self.cart[product_id] = int(product_qty)
    self.session.modified = True
    # Deal withe logged in user
    if self.request.user.is_authenticated:
      #Get the current user profile
      current_user = Profile.objects.filter(user__id=self.request     .user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      #Save carty to the Profile Model
      current_user.update(old_cart=str(carty))
    
    
  def cart_total(self):
    product_ids = self.cart.keys()
    #lookup those keys in our database
    products = Product.objects.filter(id__in=product_ids)
    #get quantities
    quantities = self.cart
    #lets start counting at 0
    total = 0
    for key, value in quantities.items():
        #converting key into string so that we can do math
        key = int(key)
        for product in products:
          if product.id == key:
            if product.is_sale:
              total = total + (product.sale_price * value)
            else:
              total = total + (product.price * value)
            
    return total
    
  def __len__(self):
    return len(self.cart)
  
  def get_prods(self):
    products_ids = self.cart.keys()
    
    #USE IDs TO LOOK UP PRODUCTS IN THE DATABASE MODELS
    products = Product.objects.filter(id__in=products_ids)
    #return those looked up products
    return products
  
  def get_quants(self):
    quantities = self.cart
    return quantities
  
  def update(self, product, quantity):
    product_id = str(product)
    product_qty = int(quantity)
    
    #get cart
    ourcart = self.cart
    #update dictionary
    ourcart[product_id] = product_qty
    
    self.session.modified = True
    thing = self.cart
    if self.request.user.is_authenticated:
      #Get the current user profile
      current_user = Profile.objects.filter(user__id=self.request     .user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      #Save carty to the Profile Model
      current_user.update(old_cart=str(carty))
    return thing
  
  def delete(self, product):
    product_id = str(product)
    #delete from dictionary/cart
    if product_id in self.cart:
      del self.cart[product_id]
      
    self.session.modified = True
    if self.request.user.is_authenticated:
      #Get the current user profile
      current_user = Profile.objects.filter(user__id=self.request     .user.id)
      carty = str(self.cart)
      carty = carty.replace("\'", "\"")
      #Save carty to the Profile Model
      current_user.update(old_cart=str(carty))