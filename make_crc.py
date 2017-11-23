def gencrc(data, polynomial, crc):    
  for i in range(0, 8):
    if (data ^ crc) & 1:
      crc = (crc >> 1) ^ polynomial
    else:
      crc >>= 1
    data >>= 1
  return crc & 0xFFFF
  
crcTable = []

def makecrctable():
  polynomial = 0xA001
  for i in range(0, 256):
    crcTable.append(gencrc(i, polynomial, 0))
    
def crc16(puscMsg, usDataLen):    
  uchCRCHi = 0xFF    
  uchCRCLo = 0xFF    
  i=0    
  while usDataLen!=0:        
    usDataLen -= 1        
    uindex = uchCRCHi ^ puscMsg[i]        
    i += 1        
    uchCRCHi = uchCRCLo ^ (crcTable[uindex] & 0xFF)        
    uchCRCLo = (crcTable[uindex] >> 8) & 0xFF   
  return (uchCRCHi<<8) | uchCRCLo
