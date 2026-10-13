import pulp
import pandas as pd

# Datos originales de la Tabla 1
profesionales = ['Ana', 'Carlos', 'Laura', 'Miguel', 'Sofía', 'Andrés']
tareas = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']

tiempos_originales = {
    'Ana':    {'T1': 12, 'T2': 18, 'T3': 15, 'T4': 20, 'T5': 14, 'T6': 16},
    'Carlos': {'T1': 16, 'T2': 11, 'T3': 19, 'T4': 14, 'T5': 17, 'T6': 13},
    'Laura':  {'T1': 14, 'T2': 16, 'T3': 10, 'T4': 18, 'T5': 15, 'T6': 17},
    'Miguel': {'T1': 18, 'T2': 13, 'T3': 16, 'T4': 11, 'T5': 19, 'T6': 15},
    'Sofía':  {'T1': 15, 'T2': 17, 'T3': 14, 'T4': 16, 'T5': 9,  'T6': 18},
    'Andrés': {'T1': 17, 'T2': 14, 'T3': 18, 'T4': 15, 'T5': 16, 'T6': 10}
}

# Crear el problema de optimización sin sumar 1000
prob = pulp.LpProblem('Asignacion_Tareas_JFV_Original', pulp.LpMinimize)

# Definir variables de decisión binarias
x = pulp.LpVariable.dicts('Asignacion', ((p, t) for p in profesionales for t in tareas), cat='Binary')

# Función Objetivo: Minimizar la suma de tiempos originales
prob += pulp.lpSum(tiempos_originales[p][t] * x[p, t] for p in profesionales for t in tareas)

# Restricciones:
# 1. Cada profesional debe recibir exactamente una tarea
for p in profesionales:
    prob += pulp.lpSum(x[p, t] for t in tareas) == 1

# 2. Cada tarea debe asignarse exactamente a un profesional
for t in tareas:
    prob += pulp.lpSum(x[p, t] for p in profesionales) == 1

# 3. Condiciones adicionales
# Ana no cuenta con la certificación requerida para ejecutar T4
prob += x['Ana', 'T4'] == 0

# Carlos no estará disponible para ejecutar T3
prob += x['Carlos', 'T3'] == 0

# T5 debe asignarse a Sofía debido a su experiencia especializada
prob += x['Sofía', 'T5'] == 1

# Resolver el modelo utilizando el solver por defecto (CBC)
status = prob.solve()

# Estructurar y mostrar resultados
resultados = []
for p in profesionales:
    for t in tareas:
        if pulp.value(x[p, t]) == 1:
            resultados.append({
                'Profesional': p,
                'Tarea': t,
                'Tiempo Original (h)': tiempos_originales[p][t]
            })

df_resultados = pd.DataFrame(resultados)

print(f"Estado de la solución: {pulp.LpStatus[status]}")
print(f"Suma mínima de horas de trabajo total (original): {pulp.value(prob.objective)} horas")
print("\nAsignación Óptima:")
print(df_resultados.to_markdown(index=False))
