from bs4 import BeautifulSoup

from utils import constants


def parse_users_name(html):
    """
    Parse the name of the logged in user from any html after the login process

    :param html: the html
    :type html: str

    :return: the name
    :rtype: str
    """
    soup = BeautifulSoup(html, 'lxml')
    return soup.find(id="loginDataName").text.split("Name:")[-1].strip()


def parse_users_modules(semester_html):
    """
    parse the modules from the modules html file

    :param semester_html: the html strings for all semesters
    :type semester_html: dict

    :return: the modules
    :rtype: list
    """
    modules = list()

    for semester, html in semester_html.items():
        soup = BeautifulSoup(html, 'lxml')
        # find the table with the modules
        for tr in soup.find_all('table', class_='nb list')[0].select('tbody tr'):
            try:
                # parse the module data
                module = parse_row_module(tr)
                module["semesters"] = semester

                # avoid duplicates if a module is present in multiple semesters
                if (len(list(filter(lambda mod: mod["module_no"] == module["module_no"], modules))) == 0):
                    modules.append(module)
                else:
                    list(filter(lambda mod: mod["module_no"] == module["module_no"], modules))[0][
                        "semesters"] += ", " + semester
            except IndexError:
                # not fatal, just means that the table row doesn't represent a module
                pass

    return modules


def parse_row_module(row):
    """
    Parse the module from a table row

    :param row: the table row
    :type row: bs4.element.Tag

    :return: the module
    :rtype: dict
    """
    module = constants.MODULE_DATA.copy()
    module["module_no"] = row.find_all('td')[0].text.strip()
    module["module_name"] = row.find_all('td')[1].text.strip()
    module["final_grade"] = row.find_all('td')[2].text.strip().replace(",", ".")
    module["credits"] = row.find_all('td')[3].text.strip()
    module["passed"] = row.find_all('td')[5].text.strip() == "bestanden"

    # parse the exams url
    s = row.find_all('script')[0].text
    module["exams_url"] = s.split('dl_popUp("')[1].split('"')[0]

    return module
