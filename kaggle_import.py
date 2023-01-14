import csv
import decimal
import psycopg2

username = 'postgres'
password = '0000'
database = 'postgres'
host = 'localhost'
port = '5432'

INPUT_CSV_FILE = 'drivers.csv'

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    with open(INPUT_CSV_FILE, 'r') as inf:
        reader = csv.DictReader(inf)
        for idx, row in enumerate(reader):
            list_id = cur.fetchone();
            if list_id is None:
                
                price = decimal.Decimal(row['unit_price'].lstrip('$'));
                values = (row['driverId'], row['driverRef'], row['number'], row['code'], row['forename'],row['surname'], row['dob'], row['nationality'], row['url']);
                cur.execute('INSERT INTO drivers(driverId, driverRef, number, code, forename, surname, dob, nationality, url) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s', values);

    conn.commit()

