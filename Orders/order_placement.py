import datetime
from Orders import prices, random_order_no_generator

def place_order(order_data, db, order_details_model, redis_client):

    date_placed = datetime.datetime.now().isoformat().split("T")[0]
    time_placed = datetime.datetime.now().isoformat().split("T")[1]
    order_number = random_order_no_generator.create_random_order_no("Gas", "Juja")
    
    #Cache the order
    redis_client.hmset(f'order:{order_number}', order_data)
    redis_client.hset(f'order:{order_number}', "date_placed", date_placed)
    redis_client.hset(f'order:{order_number}', "time_placed", time_placed)
    redis_client.expire(f'order:{order_number}', 172800) #Redis hash is deleted after 48 hours
    #Store order persistently in db
    new_order = order_details_model(order_no= order_number, name=order_data['name'], phone_no=order_data['phone_no'], order_type=order_data['order_type'], brand=order_data['brand'], size=order_data['size'],
                                gate_region=order_data['gate_region'], apartment=order_data['apartment'], date_placed=date_placed, time_placed=time_placed, complete="Pending")
    db.session.add(new_order)
    db.session.commit()
    
    # Fetching the price for the particular order
    order_type=order_data['order_type']
    brand=order_data['brand']
    size=order_data['size']

    price = prices.fetch_price(order_type,brand,size)

    message = "Order has been placed succesfully"

    response =  message, price

    return response

def get_price(order_data):
    print(order_data)
    print(type(order_data))
    order_type=order_data['order_type']
    brand=order_data['brand']
    size=order_data['size']

    price = prices.fetch_price(order_type,brand,size)
    message = "Price fetched"

    response = message, price

    return response