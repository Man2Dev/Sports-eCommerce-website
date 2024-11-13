import psycopg2
from psycopg2 import OperationalError
import time

def populate_database():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="nope",
        database="software_development_srh"
    )
    try:
        cursor = connection.cursor()

        cursor.execute("INSERT INTO sport(id, name, image_url) VALUES"
                       "(1, 'Basketball', 'https://kingsquaresportscentre.com/wp-content/uploads/2023/09/AdobeStock_520402576-scaled.jpeg'),"
                       "(2, 'Cycling', 'https://cdn.shopify.com/s/files/1/0551/0388/1250/files/cycling_benefits_styrkr.jpg?v=1676894320'),"
                       "(3, 'Tennis', 'https://spok.de/wp-content/uploads/2023/06/IMG_6682-jpg.webp'),"
                       "(4, 'Football', 'https://cdn.prod.website-files.com/5ca5fe687e34be0992df1fbe/6235ea7fbaf601e8d3980228_boy-kicking-ball-on-football-field-2021-09-24-03-47-56-utc-min-min.jpg');")

        cursor.execute("INSERT INTO category(id, name, image_url) VALUES"
                       "(1, 'Clothing', 'https://media.istockphoto.com/id/1321017606/photo/multicolored-sport-sleeveless-t-shirts-and-shirts.jpg?s=612x612&w=0&k=20&c=NddwChiHYyB2Swr3emp94PiSGHV2RQXzghkmmj3KkWo='),"
                       "(2, 'Footware', 'https://truesport.org/wp-content/uploads/choosing-footwear-post.jpg'),"
                       "(3, 'Accessories', 'https://www.snapsports.com/wp-content/uploads/2021/04/sports-pack.jpeg'),"
                       "(4, 'Sport Nutrition', 'https://cdn.prod.website-files.com/60bbd0bb03425613b8352d51/65e74d223e723f2fa7fca0b2_Nutrishop_StorePhoto_11.jpg');")

        cursor.execute("INSERT INTO item(id, price, status,amount,name,description,category,sport) VALUES"
                       "(1, 10.99, 'show', 5, '5 kg dumbells', 'Handheld weights', 3, 2),"
                       "(2, 5.99 , 'show', 10, 'Zip-up hoodie', 'Outerwear with a front zipper', 1, 3),"
                       "(3, 13.99 ,'show', 1, 'Green soccer ball', 'Soccer Ball in green color', 3, 4),"
                       "(4, 12.5 , 'show', 15, 'Black gloves', 'Soccer gloves in black', 3, 4);")

        cursor.execute("INSERT INTO item_images(item_id, image_url) VALUES"
                       "(1, 'https://beihasara.com/wp-content/uploads/2023/04/5-kg-home-gym-dumbbell-set-10-scorpion-original-imafuskvwjvxtrv2.jpeg'),"
                       "(2,'https://8mi.de/cdn/shop/files/ZipGrey.png?v=1699116639&width=1445'),"
                       "(3,'https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/04a000d26ed14562bc818fdc4b6c0fc0_9366/MLS_24_Club_Ball_Green_IP1627_01_standard.jpg'),"
                       "(4,'https://www.sbj-sportland.de/images/product_images/original_images/Boxhandschuhe-Schwarz---frontal-09-2086-SW.JPG');")
        connection.commit()
    except OperationalError as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    populate_database()