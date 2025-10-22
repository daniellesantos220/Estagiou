"""
Testes para o repositório de empresas (empresa_repo).
Cobre operações CRUD, validações e integridade de dados.
"""
import pytest
from model.empresa_model import Empresa
from repo import empresa_repo


class TestCriarTabela:
    """Testes para criação da tabela de empresas"""

    def test_criar_tabela_sucesso(self, limpar_banco_dados):
        """Deve criar tabela de empresas com sucesso"""
        resultado = empresa_repo.criar_tabela()
        assert resultado is True


class TestInserir:
    """Testes para inserção de empresas"""

    def test_inserir_empresa_completa(self, limpar_banco_dados):
        """Deve inserir empresa com todos os campos"""
        empresa = Empresa(
            id_empresa=0,
            nome="Tech Solutions LTDA",
            cnpj="12.345.678/0001-90",
            descricao="Empresa de soluções em tecnologia"
        )

        id_empresa = empresa_repo.inserir(empresa)

        assert id_empresa is not None
        assert id_empresa > 0

    def test_inserir_empresa_sem_descricao(self, limpar_banco_dados):
        """Deve inserir empresa sem descrição"""
        empresa = Empresa(
            id_empresa=0,
            nome="Empresa Teste",
            cnpj="98.765.432/0001-10",
            descricao=""
        )

        id_empresa = empresa_repo.inserir(empresa)

        assert id_empresa is not None
        assert id_empresa > 0

    def test_inserir_multiplas_empresas(self, limpar_banco_dados):
        """Deve inserir múltiplas empresas"""
        empresas = [
            Empresa(id_empresa=0, nome="Empresa A", cnpj="11.111.111/0001-11", descricao=""),
            Empresa(id_empresa=0, nome="Empresa B", cnpj="22.222.222/0001-22", descricao=""),
            Empresa(id_empresa=0, nome="Empresa C", cnpj="33.333.333/0001-33", descricao="")
        ]

        ids = [empresa_repo.inserir(empresa) for empresa in empresas]

        assert len(ids) == 3
        assert all(id_empresa > 0 for id_empresa in ids)


class TestAlterar:
    """Testes para alteração de empresas"""

    def test_alterar_empresa_existente(self, limpar_banco_dados):
        """Deve alterar empresa existente"""
        empresa = Empresa(
            id_empresa=0,
            nome="Empresa Original",
            cnpj="12.345.678/0001-90",
            descricao="Descrição original"
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_alterada = Empresa(
            id_empresa=id_empresa,
            nome="Empresa Alterada LTDA",
            cnpj="12.345.678/0001-90",
            descricao="Nova descrição"
        )
        resultado = empresa_repo.alterar(empresa_alterada)

        assert resultado is True

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)
        assert empresa_obtida.nome == "Empresa Alterada LTDA"
        assert empresa_obtida.descricao == "Nova descrição"

    def test_alterar_empresa_inexistente(self, limpar_banco_dados):
        """Deve retornar False ao alterar empresa inexistente"""
        empresa = Empresa(
            id_empresa=999,
            nome="Inexistente",
            cnpj="99.999.999/0001-99",
            descricao=""
        )
        resultado = empresa_repo.alterar(empresa)

        assert resultado is False


