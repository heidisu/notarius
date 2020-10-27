notater = [
    {'tittel': 'test', 'tekst': 'Et kjempefint nytt notat'}
]

def get_notater(db):
    return db.execute(
        'SELECT id, tittel, tekst, created'
        ' FROM notat'
        ' ORDER BY created DESC'
    ).fetchall()

def get_notat(db, id):
    return db.execute(
       """ 
        SELECT id, tittel, tekst, created
        FROM notat
        WHERE id = ?
       """, (id,) 
    ).fetchone()

def add_notat(db, tittel, tekst):
    db.execute(
                'INSERT INTO notat (tittel, tekst)'
                ' VALUES (?, ?)',
                (tittel, tekst)
            )
    db.commit()

def update_notat(db, id, tittel, tekst):
    db.execute(""" 
        UPDATE notat SET tittel = ?, tekst = ?
        WHERE id = ?
    """, (tittel, tekst, id))
    db.commit()

def delete_notat(db, id):
    db.execute(""" 
        DELETE FROM notat WHERE id = ?
    """, (id,))
    db.commit()