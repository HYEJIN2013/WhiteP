__author__ = 'Fujitsu'

lista = []

dodatek_seznamu = raw_input("Ali zelite kaj dodati v nakupovalni seznam (DA/NE): ")
while dodatek_seznamu == "DA":

    izdelek = raw_input("Kateri izdelek bi zelelni dodati? ")
    lista.append(izdelek)
    dodatek_seznamu = raw_input("Ali zelite se kaj dodati v nakupovalni seznam (DA/NE): ")

else:
    print "Kadarkoli boste zeleli kaj kupiti, ste dobrodosli pri nas. Spodaj so nasteti kupljeni artikli"
    print lista
