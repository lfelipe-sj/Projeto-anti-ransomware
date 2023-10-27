import shutil
import os
import datetime

def criar_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f'Pasta "{pasta}" criada com sucesso.')
    else:
        print(f'Pasta "{pasta}" já existe.')

def listar_backups(pasta):
    backups = [item for item in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, item))]
    if backups:
        print("Backups disponíveis:")
        for idx, backup in enumerate(backups, start=1):
            print(f"{idx}. {backup}")
        return backups
    else:
        print("Nenhum backup encontrado.")
        return []

def restaurar_backup(pasta_backup, pasta_destino):
    for item in os.listdir(pasta_destino):
        item_path = os.path.join(pasta_destino, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove arquivos no destino
        elif os.path.isdir(item_path):
            if not os.path.islink(item_path):
                remove_readonly(item_path)  # Remove pastas no destino

    for item in os.listdir(pasta_backup):
        item_path = os.path.join(pasta_backup, item)
        destination_path = os.path.join(pasta_destino, item)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, destination_path)  # Copia arquivos para o destino
        elif os.path.isdir(item_path):
            shutil.copytree(item_path, destination_path)  # Copia pastas para o destino
    print("Backup restaurado com sucesso.")

def remove_readonly(func):
    os.chmod(func, 0o777)  # Remove o atributo somente leitura
    shutil.rmtree(func, ignore_errors=True)

def abrir_pasta(diretorio):
    os.system(f'explorer "{diretorio}"')

def realizar_backup(pasta_origem, pasta_destino):
    try:
        shutil.copytree(pasta_origem, pasta_destino)
        print("Backup criado com sucesso.")
    except Exception as e:
        print(" ")
        #print(f"Erro ao criar o backup: {e}")

if __name__ == "__main__":
    pasta_backups = "C:\\Backups"
    criar_pasta(pasta_backups)

    caminho_backup = input("Digite o caminho em que deseja realizar o backup: ")
    pasta_selecionada_path = os.path.abspath(caminho_backup)

    if os.path.exists(pasta_selecionada_path):
        pasta_destino = os.path.join(pasta_backups, os.path.basename(pasta_selecionada_path))

        if os.path.exists(pasta_destino):
            criar_novo_backup = input("Já existe um backup para essa pasta. Deseja criar outro? (s/n): ")
            if criar_novo_backup.lower() == "s":
                data_hora = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                pasta_destino = os.path.join(pasta_backups, f"{os.path.basename(pasta_selecionada_path)}_{data_hora}")
                realizar_backup(pasta_selecionada_path, pasta_destino)
        else:
            realizar_backup(pasta_selecionada_path, pasta_destino)
    else:
        print("O caminho especificado não existe.")

    if os.path.exists(pasta_destino):
        opcao_restaurar = input("Deseja restaurar o backup para o destino original? (s/n): ")
        if opcao_restaurar.lower() == "s":
            backups_disponiveis = listar_backups(pasta_backups)
            if backups_disponiveis:
                indice_backup = int(input("Digite o número do backup para restaurar: ")) - 1
                if 0 <= indice_backup < len(backups_disponiveis):
                    pasta_backup_escolhido = os.path.join(pasta_backups, backups_disponiveis[indice_backup])
                    restaurar_backup(pasta_backup_escolhido, pasta_selecionada_path)
                    abrir_destino = input("Deseja abrir a pasta de destino após a restauração? (s/n): ")
                    if abrir_destino.lower() == "s":
                        abrir_pasta(pasta_selecionada_path)
                else:
                    print("Opção inválida.")
