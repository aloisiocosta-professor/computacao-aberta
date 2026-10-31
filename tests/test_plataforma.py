import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from construir_plataforma import PUBLIC,build


class PlatformTests(unittest.TestCase):
    def test_build_inclui_apenas_arquivos_publicos(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);shutil.copytree(ROOT/'data',root/'data');(root/'plataforma').mkdir()
            for name in PUBLIC:shutil.copyfile(ROOT/'plataforma'/name,root/'plataforma'/name)
            (root/'plataforma/nao-publicar.txt').write_text('Sentinela fictícia de teste')
            release=build(root/'dist',root)
            self.assertEqual(set(p.name for p in (root/'dist').iterdir()),set(PUBLIC)|{'release.json','.nojekyll'})
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
