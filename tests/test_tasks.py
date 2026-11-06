import unittest
from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes


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

    def test_pendientes_categoria_inexistente_devuelve_lista_vacia(self):
        tareas = []
        agregar_tarea(tareas, "Estudiar", "Estudio")
        agregar_tarea(tareas, "Comprar pan", "Casa")
        self.assertEqual(pendientes(tareas, "Trabajo"), [])

    def test_pendientes_categoria_vacia_lanza_error(self):
        tareas = []
        agregar_tarea(tareas, "Estudiar", "Estudio")
        for categoria in ("", "   "):
            with self.assertRaisesRegex(ValueError, "La categoría es obligatoria"):
                pendientes(tareas, categoria)

    def test_pendientes_sin_categoria_devuelve_todas(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        self.assertEqual(len(pendientes(tareas)), 2)

    def test_eliminar_tarea_existente(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        lista_original = tareas
        eliminada = eliminar_tarea(tareas, 1)
        self.assertEqual(eliminada["id"], 1)
        self.assertEqual(eliminada["titulo"], "Uno")
        self.assertIs(tareas, lista_original)
        self.assertNotIn(eliminada, tareas)
        self.assertEqual(len(tareas), 1)

    def test_eliminar_tarea_id_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        copia = [dict(t) for t in tareas]
        with self.assertRaisesRegex(ValueError, "Tarea no encontrada"):
            eliminar_tarea(tareas, 99)
        self.assertEqual(tareas, copia)
        with self.assertRaisesRegex(ValueError, "Tarea no encontrada"):
            eliminar_tarea([], 1)

    def test_eliminar_tarea_conserva_las_demas(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        agregar_tarea(tareas, "Tres", "C")
        completar_tarea(tareas, 3)
        esperadas = [dict(tareas[0]), dict(tareas[2])]
        eliminar_tarea(tareas, 2)
        self.assertEqual(tareas, esperadas)
        self.assertEqual([t["id"] for t in tareas], [1, 3])

    def test_eliminar_tarea_completada(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        completar_tarea(tareas, 1)
        eliminada = eliminar_tarea(tareas, 1)
        self.assertTrue(eliminada["completada"])
        self.assertEqual([t["id"] for t in tareas], [2])
        self.assertEqual([t["id"] for t in pendientes(tareas)], [2])

    def test_agregar_tras_eliminar_no_repite_ids(self):
        tareas = []
        agregar_tarea(tareas, "Uno", "A")
        agregar_tarea(tareas, "Dos", "B")
        eliminar_tarea(tareas, 1)
        nueva = agregar_tarea(tareas, "Tres", "C")
        self.assertEqual(nueva["id"], 3)
        ids = [t["id"] for t in tareas]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
