import visa
import simplevisa

rm = visa.ResourceManager()
print(rm.list_resources())

vna = simplevisa.HP3577(0,11)

vna.plotPolar("R")


'''
vna.getData("A")
'''