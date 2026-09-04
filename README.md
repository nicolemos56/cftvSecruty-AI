# SentinelSight AI

Sistema de monitoramento de CFTV por webcam com análise visual local, diagnóstico de anomalias por IA e notificações via Telegram.

## Funcionalidades

- Captura de vídeo em tempo real pela webcam.
- Detecção de câmera obstruída ou escura.
- Detecção de lente borrada ou suja.
- Detecção de alteração do ângulo da câmera.
- Comparação da imagem atual com uma posição de referência.
- Diagnóstico de anomalias usando o Amazon Bedrock e o modelo `amazon.nova-lite-v1:0`.
- Envio de imagem e diagnóstico para o Telegram.
- Cooldown de 30 segundos entre alertas para evitar spam.

## Requisitos

- Python 3.10 ou superior.
- Webcam disponível no computador.
- Credenciais da AWS configuradas localmente para acessar o Amazon Bedrock.
- Bot do Telegram e um `chat_id` válido para receber os alertas.

## Instalação

Clone o projeto e entre na pasta:

```powershell
git clone https://github.com/nicolemos56/cftvSecruty-AI.git
cd cftvSecruty-AI
```

Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Configure a AWS CLI ou as variáveis de ambiente usadas pelo Boto3. O projeto usa a região `us-east-1`.

Crie um arquivo `.env` na raiz do projeto a partir do exemplo e substitua os valores de exemplo pelas credenciais reais do Telegram:

```powershell
Copy-Item .env.example .env
```

Edite o arquivo `.env` e preencha `TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID`. O arquivo `.env.example` não é carregado automaticamente e não deve conter credenciais reais.

O arquivo `.env` é ignorado pelo Git e nunca deve ser commitado.

## Execução

Como os módulos estão dentro de `src`, execute a aplicação a partir dessa pasta:

```powershell
cd src
python main.py
```

Durante a execução:

- Pressione `S` para salvar a posição atual como referência.
- Pressione `R` para redefinir a referência.
- Pressione `Q` para encerrar o monitoramento.

## Como funciona

O sistema calcula o brilho e o nível de nitidez de cada frame. Depois que uma referência é salva, também calcula a similaridade estrutural entre a imagem atual e a referência. Uma anomalia é gerada quando:

- o brilho fica abaixo de `25`;
- o foco fica abaixo de `75`; ou
- a similaridade fica abaixo de `0.50`.

Quando uma anomalia é detectada, uma imagem é salva em `alert.jpg`, enviada para o agente de IA e encaminhada ao Telegram.
As imagens capturadas são armazenadas em `src/img/` e não são versionadas pelo Git.

## Segurança

Nunca publique tokens do Telegram, chaves da AWS ou outros segredos no Git. As credenciais do Telegram são carregadas pelas variáveis `TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID` no arquivo `.env`. Se o token anterior foi exposto, revogue-o pelo BotFather e gere um novo.

## Estrutura

```text
src/
  agent.py          # Diagnóstico pelo Amazon Bedrock
  img/              # Imagens capturadas durante os alertas
  main.py           # Loop principal de monitoramento
  notifier.py       # Envio de alertas ao Telegram
  vision_monitor.py # Monitor simples de brilho
  vision_utils.py   # Métricas e comparação de imagens
```

## Licença

Este projeto ainda não define uma licença de distribuição.
