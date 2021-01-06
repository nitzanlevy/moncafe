from persistence import repo


def print_db():
    tables = repo.get_tables_name()
    tables = tables.fetchall()
    tables.sort()
    for table_name in tables:
        if table_name[0] == "Activities":
            output = repo.select_by_date(table_name[0])
        else:
            output = repo.select_by_id(table_name[0])
        if output:
            first = output.fetchone()
            if first is not None:
                print(table_name[0] + ":")
                print(first)
        for row in output:
            print(row)
    # print here employee report
    print("Employees report: ")
    for row in repo.get_employee_report():
        temp = list(row)
        if temp[3] is None:
            temp[3] = 0
        print(tuple(temp))
    # now printing activities report
    activity_repo = repo.get_activity_report()
    if activity_repo:
        first = activity_repo.fetchone()
        if first is not None:
            print("Activities: ")
            print(first)
        for row in activity_repo:
            print(row)


print_db()
