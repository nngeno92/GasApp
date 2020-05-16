def fetch_price(order_type,brand,size):
    order_type = order_type
    brand = other_brand(brand)
    size = size

    if order_type=="Purchase" and brand=="Total" and size=="3kg":
        price = "2400"
        print(price)
    elif order_type=="Purchase" and brand=="Total" and size=="6kg":
        price = "4000"
        print(price)
    elif order_type=="Purchase" and brand=="Total" and size=="13kg":
        price = "7000"
    
    elif order_type=="Purchase" and brand=="K-Gas" and size=="3kg":
        price = "2500"
        print(price)
    elif order_type=="Purchase" and brand=="K-Gas" and size=="6kg":
        price = "4200"
        print(price)
    elif order_type=="Purchase" and brand=="K-Gas" and size=="13kg":
        price = "7000"
    
    elif order_type=="Purchase" and brand=="Pro-Gas" and size=="3kg":
        price = "2000"
        print(price)
    elif order_type=="Purchase" and brand=="Pro-Gas" and size=="6kg":
        price = "3500"
        print(price)
    elif order_type=="Purchase" and brand=="Pro-Gas" and size=="13kg":
        price = "6000"
    
    elif order_type=="Purchase" and brand=="Other" and size=="3kg":
        price = "3000"
        print(price)
    elif order_type=="Purchase" and brand=="Other" and size=="6kg":
        price = "3900"
        print(price)
    elif order_type=="Purchase" and brand=="Other" and size=="13kg":
        price = "6500"
    
    elif order_type=="Refill" and brand=="Total" and size=="3kg":
        price = "400"
        print(price)
    elif order_type=="Refill" and brand=="Total" and size=="6kg":
        price = "1000"
        print(price)
    elif order_type=="Refill" and brand=="Total" and size=="13kg":
        price = "2000"
    
    elif order_type=="Refill" and brand=="K-Gas" and size=="3kg":
        price = "500"
        print(price)
    elif order_type=="Refill" and brand=="K-Gas" and size=="6kg":
        price = "1200"
        print(price)
    elif order_type=="Refill" and brand=="K-Gas" and size=="13kg":
        price = "2000"
    
    elif order_type=="Refill" and brand=="Pro-Gas" and size=="3kg":
        price = "450"
        print(price)
    elif order_type=="Refill" and brand=="Pro-Gas" and size=="6kg":
        price = "1000"
        print(price)
    elif order_type=="Refill" and brand=="Pro-Gas" and size=="13kg":
        price = "2000"
    
    elif order_type=="Refill" and brand=="Other" and size=="3kg":
        price = "400"
        print(price)
    elif order_type=="Refill" and brand=="Other" and size=="6kg":
        price = "900"
        print(price)
    elif order_type=="Refill" and brand=="Other" and size=="13kg":
        price = "1900"
    
    return price

#If the brand is not one of the well known brands, assign brand to "Other"

def other_brand(brand):
    brand = brand
    if brand != "Total" and brand != "K-Gas" and brand != "Pro-Gas":
        brand = "Other"
    else:
        pass

    return brand

