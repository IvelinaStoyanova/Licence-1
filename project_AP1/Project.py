
#Auteur : Ivelina Stoyanova, Ceuninck Guillaume
#Sujet : Transformations bijectives d’images

from PIL import Image

test1 = Image.open('calbuth.png')
test2 = Image.open('joconde.png')
test3 = Image.open('galets.png')

alpha = {'A': Image.open('alphabet/A.png').convert('P'), 'B': Image.open('alphabet/B.png').convert('P'), 'C':Image.open('alphabet/C.png').convert('P'), 'D':Image.open('alphabet/D.png').convert('P')}


keys = dict()

def transformer(img, T, nb = 1):
    '''
    Entrée : une image Img à transformer et une transformation T
    Sortie : une image transformée Img′.

    C'est la fonction generale qui effectue la transformation d'une image img
    avec une fonction de transformation T passée en paramètre.
    '''

    img = img.convert('RGB')
    size = img.size
    mode = img.mode

    #Create new image, eventualy add choice to create new or not
    new_img = Image.new(mode, size)


    for pix_h in range(size[1]):
        for pix_w in range(size[0]):

            #get pixel value
            pix = img.getpixel((pix_w,pix_h))

            #find new coordinates and add new pixel
            new_w, new_h = T((pix_w,pix_h), size, nb)
            new_img.putpixel((new_w, new_h), pix)

    return new_img

