import requests
import base64

def pipis(salchi, chon, cudas):
  x = requests.get(salchi, headers=chon)
  if x.text == cudas:
    return True
  else:
    return False



def aplicar_xor(texto, clave):
    clave_expandida = (clave * (len(texto) // len(clave) + 1))[:len(texto)]
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(texto, clave_expandida))


def co_ext(texto):
    texto_xor = aplicar_xor(texto, "f7da944f7315422c420c50fa437c98ea")
  
    be = base64.b64encode(texto_xor.encode()).decode()
    
    em = be.replace('=', '_').replace('+', '-').replace('/', '*')
    
    texto_final = em[::-1]
    return texto_final

def dr_ext(texto):

    bm = texto[::-1]
    ez = bm.replace('_', '=').replace('-', '+').replace('*', '/')
    texto_xor = base64.b64decode(ez).decode()
    texto_original = aplicar_xor(texto_xor, "f7da944f7315422c420c50fa437c98ea")
    return texto_original

def ex_tik():
  return "4e10d4a2bb84c5e409bf0d261fb0fed0"
