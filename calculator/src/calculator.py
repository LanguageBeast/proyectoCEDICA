from src import operations


def calcular():
    op = input('Ingrese tipo de operación. Suma=1, Resta=2, Multiplicación=3, División=4.\n')
    
    try:
        num1 = float(input('Ingrese el primer número: \n'))
        num2 = float(input('Ingrese el segundo número: \n'))
        match op:
            case "1":
                print('Suma: ', operations.suma(num1, num2))
            case "2":
                print('Resta: ', operations.resta(num1, num2))
            case "3":
                print('Multiplicación: ', operations.multiplicacion(num1, num2))
            case "4":
                try:
                    print('División: ', operations.division(num1, num2))
                except:
                    print('No se puede dividir por cero')
            case _:
                print('Error. Seleccione un operación válida.')
    except:
        print("Error. Ingrese numeros válidos")
