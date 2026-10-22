import tkinter as tk
import json
import os
import time

DATA_FILE = "restaurant_db.json"


class MenuItem:

    item_counter = 1

    def __init__(self, name, price, item_type, available=True, item_id=None):
        self.name = name
        self.price = price
        self.type = item_type
        self.available = available

        #create new id if not provided
        if item_id == None:
            self.id = "I" + str(MenuItem.item_counter)
            MenuItem.item_counter = MenuItem.item_counter + 1
        else:
            self.id = item_id

            #update counter based on existing id
            number = int(item_id[1:])
            if number >= MenuItem.item_counter:
                MenuItem.item_counter = number + 1

    def info(self):

        #check availability status
        if self.available == True:
            status = "Available"
        else:
            status = "Not Available"

        #return item info as text
        text = self.id + " | " + self.name + " | " + self.type + " | " + str(self.price) + " | " + status
        return text


class Order:

    order_counter = 1

    def __init__(self, customer, restaurant, items=None, order_id=None, order_time=None):
        self.customer = customer
        self.restaurant = restaurant

        #set items list
        if items == None:
            self.items = []
        else:
            self.items = items

        #create new order id if not provided
        if order_id == None:
            self.id = "O" + str(Order.order_counter)
            Order.order_counter = Order.order_counter + 1
        else:
            self.id = order_id

            #update order counter from existing id
            number = int(order_id[1:])
            if number >= Order.order_counter:
                Order.order_counter = number + 1


        #set order time
        if order_time == None:
            self.time = time.ctime()
        else:
            self.time = order_time

    def add_item(self, item):
        self.items.append(item)

    def total_price(self):
        total = 0

        #total price
        for i in self.items:
            total = total + i.price
        return total

    def text(self):
        #create text view of order
        t = "Order ID: " + self.id + "\n"
        t = t + "Customer: " + self.customer.username + "\n"
        t = t + "Restaurant: " + self.restaurant.name + "\n"
        t = t + "Time: " + self.time + "\n"


        #add item info
        for i in self.items:
            t = t + i.info() + "\n"

        #add total price
        t = t + "Total: " + str(self.total_price()) + "\n"
        t = t + "---------------------\n"
        return t


class User:
    manager_count = 1
    customer_count = 1

    def __init__(self, name, username, password, role, user_id=None):
        self.name = name
        self.username = username
        self.password = password
        self.role = role


        #create new user id if not provided
        if user_id == None:
            self.id = self.generate_id()
        else:
            self.id = user_id
            self.update_counter_from_id()

    def generate_id(self):

        #generate id based on user role
        if self.role == "manager":
            uid = "m" + str(User.manager_count)
            User.manager_count = User.manager_count + 1
            return uid

        if self.role == "customer":
            uid = "c" + str(User.customer_count)
            User.customer_count = User.customer_count + 1
            return uid

    def update_counter_from_id(self):

        #update manager counter
        if self.role == "manager" and self.id[0] == "m":
            number = int(self.id[1:])
            if number >= User.manager_count:
                User.manager_count = number + 1

        #update customer counter
        if self.role == "customer" and self.id[0] == "c":
            number = int(self.id[1:])
            if number >= User.customer_count:
                User.customer_count = number + 1


class Manager(User):
    def __init__(self, name, username, password, user_id=None):
        User.__init__(self, name, username, password, "manager", user_id)
        self.restaurant = None

    def add_menu_item(self, name, price, item_type):

        #create and add new item
        item = MenuItem(name, price, item_type)
        self.restaurant.menu.append(item)

    def remove_menu_item(self, item_key):
        item_to_remove = None

        #search item by id or name
        for i in self.restaurant.menu:
            name_lower = i.name.lower()
            key_lower = item_key.lower()

            if i.id == item_key or name_lower == key_lower:
                item_to_remove = i
                break

        #remove item if found
        if item_to_remove != None:
            self.restaurant.menu.remove(item_to_remove)

    def edit_menu_item_price(self, item_key, new_price):
        #find item and change its price
        for i in self.restaurant.menu:
            name_lower = i.name.lower()
            key_lower = item_key.lower()

            if i.id == item_key or name_lower == key_lower:
                i.price = new_price
                break

    def toggle_item(self, item_key):

        #find item and change availability
        for i in self.restaurant.menu:
            name_lower = i.name.lower()
            key_lower = item_key.lower()

            if i.id == item_key or name_lower == key_lower:
                if i.available == True:
                    i.available = False
                else:
                    i.available = True
                break


