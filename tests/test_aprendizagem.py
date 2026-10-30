"""Testes do vínculo item/unidade e da separação entre exposição e desempenho."""
from pathlib import Path
import copy,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from aprendizagem import validate_learning,validate_progress
def load(n):return json.loads((ROOT/"data"/(n+".json")).read_text(encoding="utf-8"))
class LearningTests(unittest.TestCase):
    def setUp(self):
        self.subs=load("disciplinas");self.courses=load("cursos")
        self.indices=load("indices-disciplinas")+load("indices-cursos")
        self.skills=load("habilidades");self.profiles=load("perfis-habilidades");self.missions=load("missoes")
    def errors(self):return validate_learning(self.subs,self.courses,self.indices,self.skills,self.profiles,self.missions)
    def test_registered_items_have_units(self):self.assertEqual(self.errors(),[])
    def test_missing_unit_is_rejected(self):
        self.skills.pop()
        self.assertTrue(any("exatamente uma" in e for e in self.errors()))
    def test_invented_index_item_is_rejected(self):
        self.skills[0]["item"]="item_inexistente"
        self.assertTrue(any("item inexistente" in e for e in self.errors()))
    def test_authorial_index_drift_is_rejected(self):
        self.indices[0]["itens"][0]["titulo"]="Título alterado só no índice"
        self.assertTrue(any("não corresponde aos tópicos" in e for e in self.errors()))
    def test_external_index_without_origin_is_rejected(self):
        next(ix for ix in self.indices if ix["tipo"]=="curso_externo")["fonte_url"]=None
        self.assertTrue(any("sem origem" in e for e in self.errors()))
    def test_skill_cycle_is_rejected(self):
        self.skills[0]["pre_requisitos"]=[self.skills[0]["id"]]
        self.assertTrue(any("Ciclo nas habilidades" in e for e in self.errors()))
    def test_visual_requires_text_alternative(self):
        self.profiles[0]["visualizacao"]["alternativa_textual"]=""
        self.assertTrue(any("alternativa textual" in e for e in self.errors()))
    def test_mission_requires_explained_contributions(self):
        self.missions[0]["contribuicoes"]={}
        self.assertTrue(any("contribuição" in e for e in self.errors()))
    def test_ready_lesson_requires_file_reference(self):
        self.skills[0].update(estado_editorial="AULA_INICIAL",aula_local=None)
        self.assertTrue(any("Aula sem arquivo" in e for e in self.errors()))
    def fixture(self):
        return {"id":"ficticio-1","unidade":"U-PRG01-01","estado":"desempenho_independente","data":"2026-10-30","apoio":"nenhum","artefatos":["artefato-ficticio-apenas-para-teste"],"avaliador":"ferramenta fictícia de teste","justificativa":"Somente fixture estrutural; não relata desempenho real.","criterios_atendidos":["correcao","explicacao","representacao","limites"],"contexto":"caso fictício A"}
    def test_empty_progress_does_not_invent_learning(self):self.assertEqual(validate_progress({"registros":[]},self.skills),[])
    def test_reading_is_only_exposure(self):
        r=self.fixture();r.update(estado="exposicao",apoio="nao_informado",artefatos=[],criterios_atendidos=[])
        self.assertEqual(validate_progress({"registros":[r]},self.skills),[])
    def test_independence_with_solution_is_rejected(self):
        r=self.fixture();r["apoio"]="solucao"
        self.assertTrue(any("não pode usar" in e for e in validate_progress({"registros":[r]},self.skills)))
    def test_independence_without_artifact_is_rejected(self):
        r=self.fixture();r["artefatos"]=[]
        self.assertTrue(any("exige artefato" in e for e in validate_progress({"registros":[r]},self.skills)))
    def test_transfer_requires_different_context(self):
        first=self.fixture();second=copy.deepcopy(first);second.update(id="ficticio-2",estado="transferencia_demonstrada",registro_anterior=first["id"])
        self.assertTrue(any("contexto diferente" in e for e in validate_progress({"registros":[first,second]},self.skills)))
    def test_retention_requires_later_date(self):
        first=self.fixture();second=copy.deepcopy(first);second.update(id="ficticio-2",estado="retencao_verificada",registro_anterior=first["id"])
        self.assertTrue(any("data posterior" in e for e in validate_progress({"registros":[first,second]},self.skills)))
    def test_well_formed_evidence_is_only_structurally_accepted(self):
        first=self.fixture();second=copy.deepcopy(first);second.update(id="ficticio-2",estado="transferencia_demonstrada",registro_anterior=first["id"],contexto="caso fictício B")
        self.assertEqual(validate_progress({"registros":[first,second]},self.skills),[])
    def test_invalid_progress_shape_is_rejected(self):
        self.assertTrue(validate_progress({"registros":"texto"},self.skills))
if __name__=="__main__":unittest.main()
