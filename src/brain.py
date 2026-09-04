class SentinelBrain:
    """O Cérebro do SentinelSight que interpreta dados numéricos em linguagem humana."""

    @staticmethod
    def interpretar_anomalia(tipo, valor):
        diagnostico = ""
        acao = ""

        if tipo == "foco":
            # Valor é a Variância do Laplaciano
            if valor < 20:
                diagnostico = "A lente parece estar TOTALMENTE obstruída ou coberta."
                acao = "Verifique se há vandalismo ou se algo foi colado na câmera."
            elif valor < 50:
                diagnostico = "A imagem está muito embaçada (ofuscada)."
                acao = "Pode ser sujeira, humidade ou teia de aranha. Limpe a lente."

        elif tipo == "angulo":
            # Valor é a Similaridade Estrutural (0.0 a 1.0)
            if valor < 0.4:
                diagnostico = "DESVIO CRÍTICO: A câmera foi movida ou virada para a parede!"
                acao = "Reposição física imediata é necessária."
            elif valor < 0.6:
                diagnostico = "Mudança de ângulo detectada (Deslocamento leve)."
                acao = "Verifique se o suporte da câmera está frouxo ou se foi tocada."

        elif tipo == "brilho":
            if valor < 15:
                diagnostico = "ESCURIDÃO TOTAL detectada."
                acao = "A câmera pode ter sido pintada com spray ou coberta com pano preto."
            elif valor > 240:
                diagnostico = "OFUSCAMENTO POR LUZ (Glare)."
                acao = "Alguém está apontando uma lanterna ou laser diretamente para a lente."

        return f"🤖 [DIAGNÓSTICO IA]: {diagnostico}\n📢 [AÇÃO]: {acao}"
