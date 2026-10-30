import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"laboratorio"))
import referencia
class LaboratorioTests(unittest.TestCase):
    def test_soma_inclui_cada_valor(self):
        self.assertEqual(referencia.somar([3,5,2]),10)
    def test_lista_vazia(self):
        self.assertEqual(referencia.somar([]),0)
        self.assertEqual(referencia.contar_alertas([],12),0)
    def test_fronteira_alerta(self):
        self.assertEqual([referencia.classificar(x,12) for x in [11,12,13]],["normal","alerta","alerta"])
    def test_contagem(self):
        self.assertEqual(referencia.contar_alertas([11,12,13,7],12),2)
    def test_integracao(self):
        self.assertEqual(referencia.resumir([3,5,2],10),{"total":10,"estado":"alerta"})
if __name__=="__main__":unittest.main()
