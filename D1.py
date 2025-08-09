"""
# MM2015 - Desafío de programación 1: Lógica proposicional
# autor: macastillo

# NOTA:
# Debe utilizar letras minúsculas para los nombres de las variables, por ejemplo, a, b, c.
# Puede utilizar paréntesis para agrupar expresiones, como «a and (b or c)».

# Implemente las cuatro funciones siguientes:
# tabla_verdad, tautologia, equivalentes e inferencia

# Entrega:
# Deberá subir este archivo a la página del curso en Canvas.
"""


######## No modifique el siguiente bloque de código ########
# ********************** COMIENZO *******************************

from functools import partial
import re


class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

@Infix
def implies(p, q) :
    return not p or q

@Infix
def iff(p, q) :
    return (p |implies| q) and (q |implies| p)

# Debe utilizar esta función para extraer variables.
# Esta función toma una expresión como entrada y devuelve una lista ordenada de variables.
# NO modifique esta función.

def extract_variables(expression):
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set


# ********************** FIN *******************************



############## IMPLEMENTAR LAS SIGUIENTES FUNCIONES  ##############
############## No modificar las definiciones de las funciones ##############

# Función: tabla_verdad
# Esta función calcula una tabla de verdad para una expresión dada.
# Entrada: expresión.
# Salida: tabla de verdad como una lista de listas.

def tabla_verdad(expr):
    pass

# Función: tautologia
# Esta función determina si la expresión es una tautología, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión.
# Salida: booleano.
def tautologia(expr):
    pass

# Función: equivalentes
# Esta función determina si expr1 es equivalente a expr2, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión 1 y expresión 2.
# Salida: booleano.
def equivalentes(expr1, expr2):
    pass

# Función: inferencia
# Esta función determina los valores de verdad para una valuación de una proposición dada.
# Entrada: expresión.
# Salida: lista de listas.

def inferencia(expr):
    pass

############## FUNCIONES AUXILIARES ##############

def evaluar_expresion(expr, asignaciones):
    """
    Evalúa una expresión lógica con asignaciones de variables dadas.
    
    Args:
        expr (str): Expresión lógica
        asignaciones (dict): Diccionario variable -> valor booleano
        
    Returns:
        bool: Resultado de evaluar la expresión
    """
    pass

def procesar_tabla_verdad():
    #Procesa la opción de tabla de verdad.
    pass

def procesar_tautologia():
    #Procesa la opción de verificar tautología.
    pass

def procesar_equivalencias():
    #Procesa la opción de verificar equivalencias.
    pass

def procesar_inferencia():
    #Procesa la opción de realizar inferencia.
    pass

def mostrar_menu():
    # Muestra el menú principal del programa.
    print("\n--- Calculadora de Lógica Proposicional ---")
    print("1. Tabla de verdad")
    print("2. Verificar tautología")
    print("3. Verificar equivalencias")
    print("4. Realizar inferencia")
    print("5. Finalizar")
    print("=" * 45)


def main():
    """Función principal del programa con interfaz de usuario."""
    continuar = True
    
    # Diccionario para simular switch-case
    opciones = {
        '1': procesar_tabla_verdad,
        '2': procesar_tautologia,
        '3': procesar_equivalencias,
        '4': procesar_inferencia
    }
    
    while continuar:
        mostrar_menu()
        
        try:
            opcion = input("Seleccione una opción (1-5): ").strip()
            
            if opcion in opciones:
                # Ejecutar la función correspondiente
                opciones[opcion]()
            elif opcion == '5':
                print("\n¡Gracias por usar la calculadora de lógica proposicional!")
                continuar = False
            else:
                print("\nOpción inválida. Por favor seleccione un número del 1 al 5.")
                
        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
        
        if continuar:
            input("\nPresione Enter para continuar...")

#Validación de la entrada del usuario
def validar_entrada(entrada) :

    #Se valida que existan proposiciones en la entrada
    proposiciones = extract_variables(entrada)
    if not proposiciones:
        raise ValueError("La expresión no posee variables válidas (letras minúsculas a - z)")
    
    #Se valida que únicamente los operadores validos se encuentren en la entrada
    operadores_permitidos = r'^[a-z\s()|andornot|iff||implies|]+$'
    if not re.fullmatch(operadores_permitidos,entrada):
        raise ValueError("Ingresó operadores lógicos no pérmitidos")

    #Uso de stack para validar el orden de los paréntesis
    stack = []
    for caracter in enumerate(entrada):
        if caracter == "(":
            stack.append(caracter)
        elif caracter == ")":
            if not stack:
                raise ValueError("Ingresó un paréntesis de cierre sin un paréntesis de apertura anteriormente")
            stack.pop()
    if stack:
        raise ValueError("Ingresó un paréntesis de apertura sin unn paréntesis de cierre posterior")
    
    #Se verifica que la sintaxis siga un orden adecuado
    estructuras_invalidas = [
        r'^\s*(and|or|\|implies\||\|iff\|)',
        r'(and|or|\|implies\||\|iff\|)\s*$',
        r'(not\s+not\s+)',
        r'(and|or|\|implies\||\|iff\|)\s*(and|or|\|implies\||\|iff\|)',
        r'\(\s*(and|or|\|implies\||\|iff\|)',
        r'(and|or|\|implies\||\|iff\|)\s*\)',
        r'not(\s*[^a-z(])'
    ]

    for estructura in estructuras_invalidas:
        if re.search(estructura, entrada):
            raise ValueError("Ingresó una estructura de operación inválida")
        
    return True