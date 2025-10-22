"""
Testes para o repositório de áreas (area_repo).
Cobre operações CRUD, validações e integridade de dados.
"""
import pytest
from model.area_model import Area
from repo import area_repo


class TestCriarTabela:
    """Testes para criação da tabela de áreas"""

    def test_criar_tabela_sucesso(self, limpar_banco_dados):
        """Deve criar tabela de áreas com sucesso"""
        resultado = area_repo.criar_tabela()
        assert resultado is True


class TestInserir:
    """Testes para inserção de áreas"""

    def test_inserir_area_completa(self, limpar_banco_dados):
        """Deve inserir área com todos os campos"""
        area = Area(
            id_area=0,
            nome="Tecnologia da Informação",
            descricao="Área de TI e desenvolvimento de software"
        )

        id_area = area_repo.inserir(area)

        assert id_area is not None
        assert id_area > 0

    def test_inserir_area_sem_descricao(self, limpar_banco_dados):
        """Deve inserir área sem descrição"""
        area = Area(
            id_area=0,
            nome="Marketing",
            descricao=""
        )

        id_area = area_repo.inserir(area)

        assert id_area is not None
        assert id_area > 0

    def test_inserir_multiplas_areas(self, limpar_banco_dados):
        """Deve inserir múltiplas áreas"""
        areas = [
            Area(id_area=0, nome="Saúde", descricao="Área da saúde"),
            Area(id_area=0, nome="Educação", descricao="Área educacional"),
            Area(id_area=0, nome="Jurídico", descricao="Área jurídica")
        ]

        ids = [area_repo.inserir(area) for area in areas]

        assert len(ids) == 3
        assert all(id_area > 0 for id_area in ids)


class TestAlterar:
    """Testes para alteração de áreas"""

    def test_alterar_area_existente(self, limpar_banco_dados):
        """Deve alterar área existente"""
        # Inserir área
        area = Area(id_area=0, nome="TI", descricao="Tecnologia")
        id_area = area_repo.inserir(area)

        # Alterar
        area_alterada = Area(
            id_area=id_area,
            nome="Tecnologia da Informação",
            descricao="Tecnologia e Inovação"
        )
        resultado = area_repo.alterar(area_alterada)

        assert resultado is True

        # Verificar alteração
        area_obtida = area_repo.obter_por_id(id_area)
        assert area_obtida.nome == "Tecnologia da Informação"
        assert area_obtida.descricao == "Tecnologia e Inovação"

    def test_alterar_area_inexistente(self, limpar_banco_dados):
        """Deve retornar False ao alterar área inexistente"""
        area = Area(id_area=999, nome="Inexistente", descricao="")
        resultado = area_repo.alterar(area)

        assert resultado is False


