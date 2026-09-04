import cv2
import time
import numpy as np
from pathlib import Path
from vision_utils import VisionProcessor
from agent import SentinelAgent
from notifier import send_telegram_alert

# Mantendo sua mudança estrutural para o GitHub
IMAGE_DIR = Path(__file__).resolve().parent / "img"

def main():
    print("\n" + "="*60)
    print("🛡️  CFTVSECURITY-AI - MONITORAMENTO ESTRUTURADO")
    print("="*60)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    processor = VisionProcessor()
    agent = SentinelAgent()

    reference_frame = None
    system_active = False

    # Variáveis de controle de tempo
    last_alert_time = 0
    COOLDOWN_DURATION = 30

    print("\n[PASSO 1] Posicione sua câmera.")
    print("[PASSO 2] Pressione 'S' para SALVAR a posição inicial.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Captura de métricas básicas
        foco = processor.get_blur_score(frame)
        brilho = processor.get_brightness_score(frame)

        # Inicializamos a similaridade como 1.0 (perfeita) para evitar erros
        sim = 1.0

        if not system_active:
            status_text = "AGUARDANDO CONFIGURACAO... (Aperte 'S')"
            color = (255, 191, 0)
        else:
            status_text = "SISTEMA VIGILANTE ATIVO (Aperte 'R' para Reset)"
            color = (0, 255, 0)

        # Dashboard Visual Superior
        cv2.rectangle(frame, (0, 0), (700, 45), (0,0,0), -1)
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        if system_active:
            # --- LIMITES DE SENSIBILIDADE RECALIBRADOS ---
            LIMIT_BRILHO = 22
            LIMIT_FOCO = 80   # Aumentado para detectar mãos/objetos borrados melhor
            LIMIT_SIM = 0.50  # Tolerante para evitar falsos positivos de vibração

            anomaly_detected = False
            reason = ""

            # --- HIERARQUIA DE DETECÇÃO (RESOLVE A ALUCINAÇÃO) ---

            # 1. Primeiro checamos se a imagem está muito escura
            if brilho < LIMIT_BRILHO:
                anomaly_detected = True
                reason = "OBSTRUÇÃO (Câmera Escura/Tapada)"

            # 2. Se não estiver escura, checamos se está nítida (mão próxima borra o foco)
            elif foco < LIMIT_FOCO:
                anomaly_detected = True
                reason = "TAMPERING (Lente Borrada ou Objeto Próximo)"

            # 3. SÓ SE A IMAGEM ESTIVER BRILHANTE E NÍTIDA, checamos o ângulo
            else:
                sim = processor.compare_frames(reference_frame, frame)
                if sim < LIMIT_SIM:
                    anomaly_detected = True
                    reason = f"ANGULO ALTERADO (Sim: {sim:.2f})"

            # Ação em caso de anomalia
            if anomaly_detected:
                cv2.rectangle(frame, (0,0), (640, 480), (0,0,255), 10)
                cv2.putText(frame, f"ALERTA: {reason}", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                current_time = time.time()
                if current_time - last_alert_time > COOLDOWN_DURATION:
                    print(f"🚨 NOVA ANOMALIA: {reason}. Consultando IA...")

                    IMAGE_DIR.mkdir(exist_ok=True)
                    img_path = str(IMAGE_DIR / "alert.jpg")
                    cv2.imwrite(img_path, frame)

                    # Chamada da IA (Boto3/Nova) e Telegram
                    diagnosis = agent.analyze_anomaly(img_path, reason)
                    send_telegram_alert(f"🚨 *SENTINEL:* {reason}\n\n*IA:* {diagnosis}", img_path)

                    last_alert_time = current_time

        # Informações de sensores no rodapé (Dashboard dinâmico)
        cv2.putText(frame, f"Foco: {int(foco)} | Brilho: {int(brilho)} | Sim: {sim:.2f}",
                    (10, 465), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('CFTVSECURITY-AI - Live Monitor', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and not system_active:
            reference_frame = frame.copy()
            system_active = True
            print("\n✅ POSIÇÃO FIXADA! Monitorando...")
        if key == ord('r'):
            system_active = False
            last_alert_time = 0
            print("\n🔄 Resetado. Ajuste a câmera e aperte 'S'.")
        if key == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
