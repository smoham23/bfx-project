#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector
import sys

def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('term')

    conn = mysql.connector.connect(user='smoham23', password='530247Sql', host='localhost', database='smoham23_chado')
    cursor = conn.cursor()

    qry = """
          SELECT drug_name
            FROM drug_names
           WHERE drug_name LIKE %s
           LIMIT 8
    """
    cursor.execute(qry, ('%' + str(term) + '%', ))

    print("Ran this query: {0}".format(cursor.statement), file=sys.stderr)

    drug_results = []
    for (drug_name) in cursor:
        drug_results.append({'value': drug_name, 'label': drug_name})

    conn.close()

    print(json.dumps(drug_results))


if __name__ == '__main__':
    main()
