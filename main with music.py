import requests
import re
import matplotlib.pyplot as plt
import pygame

def graf_nagrade(imena_filmov, leto1, leto2):
    nagrajeni = []
    nominirani = []
    
    for film in imena_filmov:
        leto = film.get_leto()
        if leto >= leto1 and leto <= leto2:
            if film.get_nominacije() > 0 and film.get_poraba()!= '-':
                nominirani.append((film, int(film.get_poraba())))
    
    nominirani = sorted(nominirani, key = lambda x: x[1], reverse = True)
    X = [x[1] for x in nominirani]
    Y1 = [x[0].get_nominacije() for x in nominirani]
    Y2 = [x[0].get_nagrade() for x in nominirani]
    
    
    fig, ax = plt.subplots()

    # Plot the line graph with only some y points displayed
    ax.scatter(X, [Y2[i] if Y2[i]!= 0 else None for i in range(len(Y2))], c = 'b', s = 2, marker = '*', label = 'Število oskarjev')
    ax.scatter(X, Y1, c = 'r', s = 1, label = 'Število nominacij')
#     ax.scatter(Y1, X, c = 'r', s = 0.4)

    
    # Set the x and y axis labels
    ax.set_xlabel('Poraba filma')
    ax.set_ylabel("Število nominacij/nagrad")

    
    plt.legend(loc='upper right')

    # Show the plot
    plt.show()
        
        
    

def n_najdrazjih(n, imena_filmov):
    '''naredi nam tabelo n filmov ki so imeli najvecji buget'''
    
    tab = []
    
    for film in imena_filmov:
        if film.get_poraba() != '-':
            if film.get_zasluzek() != '-':
                tab.append((film.get_ime(), film.get_poraba(), film.get_zasluzek(), film.get_leto()))
            else:
                tab.append((film.get_ime(), film.get_poraba(), 0 ,film.get_leto()))
                
    text_buget = 'Ime filma                                                              |  Poraba filma  |  Leto\n\n'
    tab2 = sorted(tab, key=lambda x: x[1], reverse=True)
    
    for i in range(n):
        elt = tab2[i]
        text_buget += f'{elt[0].upper():70} | {elt[1]:14} | {elt[3]:5}\n'
    
    text_zasluzek = 'Ime filma                                                              | Zasluzek filma |  Leto\n\n'
    tab3 = sorted(tab, key=lambda x: x[2], reverse=True)
    
    for i in range(n):
        elt = tab3[i]
        text_zasluzek += f'{elt[0].upper():70} | {elt[2]:14} | {elt[3]:5}\n'
    
    return [text_buget, text_zasluzek]
    
    

def rotten_tomatoes(ime_filma):
    ime = ime_filma.lower().replace(' ', '_').replace('&','and').replace('-','_')
    ime = re.sub('[:.,!?()\'\]\[+=%$"/\\<>]', '', ime)
    #dej stran svopicnja in take stvari
    # & spremeni u end
    web = 'https://www.rottentomatoes.com/m/' + ime
    
    req = requests.get(web)
    text = req.text
#     text = re.split('</score-icon-audience>',text)
#     print(text[0])
    audience_score = str(re.findall('audiencescore="\d+"',text))
    tomatometer_score = str(re.findall('tomatometerscore="\d+"',text))
    audience = re.findall('\d+',audience_score)
    tomatometer = re.findall('\d+',tomatometer_score)
    if len(audience) > 0:
        a = int(audience[0])
    else:
        a = '-'
    if len(tomatometer) > 0:
        t = int(tomatometer[0])
    else:
        t = '-'
    return [a,t]


def tabelica_ocen(leto, imena_filmov):
    '''naredi tabelo filmov in njihovih ocen'''
    
    filmovi = []
    
    for film in imena_filmov:
        if film.get_leto() == leto:
            filmovi.append(film)

    
    text = 'Filmovi iz leta ' + str(leto) +':\n\n'
    
    for film in filmovi:
        #{rotten_tomatoes(film.get_ime())[0]} | {rotten_tomatoes(film.get_ime())[1]} 
        text += f'{film.get_ime().upper():70} | {rotten_tomatoes(film.get_ime())[0]:5} | {rotten_tomatoes(film.get_ime())[1]:5} | {film.get_poraba():10} | {film.get_zasluzek():10} \n'
        
    return text
            
            
            

