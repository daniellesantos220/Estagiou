"""
Testes para o repositório de candidaturas (candidatura_repo).
Cobre operações CRUD, validações e integridade de dados.
"""
import pytest
from model.candidatura_model import Candidatura
from model.vaga_model import Vaga
from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario
from repo import candidatura_repo, vaga_repo, area_repo, empresa_repo, usuario_repo
from util.security import criar_hash_senha


@pytest.fixture
def area_teste(limpar_banco_dados):
    """Cria uma área de teste"""
    area = Area(id_area=0, nome="TI", descricao="")
    return area_repo.inserir(area)


@pytest.fixture
def empresa_teste(limpar_banco_dados):
    """Cria uma empresa de teste"""
    empresa = Empresa(
        id_empresa=0, nome="Tech Corp",
        cnpj="12.345.678/0001-90", descricao=""
    )
    return empresa_repo.inserir(empresa)


@pytest.fixture
def recrutador_teste(limpar_banco_dados):
    """Cria um recrutador de teste"""
    usuario = Usuario(
        id=0, nome="Recrutador",
        email="rec@test.com",
        senha=criar_hash_senha("senha"),
        perfil="RECRUTADOR"
    )
    return usuario_repo.inserir(usuario)


@pytest.fixture
def candidato_teste(limpar_banco_dados):
    """Cria um candidato de teste"""
    usuario = Usuario(
        id=0, nome="Candidato Teste",
        email="candidato@test.com",
        senha=criar_hash_senha("senha"),
        perfil="ESTUDANTE"
    )
    return usuario_repo.inserir(usuario)


@pytest.fixture
def vaga_teste(area_teste, empresa_teste, recrutador_teste):
    """Cria uma vaga de teste"""
    vaga = Vaga(
        id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
        id_recrutador=recrutador_teste, status_vaga="aberta",
        titulo="Vaga Teste", descricao="Descrição teste",
        numero_vagas=1, salario=3000.0, data_cadastro=""
    )
    return vaga_repo.inserir(vaga)


class TestCriarTabela:
    """Testes para criação da tabela de candidaturas"""

    def test_criar_tabela_sucesso(self, limpar_banco_dados):
        """Deve criar tabela de candidaturas com sucesso"""
        resultado = candidatura_repo.criar_tabela()
        assert resultado is True


class TestInserir:
    """Testes para inserção de candidaturas"""

    def test_inserir_candidatura(self, vaga_teste, candidato_teste):
        """Deve inserir candidatura com sucesso"""
        candidatura = Candidatura(
            id_candidatura=0,
            id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="",
            status="pendente"
        )

        id_candidatura = candidatura_repo.inserir(candidatura)

        assert id_candidatura is not None
        assert id_candidatura > 0

    def test_inserir_multiplas_candidaturas_mesma_vaga(self, vaga_teste, limpar_banco_dados):
        """Deve inserir múltiplas candidaturas para a mesma vaga"""
        # Criar 3 candidatos
        candidatos = []
        for i in range(3):
            usuario = Usuario(
                id=0, nome=f"Candidato {i}",
                email=f"cand{i}@test.com",
                senha=criar_hash_senha("senha"),
                perfil="ESTUDANTE"
            )
            candidatos.append(usuario_repo.inserir(usuario))

        # Inserir candidaturas
        ids = []
        for id_candidato in candidatos:
            candidatura = Candidatura(
                id_candidatura=0,
                id_vaga=vaga_teste,
                id_candidato=id_candidato,
                data_candidatura="",
                status="pendente"
            )
            ids.append(candidatura_repo.inserir(candidatura))

        assert len(ids) == 3
        assert all(id_c > 0 for id_c in ids)

    def test_inserir_candidato_multiplas_vagas(
        self, area_teste, empresa_teste, recrutador_teste, candidato_teste
    ):
        """Deve permitir candidato se candidatar a múltiplas vagas"""
        # Criar 2 vagas
        vagas = []
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vagas.append(vaga_repo.inserir(vaga))

        # Candidatar-se às 2 vagas
        ids = []
        for id_vaga in vagas:
            candidatura = Candidatura(
                id_candidatura=0,
                id_vaga=id_vaga,
                id_candidato=candidato_teste,
                data_candidatura="",
                status="pendente"
            )
            ids.append(candidatura_repo.inserir(candidatura))

        assert len(ids) == 2
        assert all(id_c > 0 for id_c in ids)


