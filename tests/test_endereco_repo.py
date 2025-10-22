"""
Testes para o repositório de endereços (endereco_repo).
Cobre operações CRUD, validações e integridade de dados.
"""
import pytest
from model.endereco_model import Endereco
from model.usuario_model import Usuario
from repo import endereco_repo, usuario_repo
from util.security import criar_hash_senha


@pytest.fixture
def usuario_teste(limpar_banco_dados):
    """Cria um usuário de teste"""
    usuario = Usuario(
        id=0,
        nome="Usuario Teste",
        email="usuario@test.com",
        senha=criar_hash_senha("senha123"),
        perfil="ESTUDANTE"
    )
    return usuario_repo.inserir(usuario)


class TestCriarTabela:
    """Testes para criação da tabela de endereços"""

    def test_criar_tabela_sucesso(self, limpar_banco_dados):
        """Deve criar tabela de endereços com sucesso"""
        resultado = endereco_repo.criar_tabela()
        assert resultado is True


class TestInserir:
    """Testes para inserção de endereços"""

    def test_inserir_endereco_completo(self, usuario_teste):
        """Deve inserir endereço com todos os campos"""
        endereco = Endereco(
            id_endereco=0,
            id_usuario=usuario_teste,
            titulo="Casa",
            logradouro="Rua das Flores",
            numero="123",
            bairro="Centro",
            cidade="São Paulo",
            uf="SP",
            cep="01234-567",
            complemento="Apto 45"
        )

        id_endereco = endereco_repo.inserir(endereco)

        assert id_endereco is not None
        assert id_endereco > 0

    def test_inserir_endereco_sem_complemento(self, usuario_teste):
        """Deve inserir endereço sem complemento"""
        endereco = Endereco(
            id_endereco=0,
            id_usuario=usuario_teste,
            titulo="Trabalho",
            logradouro="Av Principal",
            numero="456",
            bairro="Jardim",
            cidade="Rio de Janeiro",
            uf="RJ",
            cep="20000-000",
            complemento=None
        )

        id_endereco = endereco_repo.inserir(endereco)

        assert id_endereco is not None
        assert id_endereco > 0

    def test_inserir_multiplos_enderecos(self, usuario_teste):
        """Deve inserir múltiplos endereços para o mesmo usuário"""
        enderecos = [
            Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo="Casa", logradouro="Rua A", numero="1",
                bairro="B", cidade="C", uf="SP", cep="11111-111"
            ),
            Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo="Trabalho", logradouro="Rua B", numero="2",
                bairro="B", cidade="C", uf="SP", cep="22222-222"
            )
        ]

        ids = [endereco_repo.inserir(end) for end in enderecos]

        assert len(ids) == 2
        assert all(id_end > 0 for id_end in ids)


