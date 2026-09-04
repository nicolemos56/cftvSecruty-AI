import boto3
import json
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class SentinelAgent:
    def __init__(self):
        # Inicializa o cliente Boto3 diretamente para maior controle
        self.client = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.model_id = "amazon.nova-lite-v1:0"

    def analyze_anomaly(self, image_path, reason):
        print(f"--- 🧠 IA: Analisando com {self.model_id} ---")

        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            messages = [{
                "role": "user",
                "content": [
                    {"image": {"format": "jpeg", "source": {"bytes": image_bytes}}},
                    {"text": f"Você é um especialista em CFTV. O sensor detectou: {reason}. Confirme o diagnóstico e sugira uma ação curta."}
                ]
            }]

            response = self.client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig={"maxTokens": 100, "temperature": 0.5}
            )

            return response['output']['message']['content'][0]['text']

        except Exception as e:
            error_msg = str(e)
            # Se a AWS demorar ou der erro de limite (Throttling), usa o Mock
            if "Throttling" in error_msg or "AccessDenied" in error_msg:
                print("⚠️ Limite AWS ou erro de acesso. Usando diagnóstico de emergência...")
                return self._mock_diagnosis(reason)
            return f"❌ Erro na IA: {error_msg}"

    def _mock_diagnosis(self, reason):
        """Diagnóstico de emergência caso a IA esteja indisponível."""
        reason_low = reason.lower()
        if "embaçada" in reason_low or "nitidez" in reason_low:
            return "DIAGNÓSTICO: Lente suja ou embaçada detectada. AÇÃO: Limpe a lente com pano seco."
        if "obstrução" in reason_low:
            return "DIAGNÓSTICO: Câmera coberta ou vandalizada. AÇÃO: Verifique o local imediatamente."
        if "ângulo" in reason_low or "vandalismo" in reason_low:
            return "DIAGNÓSTICO: Câmera movida fisicamente. AÇÃO: Reposicione e aperte os parafusos de fixação."
        return "Falha detectada pelo sensor local. Verificação física recomendada."
