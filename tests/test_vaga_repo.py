"""
Testes para o repositório de vagas (vaga_repo).
Cobre operações CRUD, validações, buscas e integridade de dados.
"""
import pytest
from model.vaga_model import Vaga
from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario
from repo import vaga_repo, area_repo, empresa_repo, usuario_repo
from util.security import criar_hash_senha


@pytest.fixture
def area_teste(limpar_banco_dados):
    """Cria uma área de teste"""
    area = Area(id_area=0, nome="Tecnologia", descricao="TI")
    return area_repo.inserir(area)


@pytest.fixture
def empresa_teste(limpar_banco_dados):
    """Cria uma empresa de teste"""
    empresa = Empresa(
        id_empresa=0,
        nome="Tech Corp",
        cnpj="12.345.678/0001-90",
        descricao="Empresa de tecnologia"
    )
    return empresa_repo.inserir(empresa)


@pytest.fixture
def recrutador_teste(limpar_banco_dados):
    """Cria um recrutador de teste"""
    usuario = Usuario(
        id=0,
        nome="Recrutador Teste",
        email="recrutador@test.com",
        senha=criar_hash_senha("senha123"),
        perfil="RECRUTADOR"
    )
    return usuario_repo.inserir(usuario)


class TestCriarTabela:
    """Testes para criação da tabela de vagas"""

    def test_criar_tabela_sucesso(self, limpar_banco_dados):
        """Deve criar tabela de vagas com sucesso"""
        resultado = vaga_repo.criar_tabela()
        assert resultado is True


class TestInserir:
    """Testes para inserção de vagas"""

    def test_inserir_vaga_completa(self, area_teste, empresa_teste, recrutador_teste):
        """Deve inserir vaga com todos os campos"""
        vaga = Vaga(
            id_vaga=0,
            id_area=area_teste,
            id_empresa=empresa_teste,
            id_recrutador=recrutador_teste,
            status_vaga="aberta",
            titulo="Desenvolvedor Python",
            descricao="Vaga para desenvolvedor Python sênior",
            numero_vagas=2,
            salario=5000.00,
            requisitos="Python, Django, PostgreSQL",
            beneficios="VT, VR, Plano de Saúde",
            carga_horaria=40,
            modalidade="Remoto",
            cidade="São Paulo",
            uf="SP",
            data_cadastro=""
        )

        id_vaga = vaga_repo.inserir(vaga)

        assert id_vaga is not None
        assert id_vaga > 0

    def test_inserir_vaga_campos_obrigatorios(self, area_teste, empresa_teste, recrutador_teste):
        """Deve inserir vaga apenas com campos obrigatórios"""
        vaga = Vaga(
            id_vaga=0,
            id_area=area_teste,
            id_empresa=empresa_teste,
            id_recrutador=recrutador_teste,
            status_vaga="aberta",
            titulo="Vaga Simples",
            descricao="Descrição básica",
            numero_vagas=1,
            salario=0.0,
            data_cadastro=""
        )

        id_vaga = vaga_repo.inserir(vaga)

        assert id_vaga is not None
        assert id_vaga > 0

    def test_inserir_multiplas_vagas(self, area_teste, empresa_teste, recrutador_teste):
        """Deve inserir múltiplas vagas"""
        vagas = [
            Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="Desc", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            for i in range(3)
        ]

        ids = [vaga_repo.inserir(vaga) for vaga in vagas]

        assert len(ids) == 3
        assert all(id_vaga > 0 for id_vaga in ids)


