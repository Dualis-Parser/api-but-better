from bs4 import BeautifulSoup


def get_navigation(html):
    """
    Get the navigation links and names from a html page

    :param html: the complete html page
    :type html: str

    :return: the resulting links
    :rtype: dict
    """

    soup = BeautifulSoup(html, 'lxml')
    for li in soup.find(id="pageTopNavi").find_all('li'):
        yield li["title"], li.find_all('a')[0]["href"]


def parse_semesters(html):
    """
    Get all semesters in the exams html page

    :param html: the exams html page
    :type html: str

    :return: the semesters except of the current
    :rtype dict
    """
    soup = BeautifulSoup(html, 'lxml')

    semester_select = soup.find(id="semester")
    current_semester = semester_select.find("option", attrs={"selected": "selected"})
    yield current_semester.text.strip(), '-N' + current_semester["value"]

    for option in semester_select.find_all("option"):
        if (option.get("selected") != "selected"):
            yield option.text.strip(), '-N' + option["value"]