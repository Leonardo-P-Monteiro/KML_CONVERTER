# KML Converter - Prospector Map Data Extractor

Link para aplicação web: https://converterkml.pythonanywhere.com/

## Descrição do Projeto

**KML Converter** é uma aplicação web que automatiza a extração de dados de empresas a partir de arquivos KML exportados do Google Earth. A ferramenta foi desenvolvida para apoiar a prospecção comercial, capturando informações relevantes de empresas (nome, telefone, endereço e website) e disponibilizando os dados em formato Excel para download.

### Objetivo Estratégico

Prover uma solução eficiente e segura para vendedores e consultores que prospectam através de dados georreferenciados do Google Maps, eliminando processos manuais de transcrição e permitindo a importação direta em ferramentas CRM e planilhas.

---

## Arquitetura de Pastas

```
KML_CONVERTER/
├── apps/                          # Aplicações Django (modularização)
│   ├── converter/                 # App principal de conversão KML → Excel
│   │   ├── models.py              # Modelos de dados (atualmente não utilizado)
│   │   ├── views.py               # Class-based views para requisições HTTP
│   │   ├── services.py            # Lógica de negócio (parsing e conversão)
│   │   ├── forms.py               # Formulários (estrutura para expansão)
│   │   ├── urls.py                # Roteamento de URLs da aplicação
│   │   ├── selectors.py           # Seletores de dados (padrão de consulta)
│   │   ├── admin.py               # Interface administrativa Django
│   │   ├── migrations/            # Histórico de mudanças de modelo
│   │   └── templates/             # Templates HTML da aplicação
│   └── core/                      # Funcionalidades transversais
│       ├── models.py              # Modelos compartilhados
│       └── utils.py               # Utilitários gerais
├── config/                        # Configuração central do Django
│   ├── settings/                  # Configurações por ambiente
│   │   ├── base.py                # Configurações comuns
│   │   ├── development.py         # Configurações de desenvolvimento
│   │   └── production.py          # Configurações de produção
│   ├── urls.py                    # Roteamento de URLs principal
│   ├── wsgi.py                    # Interface WSGI para deploy
│   └── asgi.py                    # Interface ASGI para aplicações assíncronas
├── requirements/                  # Dependências por ambiente
│   ├── base.txt                   # Pacotes comuns
│   ├── development.txt            # Pacotes de desenvolvimento
│   └── production.txt             # Pacotes de produção
├── docs/                          # Documentação e exemplos
│   └── kml_exemple.kml            # Arquivo KML de exemplo
├── static/                        # Arquivos estáticos (público)
│   ├── style.css                  # Estilos da interface
│   ├── script.js                  # Lógica do frontend
│   └── media/                     # Uploads e assets dinâmicos
├── templates/                     # Templates globais
│   ├── base.html                  # Template base (herança)
│   ├── index.html                 # Página inicial
│   └── partials/                  # Componentes reutilizáveis
├── manage.py                      # Utilitário de gerencimento Django
├── db.sqlite3                     # Banco de dados local
├── Makefile                       # Automação de tarefas
└── README.md                      # Este arquivo
```

### Propósito de Cada Pasta

| Pasta              | Responsabilidade                                                        |
| ------------------ | ----------------------------------------------------------------------- |
| **apps/converter** | Núcleo da aplicação: validação KML, parsing de dados e geração de Excel |
| **apps/core**      | Funcionalidades comuns entre aplicações (utilitários, modelos base)     |
| **config**         | Configuração centralizada do Django com suporte a múltiplos ambientes   |
| **requirements**   | Versionamento de dependências separadas por contexto de deploy          |
| **static**         | CSS, JavaScript e assets que não mudam (servidos pelo servidor web)     |
| **templates**      | HTML com estrutura de herança para reutilização                         |
| **docs**           | Exemplos, esquemas e documentação técnica                               |

---

## Conceito e Funcionamento

### Fluxo de Processamento

```
1. Usuário faz upload/cola conteúdo KML
   ↓
2. Validação de estrutura XML (defusedxml)
   ↓
3. Parsing com BeautifulSoup (extração de tags relevantes)
   ↓
4. Deduplicação de registros por nome da empresa
   ↓
5. Extração de campos: Nome | Telefone | Endereço | Website
   ↓
6. Geração de DataFrame (pandas)
   ↓
7. Export para Excel em memória (openpyxl)
   ↓
8. Download do arquivo XLSX
```

