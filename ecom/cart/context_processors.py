from .cart import Cart


#Create context processor so that our cart works on all pages
def cart(request):
  ##Return the default data from our cart
  return{'cart':Cart(request)}