def graf_leta(leto1, leto2, imena_filmov, tab):
    '''zrise grafe za filme glede leta'''
    
    slovar_buget = dict()
    slovar_zasluzek = dict()
    
    for film in imena_filmov:
        leto = film.get_leto()
        if leto >= leto1 and leto <= leto2:
            if leto not in slovar_buget:
                slovar_buget[leto] = []
            if leto not in slovar_zasluzek:
                slovar_zasluzek[leto] = []
            #filmi.append(film.get_ime())
            if film.get_poraba() != '-':
                slovar_buget[leto].append(film.get_poraba())
            if film.get_zasluzek() != '-':
                slovar_zasluzek[leto].append(film.get_zasluzek())
                
#             if film.get_zasluzek() != '-':
#                 profit.append(film.get_zasluzek())
#             
#             oskarji.append(film.get_nagrade())
    
    X = []
    Y = []
    Y2 = []
    Y3 = []
    Y4 = []
    
        

    
    for elt in slovar_buget:
        X.append(elt)


    X = sorted(X)
    for elt in X:
        if len(slovar_buget[elt]) == 0:
            Y.append(0)
            Y3.append(0)
        else:
            Y.append(sum(slovar_buget[elt])/len(slovar_buget[elt]))
            Y3.append(max(slovar_buget[elt]))
        if len(slovar_zasluzek[elt]) == 0:
            Y2.append(0)
            Y4.append(0)
        else:
            Y2.append(sum(slovar_zasluzek[elt])/len(slovar_zasluzek[elt]))
            Y4.append(max(slovar_zasluzek[elt]))
        
    
    fig, ax = plt.subplots()

    # Plot the line graph with only some y points displayed
    if tab[0] == 1:
        ax.plot(X, Y, c = 'b', label = 'Povprečna poraba filmov')
    if tab[1] == 1:
        ax.plot(X, Y2, c = 'r', label = 'Povprečni zasluzek filmov')
    if tab[2] == 1:
        ax.scatter(X, [Y3[i] if Y3[i]!= 0 else None for i in range(len(Y3))], c = 'purple', marker = '*', label = 'Maksimalna poraba filma')
    if tab[3] == 1:
        ax.scatter(X, [Y4[i] if Y4[i]!= 0 else None for i in range(len(Y4))], c = 'green', s = 8, marker = 'o', label = 'Maksimalni zasluzek filma')
    
    plt.legend(loc='best', fontsize = 'small')
    ax.set_xlabel('Leto')
    ax.set_ylabel('Denar')
    plt.show()


from Film import Film

def index(lists,ime,leto):
    '''vrne tabelico ime leto oskarji nominacije '''
    for lst in lists: 
        if ime in lst[0]:
            if leto in lst:
                    return lst
    return [0]*len(lst)



nalozeno = False
sez_filmov = []


###########################################################################################################
###########################################################################################################