class TestAlterarStatus:
    """Testes para alteração de status de candidatura"""

    def test_alterar_status_para_em_analise(self, vaga_teste, candidato_teste):
        """Deve alterar status para em_analise"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        resultado = candidatura_repo.alterar_status(id_candidatura, "em_analise")

        assert resultado is True

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
        assert candidatura_obtida.status == "em_analise"

    def test_alterar_status_para_aprovado(self, vaga_teste, candidato_teste):
        """Deve alterar status para aprovado"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        resultado = candidatura_repo.alterar_status(id_candidatura, "aprovado")

        assert resultado is True

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
        assert candidatura_obtida.status == "aprovado"

    def test_alterar_status_para_rejeitado(self, vaga_teste, candidato_teste):
        """Deve alterar status para rejeitado"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="em_analise"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        resultado = candidatura_repo.alterar_status(id_candidatura, "rejeitado")

        assert resultado is True

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
        assert candidatura_obtida.status == "rejeitado"

    def test_alterar_status_para_cancelado(self, vaga_teste, candidato_teste):
        """Deve alterar status para cancelado"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        resultado = candidatura_repo.alterar_status(id_candidatura, "cancelado")

        assert resultado is True

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
        assert candidatura_obtida.status == "cancelado"

    def test_alterar_status_candidatura_inexistente(self):
        """Deve retornar False ao alterar status de candidatura inexistente"""
        resultado = candidatura_repo.alterar_status(999, "aprovado")
        assert resultado is False


class TestExcluir:
    """Testes para exclusão de candidaturas"""

    def test_excluir_candidatura_existente(self, vaga_teste, candidato_teste):
        """Deve excluir candidatura existente"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        resultado = candidatura_repo.excluir(id_candidatura)

        assert resultado is True
        assert candidatura_repo.obter_por_id(id_candidatura) is None

    def test_excluir_candidatura_inexistente(self):
        """Deve retornar False ao excluir candidatura inexistente"""
        resultado = candidatura_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de candidatura por ID"""

    def test_obter_candidatura_existente(self, vaga_teste, candidato_teste):
        """Deve obter candidatura por ID"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)

        assert candidatura_obtida is not None
        assert candidatura_obtida.id_candidatura == id_candidatura
        assert candidatura_obtida.id_vaga == vaga_teste
        assert candidatura_obtida.id_candidato == candidato_teste
        assert candidatura_obtida.status == "pendente"

    def test_obter_candidatura_com_data(self, vaga_teste, candidato_teste):
        """Deve obter candidatura com data de cadastro"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)

        assert candidatura_obtida.data_candidatura is not None

    def test_obter_candidatura_inexistente(self):
        """Deve retornar None para candidatura inexistente"""
        candidatura = candidatura_repo.obter_por_id(999)
        assert candidatura is None


class TestObterPorVaga:
    """Testes para busca de candidaturas por vaga"""

    def test_obter_por_vaga_sem_candidaturas(self, vaga_teste):
        """Deve retornar lista vazia para vaga sem candidaturas"""
        candidaturas = candidatura_repo.obter_por_vaga(vaga_teste)
        assert candidaturas == []

    def test_obter_por_vaga_com_candidaturas(self, vaga_teste, limpar_banco_dados):
        """Deve retornar todas as candidaturas de uma vaga"""
        # Criar 3 candidatos
        for i in range(3):
            usuario = Usuario(
                id=0, nome=f"Candidato {i}",
                email=f"cand{i}@test.com",
                senha=criar_hash_senha("senha"),
                perfil="ESTUDANTE"
            )
            id_candidato = usuario_repo.inserir(usuario)

            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=id_candidato,
                data_candidatura="", status="pendente"
            )
            candidatura_repo.inserir(candidatura)

        candidaturas = candidatura_repo.obter_por_vaga(vaga_teste)

        assert len(candidaturas) == 3
        assert all(isinstance(c, Candidatura) for c in candidaturas)
        assert all(c.id_vaga == vaga_teste for c in candidaturas)


