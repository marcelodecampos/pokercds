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
- Tela de Login: Interface completa com validação de CPF e senha
- Botão de login para acesso ao sistema
- Sem opção de auto-cadastro de membros
- Cadastro de membros do grupo de poker (apenas administradores)
- Sistema de permissões com múltiplos administradores

### ✅ Gerenciamento de Usuários
- **Perfil do Usuário**: 
  - Visualização e edição de dados pessoais
  - Campos editáveis: nome, email, chave PIX, telefone
  - Campos não editáveis: CPF (sempre), apelido (apenas admin pode alterar)
- **Troca de Senha**: Sistema seguro para alteração de senha
- **Gerenciamento de Membros (Admin)**:
  - Listagem paginada de membros (máximo 20 por página)
  - CRUD completo: criar, visualizar, editar, excluir
  - Seleção múltipla para exclusão em lote
  - Controle de permissões (admin/membro ativo/inativo)
  - Administradores podem editar todos os campos, incluindo apelidos

### ✅ Gerenciamento de Jogos (Admin)
- **Listagem de Jogos**: 
  - Jogos ordenados por data decrescente (mais recentes primeiro)
  - Visualização de data e descrição opcional
  - Paginação até 20 jogos por página
- **CRUD de Jogos**:
  - Criar novos jogos com data e descrição
  - Editar jogos existentes
  - Excluir jogos individuais ou em lote
  - Seleção múltipla para operações em lote
- **Validações**: Data obrigatória, descrição opcional

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
- Campos obrigatórios no cadastro: CPF, nome, apelido, chave PIX e telefone
- **NOVO**: Apenas administradores podem alterar apelidos (nicknames) dos membros
- Usuários comuns podem editar seus próprios dados, exceto CPF e apelido

## Permissões e Controle de Acesso

### Usuários Comuns:
- Visualizar e editar próprio perfil (exceto CPF e apelido)
- Alterar própria senha
- Acesso às funcionalidades de poker (quando implementadas)

### Administradores:
- Todas as permissões de usuários comuns
- Cadastrar novos membros
- Gerenciar todos os membros (CRUD completo)
- Alterar apelidos de qualquer membro
- Ativar/desativar membros
- Conceder/revogar privilégios de administrador
- **Gerenciar jogos**: Criar, editar, visualizar e excluir jogos
- **Controle de sessões**: Acesso ao relacionamento jogo-membro

### Campos com Restrições:
- **CPF**: Não pode ser alterado após cadastro
- **Apelido (Nickname)**: Apenas administradores podem alterar
- **Permissões de Admin**: Apenas administradores podem modificar
- **Status Ativo/Inativo**: Apenas administradores podem modificar

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

## Padrões de Desenvolvimento

### Código e Arquitetura
- Seguir princípios DRY (Don't Repeat Yourself) para componentes reutilizáveis
- Separação clara entre lógica de negócio (State) e apresentação (Components)
- Validações centralizadas nos estados base
- Componentes configuráveis através de props
- **NOVO**: Todos os componentes Reflex devem ter um ID único e representativo
- IDs devem seguir convenção hierárquica e descritiva (ex: `members-table-card`, `login-form-submit-button`)

### Interface e UX
- Design responsivo com tema escuro por padrão
- Cores de tema: aparência escura, cor de destaque sky, cor cinza sand
- Mensagens de erro e sucesso em português
- Estados de carregamento visíveis durante operações assíncronas
- Confirmação antes de ações destrutivas (exclusões)

## Benefícios dos IDs Únicos

### Desenvolvimento e Manutenção:
- **Inspeção HTML**: Elementos facilmente identificáveis no DevTools do navegador
- **Debugging**: Identificação rápida de problemas em componentes específicos
- **Testes automatizados**: Seletores específicos e confiáveis para cada elemento
- **Analytics**: Tracking detalhado de interações do usuário

### Convenção de Nomenclatura:
- `página-*` para elementos principais de páginas
- `componente-*` para elementos de componentes específicos
- `modal-*` para elementos de modais e diálogos
- `*-button`, `*-icon`, `*-text` para tipos específicos de elementos
- `item-*-{id}` para elementos específicos de itens em listas

### Exemplos:
```html
<!-- Página de gerenciamento de membros -->
<div id="members-management-page">
  <div id="members-table-card">
    <button id="members-add-button">
    <div id="member-row-1">
      <button id="member-edit-button-1">
      <button id="member-delete-button-1">
