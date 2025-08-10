# 👾 Desafío de Programación 1

__Repositorio:__ https://github.com/div468/Proyecto-1-MD.git


# ↔️ Lógica Proposicional
Programa desarrollado para la generación de tablas de verdad, verificación de tautologías, equivalencias e inferencias.


# 📌 Descripción
Herramienta desarrollada con Python para la implementación de fundamentos básicos de la lógica proposicional

- Generación de tablas de verdad
- Verificación de tautologías
- Verificación de inferencias
- Inferencia de valores para proposiciones compuestas

# 🛠️ Funciones implementadas
| Función | Descripción | Parámetros recibidos| Valores de retorno |Ejemplo de uso| 
|---|---|---|---| --- |
| tabla_verdad(expr) | Genera una tabla de verdad para una proposición ingresada | Proposición compuesta (String) | Lista de listas que representa la tabla de verdad list[list[bool]] | tabla_verdad("a and b")
| tautologia(expr) | Verifica si una proposición es o no una tautología    | Proposición compuesta (String) | True o False según la proposición | tautolgia("a or nor a") | 
| equivalentes(expr1, expr2) | Verifica si dos proposiciones son o no lógicamente equivalentes | Dos proposiciones compuestas (Strings) | True o False de acuerdo a las dos proposiciones | equivalentes("a and (b or c)", "(a and b) or (a and c)")
|inferencia(expr)| Encuentra los valores de verdad de las proposiciones de manera que se satisfaga la igualdad | Proposición compuesta seguida del operador igualdad "=" y el valor 1 para verdadero o 0 para falso | Lista de listas asignando los valores de verdad a las proposiciones de manera que se satisfaga la igualdad list[list[]bool] | inferencia("a or b = 1")

## Ejemplo tabla_verdad(expr)
![tabla_verdad()](https://github.com/user-attachments/assets/005be36a-0173-462c-82a3-e69aba73ecf4)
