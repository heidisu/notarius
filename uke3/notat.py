notater = [
    {'tittel': 'test', 'tekst': 'Et kjempefint nytt notat'}
]

def get_notater(db):
    return db.execute(
        'SELECT id, tittel, tekst, created'
        ' FROM notat'
        ' ORDER BY created DESC'
    ).fetchall()


def add_notat(db, tittel, tekst):
    db.execute(
                'INSERT INTO notat (tittel, tekst)'
                ' VALUES (?, ?)',
                (tittel, tekst)
            )
    db.commit()
