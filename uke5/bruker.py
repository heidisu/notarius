def get_bruker(db, brukernavn):
    return db.execute(""" 
        SELECT brukernavn, passord
        FROM bruker
        WHERE brukernavn = ?
    """, (brukernavn,)).fetchone()

def create_bruker(db, brukernavn, passord):
    db.execute(""" 
        INSERT INTO bruker(brukernavn, passord) values(?, ?)
    """, (brukernavn, passord))
    db.commit()