class TestAlterar:
    """Testes para alteração de endereços"""

    def test_alterar_endereco_existente(self, usuario_teste):
        """Deve alterar endereço existente"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Casa", logradouro="Rua Original",
            numero="100", bairro="Bairro Original",
            cidade="Cidade Original", uf="SP", cep="00000-000"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_alterado = Endereco(
            id_endereco=id_endereco, id_usuario=usuario_teste,
            titulo="Casa Nova", logradouro="Rua Alterada",
            numero="200", bairro="Bairro Novo",
            cidade="Cidade Nova", uf="RJ", cep="11111-111",
            complemento="Novo complemento"
        )
        resultado = endereco_repo.alterar(endereco_alterado)

        assert resultado is True

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert endereco_obtido.titulo == "Casa Nova"
        assert endereco_obtido.logradouro == "Rua Alterada"
        assert endereco_obtido.uf == "RJ"
        assert endereco_obtido.complemento == "Novo complemento"

    def test_alterar_endereco_inexistente(self, usuario_teste):
        """Deve retornar False ao alterar endereço inexistente"""
        endereco = Endereco(
            id_endereco=999, id_usuario=usuario_teste,
            titulo="Inexistente", logradouro="", numero="",
            bairro="", cidade="", uf="", cep=""
        )
        resultado = endereco_repo.alterar(endereco)

        assert resultado is False


class TestExcluir:
    """Testes para exclusão de endereços"""

    def test_excluir_endereco_existente(self, usuario_teste):
        """Deve excluir endereço existente"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Temporário", logradouro="Rua Temp",
            numero="999", bairro="B", cidade="C", uf="SP", cep="99999-999"
        )
        id_endereco = endereco_repo.inserir(endereco)

        resultado = endereco_repo.excluir(id_endereco)

        assert resultado is True
        assert endereco_repo.obter_por_id(id_endereco) is None

    def test_excluir_endereco_inexistente(self):
        """Deve retornar False ao excluir endereço inexistente"""
        resultado = endereco_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de endereço por ID"""

    def test_obter_endereco_existente(self, usuario_teste):
        """Deve obter endereço por ID"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Meu Endereço", logradouro="Rua Teste",
            numero="123", bairro="Centro", cidade="São Paulo",
            uf="SP", cep="12345-678", complemento="Apto 10"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)

        assert endereco_obtido is not None
        assert endereco_obtido.id_endereco == id_endereco
        assert endereco_obtido.titulo == "Meu Endereço"
        assert endereco_obtido.logradouro == "Rua Teste"
        assert endereco_obtido.numero == "123"
        assert endereco_obtido.complemento == "Apto 10"

    def test_obter_endereco_inexistente(self):
        """Deve retornar None para endereço inexistente"""
        endereco = endereco_repo.obter_por_id(999)
        assert endereco is None


class TestObterPorUsuario:
    """Testes para busca de endereços por usuário"""

    def test_obter_por_usuario_sem_enderecos(self, usuario_teste):
        """Deve retornar lista vazia para usuário sem endereços"""
        enderecos = endereco_repo.obter_por_usuario(usuario_teste)
        assert enderecos == []

    def test_obter_por_usuario_com_enderecos(self, usuario_teste, limpar_banco_dados):
        """Deve retornar todos os endereços do usuário"""
        # Criar segundo usuário
        usuario2 = Usuario(
            id=0, nome="Usuario 2", email="user2@test.com",
            senha=criar_hash_senha("senha"), perfil="ESTUDANTE"
        )
        id_usuario2 = usuario_repo.inserir(usuario2)

        # Inserir 2 endereços para usuario_teste
        for i in range(2):
            endereco = Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo=f"End {i}", logradouro=f"Rua {i}",
                numero=str(i), bairro="B", cidade="C", uf="SP", cep=f"{i}0000-000"
            )
            endereco_repo.inserir(endereco)

        # Inserir 1 endereço para usuario2
        endereco = Endereco(
            id_endereco=0, id_usuario=id_usuario2,
            titulo="Outro", logradouro="Outra Rua",
            numero="99", bairro="B", cidade="C", uf="RJ", cep="99999-999"
        )
        endereco_repo.inserir(endereco)

        enderecos_usuario1 = endereco_repo.obter_por_usuario(usuario_teste)

        assert len(enderecos_usuario1) == 2
        assert all(end.id_usuario == usuario_teste for end in enderecos_usuario1)


class TestObterQuantidade:
    """Testes para contagem de endereços"""

    def test_quantidade_inicial_zero(self, limpar_banco_dados):
        """Deve retornar 0 quando não há endereços"""
        quantidade = endereco_repo.obter_quantidade()
        assert quantidade == 0

    def test_quantidade_apos_insercoes(self, usuario_teste):
        """Deve contar corretamente após inserções"""
        for i in range(3):
            endereco = Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo=f"End {i}", logradouro="Rua",
                numero=str(i), bairro="B", cidade="C", uf="SP", cep=f"{i}0000-000"
            )
            endereco_repo.inserir(endereco)

        quantidade = endereco_repo.obter_quantidade()
        assert quantidade == 3

    def test_quantidade_apos_exclusao(self, usuario_teste):
        """Deve atualizar contagem após exclusão"""
        ids = []
        for i in range(3):
            endereco = Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo=f"End {i}", logradouro="Rua",
                numero=str(i), bairro="B", cidade="C", uf="SP", cep=f"{i}0000-000"
            )
            ids.append(endereco_repo.inserir(endereco))

        endereco_repo.excluir(ids[0])

        quantidade = endereco_repo.obter_quantidade()
        assert quantidade == 2


