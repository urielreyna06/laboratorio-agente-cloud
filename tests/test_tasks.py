import unittest
from tasks import agregar_tarea, completar_tarea, pendientes


class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertFalse(tarea["completada"])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_agregar_tarea_categoria_por_defecto(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Sin categoría explícita")
        self.assertEqual(tarea["categoria"], "general")

    def test_agregar_tarea_categoria_valida(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer artículo", "Estudio")
        self.assertEqual(tarea["categoria"], "Estudio")
        self.assertIn(tarea, tareas)

    def test_agregar_tarea_categoria_vacia(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Tarea", "")
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Tarea", "   ")
        self.assertEqual(tareas, [])

    def test_pendientes_filtra_por_categoria_sin_distinguir_mayusculas(self):
        tareas = []
        agregar_tarea(tareas, "Estudiar", "Estudio")
        agregar_tarea(tareas, "Comprar pan", "Casa")
        agregar_tarea(tareas, "Repasar", "ESTUDIO")
        agregar_tarea(tareas, "Leer", "estudio")
        completar_tarea(tareas, 4)
        titulos = [t["titulo"] for t in pendientes(tareas, "estudio")]
        self.assertEqual(titulos, ["Estudiar", "Repasar"])
        self.assertEqual(
            [t["titulo"] for t in pendientes(tareas, "CASA")], ["Comprar pan"]
        )
        self.assertEqual(pendientes(tareas, "Trabajo"), [])

    def test_pendientes_sin_categoria_devuelve_todas(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        self.assertEqual(len(pendientes(tareas)), 2)


if __name__ == "__main__":
    unittest.main()
