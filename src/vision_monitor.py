import cv2
import numpy as np

def monitor_camera():
    cap = cv2.VideoCapture(0) # 0 é a sua webcam

    print("Monitorando câmera... Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Converte para cinza para analisar brilho
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)

        # SE O BRILHO FOR MUITO BAIXO (Câmera tampada)
        if avg_brightness < 20:
            print("⚠️ ANOMALIA DETECTADA: Câmera possivelmente obstruída!")
            # Aqui chamaremos o Agente Strands no futuro
            cv2.putText(frame, "ALERTA: OBSTRUCAO", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('SentinelSight - Local Monitor', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    monitor_camera()