### Recursos Principais

- **Suporte a múltiplos arquivos KML concatenados**: O parser é capaz de processar vários blocos KML colados simultaneamente
- **Processamento em memória**: Nenhum arquivo temporário é criado no disco durante a conversão
- **Deduplicação automática**: Evita incorporar empresas duplicadas no mesmo batch
- **Validação de EntidadeXML**: Protege contra ataques XXE (XML External Entity)
- **Extração de dados estruturados**: Nome, telefone, endereço completo e link do Google My Business

---

## Tecnologias Aplicadas

| Tecnologia               | Versão | Propósito                               |
| ------------------------ | ------ | --------------------------------------- |
| **Python**               | 3.10+  | Linguagem de programação                |
| **Django**               | 6.0.1  | Framework web full-stack                |
| **BeautifulSoup4**       | 4.14.3 | Parsing de HTML/XML                     |
| **Pandas**               | 3.0.0  | Manipulação e transformação de dados    |
| **openpyxl**             | 3.1.5  | Geração de arquivos Excel               |
| **defusedxml**           | 0.7.1  | Proteção contra ataques XML             |
| **lxml**                 | 6.0.2  | Parser XML otimizado                    |
| **django-extensions**    | 4.1    | Utilitários e shell melhorado           |
| **django-cors-headers**  | 4.9.0  | Configuração de CORS                    |
| **django-debug-toolbar** | 6.1.0  | Ferramentas de debug em desenvolvimento |

### Stack Frontend

- **HTML5**: Markup semântico
- **CSS3**: Estilização responsiva
- **JavaScript Vanilla**: Interatividade sem dependências pesadas

---

## Conceitos Django Aplicados

### 1. **Arquitetura de Apps Modular**

O projeto segue o padrão de "fat models, skinny views" com separação de responsabilidades:

- **Models**: Estrutura de dados (extensível para futuro banco de dados)
- **Views**: Class-Based Views (CBV) para tratamento de requisições HTTP
- **Services**: Lógica de negócio isolada (padrão Service Layer)
- **Selectors**: Padrão Query Objects para consultas reutilizáveis

### 2. **Roteamento URL Hierárquico**

```python
# config/urls.py → apps.converter.urls
Estrutura: path("", include("apps.converter.urls"))
```

### 3. **Configurações Ambientadas**

```
settings/
├── base.py          # Compartilhado (INSTALLED_APPS, MIDDLEWARE)
├── development.py   # DEBUG=True, BD local, DEBUG_TOOLBAR
└── production.py    # DEBUG=False, BD persistente, segurança aplicada
```

### 4. **Template Inheritance**

Estrutura DRY com `base.html` e partials reutilizáveis:

```html
{% extends "base.html" %}
<!-- Componentes: _nav.html, _footer.html, _messages.html -->
```

### 5. **CORS Configuration**

Controle de acesso entre origens para futuras integrações com APIs:

```python
CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "https://meu-site-producao.com"]
```

### 6. **Middleware Stack**

- `SecurityMiddleware`: Headers de segurança
- `CsrfViewMiddleware`: Proteção CSRF token
- `SessionMiddleware`: Gerenciamento de sessões
- `CORSMiddleware`: Normalização de requisições cross-origin

---

## Bibliotecas Python e Sua Relevância

### Processamento de Dados

| Biblioteca         | Importância    | Justificativa                                                      |
| ------------------ | -------------- | ------------------------------------------------------------------ |
| **pandas**         | ⭐⭐⭐ Crítica | Transformação de dados em estruturas tabulares e export para Excel |
| **openpyxl**       | ⭐⭐⭐ Crítica | Engine nativo para geração de arquivos .xlsx com stylings          |
| **BeautifulSoup4** | ⭐⭐⭐ Crítica | Parsing flexível de XML (mais tolerante que parsers estritos)      |
| **lxml**           | ⭐⭐ Alta      | Parser XML otimizado, dependência do BeautifulSoup                 |

### Segurança

