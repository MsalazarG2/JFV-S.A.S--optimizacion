
import pulp
import pandas as pd

profesionales = ["Ana", "Carlos", "Laura", "Miguel", "Sofía", "Andrés"]
tareas = ["T1", "T2", "T3", "T4", "T5", "T6"]

tiempos = [
    [12, 18, 15, 20, 14, 16],
    [16, 11, 19, 14, 17, 13],
    [14, 16, 10, 18, 15, 17],
    [18, 13, 16, 11, 19, 15],
    [15, 17, 14, 16, 9, 18],
    [17, 14, 18, 15, 16, 10]
]

modelo = pulp.LpProblem("Asignacion_JFV", pulp.LpMinimize)

x = {
    (i, j): pulp.LpVariable(
        f"x_{i}_{j}", cat="Binary"
    )
    for i in range(6)
    for j in range(6)
}

# Funcion objetivo
modelo += pulp.lpSum(
    tiempos[i][j] * x[i, j]
    for i in range(6)
    for j in range(6)
)

# Cada tarea recibe exactamente un profesional
for j in range(6):
    modelo += pulp.lpSum(
        x[i, j] for i in range(6)
    ) == 1

# Cada profesional recibe exactamente una tarea
for i in range(6):
    modelo += pulp.lpSum(
        x[i, j] for j in range(6)
    ) == 1

# Restricciones adicionales
modelo += x[0, 3] == 0  # Ana no puede T4
modelo += x[1, 2] == 0  # Carlos no puede T3
modelo += x[4, 4] == 1  # Sofia debe realizar T5

# Resolver
modelo.solve(pulp.PULP_CBC_CMD(msg=False))

print("Estado:", pulp.LpStatus[modelo.status])

if modelo.status == pulp.LpStatusOptimal:
    resultados = []

    for i in range(6):
        for j in range(6):
            if pulp.value(x[i, j]) > 0.5:
                resultados.append({
                    "Profesional": profesionales[i],
                    "Tarea": tareas[j],
                    "Horas": tiempos[i][j]
                })

    df = pd.DataFrame(resultados)
    print(df.to_string(index=False))
    print("Total minimo:", pulp.value(modelo.objective), "horas")
else:
    print("No existe una solucion optima factible.")
