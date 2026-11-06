def agregar_tarea(tareas, titulo, categoria="general"):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("El título es obligatorio")
    categoria = (categoria or "").strip()
    if not categoria:
        raise ValueError("La categoría es obligatoria")
    tarea = {
        # max + 1 en lugar de len + 1: tras eliminar tareas, len + 1 podría
        # repetir un ID que todavía existe en la lista. El ID es único solo
        # entre las tareas actuales: si se eliminó la tarea con el ID más
        # alto, la siguiente tarea agregada reutiliza ese ID.
        "id": max((t["id"] for t in tareas), default=0) + 1,
        "titulo": titulo,
        "categoria": categoria,
        "completada": False,
    }
    tareas.append(tarea)
    return tarea


def completar_tarea(tareas, tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["completada"] = True
            return tarea
    raise ValueError("Tarea no encontrada")


def eliminar_tarea(tareas, tarea_id):
    for indice, tarea in enumerate(tareas):
        if tarea["id"] == tarea_id:
            return tareas.pop(indice)
    raise ValueError("Tarea no encontrada")


def pendientes(tareas, categoria=None):
    resultado = [t for t in tareas if not t["completada"]]
    if categoria is None:
        return resultado
    buscada = categoria.strip().casefold()
    if not buscada:
        raise ValueError("La categoría es obligatoria")
    return [t for t in resultado if t["categoria"].casefold() == buscada]
