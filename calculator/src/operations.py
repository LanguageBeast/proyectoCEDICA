def suma (a, b): 
    # suma dos numeros
    return a + b

def multiplicacion(a, b):
    # multiplica dos numeros
    return a * b

def resta(a,b):
    # resta dos numeros
    return a - b

def division(a, b):
    # divide dos numeros
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b