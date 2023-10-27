import os
import time
import subprocess
import psutil
import atexit

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Nomes dos arquivos que você deseja criar e monitorar
arquivos_alvo = ["bbdilha", "yydilha"]

# Função que cria os arquivos nos diretórios "Documents," "Downloads," e "Desktop"
def create_files_in_user_directories():
    # Obtém o diretório do usuário padrão
    home_dir = os.path.expanduser("~")

    # Diretórios alvo
    target_directories = ["Documents", "Downloads", "Desktop"]

    for arquivo in arquivos_alvo:
        for directory in target_directories:
            # Caminho completo para o diretório alvo
            target_dir = os.path.join(home_dir, directory)

            # Verifica se o diretório existe
            if os.path.exists(target_dir):
                # Caminho completo para o arquivo
                file_path = os.path.join(target_dir, arquivo)

                # Cria o arquivo e sobrescreve se ele já existir
                with open(file_path, "w") as f:
                    f.write("ATENCAO!!! Este arquivo é um objeto utilizado para monitorar processos maliciosos desta pasta. Arquivo criado em: {}.".format(time.strftime("%Y-%m-%d %H:%M:%S")))
                    print("Arquivo criado em:", file_path)
            else:
                print("O diretório", directory, "não existe no diretório do usuário.")

def terminate_processes(pids):
    for pid in pids:
        try:
            process = psutil.Process(pid)
            process.terminate()  # Encerra o processo com o PID especificado
            print(f"Processo com PID {pid} encerrado.")
        except psutil.NoSuchProcess:
            print(f"Processo com PID {pid} não encontrado.")
        except psutil.AccessDenied:
            print(f"Sem permissão para encerrar o processo com PID {pid}.")

# Função que monitora os diretórios alvo
def monitor_user_directories():
    # Lista dos diretórios que você deseja monitorar
    diretorios_alvo = [
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
    ]

    # Função para criar um observador para um diretório se ele existir
    def criar_observador(diretorio):
        if os.path.exists(diretorio):
            observer = Observer()
            event_handler = MeuManipuladorDeEventos()
            observer.schedule(event_handler, path=diretorio, recursive=True)
            observer.start()
            return observer
        else:
            return None

    # Crie uma classe de manipulador de eventos personalizada
    class MeuManipuladorDeEventos(FileSystemEventHandler):
        def on_any_event(self, event):
            # Este método será chamado sempre que qualquer evento ocorrer

            for arquivo in arquivos_alvo:
                # Verifique se o arquivo-alvo está presente no evento
                if event.src_path.endswith(arquivo):
                    print("\nola mundo em", event.src_path)

                    # Calcule o tempo de execução em tempo real
                    tempo_execucao = time.time() - tempo_inicio
                    print(f"Tempo de execução: {tempo_execucao:.2f} segundos")

                    # Obtenha a lista de PIDs gerados nos últimos 60 segundos
                    lista_pids = get_recent_pids(60)
                    print(f"PIDs gerados nos últimos 60 segundos: {lista_pids}")
                    terminate_processes(lista_pids)

    # Inicie o tempo de execução
    tempo_inicio = time.time()

    # Crie observadores apenas para os diretórios que existem
    observers = [criar_observador(diretorio) for diretorio in diretorios_alvo]

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            if observer:
                observer.stop()

    # Aguarde até que todos os observadores terminem
    for observer in observers:
        if observer:
            observer.join()

def get_recent_pids(intervalo_segundos):
    # Obtém o primeiro e o último PID gerados nos últimos "intervalo_segundos" segundos
    primeiro_pid, ultimo_pid = get_first_last_pids(intervalo_segundos)

    # Lista para armazenar os PIDs
    lista_pids = []

    # Lê o arquivo "LISTA" e obtém os PIDs entre o primeiro e o último PID, se ambos não forem None
    if primeiro_pid is not None and ultimo_pid is not None:
        with open("LISTA", "r") as arquivo_lista:
            pids = arquivo_lista.read().split(",")
            for pid in pids:
                try:
                    pid_int = int(pid)
                    if primeiro_pid <= pid_int <= ultimo_pid:
                        lista_pids.append(pid_int)
                except ValueError:
                    pass

    return lista_pids

def get_first_last_pids(intervalo_segundos):
    # Obtém o tempo atual
    tempo_atual = time.time()

    # Calcula o tempo limite
    tempo_limite = tempo_atual - intervalo_segundos

    # Inicializa o primeiro e o último PID como None
    primeiro_pid = None
    ultimo_pid = None

    # Itera pelos PIDs dos processos
    for proc in psutil.process_iter(['pid', 'create_time']):
        pid = proc.info['pid']
        create_time = proc.info['create_time']

        # Verifica se o processo foi criado nos últimos "intervalo_segundos" segundos
        if create_time >= tempo_limite:
            # Define o primeiro PID se ainda não estiver definido
            if primeiro_pid is None:
                primeiro_pid = pid

            # Define o último PID, substituindo o anterior a cada iteração
            ultimo_pid = pid

    return primeiro_pid, ultimo_pid

def pids_extern():
    time.sleep(2)
    pids = []  # Lista para armazenar os PIDs
    if True:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info['name'] == 'get-pid.exe':
                pids.append(proc.info['pid'])  # Adiciona o PID à lista
        return pids

def get_pid():
    try:
        get_pid = subprocess.Popen("get-pid.exe", creationflags=0x08000000)
        pidd = pids_extern()
        print(f"\nPID do get-pid.exe = {pidd}")
        atexit.register(kill_end, pids=pidd)
        return True
    except:
        print("Nao foi possível encontrar o arquivo get-pid.exe na mesma pasta")
        quit()

def kill_end(pids):
    for piid in pids:
        try:
            process = psutil.Process(piid)
            process.terminate()  # Encerra o processo com o PID especificado
            print(f"Processo com PID {piid} encerrado.")
        except psutil.NoSuchProcess:
            print(f"Processo com PID {piid} não encontrado.")
        except psutil.AccessDenied:
            print(f"Sem permissão para encerrar o processo com PID {piid}.")

def main():
    print("\n************* RWS em Operação *************")
    create_files_in_user_directories()
    if get_pid():
        print("\n-------------> get-pid.exe em execução!")
    else:
        print("Falha ao executar o get-pid.exe. Verifique se o programa está na mesma pasta.")

    # Após a execução do get-pid.exe, inicie o monitoramento dos diretórios
    monitor_user_directories()

if __name__ == "__main__":
    main()
