"""Regressões de integridade: candidatos não podem virar evidência por omissão."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from relacoes import validate_relations
def load(name):return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf-8"))
class RelationTests(unittest.TestCase):
    def setUp(self):
        self.relations=load("relacoes-fontes")
        self.subjects=load("disciplinas")
        self.refs=load("referencias")
        self.functions=load("funcoes-fontes")
    def errors(self):
        return validate_relations(self.relations,self.subjects,self.refs,self.functions)
    def test_initial_candidates_are_valid_without_claiming_support(self):
        self.relations[0].update(status_decisao="PROPOSTO",status_evidencia="NÃO VERIFICADO",localizacao=None,alegacao_sustentada=None)
        self.assertEqual(self.errors(),[])
    def test_confirmed_support_requires_location_and_claim(self):
        self.relations[0].update(status_evidencia="CONFIRMADO",localizacao=None,alegacao_sustentada=None)
        self.assertTrue(any("exige localização e alegação" in e for e in self.errors()))
    def test_located_claim_can_pass_structure_without_scientific_certification(self):
        r=self.relations[0]
        r.update(status_evidencia="CONFIRMADO",localizacao="Seção fictícia para teste",alegacao_sustentada="Alegação fictícia para teste estrutural")
        self.assertEqual(self.errors(),[])
    def test_source_limitation_requires_location(self):
        self.relations[0]["limitacoes"]=[{"tipo":"relatada_na_fonte","descricao":"Limitação fictícia para teste","origem":"fonte","localizacao":None,"status_evidencia":"PARCIAL"}]
        self.assertTrue(any("limitação atribuída à fonte" in e for e in self.errors()))
    def test_access_limitation_cannot_be_relabelled_as_source_statement(self):
        self.relations[0]["limitacoes"][0]["tipo"]="relatada_na_fonte"
        self.assertTrue(any("limitação atribuída à fonte" in e for e in self.errors()))
    def test_proposed_study_limit_requires_identified_proposer(self):
        self.relations[0]["limitacoes"][0].update(tipo="proposta_para_estudo",origem="fonte")
        self.assertTrue(any("deve identificar quem a propõe" in e for e in self.errors()))
    def suggestion(self):
        return next(r["sugestoes_pesquisa"][0] for r in self.relations if r["sugestoes_pesquisa"])
    def test_source_research_suggestion_requires_location(self):
        self.suggestion()["origem"]="fonte"
        self.suggestion()["localizacao_na_fonte"]=None
        self.assertTrue(any("sugestão atribuída à fonte" in e for e in self.errors()))
    def test_assistant_question_is_not_proof_of_research_gap(self):
        self.suggestion().update(lacuna_comprovada=True,origem="assistente",status_evidencia="NÃO VERIFICADO",localizacao_na_fonte=None)
        self.assertTrue(any("lacuna comprovada exige evidência" in e for e in self.errors()))
    def test_duplicate_relationship_is_rejected(self):
        self.relations.append(copy.deepcopy(self.relations[0]))
        self.assertTrue(any("duplicado" in e for e in self.errors()))
    def test_unknown_role_is_rejected(self):
        self.relations[0]["funcoes_propostas"]=["funcao_inexistente"]
        self.assertTrue(any("função acadêmica ausente ou inválida" in e for e in self.errors()))
    def test_missing_candidate_relationship_is_rejected(self):
        self.relations.pop()
        self.assertTrue(any("Relação candidata ausente" in e for e in self.errors()))
    def test_dangling_reference_is_rejected(self):
        self.relations[0]["referencia"]="B999"
        self.assertTrue(any("referência inexistente" in e for e in self.errors()))
if __name__=="__main__":unittest.main()
