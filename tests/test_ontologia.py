import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ontologia import export, impact, literal


class OntologyTests(unittest.TestCase):
    def test_impacto_segue_dependentes_e_missao(self):
        r=impact('U-PRG01-01')
        self.assertIn('U-PRG01-04',r['unidades_dependentes'])
        self.assertIn('M01',r['missoes_requeridas'])
        self.assertNotIn('U-PRG01-01',r['unidades_dependentes'])

    def test_impacto_nao_inverte_pre_requisito(self):
        self.assertNotIn('U-PRG01-03',impact('U-PRG01-04')['unidades_dependentes'])

    def test_unidade_inexistente_rejeitada(self):
        with self.assertRaises(ValueError):impact('U-INVENTADA')

    def test_escape_preserva_texto_sem_injetar_triplas(self):
        text='Linha "citada"\ncom barra \\ e acento ç'
        self.assertEqual(json.loads(literal(text)),text)
        self.assertNotIn('\n',literal(text))

    def test_exportacao_reproduzivel_com_origem_e_limites(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);shutil.copytree(ROOT/'data',root/'data')
            m=export(root)
            files=('esquema.ttl','dados.ttl','curriculo.ttl','manifesto.json')
            before={p:hashlib.sha256((root/'ontologia'/p).read_bytes()).hexdigest() for p in files}
            export(root)
            self.assertEqual(before,{p:hashlib.sha256((root/'ontologia'/p).read_bytes()).hexdigest() for p in files})
            self.assertEqual(m['por_classe']['UnidadeHabilidade'],len(json.loads((root/'data/habilidades.json').read_text())))
            self.assertEqual(m['validacao_cientifica'],'NÃO VERIFICADO')
            data=(root/'ontologia/dados.ttl').read_text()
            self.assertIn('ca:referenciaCandidata',data)
            self.assertIn('ca:hashOrigem',data)
            self.assertNotIn('owl:sameAs',data)