class TestAlterar:
    """Testes para alteração de vagas"""

    def test_alterar_vaga_existente(self, area_teste, empresa_teste, recrutador_teste):
        """Deve alterar vaga existente"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Título Original", descricao="Desc Original",
            numero_vagas=1, salario=3000.0, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        vaga_alterada = Vaga(
            id_vaga=id_vaga, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Título Alterado", descricao="Desc Alterada",
            numero_vagas=2, salario=4000.0, cidade="Rio de Janeiro",
            uf="RJ", data_cadastro=""
        )
        resultado = vaga_repo.alterar(vaga_alterada)

        assert resultado is True

        vaga_obtida = vaga_repo.obter_por_id(id_vaga)
        assert vaga_obtida.titulo == "Título Alterado"
        assert vaga_obtida.salario == 4000.0
        assert vaga_obtida.cidade == "Rio de Janeiro"

    def test_alterar_vaga_inexistente(self, area_teste):
        """Deve retornar False ao alterar vaga inexistente"""
        vaga = Vaga(
            id_vaga=999, id_area=area_teste, id_empresa=1,
            id_recrutador=1, status_vaga="aberta",
            titulo="Inexistente", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        resultado = vaga_repo.alterar(vaga)

        assert resultado is False


class TestAlterarStatus:
    """Testes para alteração de status de vaga"""

    def test_alterar_status_para_fechada(self, area_teste, empresa_teste, recrutador_teste):
        """Deve alterar status de vaga para fechada"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Vaga Teste", descricao="Desc", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        resultado = vaga_repo.alterar_status(id_vaga, "fechada")

        assert resultado is True

        vaga_obtida = vaga_repo.obter_por_id(id_vaga)
        assert vaga_obtida.status_vaga == "fechada"

    def test_alterar_status_vaga_inexistente(self):
        """Deve retornar False ao alterar status de vaga inexistente"""
        resultado = vaga_repo.alterar_status(999, "fechada")
        assert resultado is False


