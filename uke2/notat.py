notater = [
    {'tittel': 'test', 'tekst': 'Et kjempefint nytt notat'}
]

def get_notater():
    return notater

def add_notat(tittel, tekst):
    notater.append({'tittel': tittel, 'tekst': tekst})

if __name__ == "__main__":
   print(get_notater())
   add_notat('Et nytt notat', 'et nytt fint notat er her')
   print(get_notater()) 