class TestExcluir:
    """Testes para exclusão de empresas"""

    def test_excluir_empresa_existente(self, limpar_banco_dados):
        """Deve excluir empresa existente"""
        empresa = Empresa(
            id_empresa=0,
            nome="Temporária",
            cnpj="11.111.111/0001-11",
            descricao=""
        )
        id_empresa = empresa_repo.inserir(empresa)

        resultado = empresa_repo.excluir(id_empresa)

        assert resultado is True
        assert empresa_repo.obter_por_id(id_empresa) is None

    def test_excluir_empresa_inexistente(self, limpar_banco_dados):
        """Deve retornar False ao excluir empresa inexistente"""
        resultado = empresa_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de empresa por ID"""

    def test_obter_empresa_existente(self, limpar_banco_dados):
        """Deve obter empresa por ID"""
        empresa = Empresa(
            id_empresa=0,
            nome="Tech Corp",
            cnpj="12.345.678/0001-90",
            descricao="Empresa de tecnologia"
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)

        assert empresa_obtida is not None
        assert empresa_obtida.id_empresa == id_empresa
        assert empresa_obtida.nome == "Tech Corp"
        assert empresa_obtida.cnpj == "12.345.678/0001-90"
        assert empresa_obtida.descricao == "Empresa de tecnologia"

    def test_obter_empresa_inexistente(self, limpar_banco_dados):
        """Deve retornar None para empresa inexistente"""
        empresa = empresa_repo.obter_por_id(999)
        assert empresa is None

    def test_obter_empresa_com_data_cadastro(self, limpar_banco_dados):
        """Deve obter empresa com data de cadastro"""
        empresa = Empresa(
            id_empresa=0,
            nome="Test Company",
            cnpj="11.111.111/0001-11",
            descricao=""
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)

        assert empresa_obtida.data_cadastro is not None


class TestObterTodas:
    """Testes para listagem de todas as empresas"""

    def test_obter_todas_vazio(self, limpar_banco_dados):
        """Deve retornar lista vazia quando não há empresas"""
        empresas = empresa_repo.obter_todas()
        assert empresas == []

    def test_obter_todas_com_empresas(self, limpar_banco_dados):
        """Deve retornar todas as empresas cadastradas"""
        empresas_inserir = [
            Empresa(id_empresa=0, nome="Empresa 1", cnpj="11.111.111/0001-11", descricao=""),
            Empresa(id_empresa=0, nome="Empresa 2", cnpj="22.222.222/0001-22", descricao=""),
            Empresa(id_empresa=0, nome="Empresa 3", cnpj="33.333.333/0001-33", descricao="")
        ]

        for empresa in empresas_inserir:
            empresa_repo.inserir(empresa)

        empresas = empresa_repo.obter_todas()

        assert len(empresas) == 3
        assert all(isinstance(empresa, Empresa) for empresa in empresas)


class TestObterPorCnpj:
    """Testes para busca de empresa por CNPJ"""

    def test_obter_por_cnpj_existente(self, limpar_banco_dados):
        """Deve obter empresa por CNPJ"""
        empresa = Empresa(
            id_empresa=0,
            nome="CNPJ Test",
            cnpj="12.345.678/0001-90",
            descricao="Teste CNPJ"
        )
        empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_cnpj("12.345.678/0001-90")

        assert empresa_obtida is not None
        assert empresa_obtida.cnpj == "12.345.678/0001-90"
        assert empresa_obtida.nome == "CNPJ Test"

    def test_obter_por_cnpj_inexistente(self, limpar_banco_dados):
        """Deve retornar None para CNPJ inexistente"""
        empresa = empresa_repo.obter_por_cnpj("99.999.999/0001-99")
        assert empresa is None


class TestObterQuantidade:
    """Testes para contagem de empresas"""

    def test_quantidade_inicial_zero(self, limpar_banco_dados):
        """Deve retornar 0 quando não há empresas"""
        quantidade = empresa_repo.obter_quantidade()
        assert quantidade == 0

    def test_quantidade_apos_insercoes(self, limpar_banco_dados):
        """Deve contar corretamente após inserções"""
        for i in range(4):
            empresa = Empresa(
                id_empresa=0,
                nome=f"Empresa {i}",
                cnpj=f"{i}{i}.{i}{i}{i}.{i}{i}{i}/0001-{i}{i}",
                descricao=""
            )
            empresa_repo.inserir(empresa)

        quantidade = empresa_repo.obter_quantidade()
        assert quantidade == 4

    def test_quantidade_apos_exclusao(self, limpar_banco_dados):
        """Deve atualizar contagem após exclusão"""
        ids = []
        for i in range(3):
            empresa = Empresa(
                id_empresa=0,
                nome=f"Empresa {i}",
                cnpj=f"{i}{i}.{i}{i}{i}.{i}{i}{i}/0001-{i}{i}",
                descricao=""
            )
            ids.append(empresa_repo.inserir(empresa))

        empresa_repo.excluir(ids[0])

        quantidade = empresa_repo.obter_quantidade()
        assert quantidade == 2


class TestBuscar:
    """Testes para busca de empresas com filtros"""

    def test_buscar_sem_filtros(self, limpar_banco_dados):
        """Deve retornar todas as empresas sem filtros"""
        for i in range(3):
            empresa = Empresa(
                id_empresa=0,
                nome=f"Empresa {i}",
                cnpj=f"{i}{i}.{i}{i}{i}.{i}{i}{i}/0001-{i}{i}",
                descricao=""
            )
            empresa_repo.inserir(empresa)

        empresas = empresa_repo.buscar()
        assert len(empresas) == 3

    def test_buscar_por_nome(self, limpar_banco_dados):
        """Deve buscar empresas por nome (LIKE)"""
        empresas = [
            Empresa(id_empresa=0, nome="Tech Solutions", cnpj="11.111.111/0001-11", descricao=""),
            Empresa(id_empresa=0, nome="Tech Innovations", cnpj="22.222.222/0001-22", descricao=""),
            Empresa(id_empresa=0, nome="Health Corp", cnpj="33.333.333/0001-33", descricao="")
        ]

        for empresa in empresas:
            empresa_repo.inserir(empresa)

        resultado = empresa_repo.buscar(nome="Tech")

        assert len(resultado) == 2
        nomes = [e.nome for e in resultado]
        assert "Tech Solutions" in nomes
        assert "Tech Innovations" in nomes

    def test_buscar_com_limit(self, limpar_banco_dados):
        """Deve respeitar limite de resultados"""
        for i in range(5):
            empresa = Empresa(
                id_empresa=0,
                nome=f"Empresa {i}",
                cnpj=f"{i}{i}.{i}{i}{i}.{i}{i}{i}/0001-{i}{i}",
                descricao=""
            )
            empresa_repo.inserir(empresa)

        empresas = empresa_repo.buscar(limit=2)
        assert len(empresas) == 2

    def test_buscar_com_offset(self, limpar_banco_dados):
        """Deve respeitar offset de paginação"""
        nomes = ["Alpha", "Beta", "Gamma", "Delta"]
        for i, nome in enumerate(nomes):
            empresa = Empresa(
                id_empresa=0,
                nome=nome,
                cnpj=f"{i}{i}.{i}{i}{i}.{i}{i}{i}/0001-{i}{i}",
                descricao=""
            )
            empresa_repo.inserir(empresa)

        empresas = empresa_repo.buscar(limit=2, offset=2)
        assert len(empresas) == 2


class TestIntegridadeDados:
    """Testes de integridade e validação de dados"""

    def test_descricao_nullable(self, limpar_banco_dados):
        """Campo descricao deve aceitar valores vazios"""
        empresa = Empresa(
            id_empresa=0,
            nome="Test",
            cnpj="11.111.111/0001-11",
            descricao=""
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)
        assert empresa_obtida.descricao == ""

    def test_cnpj_formatado(self, limpar_banco_dados):
        """CNPJ deve ser armazenado com formatação"""
        empresa = Empresa(
            id_empresa=0,
            nome="Test CNPJ",
            cnpj="12.345.678/0001-90",
            descricao=""
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)
        assert empresa_obtida.cnpj == "12.345.678/0001-90"

    def test_nome_preserva_espacos(self, limpar_banco_dados):
        """Nome deve preservar espaços"""
        empresa = Empresa(
            id_empresa=0,
            nome="  Empresa com Espaços  ",
            cnpj="11.111.111/0001-11",
            descricao=""
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)
        assert empresa_obtida.nome == "  Empresa com Espaços  "

    def test_caracteres_especiais_nome(self, limpar_banco_dados):
        """Nome deve aceitar caracteres especiais"""
        empresa = Empresa(
            id_empresa=0,
            nome="Tech & Solutions (Brasil) - LTDA",
            cnpj="11.111.111/0001-11",
            descricao=""
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)
        assert empresa_obtida.nome == "Tech & Solutions (Brasil) - LTDA"

    def test_descricao_longa(self, limpar_banco_dados):
        """Descrição deve aceitar texto longo"""
        descricao_longa = "A" * 2000
        empresa = Empresa(
            id_empresa=0,
            nome="Test Long",
            cnpj="11.111.111/0001-11",
            descricao=descricao_longa
        )
        id_empresa = empresa_repo.inserir(empresa)

        empresa_obtida = empresa_repo.obter_por_id(id_empresa)
        assert len(empresa_obtida.descricao) == 2000