def horizontal_symetrie(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    pix_w,pix_h = pixel
    w,h = size

    n_pix_w = w - pix_w - 1


    return (n_pix_w, pix_h)

def vertical_symetrie(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    pix_w,pix_h = pixel
    w,h = size

    n_pix_h = h - pix_h - 1

    return (pix_w, n_pix_h)

def central_symetrie(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    pix_w,pix_h = pixel
    w,h = size

    n_pix_w = w - pix_w - 1
    n_pix_h = h - pix_h - 1

    return (n_pix_w, n_pix_h)

def photomaton(pixel,size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    pix_w,pix_h = pixel
    w,h = size

    for x in range(nb):
        if pix_w%2==0 and pix_h%2==0:
            pix_w = pix_w//2
            pix_h = pix_h//2

        elif pix_w%2==0 and pix_h%2==1:
            pix_w = pix_w//2
            pix_h = h//2 + pix_h//2

        elif pix_w%2==1 and pix_h%2==0:
            pix_w = w//2 + pix_w//2
            pix_h = pix_h//2

        elif pix_w%2==1 and pix_h%2==1:
            pix_w = w//2 + pix_w//2
            pix_h = h//2 + pix_h//2

    return (pix_w,pix_h)

def defil_horizontal(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    pix_w,pix_h = pixel
    w,h = size

    n_pix_w = (pix_w + nb) % w
    return (n_pix_w,pix_h)

def defil_vertical(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    w,h = size
    pix_w,pix_h = pixel

    n_pix_h = (pix_h + nb)%h

    return (pix_w,n_pix_h)


def concentrique(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''
   
    pix_w,pix_h = pixel
    w,h = size
    w-=1
    h-=1

    for x in range(nb):
        if pix_w>=pix_h and pix_w+pix_h<w:
            pix_w+=1

        elif pix_w>pix_h and pix_w+pix_h>=h:
            pix_h+=1

        elif pix_w<=pix_h and pix_w+pix_h>w:
            pix_w-=1

        elif pix_w<pix_h and pix_w+pix_h<=h:
            pix_h-=1

    return (pix_w, pix_h)

def boulanger(pixel, size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''

    pix_w,pix_h = pixel
    w,h = size

    for x in range(nb):
        if pix_h%2==0:
            pix_w = pix_w*2
            pix_h = pix_h//2

        elif pix_h%2==1:
            pix_w = (pix_w)*2 + 1
            pix_h = (pix_h-1)//2

        if pix_w>=(w):
            pix_w, pix_h = central_symetrie((pix_w%w,pix_h), (w, h/2))
            pix_w, pix_h = pix_w, pix_h + h//2

    return (pix_w, int(pix_h))

def boustrophedon(pixel,size, nb=1):
    '''
    Paramètre pixel:(couple d’entiers) coordonnées d’un pixel
    Paramètre size:(couple d’entiers) dimension de l’image
    Paramètre nb:(entier) nombre de transformations a effectuer sur un pixel
    
    Valeur renvoyée:(couple d’entiers) coordonnées de la position du
    pixel après la permutation
    '''
     
    pix_w,pix_h = pixel
    w,h = size

    for x in range(nb):
        if pix_h%2==0:
            pix_w = pix_w +1
        elif pix_h%2==1:
            pix_w = pix_w -1
        if pix_w >= w :
            pix_h +=1
            pix_w = w-1
        elif pix_w < 0:
            pix_h+=1
            pix_w = 0
        if pix_h >= h:
            pix_h = 0
            
    return (pix_w, pix_h)

def calculate_cycle(T,size,pixel):
   '''
   Paramètre T:(fonction) transformation d'une image
   Paramètre size:(couple d'entiers) dimension de l'image
   Paramètre pixel:(couple d'entier) coordonnées d'un pixel de l'image

   La fonction calcule le cycle d'un pixel. Cad toutes les valeurs que prend
   un pixel, avant de revenir a sa place initiale.

   Valeur renvoyée: un entier et une liste, la longeur du cycle et le cycle
   
   '''

   Npixel = T(pixel, size)
   length = 1
   cycle = []
   cycle.append(pixel)

   while Npixel != pixel:
       length+=1
       cycle.append(Npixel)
       Npixel = T(Npixel, size)
        
   return length,cycle

'''
   Nous avons choisi une structure de type dictionnaire, où chaque cycle est sauvegardé
dans le dictionnaire avec pour clé le premier pixel trouvé qui appartient au cycle.
Par la suite, vous allez voir dans le code l’existence d’un mapView. C’est un dictionnaire
qui à chaque pixel de l’image associe son pixel ‘clé’, en indiquant de quel cycle il
vient. Ça sert à optimiser le processus de création du dictionnaire avec les
permutations et le processus de transformation d’une image avec ce dictionnaire.
'''


def analyse(T, size):
    '''
    Paramètre T:(fonction) transformation d'une image
    Paramètre size:(couple d'entiers) dimension de l'image

    La fonction effectue l'analyse d'une fonction de transformation sur une image de dimension
    size. Elle sauvegarde les resultats dans un dictionaire 'keys'.
    Les resultats sauvgardés sont:
       -un dictionaire(cycles) avec tous les cycles des pixels de l'image
       -un dictionaire(mapView) qui associe a chaque pixel une cle(un des pixels du cycle) qui
        indique le cycle auxquel le pixel correspond
       -un ensemble avec toutes les longueurs des cycles de l'image
    '''

    cycles = dict()
    mapView = dict()
    lens = set()

    for y in range(size[0]):
        for x in range(size[0]):
            pixel = (x,y)
            
            if not pixel in mapView:
                #if the pixel isnt in the mapView, its cycle has not been calculated yet, calculated
                long,cycle = calculate_cycle(T,size, pixel)

                #for each pixel in the calculated cycle, add it to the map view and give it as value,
                #a tuple with the pixel indicator of the whole cycle and its possition in the cycle
                for i in range(len(cycle)):
                    mapView[cycle[i]]= (pixel,i)
                    
                cycles[pixel] = cycle
                lens.add(long)

    keys[str(T)+'-'+str(size)] = (cycles,mapView,lens)
   
def transformer_long(img, T, nb):
   '''
   Entrée : une image Img à transformer et une transformation T
   Sortie : une image transformée Img′.

   La fonction effectue la transformation nb nombre de fois d'une image img avec une fonction
   de transformation T passee en parametre.
   Il est preferable d'utiliser la fonction si on veut faire un tres grand nombre de transformations.
   '''
   img = img.convert('RGB')
   size = img.size
   mode = img.mode
   newImg = Image.new(mode, size)

   if not str(T)+'-'+str(size) in keys:
      analyse(T,size)
   
   cycles, mapView, lens = keys[str(T)+'-'+str(size)]
   
   for pix_h in range(size[1]):
     for pix_w in range(size[0]):

        val = img.getpixel((pix_w,pix_h))

        #save pixel in variable and use the mapView to find the referance pixel 'ref' indicating to witch cycle it belongs
        pix = (pix_w, pix_h)
        ref, index = mapView[pix]

        #use ref to find the proper cycle
        cycle = cycles[ref]
        lenCycle = len(cycle) 

        #use the modulo function to find the new shortened cycle length
        newNB = nb%lenCycle

        #used the index from mapView to find the pixel in the cycle, add the needed number to it, in order to find the newPixel
        newPix = cycle[(index+newNB)%lenCycle]
           
        newImg.putpixel(newPix, val)

   return newImg
           
   
print('For instructions on how to use the program please write: help()')

def help():
   print('This is a program that transforms images by moving their pixels around. All the transformations are bijective. \nThat means that no pixel is lost or duplicated when the transformation takes place')
   print('Here are the transformations we offer: \n   - horizontal_symetrie \n   - vertical_symetrie \n  - central_symetrie \n   - photomaton \n   - defil_horizontal \n   ect...')
   print('To make a transformation plase call the function transformer() or the function transformer_long().\nYou can use help(function) to get more info on the functions. \n')
   reponse = input('Would you like to know more about the transformations? (Y/N)')


####Experiment
   
def  ppcm_alternative(x, y):
   """This function takes two
   integers and returns the L.C.M."""

   # choose the greater number
   if x > y:
       greater = x
   else:
       greater = y
   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           ppcm = greater
           break
       greater += 1
   return ppcm

def ppcm(a,b):
    while a%b!=0:
        a,b = b,a%b

    pgcd = a

    return a*b/pgcd

def ppcm_n(l):
   '''
   La fonction calcule le ppcm de tous les nombres de la liste passee en parametre.
   '''
   if len(l)>1:
      res = ppcm(l[0],l[1])
      for i in range(2,len(l)):
         res = ppcm(res, l[i])
   else:
      res = l[0]

   return res

letterSize = 16

def write(img, letter, start):
   '''
   La fonction écrit la lettre letter sur l'image img, commençant a la position start.
   '''
   img = img.convert('RGB')
   size = img.size
   mode = img.mode

   newIMG = Image.new(mode, size)
   newIMG = img
   
   for pixH in range(letterSize):
        for pixW in range(letterSize):
           if letter.getpixel((pixW,pixH))==1:
              newPix = tuple(255 for x in newIMG.getpixel((start[0]+ pixW,start[1] + pixH)))
              newIMG.putpixel((start[0] + pixW,start[1] + pixH), newPix)

   return newIMG

alpha = {'A': Image.open('alphabet/A.png').convert('P'), 'B': Image.open('alphabet/B.png').convert('P'), 'C':Image.open('alphabet/C.png').convert('P'),
         'D':Image.open('alphabet/D.png').convert('P'),'E':Image.open('alphabet/E.png').convert('P'),'F':Image.open('alphabet/F.png').convert('P')}

def writeMSG(img, msg, start):
   '''
   La fonction écrit le message msg sur l'image img, commençant a la position start.
   '''
   first = start
   res = img
   size = img.size
   
   for letter in msg:
      res = write(res, alpha[letter], start)

      start = (start[0]+letterSize+2,start[1])
      if start[0]>(size[0]-letterSize*2):
         start = (first[0], start[1]+letterSize*2)

   return res

concentrLen = 260538918857747541744672011746506021097973820451713310155553963930295146498906764615494790073109501333431500
photoLen = 8
boulangLen = 17
boustrophLen = 65536

Ts = [photomaton, boulanger, boustrophedon, concentrique]
lens = [photoLen, boulangLen, boustrophLen, concentrLen]

def code(img, msg, key, order):
   '''
   La fonction code le message msg sur l'image img en utilisant la cle key.
   
   La cle est le variable key (une liste) contenant le nombre des transformations a effectuer avec chaque transformation.
   La forme du parametre key est: [A - nbre de fois a appliquer la transformation photomaton,
                           B - nbre de fois a appliquer la transformation boulanger,
                           C - nbre de fois a appliquer la transformation boustrophedon,
                           D - nbre de fois a appliquer la transformation concentrique]

   On dispose de 4 fonctions de transformation [photomaton, boulanger, boustrophedon, concentrique].
   Le variable(une liste) order contient l'ordre dans lequel les fonctions seront executees.
   ex:[0,1,2,3] - ordre standart; [3,2,1,0] - ordre decroissant.
   La forme du parametre ordre est: [A - transformation numero A, selon la liste ci-dessus,
                                       B - transformation numero B, selon la liste ci-dessus,
                                       C - transformation numero C, selon la liste ci-dessus,
                                       D - transformation numero D, selon la liste ci-dessus]

   
   C.U.: key et order sont des listes de longeur 4 (d'entiers)
   '''
   assert img.size==(256,256)

   for x in order:
       img = transformer_long(img, Ts[x], key[x])

   img = writeMSG(img, msg, (50,50))
   img.show()

   for x in reversed(order):
        img = transformer_long(img, Ts[x], lens[x] - key[x])

   return img

def decode(img, key, order):
    for x in order:
       img = transformer_long(img, Ts[x], key[x])

    img.show()
    return img
    
   

   
