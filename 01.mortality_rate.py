#!/usr/bin/env python3
from sqlalchemy import create_engine, text

# Connect to the SQLite database
engine = create_engine('sqlite:///data.db')

# Use a connection to interact with the database
with engine.connect() as connection:

    drop_view_query = text("DROP VIEW IF EXISTS joint_table;")
    connection.execute(drop_view_query)

    # Create a view that joins data_pacienti and data_lecba
    create_view_query = text(
    """
    CREATE VIEW joint_table AS
    SELECT p.id, p.datum_umrti, MAX(l.datum_aplikace) AS posledni_aplikace
    FROM data_pacienti p
    JOIN
        data_lecba l
    ON
        p.id = l.id
    WHERE p.datum_umrti IS NOT NULL
    GROUP BY p.id;
    ---LIMIT 10
        """)

    connection.execute(create_view_query)
    #print("view created")

    query2 = text("""
    SELECT COUNT(*)
    FROM joint_table
    WHERE JULIANDAY(datum_umrti) - JULIANDAY(posledni_aplikace) <= 30
          AND posledni_aplikace <= '2022-11-30' --filter patients that received treatment in the last 30 days of the time-frame
    --LIMIT 10
    """)
    result2 = connection.execute(query2)
    # Print the results
    for row in result2:
        print("Pacienti zemřelí během 30 dní po poslední aplikaci léčby:", row[0])
        dead = row[0]

    #overwrite the view if exists
    drop_view_query2 = text("DROP VIEW IF EXISTS leceni_pacienti;")
    connection.execute(drop_view_query2)

    # Create a view that contains the IDs of patients and the date of their last treatment
    create_view_query2 = text(
    """
    CREATE VIEW leceni_pacienti AS
    SELECT id, MAX(datum_aplikace) AS posledni_aplikace
    FROM data_lecba
    GROUP BY id;
        """)
    connection.execute(create_view_query2)
    #print("view created")

    query3 = text("""
    SELECT COUNT(*)
    FROM leceni_pacienti
    WHERE posledni_aplikace <= '2022-11-30'  --filter patients that received treatment in the last 30 days of the time-frame
    --LIMIT 10
    """)
    result3 = connection.execute(query3)

    # Print the results
    for row in result3:
        print("Všichni léčení pacienti:", row[0])
        all_treated = row[0]

    i = dead / all_treated
    print (f"30denní mortalita: {i:.4}")
    i_p = i * 100
    print (f"30denní mortalita: {i_p:.2f} %")
