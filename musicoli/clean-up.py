with open('datas/all_genre.txt', 'r') as f:
    raw = f.readlines()
    cor = []
    for l in raw:
        l = l.split( ' (' )[0]
        if len(l)>2:
            print(l)
            cor.append(l)
        
    
with open('datas/all_genre2.txt', 'w') as file:
    file.write(''.join(cor))