class Customer(User):
    def __init__(self, name, username, password, user_id=None):
        User.__init__(self, name, username, password, "customer", user_id)
        self.cart = [] #shopping cart
        self.orders = [] #customer orders

    def add_to_cart(self, item):
        #add item if available
        if item.available == True:
            self.cart.append(item)

    def remove_from_cart(self, item_key):
        #remove item from cart
        for i in self.cart:
            name_lower = i.name.lower()
            key_lower = item_key.lower()

            if i.id == item_key or name_lower == key_lower:
                self.cart.remove(i)
                break

    def finalize_order(self, restaurant):

        #create new order
        order = Order(self, restaurant)
        #add cart items to order
        for i in self.cart:
            order.add_item(i)
        #save order in restaurant and customer
        restaurant.orders.append(order)
        self.orders.append(order)
        #clear cart
        self.cart = []
        return order


class Restaurant:
    restaurant_counter = 1

    def __init__(self, name, manager_username, menu=None, orders=None, restaurant_id=None):
        self.name = name
        self.manager_username = manager_username


        #set menu list
        if menu == None:
            self.menu = []
        else:
            self.menu = menu

        #set orders list
        if orders == None:
            self.orders = []
        else:
            self.orders = orders
        #create restaurant id
        if restaurant_id == None:
            self.id = "R" + str(Restaurant.restaurant_counter)
            Restaurant.restaurant_counter = Restaurant.restaurant_counter + 1
        else:
            self.id = restaurant_id

            #update counter from existing id
            number = int(restaurant_id[1:])
            if number >= Restaurant.restaurant_counter:
                Restaurant.restaurant_counter = number + 1

    def menu_text(self):
        t = ""
        #check if menu is empty
        if len(self.menu) == 0:
            t = "Menu empty\n"

        #add each item info
        for i in self.menu:
            t = t + i.info() + "\n"

        return t

    def orders_text(self):
        t = ""
        #check if there are no orders
        if len(self.orders) == 0:
            t = "No orders\n"

        #add order text
        for o in self.orders:
            t = t + o.text()

        return t


