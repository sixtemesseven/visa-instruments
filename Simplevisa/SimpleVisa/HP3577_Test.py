import visa
import simplevisa

rm = visa.ResourceManager()
print(rm.list_resources())
