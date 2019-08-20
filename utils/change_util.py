import json

from database.mysql_connection import MySQL


def check_for_change(modules, username):
    mysql = MySQL()
    stored_modules = mysql.query("SELECT * FROM new_module WHERE user = ?", [username, ])

    for module in modules:
        compare_to = list(filter(lambda mod: mod[1] == module["module_no"], stored_modules))
        if (len(compare_to) == 0):
            # module new
            module["updated"] = True
        else:
            compare_to = json.loads(compare_to[0][4])
            grades = module["grades"]

            module["updated"] = compare_to != grades
