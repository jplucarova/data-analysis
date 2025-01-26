#!/usr/bin/env python3
from sqlalchemy import create_engine, text

# Connect to the SQLite database
engine = create_engine('sqlite:///data.db')

# Use a connection to interact with the database
with engine.connect() as connection:
    # View1: Remove the view if exists
    drop_view_query1 = text("DROP VIEW IF EXISTS joint_table;")
    connection.execute(drop_view_query1)

    # Create a view that joins data_pacienti and data_lecba
    create_view_query1 = text("""
    CREATE VIEW joint_table AS
    SELECT p.id, p.datum_umrti, MAX(l.datum_aplikace) AS posledni_aplikace
    FROM data_pacienti p
    JOIN data_lecba l ON p.id = l.id
    WHERE p.datum_umrti IS NOT NULL
    GROUP BY p.id;
    """)
    connection.execute(create_view_query1)

    # Query 1: Count the number of patients that died within 30 days after their last treatment
    query1 = text("""
    SELECT COUNT(*)
    FROM joint_table
    WHERE JULIANDAY(datum_umrti) - JULIANDAY(posledni_aplikace) <= 30
          AND posledni_aplikace <= '2022-11-30' --filter patients that received treatment in the last month of the time-frame
    """)
    result2 = connection.execute(query1)

    # Print the results
    for row in result2:
        print("Pacienti zemřelí během 30 dní po poslední aplikaci léčby:", row[0])
        dead = row[0]

    # View 2: Remove the view if exists
    drop_view_query2 = text("DROP VIEW IF EXISTS leceni_pacienti;")
    connection.execute(drop_view_query2)

    # Create a view that contains the IDs of patients and the date of their last treatment
    create_view_query2 = text("""
    CREATE VIEW leceni_pacienti AS
    SELECT id, MAX(datum_aplikace) AS posledni_aplikace
    FROM data_lecba
    GROUP BY id;
    """)
    connection.execute(create_view_query2)

    # Query 2: Count all patients that received treatment (without the last month of the time-frame)
    query2 = text("""
    SELECT COUNT(*)
    FROM leceni_pacienti
    --filter patients that received treatment in the last month of the time-frame
    --(might include patients that will die within 30 days after the last treatment, but after the end of the time-frame)
    WHERE posledni_aplikace <= '2022-11-30'
    """)
    result3 = connection.execute(query2)

    # Print the results
    for row in result3:
        print("Všichni léčení pacienti:", row[0])
        all_treated = row[0]

    # Calculate the 30-day mortality rate
    i = dead / all_treated
    print (f"30denní mortalita: {i:.4}")
    i_p = i * 100
    print (f"30denní mortalita: {i_p:.2f} %")
