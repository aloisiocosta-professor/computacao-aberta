"""Integridade das relações exportadas, sem avaliar aprendizagem."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from mapa import build_graph, validate_graph


class MapaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph()

    def test_uma_unidade_por_habilidade(self):
        import json
        root = Path(__file__).resolve().parents[1]
        expected = {'habilidade:' + h['id'] for h in json.loads((root/'data/habilidades.json').read_text())}
        actual = {n['id'] for n in self.graph['nodes'] if n['id'].startswith('habilidade:')}
        self.assertEqual(actual, expected)

    def test_determinismo(self):
        self.assertEqual(self.graph, build_graph())

    def test_referencias_nao_sao_suporte_confirmado(self):
        edges = [e for e in self.graph['edges'] if e['target'].startswith('fonte:')]
        self.assertTrue(edges)
        self.assertTrue(all(e['type']=='related' and 'CANDIDATA' in e['description'] for e in edges))

    def test_pre_requisito_direcao(self):
        self.assertTrue(any(e['source']=='habilidade:U-PRG01-02' and e['target']=='habilidade:U-PRG01-01'
                            and e['type']=='depends_on' for e in self.graph['edges']))

    def test_rejeita_no_ausente(self):
        g = copy.deepcopy(self.graph)
        g['edges'][0]['target'] = 'inexistente'
        with self.assertRaises(ValueError): validate_graph(g)

    def test_rejeita_path_externo(self):
        g = copy.deepcopy(self.graph)
        g['nodes'][0]['filePath'] = '../segredo.txt'
        with self.assertRaises(ValueError): validate_graph(g)

    def test_rejeita_camada_duplicada(self):
        g = copy.deepcopy(self.graph)
        g['layers'][0]['nodeIds'].append(g['nodes'][0]['id'])
        with self.assertRaises(ValueError): validate_graph(g)

    def test_tour_leva_a_pratica(self):
        self.assertEqual(self.graph['tour'][-1]['nodeIds'], ['missao:M01'])
        self.assertEqual(len(self.graph['tour']), 5)