while True:
    print("Pozdravljeni v malem programcku ki obdeluje filme zabavajte se.")
    
    if not nalozeno:
        razred_film=[]


        #podatke iz datoteke damo v tabelo tabela_filmi
        #datoka vsebuje ime filma, leto, buget in profit

        tabela_filmi=[]
        with open('tabela_filmov.txt', 'r',encoding="utf-8") as file:
            for vrstica in file:
                tabela_filmi.append(eval(vrstica))


        #iz datoteke doda elemente v tabelo
        #vrstica v datoteki vsebuje ime, leto, nagrade in nominacije
        tabela_oskarji=[]
        with open('tabela_oskarji.txt', 'r',encoding="utf-8") as file:
            for vrstica in file:
                tabela_oskarji.append(eval(vrstica))

        #gremo cez flme iz tabele filmov in njihova imena dodamo v mnozico
        #sproti ustvarjamo element razreda filmi 
        tabela_imen=set()
        for film in tabela_filmi:
            ime1=film[0]
            leto1=film[1]
            stroski=film[2]
            zasluzek=film[3]
             
            tabela_imen.add(ime1)

            oskarf = index(tabela_oskarji,ime1,leto1)
            ime2=oskarf[0]
            leto2=oskarf[1]
            oskar=oskarf[2]
            nominacije=oskarf[3]
            
            ime = ime1
            ime = Film(ime1,leto1,stroski,zasluzek,oskar,nominacije)
            
            razred_film.append(ime)

        #gremo se cez tabelo oskarjev in ustvarjamo elemente ki jih ni bilo
        #v prvi tabeli
        for film4 in tabela_oskarji:
            if str(film4[0])not in tabela_imen:
                ime = film4[0]
                ime = Film(film4[0],film4[1],'-','-',film4[2],film4[3])
                razred_film.append(ime)
        
        imena_filmov = razred_film
                
        nalozeno = True
    

    kaj=input("1. Ponovno naloži podatke \n2. Analiza leto \n3. Analiza ocene \n4. Analiza finance \n5. Analiza nagrade \n6. Izhod\n: ")
    
    
    if kaj=="1":
        nalozeno = False
        
        print('Nalaganje traja približno dve minute...')
        
        pygame.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play()



        
        ##################################################################################################
        
        #tabela je oblike[....[ime,leto,stroški,zaslužek].....].... vsi filmi
        tabela_filmov=[]
        headers = {"User-agent": "Chrome/111.0.5563.111"}
        for i in range(1,6401,100):
            #imamo strani vse se zacnejo z 1 razen prva ki je all koraki 100 ker 100 filmou na stran in gremo do 6301
            if i==1:
                url = 'https://www.the-numbers.com/movie/budgets/all'  
            else:
                url = f'https://www.the-numbers.com/movie/budgets/all/{i}'
            req = requests.get(url, headers=headers)    
            text = req.text # HTML format

            skrcitev1=re.split('<table >',text)
            skrcitev2=re.split('<br>',skrcitev1[1])

            #datumi
            tab_leto=[]
            datumi=re.findall('<td><a href="/box-office-chart/daily/.+</a></td>',skrcitev2[0])
            for datum in datumi:
                celi_datum=re.sub('<.*?>','',datum)
                if celi_datum=='Unknown':
                    celi_datum=0
                else:
                    celi_datum=int(celi_datum[-4:])
                tab_leto.append(celi_datum)


            #naslovi
            tab_ime=[]
            imena=re.findall('<td><b><a href="/movie/.+</a></td>',skrcitev2[0])
            for ime in imena:
                ime_cisto=(re.sub('<.*?>','',ime))
                malo_ime=ime_cisto.lower()
                tab_ime.append(malo_ime)


            #finance
            tab_cifer=[]
            vse_cifre=re.findall('<td class="data">&nbsp;.+</td>',skrcitev2[0])
            for cifra in vse_cifre:
                grda_cifra=re.sub('<.*?>','',cifra)
                grda_cifra=grda_cifra[7:]
                grda_cifra=grda_cifra.replace(',','')
                tab_cifer.append(int(grda_cifra))


            #[ime,leto,cifra,cifra]
            for i in range(len(tab_ime)):
                seznamcki=[]#[leto,ime,cifra,cifra]
                seznamcki.append(tab_ime[i])
                seznamcki.append(tab_leto[i])
                seznamcki.append(tab_cifer[3*i])
                seznamcki.append(tab_cifer[2+3*i])
                tabela_filmov.append(seznamcki)
            

        with open('tabela_filmov.txt', 'w',encoding="utf-8") as file:
            for i in tabela_filmov:
                file.write(f"{i}\n")
        
        #############################################################################################
        #[...[film,leto,oskarji,nominacije]....]
        tabela_oskaji=[]

        req = requests.get('https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films')
        text = req.text # HTML format
        skrcitev1=re.split('<tbody>',text)
        skrcitev2=re.split('</tbody>',skrcitev1[1])


        #filmi       
        tab_ime=[]
        imena=re.findall('<i>.+</i>.*',skrcitev2[0])
        for ime in imena:
            ime=re.sub('&amp;','&',ime)
            ime=re.sub('<.*?>','',ime)
            ime=ime.strip()
            ime=ime.lower()
            tab_ime.append(ime)


        #leto
        tab_leto=[]
        leta=re.findall('<td><a.+',skrcitev2[0])
        for leto in leta:
            leto=re.sub('<.*?>','',leto)
            leto=leto.strip()
            leto=leto[:4]
            tab_leto.append(int(leto))


        #nagrade in nominacije
        tab_nagrad_nominacije=[]
        vrstice1=re.findall('<td>\d.*',skrcitev2[0])
        for vrstica in vrstice1:
            spucano=re.sub('<.*?>','',vrstica)
            if len(spucano)>2:
                spucano=re.sub('&.*;','',spucano)
                spucano=re.sub(' \(\d+\)','',spucano)
            tab_nagrad_nominacije.append(int(spucano))



        #gradimo tabelo_oskarji[]
        for i in range(len(tab_ime)):
            seznamcki=[]#ime,leto,cifra,cifra
            seznamcki.append(tab_ime[i])
            seznamcki.append(tab_leto[i])
            seznamcki.append(tab_nagrad_nominacije[2*i])
            seznamcki.append(tab_nagrad_nominacije[2*i+1])
            tabela_oskaji.append(seznamcki)

        with open('tabela_oskarji.txt', 'w',encoding="utf-8") as file:
            for i in tabela_oskaji:
                file.write(f"{i}\n")
        
        pygame.mixer.music.stop()
        
        #########################################################################################


    elif kaj=="2":
        print('Podatke imamo od leta 1920 do danes.')
        print("leto1<=leto2")
        leto1, leto2 = input('Od kereg do kereg leta? (leto1-leto2)\n:').split('-')
        
        if int(leto1) >= 1920 and int(leto2) <= 2023 and int(leto1)<=int(leto2):
            tab = []
            print('Kaj vas zanima? (Vtipkajte 0 ce vas ne zanima, 1 ce vas zanima)')
            #Če vnos ni št. bo value error...ce vnos je število in je rezlično od 1 bo vzel kot da je vnos 0
            try:
                tab.append(int(input('Povprečna poraba filmov?: ')))
                tab.append(int(input('Povprečni zaslužek filmov?: ')))
                tab.append(int(input('Maksimalna poraba filma?: ')))
                tab.append(int(input('Maksimalni zaslužek filma?: ')))
            except:
                raise ValueError("Vnos ni število")
            if sum(tab) != 0:
                graf_leta(int(leto1), int(leto2), imena_filmov, tab)
            else:
                print('Graf ni prikazal nic.')
        else:
            print('Vnos podatkov ni veljaven.')
            
        
             
               
        
        
    elif kaj=="3":
        print('Analiza ocen lahko traja nekaj minut.')
        print('Okvirno traja pod 10 min, za krajše čakanje priporočamo leta pred 2000.')
        leto = int(input('Katere leto vas zanima?\n:'))
        
        pygame.init()
        pygame.mixer.music.load("music2.mp3")
        pygame.mixer.music.play()
        
        print(tabelica_ocen(leto, imena_filmov))
        
        pygame.mixer.music.stop()

    elif kaj=="4":
        

        n = int(input('Koliko najdrazjih filmov?\n:'))
        try:
            print(n_najdrazjih(n, imena_filmov)[0])
            print('\n\n\n')
            print(n_najdrazjih(n, imena_filmov)[1])
        except:
            raise ValueError(f'Filmov je samo {len(imena_filmov)}.')
        
        
    elif kaj=="5":
        
        print('Podatke imamo za filme od leta 1920. do danes.')
        print("leto1<=leto2")
        leto1, leto2 = input('Od kereg do kereg leta? (leto1-leto2)\n:').split('-')
        
        if int(leto1) >= 1920 and int(leto2) <= 2023 and int(leto1)<=int(leto2):
            graf_nagrade(imena_filmov, int(leto1), int(leto2))
        else:
            print('Vnos podatkov ni veljaven.')

        
        
        

    elif kaj=="6":
        #gremo ven iz programa
        print('Lep dan.')
        break 
    else:
        print("Sledi navodilom!!!")
