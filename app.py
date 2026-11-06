from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes

tareas = []
agregar_tarea(tareas, "Estudiar agentes cloud", "Estudio")
agregar_tarea(tareas, "Preparar laboratorio", "Laboratorio")
agregar_tarea(tareas, "Repasar Git", "estudio")
completar_tarea(tareas, 1)

print("Pendientes:")
for tarea in pendientes(tareas):
    print(f'- {tarea["id"]}: {tarea["titulo"]} [{tarea["categoria"]}]')

print("\nPendientes de la categoría 'estudio':")
for tarea in pendientes(tareas, "estudio"):
    print(f'- {tarea["id"]}: {tarea["titulo"]} [{tarea["categoria"]}]')

eliminada = eliminar_tarea(tareas, 2)
print(f'\nTarea eliminada: {eliminada["id"]}: {eliminada["titulo"]}')

print("\nTareas restantes:")
for tarea in tareas:
    estado = "completada" if tarea["completada"] else "pendiente"
    print(f'- {tarea["id"]}: {tarea["titulo"]} [{tarea["categoria"]}] ({estado})')