class Platform:
    def __init__(self):
        self.users = []
        self.restaurants = []
        self.current_user = None
        self.load()

    def signup(self, name, username, password, role):
        if self.valid_name(name) == False:
            return False

        if self.valid_username(username) == False:
            return False

        #check if username already exists
        for u in self.users:
            if u.username == username:
                return False

        #create manager account
        if role == "manager":
            m = Manager(name, username, password)

            #create restaurant for manager
            r = Restaurant("Restaurant_" + username, m.username)

            m.restaurant = r

            self.users.append(m)
            self.restaurants.append(r)

            self.save()
            return True


        #create customer account
        if role == "customer":
            c = Customer(name, username, password)

            self.users.append(c)

            self.save()
            return True

        return False

    def login(self, username, password):

        for u in self.users:
            if u.username == username and u.password == password:
                self.current_user = u
                return True

        return False

    def valid_name(self, name):
        name = name.strip()

        if len(name) < 3:
            return False
        else:
            return True

    def valid_username(self, username):
        username = username.strip()

        if len(username) < 3:
            return False

        for ch in username:
            if ch == " ":
                return False

        return True

    def find_user(self, username):
        #search user by username
        for u in self.users:
            if u.username == username:
                return u

        return None

    def find_restaurant_by_id(self, restaurant_id):
        #search restaurant by id
        for r in self.restaurants:
            if r.id == restaurant_id:
                return r

        return None

    def save(self):
        data = {}

        data["users"] = []
        data["restaurants"] = []

        for u in self.users:
            user_data = {}
            user_data["id"] = u.id
            user_data["name"] = u.name
            user_data["username"] = u.username
            user_data["password"] = u.password
            user_data["role"] = u.role

            data["users"].append(user_data)
        for r in self.restaurants:
            menu_list = []

            for i in r.menu:
                item_data = {}
                item_data["id"] = i.id
                item_data["name"] = i.name
                item_data["price"] = i.price
                item_data["type"] = i.type
                item_data["available"] = i.available

                menu_list.append(item_data)

            orders_list = []

            for o in r.orders:
                items_list = []

                for it in o.items:
                    item_data = {}
                    item_data["id"] = it.id
                    item_data["name"] = it.name
                    item_data["price"] = it.price
                    item_data["type"] = it.type
                    item_data["available"] = it.available

                    items_list.append(item_data)

                #order information
                order_data = {}
                order_data["id"] = o.id
                order_data["customer_username"] = o.customer.username
                order_data["restaurant_id"] = r.id
                order_data["time"] = o.time
                order_data["items"] = items_list

                orders_list.append(order_data)

            #restaurant information
            restaurant_data = {}
            restaurant_data["id"] = r.id
            restaurant_data["name"] = r.name
            restaurant_data["manager_username"] = r.manager_username
            restaurant_data["menu"] = menu_list
            restaurant_data["orders"] = orders_list

            data["restaurants"].append(restaurant_data)


        #write data to json file
        f = open(DATA_FILE, "w")
        json.dump(data, f, indent=4)
        f.close()

    def load(self):
        if os.path.exists(DATA_FILE) == False:
            return

        #read json data
        f = open(DATA_FILE)
        data = json.load(f)
        f.close()

        self.users = []
        self.restaurants = []

        max_manager = 0
        max_customer = 0
        max_restaurant = 0
        max_item = 0
        max_order = 0

        #load users
        if "users" in data:
            for u in data["users"]:


                #create id if missing
                if "id" not in u:
                    if u["role"] == "manager":
                        u["id"] = "m" + str(max_manager + 1)
                    elif u["role"] == "customer":
                        u["id"] = "c" + str(max_customer + 1)

                #create manager object
                if u["role"] == "manager":
                    user = Manager(u["name"], u["username"], u["password"], u["id"])
                    self.users.append(user)

                    if user.id[0] == "m":
                        num = int(user.id[1:])
                        if num > max_manager:
                            max_manager = num

                #create customer object
                if u["role"] == "customer":
                    user = Customer(u["name"], u["username"], u["password"], u["id"])
                    self.users.append(user)

                    if user.id[0] == "c":
                        num = int(user.id[1:])
                        if num > max_customer:
                            max_customer = num

        #load restaurants 
        if "restaurants" in data:
            for r in data["restaurants"]:

                menu_list = []

                #get restaurant id if exists
                if "id" in r:
                    restaurant_id = r["id"]
                else:
                    restaurant_id = None


                #create restaurant object
                restaurant = Restaurant(r["name"], r["manager_username"], menu_list, [], restaurant_id)

                if restaurant.id[0] == "R":
                    num = int(restaurant.id[1:])
                    if num > max_restaurant:
                        max_restaurant = num

                #load menu item
                if "menu" in r:
                    for i in r["menu"]:

                        if "id" in i:
                            item_id = i["id"]
                        else:
                            item_id = None

                        item = MenuItem(i["name"], i["price"], i["type"], i["available"], item_id)
                        restaurant.menu.append(item)

                        if item.id[0] == "I":
                            num = int(item.id[1:])
                            if num > max_item:
                                max_item = num

                self.restaurants.append(restaurant)

            #load orders
            for r in data["restaurants"]:

                restaurant = self.find_restaurant_by_id(r["id"])

                if "orders" in r:
                    for o in r["orders"]:

                        customer = self.find_user(o["customer_username"])
                        items = []

                        for it in o["items"]:

                            if "id" in it:
                                item_id = it["id"]
                            else:
                                item_id = None

                            item = MenuItem(it["name"], it["price"], it["type"], it["available"], item_id)
                            items.append(item)

                            if item.id[0] == "I":
                                num = int(item.id[1:])
                                if num > max_item:
                                    max_item = num

                        if "id" in o:
                            order_id = o["id"]
                        else:
                            order_id = None

                        if "time" in o:
                            order_time = o["time"]
                        else:
                            order_time = None

                        #create order object
                        order = Order(customer, restaurant, items, order_id, order_time)
                        restaurant.orders.append(order)

                        if customer != None:
                            customer.orders.append(order)

                        if order.id[0] == "O":
                            num = int(order.id[1:])
                            if num > max_order:
                                max_order = num

                #connect manager to restaurant
                manager = self.find_user(r["manager_username"])

                if manager != None and manager.role == "manager":
                    manager.restaurant = restaurant

        User.manager_count = max_manager + 1
        User.customer_count = max_customer + 1
        Restaurant.restaurant_counter = max_restaurant + 1
        MenuItem.item_counter = max_item + 1
        Order.order_counter = max_order + 1