class TestObterPorCandidato:
    """Testes para busca de candidaturas por candidato"""

    def test_obter_por_candidato_sem_candidaturas(self, candidato_teste):
        """Deve retornar lista vazia para candidato sem candidaturas"""
        candidaturas = candidatura_repo.obter_por_candidato(candidato_teste)
        assert candidaturas == []

    def test_obter_por_candidato_com_candidaturas(
        self, area_teste, empresa_teste, recrutador_teste, candidato_teste
    ):
        """Deve retornar todas as candidaturas de um candidato"""
        # Criar 2 vagas
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            id_vaga = vaga_repo.inserir(vaga)

            candidatura = Candidatura(
                id_candidatura=0, id_vaga=id_vaga,
                id_candidato=candidato_teste,
                data_candidatura="", status="pendente"
            )
            candidatura_repo.inserir(candidatura)

        candidaturas = candidatura_repo.obter_por_candidato(candidato_teste)

        assert len(candidaturas) == 2
        assert all(isinstance(c, Candidatura) for c in candidaturas)
        assert all(c.id_candidato == candidato_teste for c in candidaturas)


class TestObterPorStatus:
    """Testes para busca de candidaturas por status"""

    def test_obter_por_status(self, vaga_teste, limpar_banco_dados):
        """Deve filtrar candidaturas por status"""
        # Criar candidatos com diferentes status
        status_list = ["pendente", "pendente", "aprovado", "rejeitado"]

        for i, status in enumerate(status_list):
            usuario = Usuario(
                id=0, nome=f"Candidato {i}",
                email=f"cand{i}@test.com",
                senha=criar_hash_senha("senha"),
                perfil="ESTUDANTE"
            )
            id_candidato = usuario_repo.inserir(usuario)

            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=id_candidato,
                data_candidatura="", status="pendente"
            )
            id_candidatura = candidatura_repo.inserir(candidatura)

            # Alterar para o status desejado
            if status != "pendente":
                candidatura_repo.alterar_status(id_candidatura, status)

        candidaturas_pendentes = candidatura_repo.obter_por_status("pendente")
        candidaturas_aprovadas = candidatura_repo.obter_por_status("aprovado")

        assert len(candidaturas_pendentes) == 2
        assert len(candidaturas_aprovadas) == 1
        assert all(c.status == "pendente" for c in candidaturas_pendentes)
        assert all(c.status == "aprovado" for c in candidaturas_aprovadas)


class TestObterQuantidade:
    """Testes para contagem de candidaturas"""

    def test_quantidade_inicial_zero(self, limpar_banco_dados):
        """Deve retornar 0 quando não há candidaturas"""
        quantidade = candidatura_repo.obter_quantidade()
        assert quantidade == 0

    def test_quantidade_apos_insercoes(self, vaga_teste, limpar_banco_dados):
        """Deve contar corretamente após inserções"""
        for i in range(4):
            usuario = Usuario(
                id=0, nome=f"Candidato {i}",
                email=f"cand{i}@test.com",
                senha=criar_hash_senha("senha"),
                perfil="ESTUDANTE"
            )
            id_candidato = usuario_repo.inserir(usuario)

            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=id_candidato,
                data_candidatura="", status="pendente"
            )
            candidatura_repo.inserir(candidatura)

        quantidade = candidatura_repo.obter_quantidade()
        assert quantidade == 4


class TestVerificarCandidatura:
    """Testes para verificação de candidatura existente"""

    def test_verificar_candidatura_existente(self, vaga_teste, candidato_teste):
        """Deve retornar True se candidatura existe"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        candidatura_repo.inserir(candidatura)

        existe = candidatura_repo.verificar_candidatura(vaga_teste, candidato_teste)

        assert existe is True

    def test_verificar_candidatura_inexistente(self, vaga_teste, candidato_teste):
        """Deve retornar False se candidatura não existe"""
        existe = candidatura_repo.verificar_candidatura(vaga_teste, candidato_teste)
        assert existe is False


class TestIntegridadeDados:
    """Testes de integridade e validação de dados"""

    def test_status_default_pendente(self, vaga_teste, candidato_teste):
        """Status padrão deve ser 'pendente'"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
        assert candidatura_obtida.status == "pendente"

    def test_data_candidatura_automatica(self, vaga_teste, candidato_teste):
        """Data de candidatura deve ser gerada automaticamente"""
        candidatura = Candidatura(
            id_candidatura=0, id_vaga=vaga_teste,
            id_candidato=candidato_teste,
            data_candidatura="", status="pendente"
        )
        id_candidatura = candidatura_repo.inserir(candidatura)

        candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
        assert candidatura_obtida.data_candidatura is not None
        assert candidatura_obtida.data_candidatura != ""

    def test_todos_status_validos(self, vaga_teste, candidato_teste):
        """Deve aceitar todos os status válidos"""
        status_validos = ["pendente", "em_analise", "aprovado", "rejeitado", "cancelado"]

        for status in status_validos:
            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=candidato_teste,
                data_candidatura="", status="pendente"
            )
            id_candidatura = candidatura_repo.inserir(candidatura)

            # Alterar para o status desejado
            if status != "pendente":
                candidatura_repo.alterar_status(id_candidatura, status)

            candidatura_obtida = candidatura_repo.obter_por_id(id_candidatura)
            assert candidatura_obtida.status == status

            # Limpar para próximo teste
            candidatura_repo.excluir(id_candidatura)


