# PokerCDS

*Read this in other languages: [English](README.en.md), [Português](README.md)*

Um sistema de controle financeiro para noites de poker entre amigos construído com Reflex.

## Visão Geral

PokerCDS é um sistema web para organizar e controlar a movimentação financeira durante noites de poker entre amigos. O sistema gerencia compras de cacifes, controle de fichas e movimentação financeira dos jogadores.

## Tecnologias Utilizadas

- **Reflex**: Framework web moderno para Python
- **SQLAlchemy**: ORM para gerenciamento do banco de dados
- **Alembic**: Ferramenta de migração de banco de dados
- **psycopg3**: Driver PostgreSQL para Python
- **TailwindCSS v4**: Framework CSS para estilização

## Funcionalidades

- **Autenticação e Acesso**
  - Tela de login com CPF e senha
  - Botão de login para acesso ao sistema
  - Sem opção de auto-cadastro de membros
  - Cadastro de membros do grupo de poker (apenas administradores)
  - Sistema de permissões com múltiplos administradores
- **Gerenciamento de Membros**
  - Cadastro com CPF, nome (até 64 caracteres), chave PIX (até 128 caracteres) e telefone
  - Opção para habilitar/desabilitar membros
  - Controle de acesso baseado no status do membro
- **Controle Financeiro**
  - Controle de compra de cacifes (R$ 50,00 cada)
  - Registro de jogadores e suas compras
  - Formas de pagamento: dinheiro, cartão ou promissória
  - Controle de garantias (cartões e promissórias) por jogador
  - Acompanhamento da movimentação financeira em tempo real
  - Histórico de cacifes por jogador
  - Contabilidade final da jogatina
  - Geração de lista de débitos e créditos entre jogadores
  - Relatório de quem deve e para quem deve pagar
  - Cálculo automático de acertos baseado em fichas vs garantias

## Funcionalidades Implementadas

### ✅ Autenticação
- **Tela de Login**: Interface completa com validação de CPF e senha
  - Campo CPF com máscara visual
  - Campo senha com ocultação de caracteres
  - Validação de CPF (11 dígitos obrigatórios)
  - Tratamento de erros com mensagens em português
  - Estado de carregamento durante autenticação
  - Design responsivo com gradiente de fundo

### 🔄 Em Desenvolvimento
- Integração com banco de dados para autenticação
- Dashboard principal após login
- Gerenciamento de membros (apenas administradores)
- Sistema de controle de cacifes
- Relatórios financeiros

## Estrutura do Projeto

```
PokerCDS/
├── PokerCDS/
│   ├── components/          # Componentes de UI reutilizáveis
│   │   ├── __init__.py
│   │   └── login_form.py    # Formulário de login
│   ├── pages/              # Páginas da aplicação
│   │   ├── __init__.py
│   │   └── login.py        # Página de login
│   ├── entities/           # Modelos de banco de dados
│   │   ├── __init__.py
│   │   ├── base.py         # Classe base SQLModel
│   │   └── member.py       # Modelo de membro
│   ├── utils/              # Utilitários
│   │   ├── __init__.py
│   │   ├── timezone.py     # Funções de timezone
│   │   └── password.py     # Utilitários de senha
│   └── PokerCDS.py         # Aplicação principal
├── alembic/                # Migrações de banco de dados
├── rxconfig.py            # Configuração do Reflex
└── README.md
```

## Como Testar o Login

1. Execute a aplicação:
```bash
reflex run
```

2. Acesse `http://localhost:3000`

3. Use as credenciais temporárias:
   - CPF: `594.693.904-15` (ou `59469390415`)
   - Senha: `admin123`

**Nota**: Estas são credenciais temporárias para desenvolvimento. Na versão final, a autenticação será feita através do banco de dados com senhas criptografadas.

## Regras do Sistema

- Cada cacife custa exatamente R$ 50,00 e equivale ao mesmo valor em fichas
- Não é permitido comprar valores diferentes de R$ 50,00
- Jogadores podem comprar múltiplos cacifes durante a noite
- Cada compra deve ser feita individualmente (um cacife por vez)
- Apenas administradores podem cadastrar novos membros no sistema
- O sistema permite múltiplos administradores
- Acesso ao sistema é feito através de CPF e senha
- Não há opção de auto-cadastro na tela de login
- Membros desabilitados não podem acessar o sistema
- Campos obrigatórios no cadastro: CPF, nome, chave PIX e telefone
- **Formas de Pagamento de Cacifes:**
  - Dinheiro: pagamento à vista no valor de R$ 50,00
  - Cartão: deixado como garantia equivalente a R$ 50,00
  - Promissória: compromisso de pagamento equivalente a R$ 50,00
- **Acerto Final:**
  - Jogadores que pagaram em dinheiro recebem o valor exato das fichas finais
  - Se valor das fichas > (cartões + promissórias) × R$ 50,00: jogador tem a receber
  - Se valor das fichas < (cartões + promissórias) × R$ 50,00: jogador deve pagar
  - Ao final da jogatina, é gerada a contabilidade com lista de pagamentos entre jogadores

## Pré-requisitos

- Python 3.12+
- Node.js 16+ (para dependências do frontend)
- PostgreSQL (banco de dados)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/marcelodecampos/PokerCDS.git
cd PokerCDS
```

2. Configure o banco de dados PostgreSQL e crie um banco para a aplicação

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as migrações do banco de dados:
```bash
alembic upgrade head
```

5. Inicialize a aplicação Reflex:
```bash
reflex init
```

## Uso

1. Execute o servidor de desenvolvimento:
```bash
reflex run
```

2. Abra seu navegador e navegue para `http://localhost:3000`

## Configuração

A aplicação usa Reflex com os seguintes plugins:
- SitemapPlugin: Gera automaticamente o sitemap.xml
- TailwindV4Plugin: Framework CSS moderno para estilização

## Desenvolvimento

Para começar a desenvolver:

1. Faça suas alterações nos arquivos Python
2. A aplicação irá recarregar automaticamente com hot reloading habilitado
3. Visite o servidor de desenvolvimento local para ver suas alterações

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua funcionalidade
3. Faça suas alterações
4. Envie um pull request

## Licença

[Adicione suas informações de licença aqui]
