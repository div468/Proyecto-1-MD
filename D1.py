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
    """
    Genera una tabla de verdad para una expresión lógica dada.
    
    Args:
        expr (str): Expresión lógica con variables minúsculas (a-z)
        
    Returns:
        list[list[bool]]: Tabla de verdad donde cada fila contiene los valores de las variables seguidos del resultado
    """
    try:
        # Extraer variables de la expresión
        variables = extract_variables(expr)
        n = len(variables)
        
        # Generar todas las combinaciones posibles de valores de verdad
        tabla = []
        for i in range(2**n):
            # Generar combinación binaria para esta fila
            valores = []
            for j in range(n):
                # Extraer el j-ésimo bit (de derecha a izquierda)
                bit = (i >> (n - 1 - j)) & 1
                valores.append(bool(bit))
            
            # Crear diccionario de asignaciones para evaluar la expresión
            asignaciones = dict(zip(variables, valores))
            
            # Evaluar la expresión con estas asignaciones
            resultado = evaluar_expresion(expr, asignaciones)
            
            # Agregar fila a la tabla (valores + resultado)
            fila = valores + [resultado]
            tabla.append(fila)
            
        return tabla
        
    except Exception as e:
        raise ValueError(f"Error al procesar la expresión: {e}")

# Función: tautologia
# Esta función determina si la expresión es una tautología, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión.
# Salida: booleano.
def tautologia(expr):
    """
    Determina si una expresión lógica es una tautología.
    
    Args:
        expr (str): Expresión lógica con variables minúsculas (a-z)
        
    Returns:
        bool: True si la expresión es una tautología, False en caso contrario
    """
    try:
        # Extraer variables de la expresión
        variables = extract_variables(expr)
        n = len(variables)
        
        # Generar todas las combinaciones posibles de valores de verdad
        for i in range(2**n):
            # Generar combinación binaria para esta fila
            asignaciones = {}
            for j in range(n):
                # Extraer el j-ésimo bit (de derecha a izquierda)
                bit = (i >> (n - 1 - j)) & 1
                asignaciones[variables[j]] = bool(bit)
            
            # Evaluar la expresión con estas asignaciones
            resultado = evaluar_expresion(expr, asignaciones)
            
            # Si encontramos al menos un caso donde la expresión es False,
            # entonces no es una tautología
            if not resultado:
                return False
        
        # Si llegamos aquí, todas las evaluaciones fueron True
        return True
        
    except Exception as e:
        raise ValueError(f"Error al procesar la expresión: {e}")


