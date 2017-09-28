#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: module

:author: FIL - IEEA - Univ. Lille1.fr <http://portail.fil.univ-lille1.fr>_

:date: mars 2017


Chaine complète 

- prise de vue d'une photo (nécessite un APN branché et gphoto2)
- récupération photo 
- rognage et redimensionnement 256x256 (nécessite PIL)
- 8 transformations successives du Photo-Maton 
- production d'un PDF (nécessite FPDF)

"""
import sys, os
from PIL import Image
from fpdf import FPDF
from datetime import date
from transformations import photo_maton
from transforme_image import transforme

TITRE = 'Transformations de {:s}'.format(sys.argv[1])
DATE = date.today()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'u', 8)
        self.set_text_color(0, 0, 255)
        self.cell(0,10, txt='FIL - IEEA - Univ. Lille1', ln=0,
                  link='http://www.fil.univ-lille1.fr/')
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0)
        self.set_fill_color(200)
        self.set_x(150)
        self.cell(w=self.get_string_width(TITRE) + 4,
                  h=10, txt=TITRE, border='LB',
                  ln=0, align='C', fill=True)
        self.ln(20)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', style='', size=8)
        self.cell(0, 10, DATE.strftime('%d/%m/%Y'), border=0, ln=0, align='L')
        self.set_font('Arial', 'I', 8)
        self.set_x(30)
        self.cell(0, 10, txt='Page {:d}'.format(self.page_no()), border=0, ln=0, align='C')



if __name__ == '__main__':

    # commande système pour la prise de vue par un appareil photo numérique (APN)
    # (nécessite l'installation préalable de gphoto2)
    COMMANDE_PRISE_VUE = 'gphoto2 --filename "{:s}" --capture-image-and-download '

    # nom donné sur la ligne de commande
    # ce nom sert ensuite pour les noms de fichiers produits, et le titre du document PDF
    nom = sys.argv[1]

    # Nom du fichier à donner à l'image produite par l'APN 
    IMAGE_PRISE = '{:s}.jpg'.format(nom)
    # Noms des fichiers à donner aux images transformées
    IMAGE_TRANSFORMEE = '{:s}_{:d}.jpg'
    
    TAILLE_IMAGES_TRANSFORMEES = 256
    AUTEUR = 'EW'

    # Prise de vue de l'image depuis un APN
    os.system(COMMANDE_PRISE_VUE.format(IMAGE_PRISE))

    # Chargement en mémoire de l'image à transformer
    img_orig = Image.open(IMAGE_PRISE).convert('RGB')
    larg, haut = img_orig.size
    print('Taille image originale : {:d}x{:d}'.format(larg, haut))

    # Découpage de l'image originale de façon à obtenir une image carrée
    size = min(larg, haut)
    if size == larg:
        # l'image originale est en portrait
        coupe_vert = (haut - larg) // 2
        boite = (0, coupe_vert, larg, haut - coupe_vert)
    else:
        # l'image originale est en paysage
        coupe_horiz = (larg - haut) // 2
        boite = (coupe_horiz, 0, larg - coupe_horiz, haut)
    img_carree = img_orig.crop(boite)

    # réduction de l'image à une image TAILLE_IMAGES_TRANSFORMEES x TAILLE_IMAGES_TRANSFORMEES
    img = img_carree.resize((TAILLE_IMAGES_TRANSFORMEES, TAILLE_IMAGES_TRANSFORMEES))

    larg, haut = img.size
    print('Taille image redimensionnee : {:d}x{:d}'.format(larg, haut))


    # Sauvegardes et transformations successives photo_maton des images 
    for i in range(9):
        img.save(IMAGE_TRANSFORMEE.format(nom, i))
        img = transforme(photo_maton, img)
    
    # Production du PDF
    mon_pdf = PDF(orientation='L', unit='mm', format='A4')
    mon_pdf.set_title(TITRE)
    mon_pdf.set_author(AUTEUR)
    mon_pdf.set_font('Times', style='', size=11)

    mon_pdf.add_page()
    mon_pdf.cell(60)
    X = mon_pdf.get_x()
    Y = mon_pdf.get_y()
    mon_pdf.set_fill_color(200,220,0)
    mon_pdf.set_draw_color(255,0,0)
    mon_pdf.rect(X - 8, Y - 8, w=3 * 52 + 14, h=3 * 52 + 14, style='DF')
    for i in range(9):
        mon_pdf.image('{:s}_{:d}.jpg'.format(nom, i),
                      w=50, h=50, x=X + 52 * (i % 3), y=Y + 52 * (i // 3))

    # Sauvegarde du PDF dans un fichier
    mon_pdf.output('{:s}.pdf'.format(nom))

    # Visualisation du PDF (éventuellement remplacer le lecteur de PDF evince par un autre)
    os.system('evince {:s}.pdf &'.format(nom))