class TestIntegridadeDados:
    """Testes de integridade e validação de dados"""

    def test_complemento_nullable(self, usuario_teste):
        """Campo complemento deve aceitar None"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Sem Complemento", logradouro="Rua",
            numero="1", bairro="B", cidade="C", uf="SP", cep="00000-000",
            complemento=None
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert endereco_obtido.complemento is None

    def test_cep_formatado(self, usuario_teste):
        """CEP deve ser armazenado com formatação"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="CEP Teste", logradouro="Rua",
            numero="1", bairro="B", cidade="C", uf="SP", cep="12345-678"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert endereco_obtido.cep == "12345-678"

    def test_numero_como_string(self, usuario_teste):
        """Número deve aceitar valores como string (ex: S/N)"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Sem Número", logradouro="Rua",
            numero="S/N", bairro="B", cidade="C", uf="SP", cep="00000-000"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert endereco_obtido.numero == "S/N"

    def test_uf_sigla(self, usuario_teste):
        """UF deve ser armazenado como sigla"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="UF Teste", logradouro="Rua",
            numero="1", bairro="B", cidade="C", uf="MG", cep="00000-000"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert endereco_obtido.uf == "MG"
        assert len(endereco_obtido.uf) == 2

    def test_titulo_personalizado(self, usuario_teste):
        """Título deve aceitar valores personalizados"""
        titulos = ["Casa", "Trabalho", "Casa dos Pais", "Endereço Comercial"]

        for titulo in titulos:
            endereco = Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo=titulo, logradouro="Rua",
                numero="1", bairro="B", cidade="C", uf="SP", cep="00000-000"
            )
            id_endereco = endereco_repo.inserir(endereco)

            endereco_obtido = endereco_repo.obter_por_id(id_endereco)
            assert endereco_obtido.titulo == titulo

    def test_logradouro_longo(self, usuario_teste):
        """Logradouro deve aceitar nomes longos"""
        logradouro_longo = "Rua " + "A" * 200
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Long", logradouro=logradouro_longo,
            numero="1", bairro="B", cidade="C", uf="SP", cep="00000-000"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert endereco_obtido.logradouro == logradouro_longo

    def test_caracteres_especiais(self, usuario_teste):
        """Deve aceitar caracteres especiais em campos de texto"""
        endereco = Endereco(
            id_endereco=0, id_usuario=usuario_teste,
            titulo="Casa (Principal)",
            logradouro="Rua João da Silva, Nº",
            numero="123-A",
            bairro="Bairro São José",
            cidade="São Paulo",
            uf="SP",
            cep="01234-567",
            complemento="Apto 45-B (Bloco A)"
        )
        id_endereco = endereco_repo.inserir(endereco)

        endereco_obtido = endereco_repo.obter_por_id(id_endereco)
        assert "João" in endereco_obtido.logradouro
        assert "São José" in endereco_obtido.bairro
        assert "45-B" in endereco_obtido.complemento


class TestObterTodos:
    """Testes para listagem de todos os endereços"""

    def test_obter_todos_vazio(self, limpar_banco_dados):
        """Deve retornar lista vazia quando não há endereços"""
        enderecos = endereco_repo.obter_todos()
        assert enderecos == []

    def test_obter_todos_com_enderecos(self, usuario_teste):
        """Deve retornar todos os endereços cadastrados"""
        for i in range(3):
            endereco = Endereco(
                id_endereco=0, id_usuario=usuario_teste,
                titulo=f"End {i}", logradouro="Rua",
                numero=str(i), bairro="B", cidade="C", uf="SP", cep=f"{i}0000-000"
            )
            endereco_repo.inserir(endereco)

        enderecos = endereco_repo.obter_todos()
        assert len(enderecos) == 3
        assert all(isinstance(e, Endereco) for e in enderecos)
