import boto3
import json

def test_aws_direct():
    print("--- 🚀 TESTE DIRETO: BOTO3 + AMAZON NOVA PRO ---")

    # Inicializa o cliente Bedrock
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    model_id = "amazon.nova-pro-v1:0"

    # Estrutura exata que o Bedrock exige
    messages = [
        {
            "role": "user",
            "content": [{"text": "Olá! Se você recebeu esta mensagem, responda apenas: 'Conexão Direta AWS OK'."}]
        }
    ]

    print(f"Enviando mensagem para o modelo: {model_id}...")

    try:
        # Usamos 'converse' em vez de 'invoke_model' para ser mais moderno
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={"maxTokens": 50, "temperature": 0.5}
        )

        # Extrai a resposta
        texto_resposta = response['output']['message']['content'][0]['text']
        print("\n--- ✅ SUCESSO! ---")
        print(f"🤖 IA respondeu: {texto_resposta}")
        print("-------------------\n")
        return True

    except Exception as e:
        print("\n--- ❌ FALHA NO MOTOR AWS ---")
        print(f"Erro: {str(e)}")
        return False

if __name__ == "__main__":
    test_aws_direct()
