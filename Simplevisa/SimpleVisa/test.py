import simplevisa

rm = visa.ResourceManager()
print(rm.list_resources())

vna = simplevisa.HP3577(0, 11)
