import os
import win32file
import win32con

def hide_directory_recursive(directory_path):
    # Oculta o diretório principal
    try:
        win32file.SetFileAttributes(directory_path, win32con.FILE_ATTRIBUTE_HIDDEN)
        print(f"O diretório {directory_path} está oculto.")
    except Exception as e:
        print(f"Erro ao ocultar o diretório {directory_path}: {e}")

    # Oculta arquivos e subdiretórios dentro do diretório
    for root, dirs, files in os.walk(directory_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                win32file.SetFileAttributes(dir_path, win32con.FILE_ATTRIBUTE_HIDDEN)
                #print(f"O diretório {dir_path} está oculto.")
            except Exception as e:
                print(f"Erro ao ocultar o diretório {dir_path}: {e}")

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                win32file.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_HIDDEN)
                #print(f"O arquivo {file_path} está oculto.")
            except Exception as e:
                print(f"Erro ao ocultar o arquivo {file_path}: {e}")

def unhide_directory_recursive(directory_path):
    # Remove o atributo de oculto do diretório principal
    try:
        win32file.SetFileAttributes(directory_path, win32con.FILE_ATTRIBUTE_NORMAL)
        print(f"O diretório {directory_path} foi desocultado.")
    except Exception as e:
        print(f"Erro ao desocultar o diretório {directory_path}: {e}")

    # Remove o atributo de oculto de arquivos e subdiretórios dentro do diretório
    for root, dirs, files in os.walk(directory_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                win32file.SetFileAttributes(dir_path, win32con.FILE_ATTRIBUTE_NORMAL)
                #print(f"O diretório {dir_path} foi desocultado.")
            except Exception as e:
                print(f"Erro ao desocultar o diretório {dir_path}: {e}")

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                win32file.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_NORMAL)
                #print(f"O arquivo {file_path} foi desocultado.")
            except Exception as e:
                print(f"Erro ao desocultar o arquivo {file_path}: {e}")

def protect_files(files):
    try:
        for file_path in files:
            os.chmod(file_path, 0o444)  # Define permissões de leitura somente para os arquivos
        print("Permissões de escrita removidas dos arquivos.")
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def restore_permissions(files):
    try:
        for file_path in files:
            os.chmod(file_path, 0o666)  # Restaura permissões originais
        print("Permissões de escrita restauradas nos arquivos.")
    except FileNotFoundError:
        print("Arquivo não encontrado.")

if __name__ == "__main__":
    folder_path = input("Digite o caminho para a pasta de backup que deseja proteger/restaurar: ")
    option = input("Escolha uma opção:\n1 - Ocultar diretório e subdiretórios\n2 - Desocultar diretório e subdiretórios\n3 - Proteger arquivos \n4 - Restaurar permissões dos arquivos\n")

    if option == "1":
        hide_directory_recursive(folder_path)
    elif option == "2":
        unhide_directory_recursive(folder_path)
    elif option == "3":
        files = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files]
        protect_files(files)
    elif option == "4":
        files = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files]
        restore_permissions(files)
    else:
        print("Opção inválida.")
