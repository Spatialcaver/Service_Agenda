# ServiceAgenda ✂️📅

O **ServiceAgenda** é uma solução SaaS multi-tenant robusta, desenvolvida para gerir agendamentos em estabelecimentos de serviços (como barbearias, salões de beleza e clínicas). O sistema foca na organização de horários, gestão de equipes e controle de faturação, garantindo que não existam conflitos de marcações entre funcionários.

## Observação:
 Este sistema se encontra em fase de desenvolvimento, Algumas funcionalidades ainda estão sendo implementadas. 


## 🚀 Tecnologias

* **Backend:** Python 3.12 & Django 6.0.4.
* **API:** Django Rest Framework (DRF).
* **Banco de Dados:** PostgreSQL 15 (via Docker).
* **Autenticação:** JWT com `djangorestframework-simplejwt`.
* **Containerização:** Docker & Docker Compose.

## 🛠️ Funcionalidades Principais

* **Multi-tenancy:** Gestão de múltiplos estabelecimentos de forma isolada através do modelo `Estabelecimento`.
* **Gestão de Utilizadores:** Sistema de permissões customizado com tipos de utilizador: Cliente, Funcionário e Administrador.
* **Validação de Conflitos:** Lógica integrada para impedir que um funcionário receba dois agendamentos no mesmo intervalo de tempo.
* **Dashboard de Gestão:** Visão detalhada de métricas, incluindo faturamento realizado (serviços concluídos) e previsto (pendentes).
* **Consulta de Disponibilidade:** Endpoint inteligente que verifica o horário de funcionamento do local e a agenda individual dos funcionários.

## 📦 Como Executar o Projeto

### Pré-requisitos
* Docker e Docker Compose instalados.
* Git para clonar o repositório.

### Configuração e Execução

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/Spatialcaver/Service_Agenda.git](https://github.com/Spatialcaver/Service_Agenda.git)
    cd Service_Agenda
    ```

2.  **Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto seguindo este modelo:
    ```ini
    DEBUG=True
    SECRET_KEY='sua_chave_secreta'
    DATABASE_URL=postgres://postgres:postgres@db:5432/service_agenda
    ```

3.  **Subir os Containers:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Configurar o Banco de Dados:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Criar Acesso Administrativo:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## 📡 Endpoints da API

| Método | Caminho | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/token/` | Geração de token JWT |
| `GET` | `/api/reserva/disponibilidade/` | Verifica horários livres |
| `POST` | `/api/reserva/reserva/` | Cria um novo agendamento |
| `GET` | `/api/user/users/` | Gestão de utilizadores |

## 📂 Estrutura de Pastas

* `/Agenda`: Configurações centrais do projeto e definições de ambiente.
* `/user`: Gestão de modelos de utilizador customizados e autenticação.
* `/estabelecimento`: Gestão de locais, serviços e preços.
* `/reserva`: Lógica de agendamentos e validação de disponibilidade.

---
Desenvolvido por **Everton Anjos**.