# Función: equivalentes
# Esta función determina si expr1 es equivalente a expr2, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión 1 y expresión 2.
# Salida: booleano.
def equivalentes(expr1, expr2):
        #Se extraen las variables de cada expresion
        variables_expr1 = extract_variables(expr1)
        variables_expr2 = extract_variables(expr2)

        #Si no son las mismas, automáticamente descartamos la equivalencia
        if (set(variables_expr1) != set(variables_expr2)):
            return False
        #Se juntan todas las variables para tomar en cuenta todos los casos posibles
        variables = sorted(list(set(variables_expr1 + variables_expr2)))
        n = len(variables)

        #Se calculan todas las combinaciones posibles
        for i in range(2 ** n):
            asignacion = {}
            for j in range(n):
                valor = (i // (2 ** j)) % 2 == 1
                asignacion[variables[j]] = valor
            
            #Si las combinaciones y sus resultados no son iguales, no son logicamente equivalentes
            if evaluar_expresion(expr1, asignacion) != evaluar_expresion(expr2, asignacion):
                return False
        
        return True

# Función: inferencia
# Esta función determina los valores de verdad para una valuación de una proposición dada.
# Entrada: expresión.
# Salida: lista de listas.

def inferencia(expr):
    pass

############## FUNCIONES AUXILIARES ##############

# Función alternativa más robusta para evaluar expresiones
def evaluar_expresion_alternativa(expr, asignaciones):
    """
    Versión alternativa más robusta para evaluar expresiones lógicas.
    """
    # Crear una copia de la expresión para modificar
    expr_eval = expr.strip()
    
    # Primero, reemplazar todas las variables con sus valores
    for variable, valor in asignaciones.items():
        # Usar word boundaries para evitar reemplazos parciales
        expr_eval = re.sub(r'\b' + variable + r'\b', str(valor), expr_eval)
    
    # Ahora manejar los operadores personalizados paso a paso
    # Procesar |implies| - convertir a operación lógica básica
    while '|implies|' in expr_eval:
        # Buscar patrones de la forma (expr1) |implies| (expr2)
        match = re.search(r'([^|]+)\s*\|implies\|\s*([^|]+)', expr_eval)
        if match:
            left = match.group(1).strip()
            right = match.group(2).strip()
            # p |implies| q equivale a (not p or q)
            replacement = f"(not ({left}) or ({right}))"
            expr_eval = expr_eval[:match.start()] + replacement + expr_eval[match.end():]
        else:
            break
    
    # Procesar |iff| - convertir a operación lógica básica  
    while '|iff|' in expr_eval:
        match = re.search(r'([^|]+)\s*\|iff\|\s*([^|]+)', expr_eval)
        if match:
            left = match.group(1).strip()
            right = match.group(2).strip()
            # p |iff| q equivale a ((p and q) or (not p and not q))
            replacement = f"(({left}) and ({right})) or ((not ({left})) and (not ({right})))"
            expr_eval = expr_eval[:match.start()] + replacement + expr_eval[match.end():]
        else:
            break
    
    try:
        # Evaluar la expresión resultante
        resultado = eval(expr_eval, {"__builtins__": {}}, {})
        return bool(resultado)
    except Exception as e:
        raise ValueError(f"Error al evaluar expresión '{expr}': {e}")


# Función mejorada que combina ambos enfoques
def evaluar_expresion(expr, asignaciones):
    """
    Evalúa una expresión lógica con asignaciones de variables dadas.
    Usa un enfoque híbrido para manejar operadores personalizados.
    
    Args:
        expr (str): Expresión lógica
        asignaciones (dict): Diccionario variable -> valor booleano
        
    Returns:
        bool: Resultado de evaluar la expresión
    """
    try:
        # Método 1: Intentar con operadores infijos
        expr_eval = expr
        contexto = asignaciones.copy()
        contexto['implies'] = implies
        contexto['iff'] = iff
        
        resultado = eval(expr_eval, {"__builtins__": {}}, contexto)
        return bool(resultado)
        
    except:
        # Método 2: Si falla, usar conversión manual
        try:
            return evaluar_expresion_alternativa(expr, asignaciones)
        except Exception as e:
            raise ValueError(f"Error al evaluar expresión '{expr}': {e}")

def procesar_tabla_verdad():
    """Procesa la opción de tabla de verdad."""
    expr = input("Ingrese la expresión para tabla de verdad: ").strip()
    tabla = tabla_verdad(expr)
    variables = extract_variables(expr)
    
    print(f"\nTabla de verdad para: {expr}")
    print(f"Variables: {variables}")
    print("-" * (len(variables) * 8 + 15))
    
    # Encabezados
    header = ""
    for var in variables:
        header += f"{var:>6} "
    header += f"{'Resultado':>10}"
    print(header)
    print("-" * (len(variables) * 8 + 15))
    
    # Filas de la tabla
    for fila in tabla:
        linea = ""
        for valor in fila:
            linea += f"{str(valor):>6} "
        print(linea)

def procesar_tautologia():
    """Procesa la opción de verificar tautología."""
    try:
        expr = input("Ingrese la expresión para verificar tautología: ").strip()
        
        # Validar la entrada
        if not validar_entrada(expr):
            print("La expresión ingresada no es válida, inténtelo de nuevo")
            return
        
        # Verificar si es tautología
        es_tautologia = tautologia(expr)
        
        print(f"\nExpresión: {expr}")
        if es_tautologia:
            print("✓ La expresión ES una tautología (siempre verdadera)")
        else:
            print("✗ La expresión NO es una tautología")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def procesar_equivalencias():
    expr1 = input("Ingrese la primera expresión: ")
    expr2 = input("Ingrese la segunda expresión: ")

    if (validar_entrada(expr1) and validar_entrada(expr2) != True):
        print("Una de las expresiones ingresadas no es válida, inténtelo de nuevo")
    else:
        equivalencia = equivalentes(expr1, expr2)
        if equivalencia == True:
            print("Las funciones son lógicamente equivalentes")
        else :
            print("Las funciones no son lógicamente equivalentes")

def procesar_inferencia():
    #Procesa la opción de realizar inferencia.
    pass


#Validación de la entrada del usuario
def validar_entrada(entrada):
    # Validar que existan variables proposicionales
    proposiciones = extract_variables(entrada)
    if not proposiciones:
        raise ValueError("La expresión no posee variables válidas (letras minúsculas a - z)")
    
    # Validar caracteres permitidos y estructura general
    patron_valido = r'^([a-z]\s*|\b(and|or|not)\b\s*|\|implies\|\s*|\|iff\|\s*|\(|\)\s*)+$'
    if not re.fullmatch(patron_valido, entrada.strip()):
        raise ValueError("Sintaxis inválida: operadores mal formados o caracteres no permitidos")

    # Validar paréntesis balanceados
    stack = []
    for i, caracter in enumerate(entrada):
        if caracter == '(':
            stack.append(i)
        elif caracter == ')':
            if not stack:
                raise ValueError(f"Paréntesis de cierre ')' sin apertura en posición {i}")
            stack.pop()
    if stack:
        raise ValueError(f"Paréntesis de apertura '(' sin cierre en posición {stack[-1]}")

    # Validar estructura de operadores
    estructuras_invalidas = [
        r'^\s*(and|or|\|implies\||\|iff\|)',
        r'(and|or|\|implies\||\|iff\|)\s*$',
        r'(not\s+not\s+)',
        r'(and|or|\|implies\||\|iff\|)\s*(and|or|\|implies\||\|iff\|)',
        r'\(\s*(and|or|\|implies\||\|iff\|)',
        r'(and|or|\|implies\||\|iff\|)\s*\)',
        
    ]

    for patron in estructuras_invalidas:
        if re.search(patron, entrada):
            raise ValueError("Estructura de operadores inválida")
    
    # Validaciones adicionales para 'not'
    # Verificar que 'not' siempre esté seguido por una variable o paréntesis de apertura
    if re.search(r'\bnot\s+(?![a-z(])', entrada):
        raise ValueError("El operador 'not' debe estar seguido por una variable o paréntesis de apertura")
    
    # Verificar que no haya múltiples 'not' consecutivos sin paréntesis
    if re.search(r'\bnot\s+not\s+(?![a-z(])', entrada):
        raise ValueError("Múltiples operadores 'not' consecutivos requieren paréntesis")
        
    return True

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

main()
