import cv2
import time
import numpy as np
from pathlib import Path
from vision_utils import VisionProcessor
from agent import SentinelAgent
from notifier import send_telegram_alert

IMAGE_DIR = Path(__file__).resolve().parent / "img"

def main():
    print("\n" + "="*60)
    print("🛡️  SENTINELSIGHT AI - MONITORAMENTO FLUIDO")
    print("="*60)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    processor = VisionProcessor()
    agent = SentinelAgent()

    reference_frame = None
    system_active = False

    # --- VARIÁVEIS DE COOLDOWN (CONTROLE DE TEMPO) ---
    last_alert_time = 0
    COOLDOWN_DURATION = 30 # Segundos entre um envio de Telegram e outro

    print("\n[PASSO 1] Posicione sua câmera.")
    print("[PASSO 2] Pressione 'S' para SALVAR a posição inicial.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        foco = processor.get_blur_score(frame)
        brilho = processor.get_brightness_score(frame)

        if not system_active:
            status_text = "AGUARDANDO CONFIGURACAO... (Aperte 'S')"
            color = (255, 191, 0)
        else:
            status_text = "SISTEMA VIGILANTE ATIVO (Aperte 'R' para Reset)"
            color = (0, 255, 0)

        # Dashboard Visual
        cv2.rectangle(frame, (0, 0), (700, 45), (0,0,0), -1)
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Lógica de Monitoramento
        if system_active:
            sim = processor.compare_frames(reference_frame, frame)

            # Limites de sensibilidade
            LIMIT_BRILHO = 25
            LIMIT_FOCO = 75
            LIMIT_SIM = 0.50

            anomaly_detected = False
            reason = ""

            # Hierarquia de detecção
            if brilho < LIMIT_BRILHO:
                anomaly_detected = True
                reason = "OBSTRUÇÃO (Câmera Escura)"
            elif foco < LIMIT_FOCO:
                anomaly_detected = True
                reason = "TAMPERING (Lente Borrada/Suja)"
            elif sim < LIMIT_SIM:
                anomaly_detected = True
                reason = "ANGULO ALTERADO"

            # SE DETECTAR ANOMALIA
            if anomaly_detected:
                # 1. Mostra visualmente na tela na HORA (sem travar o vídeo)
                cv2.rectangle(frame, (0,0), (640, 480), (0,0,255), 10)
                cv2.putText(frame, f"ALERTA: {reason}", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # 2. Verifica se já pode enviar uma nova notificação (Cooldown)
                current_time = time.time()
                if current_time - last_alert_time > COOLDOWN_DURATION:
                    print(f"🚨 NOVA ANOMALIA: {reason}. Enviando para IA e Telegram...")

                    IMAGE_DIR.mkdir(exist_ok=True)
                    img_path = str(IMAGE_DIR / "alert.jpg")
                    cv2.imwrite(img_path, frame)

                    # Chamada da IA e Telegram
                    diagnosis = agent.analyze_anomaly(img_path, reason)
                    send_telegram_alert(f"🚨 *SENTINEL:* {reason}\n\n*IA:* {diagnosis}", img_path)

                    # Atualiza o cronômetro do último alerta
                    last_alert_time = current_time
                else:
                    # Apenas log interno, sem enviar Telegram para não spammar
                    # O vídeo continua rodando normalmente aqui
                    pass

        # Informações de sensores no rodapé
        cv2.putText(frame, f"Foco: {int(foco)} | Brilho: {int(brilho)}", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # MOSTRA O VÍDEO (Sempre rodando!)
        cv2.imshow('SentinelSight AI', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and not system_active:
            reference_frame = frame.copy()
            system_active = True
            print("\n✅ POSIÇÃO SALVA! Monitorando...")
        if key == ord('r'):
            system_active = False
            last_alert_time = 0 # Reseta o tempo ao resetar o sistema
            print("\n🔄 Resetado. Ajuste e aperte 'S'.")
        if key == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