class TestExcluir:
    """Testes para exclusão de vagas"""

    def test_excluir_vaga_existente(self, area_teste, empresa_teste, recrutador_teste):
        """Deve excluir vaga existente"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Temporária", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        resultado = vaga_repo.excluir(id_vaga)

        assert resultado is True
        assert vaga_repo.obter_por_id(id_vaga) is None

    def test_excluir_vaga_inexistente(self):
        """Deve retornar False ao excluir vaga inexistente"""
        resultado = vaga_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de vaga por ID"""

    def test_obter_vaga_existente(self, area_teste, empresa_teste, recrutador_teste):
        """Deve obter vaga por ID"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Desenvolvedor", descricao="Vaga dev",
            numero_vagas=1, salario=5000.0, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        vaga_obtida = vaga_repo.obter_por_id(id_vaga)

        assert vaga_obtida is not None
        assert vaga_obtida.id_vaga == id_vaga
        assert vaga_obtida.titulo == "Desenvolvedor"
        assert vaga_obtida.salario == 5000.0

    def test_obter_vaga_inexistente(self):
        """Deve retornar None para vaga inexistente"""
        vaga = vaga_repo.obter_por_id(999)
        assert vaga is None


class TestObterTodas:
    """Testes para listagem de todas as vagas"""

    def test_obter_todas_vazio(self, limpar_banco_dados):
        """Deve retornar lista vazia quando não há vagas"""
        vagas = vaga_repo.obter_todas()
        assert vagas == []

    def test_obter_todas_com_vagas(self, area_teste, empresa_teste, recrutador_teste):
        """Deve retornar todas as vagas cadastradas"""
        for i in range(3):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="Desc", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.obter_todas()

        assert len(vagas) == 3
        assert all(isinstance(vaga, Vaga) for vaga in vagas)


class TestObterPorEmpresa:
    """Testes para busca de vagas por empresa"""

    def test_obter_por_empresa(self, area_teste, empresa_teste, recrutador_teste, limpar_banco_dados):
        """Deve retornar vagas da empresa especificada"""
        # Criar segunda empresa
        empresa2 = Empresa(
            id_empresa=0, nome="Outra Empresa",
            cnpj="99.999.999/0001-99", descricao=""
        )
        id_empresa2 = empresa_repo.inserir(empresa2)

        # Inserir vagas para empresa_teste
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga Empresa 1 - {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        # Inserir vaga para empresa2
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=id_empresa2,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Vaga Empresa 2", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        vaga_repo.inserir(vaga)

        vagas_empresa1 = vaga_repo.obter_por_empresa(empresa_teste)

        assert len(vagas_empresa1) == 2
        assert all(vaga.id_empresa == empresa_teste for vaga in vagas_empresa1)


class TestObterPorRecrutador:
    """Testes para busca de vagas por recrutador"""

    def test_obter_por_recrutador(self, area_teste, empresa_teste, recrutador_teste, limpar_banco_dados):
        """Deve retornar vagas do recrutador especificado"""
        # Criar segundo recrutador
        usuario2 = Usuario(
            id=0, nome="Recrutador 2", email="rec2@test.com",
            senha=criar_hash_senha("senha"), perfil="RECRUTADOR"
        )
        id_recrutador2 = usuario_repo.inserir(usuario2)

        # Inserir vagas para recrutador_teste
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga Rec 1 - {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        # Inserir vaga para recrutador2
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=id_recrutador2, status_vaga="aberta",
            titulo="Vaga Rec 2", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        vaga_repo.inserir(vaga)

        vagas_rec1 = vaga_repo.obter_por_recrutador(recrutador_teste)

        assert len(vagas_rec1) == 2
        assert all(vaga.id_recrutador == recrutador_teste for vaga in vagas_rec1)


class TestBuscar:
    """Testes para busca de vagas com filtros"""

    def test_buscar_sem_filtros(self, area_teste, empresa_teste, recrutador_teste):
        """Deve retornar todas as vagas abertas sem filtros"""
        for i in range(3):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar()
        assert len(vagas) == 3

    def test_buscar_por_area(self, area_teste, empresa_teste, recrutador_teste, limpar_banco_dados):
        """Deve filtrar vagas por área"""
        # Criar segunda área
        area2 = Area(id_area=0, nome="Saúde", descricao="")
        id_area2 = area_repo.inserir(area2)

        # Inserir vagas para area_teste
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga TI {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        # Inserir vaga para area2
        vaga = Vaga(
            id_vaga=0, id_area=id_area2, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Vaga Saúde", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(id_area=area_teste)

        assert len(vagas) == 2
        assert all(vaga.id_area == area_teste for vaga in vagas)

    def test_buscar_por_cidade(self, area_teste, empresa_teste, recrutador_teste):
        """Deve filtrar vagas por cidade"""
        vagas_cidades = [
            ("Vaga SP", "São Paulo", "SP"),
            ("Vaga SP 2", "São Paulo", "SP"),
            ("Vaga RJ", "Rio de Janeiro", "RJ")
        ]

        for titulo, cidade, uf in vagas_cidades:
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=titulo, descricao="", numero_vagas=1,
                salario=0.0, cidade=cidade, uf=uf, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(cidade="São Paulo")

        assert len(vagas) == 2
        assert all("São Paulo" in (vaga.cidade or "") for vaga in vagas)

    def test_buscar_por_uf(self, area_teste, empresa_teste, recrutador_teste):
        """Deve filtrar vagas por UF"""
        vagas_dados = [
            ("Vaga SP 1", "SP"),
            ("Vaga SP 2", "SP"),
            ("Vaga RJ", "RJ")
        ]

        for titulo, uf in vagas_dados:
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=titulo, descricao="", numero_vagas=1,
                salario=0.0, uf=uf, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(uf="SP")

        assert len(vagas) == 2
        assert all(vaga.uf == "SP" for vaga in vagas)

    def test_buscar_por_modalidade(self, area_teste, empresa_teste, recrutador_teste):
        """Deve filtrar vagas por modalidade"""
        modalidades = ["Remoto", "Remoto", "Presencial"]

        for i, modalidade in enumerate(modalidades):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, modalidade=modalidade, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(modalidade="Remoto")

        assert len(vagas) == 2
        assert all(vaga.modalidade == "Remoto" for vaga in vagas)

    def test_buscar_por_salario_minimo(self, area_teste, empresa_teste, recrutador_teste):
        """Deve filtrar vagas por salário mínimo"""
        salarios = [2000.0, 3000.0, 4000.0, 5000.0]

        for i, salario in enumerate(salarios):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=salario, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(salario_min=3500.0)

        assert len(vagas) == 2
        assert all(vaga.salario >= 3500.0 for vaga in vagas)

    def test_buscar_com_limit(self, area_teste, empresa_teste, recrutador_teste):
        """Deve respeitar limite de resultados"""
        for i in range(5):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(limit=2)
        assert len(vagas) == 2

    def test_buscar_com_offset(self, area_teste, empresa_teste, recrutador_teste):
        """Deve respeitar offset de paginação"""
        for i in range(5):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vagas = vaga_repo.buscar(limit=2, offset=3)
        assert len(vagas) == 2


class TestObterQuantidade:
    """Testes para contagem de vagas"""

    def test_quantidade_inicial_zero(self, limpar_banco_dados):
        """Deve retornar 0 quando não há vagas"""
        quantidade = vaga_repo.obter_quantidade()
        assert quantidade == 0

    def test_quantidade_apos_insercoes(self, area_teste, empresa_teste, recrutador_teste):
        """Deve contar corretamente após inserções"""
        for i in range(4):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        quantidade = vaga_repo.obter_quantidade()
        assert quantidade == 4


class TestObterQuantidadePorStatus:
    """Testes para contagem de vagas por status"""

    def test_contar_por_status(self, area_teste, empresa_teste, recrutador_teste):
        """Deve contar vagas por status"""
        # Criar 2 abertas e 1 fechada
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga Aberta {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            id_vaga = vaga_repo.inserir(vaga)

        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="fechada",
            titulo="Vaga Fechada", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        vaga_repo.inserir(vaga)

        qtd_abertas = vaga_repo.obter_quantidade_por_status("aberta")
        qtd_fechadas = vaga_repo.obter_quantidade_por_status("fechada")

        assert qtd_abertas == 2
        assert qtd_fechadas == 1


class TestObterVagasAbertas:
    """Testes para listagem de vagas abertas"""

    def test_obter_vagas_abertas(self, area_teste, empresa_teste, recrutador_teste):
        """Deve retornar apenas vagas abertas"""
        # Criar 2 abertas e 1 fechada
        for i in range(2):
            vaga = Vaga(
                id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
                id_recrutador=recrutador_teste, status_vaga="aberta",
                titulo=f"Vaga Aberta {i}", descricao="", numero_vagas=1,
                salario=0.0, data_cadastro=""
            )
            vaga_repo.inserir(vaga)

        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="fechada",
            titulo="Vaga Fechada", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        vaga_repo.inserir(vaga)

        vagas = vaga_repo.obter_vagas_abertas()

        assert len(vagas) == 2
        assert all(vaga.status_vaga == "aberta" for vaga in vagas)


class TestIntegridadeDados:
    """Testes de integridade e validação de dados"""

    def test_campos_opcionais_null(self, area_teste, empresa_teste, recrutador_teste):
        """Campos opcionais devem aceitar None"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Vaga Mínima", descricao="Desc", numero_vagas=1,
            salario=0.0, requisitos=None, beneficios=None,
            carga_horaria=None, modalidade=None, cidade=None,
            uf=None, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        vaga_obtida = vaga_repo.obter_por_id(id_vaga)
        assert vaga_obtida.requisitos is None
        assert vaga_obtida.beneficios is None
        assert vaga_obtida.carga_horaria is None

    def test_salario_zero(self, area_teste, empresa_teste, recrutador_teste):
        """Salário 0 deve ser aceito"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Vaga Voluntária", descricao="", numero_vagas=1,
            salario=0.0, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        vaga_obtida = vaga_repo.obter_por_id(id_vaga)
        assert vaga_obtida.salario == 0.0

    def test_numero_vagas_multiplas(self, area_teste, empresa_teste, recrutador_teste):
        """Deve aceitar múltiplas vagas"""
        vaga = Vaga(
            id_vaga=0, id_area=area_teste, id_empresa=empresa_teste,
            id_recrutador=recrutador_teste, status_vaga="aberta",
            titulo="Várias Vagas", descricao="", numero_vagas=10,
            salario=0.0, data_cadastro=""
        )
        id_vaga = vaga_repo.inserir(vaga)

        vaga_obtida = vaga_repo.obter_por_id(id_vaga)
        assert vaga_obtida.numero_vagas == 10
