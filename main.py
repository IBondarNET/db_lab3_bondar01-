import psycopg2
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


username = 'postgres'
password = 'password'
database = 'postgres'
host = 'localhost'
port = '5432'

query_1 = '''
create view DriverLaps as
select d."driverRef", sum(r."laps") from drivers d
left join results r on d."driverId" = r."driverId"
GROUP by d."driverRef"
order by sum(r."laps") desc
limit 50;
'''

query_2 = '''
create view DriverPosition as
select d."driverRef", count(r."position") from drivers d
left join results r on d."driverId" = r."driverId"
where r."position" = 1
GROUP by d."driverRef"
order by count(r."laps") desc
limit 50;
'''

query_3 = '''
create view DriverFastestSpeed as
select age(to_date(d."dob",'DD/MM/YYYY')) , max(CAST(r."fastestLapSpeed" as float)) from drivers d
left join results r on r."driverId" = d."driverId"
where r."fastestLapSpeed" != 0
GROUP by d."dob" 
order by max(CAST(r."fastestLapSpeed" as float)) desc
limit 50;
'''



conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()
    cur.execute('DROP VIEW IF EXISTS DriverLaps')
    cur.execute(query_1)
    cur.execute('SELECT * FROM DriverLaps')
    names = []
    laps = []
    for row in cur:
        names.append(row[0])
        laps.append(row[1])
    x_range = range(len(names))

    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)
    bar = bar_ax.bar(x_range, laps, label='Total')
    bar_ax.set_xlabel('Ім`я')
    bar_ax.set_ylabel('Кількість кругів')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(names)

    cur.execute('DROP VIEW IF EXISTS DriverPosition')
    cur.execute(query_2)
    cur.execute('SELECT * FROM DriverPosition')
    item_name = []
    item_quantity = []
    for row in cur:
        item_name.append(row[0])
        item_quantity.append(row[1])
    pie_ax.pie(item_quantity, labels=item_name, autopct='%1.1f%%')
    pie_ax.set_title('Частка замовлень кожної піци')

    cur.execute('DROP VIEW IF EXISTS DriverFastestSpeed')
    cur.execute(query_3)
    cur.execute('SELECT * FROM DriverFastestSpeed')
    age = []
    time = []
    for row in cur:
        age.append(row[1])
        time.append(row[0])    
    graph_ax.plot( age,list(map(lambda x: x.total_seconds(), time)))
    graph_ax.set_xlabel('Вік')
    graph_ax.set_ylabel('Максимальна швидкість')
    graph_ax.set_title('Графік максимальної швидкості від віку')

    graph_ax = plt.figure().gca()
    graph_ax.xaxis.set_major_locator(MaxNLocator())


    # for qnt, price in zip(age, time):
    #     graph_ax.annotate(price, xy=(qnt, price), xytext=(7, 2), textcoords='offset points')

    mng = plt.get_current_fig_manager()
    mng.resize(1400, 600)
    plt.show()