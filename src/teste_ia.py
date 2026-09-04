import asyncio
import warnings
from strands import Agent

# Silenciar avisos chatos do SDK
warnings.filterwarnings("ignore", category=UserWarning)

async def test_ia_connection():
    print("--- 🛠️ DEBUG: TESTE DE CONEXÃO AWS BEDROCK ---")

    # 1. Instanciamos o Agente da forma mais simples possível
    # Usamos o modelo Nova Pro que você listou anteriormente
    try:
        print("1. Inicializando Agente...")
        agent = Agent(model="amazon.nova-pro-v1:0")

        print("2. Enviando mensagem: 'Olá, você está me ouvindo?'")

        # 2. Chamada direta (sem system prompt, sem imagem, sem nada extra)
        # O invoke_async é o método mais puro do SDK v10
        response = await agent.invoke_async(
            input_text="Olá! Este é um teste de conexão. Se você recebeu isso, responda: 'Conexão AWS OK'."
        )

        print("\n--- RESPOSTA DA IA ---")
        if hasattr(response, 'output_text'):
            print(f"🤖 IA diz: {response.output_text}")
        else:
            print(f"🤖 Resposta bruta: {response}")
        print("-----------------------\n")

    except Exception as e:
        print("\n❌ FALHA NO TESTE:")
        print(f"Tipo do Erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")

        if "ValidationException" in str(e):
            print("\nDICA: O Bedrock ainda acha que a conversa não começou com o Usuário.")
            print("Isso pode ser um comportamento do SDK Strands injetando 'System Messages' escondidas.")

if __name__ == "__main__":
    asyncio.run(test_ia_connection())
