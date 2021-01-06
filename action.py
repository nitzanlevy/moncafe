import sys
from persistence import repo, Activity


def act_command(line):
    prod_id = line[0]
    quantity = line[1]
    sup_id = line[2]
    date = line[3]
    activity = Activity(prod_id, quantity, sup_id, date)
    repo.activities.insert(activity)
    repo.execute_activity(activity)


def act():
    with open(sys.argv[1]) as config_file:
        for line in config_file:
            act_command(line.split(", "))


def print_db():
    tables = repo.get_tables_name()
    tables = tables.fetchall()
    tables.sort()
    for table_name in tables:
        output = repo.select_all_from(table_name[0])
        print(table_name[0]+":")
        for row in output:
            print(row)


act()
print_db()