class App:
    def __init__(self):

        self.platform = Platform() #create platform object
       
        self.win = tk.Tk()
        self.win.title("Restaurant System")
        self.win.geometry("800x650")

        self.login_page()
        self.win.mainloop()

    def clear(self):
        #remove all widgets from window
        children = self.win.winfo_children()

        for w in children:
            w.destroy()

    def login_page(self):

        self.clear()


        #username label
        label1 = tk.Label(self.win, text="Username")
        label1.pack()

        self.username = tk.Entry(self.win)
        self.username.pack()

        #password label
        label2 = tk.Label(self.win, text="Password")
        label2.pack()

        self.password = tk.Entry(self.win)
        self.password.pack()

        self.message = tk.Label(self.win, text="", fg="red")
        self.message.pack()

        #login button
        btn1 = tk.Button(self.win, text="Login", command=self.login)
        btn1.pack()

        #signup manager button
        btn2 = tk.Button(self.win, text="Signup Manager", command=self.signup_manager)
        btn2.pack()


        #signup customer button
        btn3 = tk.Button(self.win, text="Signup Customer", command=self.signup_customer)
        btn3.pack()

    def login(self):
        username = self.username.get()
        password = self.password.get()

        ok = self.platform.login(username, password)

        if ok == True:
            role = self.platform.current_user.role

            if role == "manager":
                self.manager_page()
            else:
                self.customer_page()
        else:
            self.message.config(text="Invalid username or password")

    def signup_manager(self):
        name = self.username.get()
        username = self.username.get()
        password = self.password.get()

        ok = self.platform.signup(name, username, password, "manager")

        if ok == True:
            self.message.config(text="Manager signed up successfully")
        else:
            self.message.config(text="Signup failed")

    def signup_customer(self):
        name = self.username.get()
        username = self.username.get()
        password = self.password.get()

        ok = self.platform.signup(name, username, password, "customer")

        if ok == True:
            self.message.config(text="Customer signed up successfully")
        else:
            self.message.config(text="Signup failed")

    def manager_page(self):
        self.clear()

        m = self.platform.current_user

        label1 = tk.Label(self.win, text="Manager Panel")
        label1.pack()

        label2 = tk.Label(self.win, text="Restaurant: " + m.restaurant.name)
        label2.pack()

        #menu display box
        self.menu_box = tk.Text(self.win, height=16, width=90)
        self.menu_box.pack()

        self.refresh_manager_menu()

        label3 = tk.Label(self.win, text="Item ID or Name")
        label3.pack()
        self.item_key = tk.Entry(self.win)
        self.item_key.pack()

        label4 = tk.Label(self.win, text="Item Name")
        label4.pack()
        self.name = tk.Entry(self.win)
        self.name.pack()

        label5 = tk.Label(self.win, text="Price")
        label5.pack()
        self.price = tk.Entry(self.win)
        self.price.pack()

        label6 = tk.Label(self.win, text="Type (food/drink)")
        label6.pack()
        self.type = tk.Entry(self.win)
        self.type.pack()

        #action buttons
        btn1 = tk.Button(self.win, text="Add Item", command=self.add_item)
        btn1.pack()

        btn2 = tk.Button(self.win, text="Remove Item", command=self.remove_item)
        btn2.pack()

        btn3 = tk.Button(self.win, text="Edit Price", command=self.edit_price)
        btn3.pack()

        btn4 = tk.Button(self.win, text="Toggle Available", command=self.toggle_item)
        btn4.pack()


        btn5 = tk.Button(self.win, text="View Orders", command=self.view_orders_manager)
        btn5.pack()

        btn6 = tk.Button(self.win, text="Save", command=self.save_data)
        btn6.pack()


        btn7 = tk.Button(self.win, text="Logout", command=self.logout)
        btn7.pack()

    def refresh_manager_menu(self):
        m = self.platform.current_user
        self.menu_box.delete("1.0", tk.END)

        text = m.restaurant.menu_text()
        self.menu_box.insert(tk.END, text)

    def add_item(self):
        name = self.name.get()
        price_text = self.price.get()
        item_type = self.type.get()

        if name.strip() == "":
            return

        if price_text.isdigit() == False:
            return

        if item_type != "food":
            if item_type != "drink":
                return

        m = self.platform.current_user
        m.add_menu_item(name, int(price_text), item_type)

        self.refresh_manager_menu()
        self.platform.save()

    def remove_item(self):
        key = self.item_key.get()

        m = self.platform.current_user
        m.remove_menu_item(key)

        self.refresh_manager_menu()
        self.platform.save()

    def edit_price(self):
        key = self.item_key.get()
        price_text = self.price.get()

        if price_text.isdigit() == False:
            return

        m = self.platform.current_user
        m.edit_menu_item_price(key, int(price_text))

        self.refresh_manager_menu()
        self.platform.save()

    def toggle_item(self):
        key = self.item_key.get()

        m = self.platform.current_user
        m.toggle_item(key)

        self.refresh_manager_menu()
        self.platform.save()

    def view_orders_manager(self):
        self.clear()

        m = self.platform.current_user

        box = tk.Text(self.win, height=30, width=90)
        box.pack()

        text = m.restaurant.orders_text()
        box.insert(tk.END, text)

        btn1 = tk.Button(self.win, text="Back", command=self.manager_page)
        btn1.pack()

    def save_data(self):
        self.platform.save()

    def customer_page(self):
        self.clear()

        label1 = tk.Label(self.win, text="Customer Panel")
        label1.pack()
        label2 = tk.Label(self.win, text="Restaurants")
        label2.pack()
        
        #show restaurants
        for r in self.platform.restaurants:
            btn = tk.Button(self.win, text=r.name, command=lambda x=r: self.restaurant_page(x))
            btn.pack()

        btn1 = tk.Button(self.win, text="View My Orders", command=self.view_orders)
        btn1.pack()
        btn2 = tk.Button(self.win, text="Logout", command=self.logout)
        btn2.pack()

    def restaurant_page(self, restaurant):
        self.clear()

        self.current_restaurant = restaurant

        label1 = tk.Label(self.win, text=restaurant.name)
        label1.pack()

        self.menu_box = tk.Text(self.win, height=18, width=90)
        self.menu_box.pack()

        self.refresh_restaurant_menu()

        label2 = tk.Label(self.win, text="Item ID or Name")
        label2.pack()
        self.search = tk.Entry(self.win)
        self.search.pack()

        btn1 = tk.Button(self.win, text="Add To Cart", command=self.add_to_cart)
        btn1.pack()

        btn2 = tk.Button(self.win, text="Remove From Cart", command=self.remove_from_cart)
        btn2.pack()

        btn3 = tk.Button(self.win, text="View Cart", command=self.view_cart)
        btn3.pack()

        btn4 = tk.Button(self.win, text="Finalize Order", command=self.finalize_order)
        btn4.pack()

        btn5 = tk.Button(self.win, text="Back", command=self.customer_page)
        btn5.pack()

    def refresh_restaurant_menu(self):
        self.menu_box.delete("1.0", tk.END)

        text = self.current_restaurant.menu_text()
        self.menu_box.insert(tk.END, text)

    def add_to_cart(self):
        key = self.search.get()
        item = None

        for i in self.current_restaurant.menu:
            name_lower = i.name.lower()
            key_lower = key.lower()

            if i.id == key or name_lower == key_lower:
                item = i
                break

        if item != None:
            if item.available == True:
                self.platform.current_user.add_to_cart(item)

    def remove_from_cart(self):
        key = self.search.get()
        self.platform.current_user.remove_from_cart(key)

    def view_cart(self):
        self.menu_box.insert(tk.END, "\n--- CART ---\n")

        total = 0

        for i in self.platform.current_user.cart:
            self.menu_box.insert(tk.END, i.info() + "\n")
            total = total + i.price

        self.menu_box.insert(tk.END, "Cart Total: " + str(total) + "\n")

    def finalize_order(self):
        c = self.platform.current_user

        #check if cart is empty
        if len(c.cart) == 0:
            return

        order = c.finalize_order(self.current_restaurant)

        self.menu_box.insert(tk.END, "\nORDER CREATED\n")

        text = order.text()
        self.menu_box.insert(tk.END, text)

        self.platform.save()

    def view_orders(self):
        self.clear()

        c = self.platform.current_user

        box = tk.Text(self.win, height=30, width=90)
        box.pack()

        if len(c.orders) == 0:
            box.insert(tk.END, "No orders\n")

        for o in c.orders:
            text = o.text()
            box.insert(tk.END, text)

        btn = tk.Button(self.win, text="Back", command=self.customer_page)
        btn.pack()

    def logout(self):
        self.platform.current_user = None
        self.login_page()


App()
