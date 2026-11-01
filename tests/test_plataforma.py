import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from construir_plataforma import PUBLIC,build,permute_options


class PlatformTests(unittest.TestCase):
    def test_build_inclui_apenas_arquivos_publicos(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);shutil.copytree(ROOT/'data',root/'data');(root/'plataforma').mkdir()
            for name in PUBLIC:
                (root/'plataforma'/name).parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/'plataforma'/name,root/'plataforma'/name)
            (root/'plataforma/nao-publicar.txt').write_text('Sentinela fictícia de teste')
            release=build(root/'dist',root)
            self.assertEqual(set(str(p.relative_to(root/'dist')) for p in (root/'dist').rglob('*') if p.is_file()),set(PUBLIC)|{'release.json','.nojekyll'})
            self.assertEqual(release['disciplinas'],108)
            catalog=json.loads((root/'dist/catalogo.json').read_text())
            self.assertEqual(sum(len(s['unidades']) for s in catalog),447)

    def test_build_rejeita_pasta_com_arquivos_alheios(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'dist').mkdir();(root/'dist/outro.txt').write_text('Sentinela fictícia')
            with self.assertRaises(ValueError):build(root/'dist',root)
            self.assertTrue((root/'dist/outro.txt').is_file())

    def test_build_nao_sobrescreve_fonte(self):
        with self.assertRaises(ValueError):build(ROOT/'plataforma')
        with self.assertRaises(ValueError):build(ROOT)

    def test_barreira_de_publicacao_verifica_subpastas(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'dist/vendor/colorfigures/privado.txt';p.parent.mkdir(parents=True);p.write_text('Sentinela fictícia')
            with self.assertRaises(ValueError):build(root/'dist',root)
            self.assertTrue(p.exists())

    def test_permutacao_preserva_resposta_e_feedback(self):
        lessons=json.loads((ROOT/'data/conteudos-fundamentos.json').read_text())
        rotated=permute_options(lessons)
        for original,compiled in zip(lessons,rotated):
            for a,b in zip(original['questoes'],compiled['questoes']):
                self.assertEqual(a['alternativas'][a['correta']],b['alternativas'][b['correta']])
                self.assertEqual(a['feedback'][a['correta']],b['feedback'][b['correta']])
        self.assertGreater(len({q['correta'] for l in rotated for q in l['questoes']}),1)
