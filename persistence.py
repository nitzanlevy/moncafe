import sqlite3
import atexit


class Employee(object):

    def __init__(self, _id, _name, _salary, _coffee_stand):
        self.id = _id
        self.name = _name
        self.salary = _salary
        self.coffee_stand = _coffee_stand


class Supplier(object):

    def __init__(self, _id, _name, _contact_information):
        self.id = _id
        self.name = _name
        self.contact_information = _contact_information


class Product(object):

    def __init__(self, _id, _description, _price, _quantity):
        self.id = _id
        self.description = _description
        self.price = _price
        self.quantity = _quantity


class CoffeeStand(object):

    def __init__(self, _id, _location, _number_of_employees):
        self.id = _id
        self.location = _location
        self.number_of_employees = _number_of_employees


class Activity(object):
    def __init__(self, _product_id, _quantity, _activator_id, _date):
        self.product_id = _product_id
        self.quantity = _quantity
        self.activator_id = _activator_id
        self.date = _date


class Employees(object):
    def __init__(self, _conn):
        self.conn = _conn

    def insert(self, employee):
        self.conn.execute("INSERT INTO Employees (id, name, salary, coffee_stand) VALUES"
                          "(?, ?, ?, ?)", [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def find(self, emp_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Employees WHERE id = ? ", [emp_id])
        return Employee(*c.fetchone())


class Suppliers(object):
    def __init__(self, _conn):
        self.conn = _conn

    def insert(self, supplier):
        self.conn.execute("INSERT INTO Suppliers (id, name, contact_information) VALUES"
                          "(?, ?, ?)", [supplier.id, supplier.name, supplier.contact_information])

    def find(self, sup_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Suppliers WHERE id = ? ", [sup_id])
        return Supplier(*c.fetchone())


class Products(object):
    def __init__(self, _conn):
        self.conn = _conn

    def insert(self, product):
        self.conn.execute("INSERT INTO Products (id, description, price, quantity) VALUES"
                          "(?, ?, ?, ?)", [product.id, product.description, product.price, product.quantity])

    def find(self, prod_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Products WHERE id = ? ", [prod_id])
        return Product(*c.fetchone())


class CoffeeStands(object):
    def __init__(self, _conn):
        self.conn = _conn

    def insert(self, coffee_stand):
        self.conn.execute("INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES"
                          "(?, ?, ?)", [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def find(self, cof_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Coffee_stands WHERE id = ? ", [cof_id])
        return CoffeeStand(*c.fetchone())


class Activities(object):
    def __init__(self, _conn):
        self.conn = _conn

    def insert(self, activity):
        self.conn.execute("INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES"
                          "(?, ?, ?, ?)",
                          [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def find(self, act_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Activities WHERE id = ? ", [act_id])
        return Activity(*c.fetchone())


class Repository(object):
    def __init__(self):
        self.conn = sqlite3.connect('moncafe.db')
        self.employees = Employees(self.conn)
        self.suppliers = Suppliers(self.conn)
        self.products = Products(self.conn)
        self.coffee_stands = CoffeeStands(self.conn)
        self.activities = Activities(self.conn)

    def execute_activity(self, activity):
        product = self.products.find(activity.product_id)
        activity_quantity = int(activity.quantity)
        actual_quantity = int(product.quantity)
        if activity_quantity < 0:
            sell = abs(activity_quantity)
            if actual_quantity >= sell:
                product.quantity = str(actual_quantity - sell)
                self.products.conn.execute("UPDATE Products SET quantity = ? WHERE id = ?",
                                           [product.quantity, product.id])
        elif activity_quantity > 0:
            product.quantity = str(actual_quantity + activity_quantity)
            self.products.conn.execute("UPDATE Products SET quantity = ? WHERE id = ?",
                                       [product.quantity, product.id])

    def close_db(self):
        self.conn.commit()
        self.conn.close()

    def select_all_from(self, table_name):
        return self.conn.cursor().execute("SELECT * FROM %s" % table_name)

    def get_tables_name(self):
        return self.conn.cursor().execute("SELECT name FROM sqlite_master WHERE type='table' ")

    def select_by_date(self, table_name):
        return self.conn.cursor().execute("SELECT * FROM %s ORDER BY date" % table_name)

    def select_by_id(self, table_name):
        return self.conn.cursor().execute("SELECT * FROM %s ORDER BY id" % table_name)

    def get_employee_report(self):
        return self.conn.cursor().execute("""
                SELECT Employees.name, Employees.salary, Coffee_stands.location
                ,(SELECT (sum(abs(Activities.quantity)) * (SELECT Products.price
                FROM Products WHERE Products.id=Activities.Product_id))
                FROM Activities WHERE Activities.activator_id==Employees.id)
                FROM Employees,Coffee_stands
                WHERE Employees.coffee_stand=Coffee_stands.id
                ORDER BY Employees.name
            """)

    def get_activity_report(self):
        return self.conn.cursor().execute(""" 
                            SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name
                            FROM Activities
                            INNER JOIN Products on Products.id = Activities.Product_id
                            LEFT JOIN Employees on Employees.id = Activities.activator_id
                            LEFT JOIN Suppliers
                            on Suppliers.id = Activities.activator_id ORDER BY Activities.date
                           """)

    def create_tables(self):
        self.conn.execute("DROP TABLE IF EXISTS Employees")
        self.conn.execute("DROP TABLE IF EXISTS Suppliers")
        self.conn.execute("DROP TABLE IF EXISTS Products")
        self.conn.execute("DROP TABLE IF EXISTS Coffee_stands")
        self.conn.execute("DROP TABLE IF EXISTS Activities")
        self.conn.executescript("""
        CREATE TABLE Coffee_stands (
            id INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            number_of_employees INTEGER
        );

        CREATE TABLE Employees (
            id	INTEGER,
            name	TEXT NOT NULL,
            salary	REAL NOT NULL,
            coffee_stand	INTEGER,
            PRIMARY KEY(id),
            FOREIGN KEY(coffee_stand) REFERENCES Coffee_stands(id)
        );

        CREATE TABLE Suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_information TEXT
        );

        CREATE TABLE Products (
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        );

        CREATE TABLE Activities (
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            activator_id INTEGER NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY(product_id) REFERENCES Products(id)
        );
        """)


repo = Repository()
atexit.register(repo.close_db)
