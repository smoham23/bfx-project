#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector
import cgitb
cgitb.enable()

def main():
    print("Content-Type: applications/json\n\n")


    form = cgi.FieldStorage()
    val1 = form.getvalue('input_drug1')
    val2 = form.getvalue('input_drug2')
    values = [val1, val2]
    drug_results1 = {'drug1': '', 'count1': 0, 'drugs1': list(), 'drug2': '', 'count2': 0, 'drugs2': list(), 'check': '' }
    ID_1 = ''
    ID_2 = ''

    conn = mysql.connector.connect(user="smoham23", password="530247Sql", host="localhost", database="smoham23_chado")

    for val in values:
        drug = list()
        if val == val1:
            ID_1 = val
        if val == val2:
            ID_2 = val
        # the cursor object allows you to issue commands
        curs1 = conn.cursor()

        qry1 = "SELECT n.drug_id FROM drug_names n WHERE n.drug_name LIKE %s"
        curs1.execute(qry1, (str(val), ))

        for i in curs1:
            ID = i[0]
        curs1.close()

        curs2 = conn.cursor()

        qry2 = "SELECT i.drug_2 FROM drug_interactions i WHERE i.drug_1 LIKE %s"

        curs2.execute(qry2, (ID, ))

        for line in curs2:
            drug.append(line[0])

        curs2.close()

        curs3 = conn.cursor()

        qry3 = "SELECT i.drug_1 FROM drug_interactions i WHERE i.drug_2 LIKE %s"

        curs3.execute(qry3, (ID, ))

        for line in curs3:
            drug.append(line[0])

        curs3.close()

        curs4 = conn.cursor()

        qry4 = "SELECT n.drug_name FROM drug_names n WHERE n.drug_id LIKE %s"
        for i in range(len(drug)):
            curs4.execute(qry4, (drug[i], ))
            for drug_name in curs4:
                if val == val1:
                    drug_results1['drugs1'].append({'value': drug_name})
                    drug_results1['count1'] += 1
                    drug_results1['drug1'] = val
                else:
                    drug_results1['drugs2'].append({'value': drug_name})
                    drug_results1['count2'] += 1
                    drug_results1['drug2'] = val
        curs4.close()

    curs = conn.cursor()
    qry = "SELECT i.drug_1 FROM drug_interactions i WHERE (i.drug_1 = %s AND i.drug_2 = %s) OR (i.drug_2 = %s AND i.drug_1 = %s)"
    curs.execute(qry, [ID_1, ID_2, ID_1, ID_2])
    if curs.rowcount > 0:
        drug_results1['check'] = "Drug-drug interaction was found!"
    else:
        drug_results1['check'] = "No interactions were found!" 
    
    conn.close()

    print(json.dumps(drug_results1))


if __name__ == '__main__':
    main()

