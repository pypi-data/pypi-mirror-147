import os
import re

from structure import Structure


def find_table_names_from_sql(sql_expression: str, filename: str) -> tuple:
    """
    Find table names in string and return table name and parents name.
    :param sql_expression: text of sql expression
    :param filename: name of a file in witch sql expression is stored
    :return: table_name: name of a table will be created
    :return: parents_names: name of tables that a used to create new table
    """
    string = ''

    for line in re.split('\n', sql_expression):
        line = re.sub('[ \t]+$', '', line, )
        line = re.split('//', line)[0]
        line = re.split('--', line)[0]
        line = re.split('#', line)[0]
        line = re.sub('\(', ' ( ', line)
        line = re.sub('\)', ' ) ', line)
        line = re.sub(r"\s+,", ",", line, flags=re.UNICODE)
        string += ' ' + line

    string = string.lower()

    while string.find('/*') > -1 and string.find('*/') > -1:
        l_multi_line = string.find('/*')
        r_multi_line = string.find('*/')
        string = string[:l_multi_line] + string[r_multi_line + 2:]

    try:
        p = r'create table(.*?)as select'
        table_name = re.search(p, string).group(1).strip()
    except AttributeError:
        error_msg = 'Check for matching query pattern: CREATE TABLE ... AS SELECT... in file {}'.format(filename)
        raise AttributeError(error_msg)

    words = string.split()
    parents_names = find_parents_names(words)

    return table_name, parents_names


def find_parents_names(words: list) -> list:
    """
    Find tables that a used to create a new table.
    :param words: cleaned sql expression in list format
    :return: list of parent tables
    """
    parents_names = list()
    previous_word = None
    for word in words:
        if previous_word == 'from' or\
                len(parents_names) > 0\
                and parents_names[-1][-1] == ','\
                or previous_word == 'join':
            if word != '(':
                parents_names.append(word)
        previous_word = word

    parents_names = [parent.replace(',', '') for parent in parents_names]
    return sorted(parents_names)


def analyze(dir: str) -> Structure:
    """
    Analyze sql expressions and build dependencies graph.
    :param dir: directory with sql expressions
    :return: structure of a graph describing sql dependencies
    """

    structure = Structure()
    for file in os.listdir(dir):
        with open(dir + file, 'r') as f:
            sql_expression = f.read()

        table_name, parents_names = find_table_names_from_sql(sql_expression, file)
        structure.add_vertex(table_name)
        for parent in parents_names:
            structure.add_vertex(parent)
            structure.add_edge(table_name, parent)

    return structure