class TestExcluir:
    """Testes para exclusão de áreas"""

    def test_excluir_area_existente(self, limpar_banco_dados):
        """Deve excluir área existente"""
        area = Area(id_area=0, nome="Temporária", descricao="")
        id_area = area_repo.inserir(area)

        resultado = area_repo.excluir(id_area)

        assert resultado is True
        assert area_repo.obter_por_id(id_area) is None

    def test_excluir_area_inexistente(self, limpar_banco_dados):
        """Deve retornar False ao excluir área inexistente"""
        resultado = area_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de área por ID"""

    def test_obter_area_existente(self, limpar_banco_dados):
        """Deve obter área por ID"""
        area = Area(id_area=0, nome="Engenharia", descricao="Área de engenharia")
        id_area = area_repo.inserir(area)

        area_obtida = area_repo.obter_por_id(id_area)

        assert area_obtida is not None
        assert area_obtida.id_area == id_area
        assert area_obtida.nome == "Engenharia"
        assert area_obtida.descricao == "Área de engenharia"

    def test_obter_area_inexistente(self, limpar_banco_dados):
        """Deve retornar None para área inexistente"""
        area = area_repo.obter_por_id(999)
        assert area is None


class TestObterTodas:
    """Testes para listagem de todas as áreas"""

    def test_obter_todas_vazio(self, limpar_banco_dados):
        """Deve retornar lista vazia quando não há áreas"""
        areas = area_repo.obter_todas()
        assert areas == []

    def test_obter_todas_com_areas(self, limpar_banco_dados):
        """Deve retornar todas as áreas cadastradas"""
        areas_inserir = [
            Area(id_area=0, nome="TI", descricao="Tech"),
            Area(id_area=0, nome="Saúde", descricao="Health"),
            Area(id_area=0, nome="Educação", descricao="Education")
        ]

        for area in areas_inserir:
            area_repo.inserir(area)

        areas = area_repo.obter_todas()

        assert len(areas) == 3
        assert all(isinstance(area, Area) for area in areas)
        nomes = [area.nome for area in areas]
        assert "TI" in nomes
        assert "Saúde" in nomes
        assert "Educação" in nomes


class TestObterPorNome:
    """Testes para busca de área por nome"""

    def test_obter_por_nome_existente(self, limpar_banco_dados):
        """Deve obter área por nome exato"""
        area = Area(id_area=0, nome="Design", descricao="Design gráfico")
        area_repo.inserir(area)

        area_obtida = area_repo.obter_por_nome("Design")

        assert area_obtida is not None
        assert area_obtida.nome == "Design"

    def test_obter_por_nome_inexistente(self, limpar_banco_dados):
        """Deve retornar None para nome inexistente"""
        area = area_repo.obter_por_nome("Inexistente")
        assert area is None

    def test_obter_por_nome_case_sensitive(self, limpar_banco_dados):
        """Nome deve ser case sensitive"""
        area = Area(id_area=0, nome="Marketing", descricao="")
        area_repo.inserir(area)

        area_obtida = area_repo.obter_por_nome("marketing")
        assert area_obtida is None


class TestObterQuantidade:
    """Testes para contagem de áreas"""

    def test_quantidade_inicial_zero(self, limpar_banco_dados):
        """Deve retornar 0 quando não há áreas"""
        quantidade = area_repo.obter_quantidade()
        assert quantidade == 0

    def test_quantidade_apos_insercoes(self, limpar_banco_dados):
        """Deve contar corretamente após inserções"""
        for i in range(5):
            area = Area(id_area=0, nome=f"Área {i}", descricao="")
            area_repo.inserir(area)

        quantidade = area_repo.obter_quantidade()
        assert quantidade == 5

    def test_quantidade_apos_exclusao(self, limpar_banco_dados):
        """Deve atualizar contagem após exclusão"""
        ids = []
        for i in range(3):
            area = Area(id_area=0, nome=f"Área {i}", descricao="")
            ids.append(area_repo.inserir(area))

        area_repo.excluir(ids[0])

        quantidade = area_repo.obter_quantidade()
        assert quantidade == 2


class TestVerificarUso:
    """Testes para verificação de uso de área em vagas"""

    def test_verificar_uso_area_sem_vagas(self, limpar_banco_dados):
        """Deve retornar 0 para área sem vagas"""
        area = Area(id_area=0, nome="Sem Vagas", descricao="")
        id_area = area_repo.inserir(area)

        quantidade = area_repo.verificar_uso(id_area)
        assert quantidade == 0

    def test_verificar_uso_area_inexistente(self, limpar_banco_dados):
        """Deve retornar 0 para área inexistente"""
        quantidade = area_repo.verificar_uso(999)
        assert quantidade == 0


class TestIntegridadeDados:
    """Testes de integridade e validação de dados"""

    def test_descricao_nullable(self, limpar_banco_dados):
        """Campo descricao deve aceitar valores vazios"""
        area = Area(id_area=0, nome="Teste", descricao="")
        id_area = area_repo.inserir(area)

        area_obtida = area_repo.obter_por_id(id_area)
        assert area_obtida.descricao == ""

    def test_nome_preserva_espacos(self, limpar_banco_dados):
        """Nome deve preservar espaços"""
        area = Area(id_area=0, nome="  Nome com espaços  ", descricao="")
        id_area = area_repo.inserir(area)

        area_obtida = area_repo.obter_por_id(id_area)
        assert area_obtida.nome == "  Nome com espaços  "

    def test_caracteres_especiais_nome(self, limpar_banco_dados):
        """Nome deve aceitar caracteres especiais"""
        area = Area(id_area=0, nome="TI & Tecnologia (Dev)", descricao="Área de TI")
        id_area = area_repo.inserir(area)

        area_obtida = area_repo.obter_por_id(id_area)
        assert area_obtida.nome == "TI & Tecnologia (Dev)"

    def test_descricao_longa(self, limpar_banco_dados):
        """Descrição deve aceitar texto longo"""
        descricao_longa = "A" * 1000
        area = Area(id_area=0, nome="Teste Long", descricao=descricao_longa)
        id_area = area_repo.inserir(area)

        area_obtida = area_repo.obter_por_id(id_area)
        assert len(area_obtida.descricao) == 1000
