from persistence import repo, CoffeeStand, Supplier, Employee, Product
import sys


def insert_command(command):
    command = command.rstrip('\n')
    line = command.split(", ")
    if line[0] == 'C':
        repo.coffee_stands.insert(CoffeeStand(line[1], line[2], line[3]))
    elif line[0] == 'S':
        repo.suppliers.insert(Supplier(line[1], line[2], line[3]))
    elif line[0] == 'E':
        repo.employees.insert(Employee(line[1], line[2], line[3], line[4]))
    elif line[0] == 'P':
        repo.products.insert(Product(line[1], line[2], line[3], 0))


def initiate():
    repo.create_tables()
    with open(sys.argv[1]) as config_file:
        for line in config_file:
            insert_command(line)


initiate()