class TestObterQuantidadePorVaga:
    """Testes para contagem de candidaturas por vaga"""

    def test_obter_quantidade_por_vaga(self, vaga_teste, limpar_banco_dados):
        """Deve contar candidaturas de uma vaga específica"""
        for i in range(3):
            usuario = Usuario(
                id=0, nome=f"Cand {i}", email=f"c{i}@test.com",
                senha=criar_hash_senha("senha"), perfil="ESTUDANTE"
            )
            id_candidato = usuario_repo.inserir(usuario)
            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=id_candidato, data_candidatura="", status="pendente"
            )
            candidatura_repo.inserir(candidatura)

        quantidade = candidatura_repo.obter_quantidade_por_vaga(vaga_teste)
        assert quantidade == 3


class TestObterQuantidadePorCandidato:
    """Testes para contagem de candidaturas por candidato"""

    def test_obter_quantidade_por_candidato(self, area_teste, empresa_teste, recrutador_teste, candidato_teste):
        """Deve contar candidaturas de um candidato específico"""
        # Criar múltiplas vagas e candidatar o mesmo candidato
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1, salario=0.0, data_cadastro=""
            )
            id_vaga = vaga_repo.inserir(vaga)

            candidatura = Candidatura(
                id_candidatura=0, id_vaga=id_vaga,
                id_candidato=candidato_teste, data_candidatura="", status="pendente"
            )
            candidatura_repo.inserir(candidatura)

        quantidade = candidatura_repo.obter_quantidade_por_candidato(candidato_teste)
        assert quantidade == 2


class TestObterQuantidadePorStatus:
    """Testes para contagem de candidaturas por status"""

    def test_obter_quantidade_por_status(self, vaga_teste, limpar_banco_dados):
        """Deve contar candidaturas por status"""
        for i in range(3):
            usuario = Usuario(
                id=0, nome=f"Cand {i}", email=f"c{i}@test.com",
                senha=criar_hash_senha("senha"), perfil="ESTUDANTE"
            )
            id_candidato = usuario_repo.inserir(usuario)
            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=id_candidato, data_candidatura="", status="pendente"
            )
            id_cand = candidatura_repo.inserir(candidatura)

            # Alterar status de 1 para aprovado
            if i == 0:
                candidatura_repo.alterar_status(id_cand, "aprovado")

        qtd_pendentes = candidatura_repo.obter_quantidade_por_status("pendente")
        qtd_aprovados = candidatura_repo.obter_quantidade_por_status("aprovado")

        assert qtd_pendentes == 2
        assert qtd_aprovados == 1


class TestBuscarPorStatusEVaga:
    """Testes para busca por status e vaga"""

    def test_buscar_por_status_e_vaga(self, vaga_teste, limpar_banco_dados):
        """Deve filtrar candidaturas por vaga e status"""
        for i in range(3):
            usuario = Usuario(
                id=0, nome=f"Cand {i}", email=f"c{i}@test.com",
                senha=criar_hash_senha("senha"), perfil="ESTUDANTE"
            )
            id_candidato = usuario_repo.inserir(usuario)
            candidatura = Candidatura(
                id_candidatura=0, id_vaga=vaga_teste,
                id_candidato=id_candidato, data_candidatura="", status="pendente"
            )
            id_cand = candidatura_repo.inserir(candidatura)

            # Aprovar 2 candidaturas
            if i < 2:
                candidatura_repo.alterar_status(id_cand, "aprovado")

        candidaturas_aprovadas = candidatura_repo.buscar_por_status_e_vaga(vaga_teste, "aprovado")
        candidaturas_pendentes = candidatura_repo.buscar_por_status_e_vaga(vaga_teste, "pendente")

        assert len(candidaturas_aprovadas) == 2
        assert len(candidaturas_pendentes) == 1