| Biblioteca       | Importância    | Justificativa                                                 |
| ---------------- | -------------- | ------------------------------------------------------------- |
| **defusedxml**   | ⭐⭐⭐ Crítica | Mitigação de ataques XXE (XML External Entity Injection)      |
| **cryptography** | ⭐⭐ Alta      | Criptografia assimétrica e simétrica subjacente ao Django/SSL |
| **pyOpenSSL**    | ⭐⭐ Alta      | Binding Python para OpenSSL, essencial para HTTPS             |

### Utilidades

| Biblioteca            | Importância     | Justificativa                                                          |
| --------------------- | --------------- | ---------------------------------------------------------------------- |
| **python-decouple**   | ⭐⭐ Alta       | Carregamento seguro de variáveis de ambiente (SECRET_KEY, credenciais) |
| **python-dotenv**     | ⭐⭐ Alta       | Suporte alternativo para .env files                                    |
| **arrow**             | ⭐ Complementar | Manipulação intuitiva de datas e timezones                             |
| **django-extensions** | ⭐⭐ Alta       | Shell melhorado e extensões ao management                              |

### Desenvolvimento

| Biblioteca               | Importância | Justificativa                                          |
| ------------------------ | ----------- | ------------------------------------------------------ |
| **django-stubs**         | ⭐⭐ Alta   | Type hints para Django (integração com mypy)           |
| **django-debug-toolbar** | ⭐⭐ Alta   | Profiling de queries SQL e requests em desenvolvimento |

---

## Configurações de Segurança Implementadas

### 1. **Proteção contra Cross-Site Scripting (XSS)**

```python
# ativado em settings/base.py
SECURE_BROWSER_XSS_FILTER = True
```

**Efeito**: Adiciona header `X-XSS-Protection: 1; mode=block` para navegadores legados.
**Escopo**: Impede injeção de scripts JavaScript maliciosos.

---

### 2. **Prevenção de MIME Type Sniffing**

```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Efeito**: Header `X-Content-Type-Options: nosniff`
**Escopo**: Força o navegador a respeitar o Content-Type declarado. Protege contra download de malware disfarçado de imagem/documento.

---

### 3. **Proteção contra Clickjacking**

```python
X_FRAME_OPTIONS = "DENY"
```

**Efeito**: Header `X-Frame-Options: DENY`
**Escopo**: Impede que a aplicação seja embutida em um iframe, evitando ataques de clickjacking.

---

### 4. **Redirecionamento Forçado para HTTPS**

```python
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

**Efeito**:

- Toda requisição HTTP (porta 80) retorna 301 Permanent Redirect para HTTPS
- Suporta reverse proxies (Nginx, AWS ELB) que terminam SSL antes do Django

**Escopo**: Garante criptografia de dados em trânsito.

---

### 5. **Cookies Seguros**

```python
SESSION_COOKIE_SECURE = True  # Cookie de sessão apenas via HTTPS
CSRF_COOKIE_SECURE = True     # Token CSRF apenas via HTTPS
```

**Efeito**: Cookie com flag `Secure`, impedindo transmissão em conexões HTTP.
**Escopo**: Mitiga roubo de sessão em redes abertas (WiFi público).

---

### 6. **HTTP Strict Transport Security (HSTS)**

```python
SECURE_HSTS_SECONDS = 31536000  # 1 ano
```

**Efeito**: Header `Strict-Transport-Security: max-age=31536000`
**Escopo**:

- Após primeira visita HTTPS, navegador **automaticamente** usa HTTPS para todas as requisições futuras
- Mitiga ataques MITM (Man-in-the-Middle) mesmo em redes comprometidas
- Válido por 1 ano (31536000 segundos)

---

### 7. **Controle de Referência (Referrer Policy)**

```python
SECURE_REFERRER_POLICY = "same-origin"
```

**Efeito**: Header `Referrer-Policy: same-origin`
**Escopo**:

- Envia informação de referência completa para links internos
- Remove referência ao navegar para domínios externos
- Previne vazamento de URLs com parâmetros sensíveis

---

### 8. **Proteção contra XXE (XML External Entity Injection)**

```python
# services.py
import defusedxml.ElementTree as Et
from defusedxml.common import DefusedXmlException

root = Et.fromstring(bloco.strip())  # Parsing seguro
```

**Efeito**: Parser XML resistente a:

- Expandsão de entidades bilhão (Billion Laughs Attack)
- Referências a entidades externas
- Ataques de negação de serviço XML

