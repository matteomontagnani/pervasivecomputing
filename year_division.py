year = 2006
with open('{}.txt'.format(year), 'a') as the_file:
    # leggi il file
    file = open('data.txt', 'r')
    # ottieni le righe
    lines = file.readlines()
    # per ogni riga
    for l in lines:
        # pulisci gli spazi bianchi
        data = l.strip()
        # se la riga fa parte di quell'anno inseriscila
        if int(data.split(",")[5]) == year:
            the_file.write(l)
        else:
            continue

        