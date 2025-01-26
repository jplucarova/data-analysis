#!/usr/bin/env python3
from sqlalchemy import create_engine, text

# Connect to the SQLite database
engine = create_engine('sqlite:///data.db')

# Use a connection to interact with the database
with engine.connect() as connection:

    # Query 1: Count distinct IDs in data_pacienti
    query1 = text("SELECT COUNT(DISTINCT id) FROM 'data_pacienti'")
    result1 = connection.execute(query1)

    # Print the result for data_pacienti
    for row in result1:
        print("Různá ID v data_pacienti:", row[0])

    # Query 2: Count distinct IDs in data_lecba
    query2= text("SELECT COUNT(DISTINCT id) FROM 'data_lecba'")
    result2 = connection.execute(query2)

    # Print the query results
    for row in result2:
        print("Různá ID v data_lecba:", row[0])
        pacients = row[0]

    # Query3 : Count distinct IDs in data_pacienti
    query3 = text("SELECT COUNT(id) FROM 'data_neutropenie'")
    result3 = connection.execute(query3)

    # Print the result for data_pacienti
    for row in result3:
        print("Různá ID v data_neutropenie:", row[0])
        neutr = row[0]

i = neutr / pacients
print ("Incidence neutropenie:", i)
i_p = i * 100
print ("Incidence neutropenie v procentech:", i_p, "%")