**Escopo**: Critical para aplicações que processam XML user-supplied.

---

### 9. **Proteção CSRF (Cross-Site Request Forgery)**

```python
# settings/base.py
'django.middleware.csrf.CsrfViewMiddleware'

# templates/converter/home.html
{% csrf_token %}
```

**Efeito**: Token CSRF único por sessão. Formulários POST requerem token válido.
**Escopo**: Impede requisições não autorizadas em nome do usuário.

---

### 10. **Variáveis de Ambiente para Credenciais**

```python
# settings/base.py
from decouple import config

SECRET_KEY = config("SECRET_KEY")
```

**Efeito**: Chaves sensíveis carregadas de `.env`, nunca hardcoded.
**Escopo**: Evita exposição de credenciais em repositórios Git.

---

### 11. **Desabilitar acesso administrativo em produção** (Recomendação)

```python
# settings/production.py
if settings.DEBUG is False:
    # Mover admin para URL obscura
    urlpatterns = [
        path("super-secret-admin-xyz/", admin.site.urls),
    ]
```

---

## Fluxo de Processamento Técnico (JavaScript)

### Frontend Interativo

O arquivo `static/script.js` implementa:

1. **Event Listener para Upload de KML**
   - Captura evento de mudança no input file
   - Lê conteúdo do arquivo via FileReader API

2. **Validação Cliente**
   - Verifica extensão .kml
   - Valida tamanho máximo

3. **Envio via AJAX**
   - Submissão assíncrona sem reload de página
   - Atualização dinâmica de feedback ao usuário

4. **Manipulação de Response**
   - Download automático de Excel
   - Exibição de mensagens de sucesso/erro

---

## Fluxo de Processamento Técnico (Backend)

### Validação e Parsing

1. **Divisão de Blocos KML**

   ```python
   blocos_kml = re.split(r"<\?xml.*?\?>", kml_content)
   ```

   - Suporta múltiplos arquivos KML concatenados
   - Cada bloco é processado isoladamente

2. **Validação com defusedxml**

   ```python
   root = Et.fromstring(bloco.strip())
   if root.tag.strip().lower().endswith("kml"):
       # KML válido
   ```

3. **Parsing com BeautifulSoup**

   ```python
   soup = BeautifulSoup(bloco, "xml")
   placemarks = soup.find_all("Placemark")
   ```

   - Extrai tags: `<name>`, `<address>`, `<phoneNumber>`, `<ExtendedData>`

4. **Deduplicação**

   ```python
   nomes_processados = set()
   if nome_empresa not in nomes_processados:
       nomes_processados.add(nome_empresa)
   ```

5. **Geração de DataFrame**
   ```python
   df = pd.DataFrame(lista_empresas)
   df.to_excel(output_destination, engine="openpyxl")
   ```

---

## Setup e Instalação

### Pré-requisitos

- Python 3.10+
- pip ou uvenv
- Git

### Instalação Local

```bash
# 1. Clone o repositório
git clone <seu-repo>
cd KML_CONVERTER

# 2. Crie um ambiente virtual
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements/development.txt

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 5. Aplique migrações
python manage.py migrate

# 6. Colete arquivos estáticos
python manage.py collectstatic

# 7. Execute o servidor
python manage.py runserver
```

Acesse: `http://localhost:8000`

---

## Deployment em Produção

### Variáveis de Ambiente Obrigatórias

```bash
SECRET_KEY=sua-chave-aleatoria-super-secreta
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgres://user:pass@host:5432/db
```

### Servidor Web (Nginx + Gunicorn)

```bash
# Instale dependências de produção
pip install -r requirements/production.txt

# Colete assets estáticos
python manage.py collectstatic --noinput

# Execute Gunicorn
gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

---

## Contribuição e Suporte

Este projeto foi desenvolvido como showcase técnico de habilidades em:

- **Backend**: Django, Python, processamento de XML
- **Segurança**: Implementação de headers de segurança, proteção contra XXE
- **Arquitetura**: Separação de responsabilidades, padrão Service Layer
- **DevOps**: Configurações ambientadas, virtualenv, deploy

Para contato ou consultoria: [Seus dados de contato]

---

## Licença

MIT License - Sinta-se livre para usar, modificar e distribuir.

---

**Última atualização**: Fevereiro 2026
