# RWS #

Esse Projeto consiste no desenvolvimento de uma Solução Anti-Ransomware. Desenvolvido pela Equipe RansomWShield\
Fique a vontade para ajudar na evolução dos programas para a proteção de sistemas Windows

## Sumário
* [Descrição](#Descrição)
* [Tecnologias](#Tecnologias)
* [Back-end e Funcionamento](#Back-end)

## Descrição

Esse projeto consiste em um programa que cria um backup que permite ao usuário criar, gerenciar e restaurar backups das pastas do seu computador. O outro programa é responsável por proteger os arquivos do backup contra escrita de ransomwares nos arquivos, e além disso oculta os seus arquivos do diretório backup do usuário.\
\
O próximo programa foi desenvolvido com a inteção de detectar ações de ransomwares a partir de armadilha que chamamos de honeypot. Com ele é possível identificar as alterações de arquivos em que o usuário não deveria alterar, mas um ransomware com foco em criptograr todos os arquivos acaba caindo nas "traps" e alertando a ferramenta. A partir disso, a ferramenta analisa um arquivo chamado LISTA que armazena todos os novos PIDs executados do sistema windows - esse arquivo é gerado pelo programa "get-pid.exe" que é responsável por monitorar os novos PIDs gerados. Usando uma relação, se torna possivel identificar os PIDs responsáveis pelas modificações dos arquivos honeyfile do sistema, permitindo encerrar as ações do ransomware antes que prejudique mais o ambiente. \
\
Para instalar nossas ferramentas, acesse https://github.com/RansomWshielD/RWS-Challenge/tree/main/RWS-setup e leia o arquivo LEIA-ME.txt. Após isso instale os programas contidos na pasta Honeypot e Backup do link https://github.com/RansomWshielD/RWS-Challenge/tree/main/RWS-setup .\
\
Caso queria consultar nosso código fonte acesse as pastas Honeypot e Backup do link https://github.com/RansomWshielD/RWS-Challenge/. E para saber mais consulte o tópico Back-end e Funcionamento.

## Tecnologias
* Pyhton
* Visual Studio 2022
* Visual Studio Code
* Inno Setup

## Back-end
Honeypot (dTrapRWS.py e get-pid.py)

* get-pid.py: \
O código utiliza a biblioteca wmi para interagir com o Windows Management Instrumentation (WMI), que permite acessar informações e funcionalidades do sistema Windows.\
\
Ele define uma função chamada process_monitor, cujo objetivo é monitorar a criação de novos processos no sistema Windows em tempo real.\
\
Dentro dessa função, um objeto WMI é criado para interagir com o sistema operacional Windows.\
\
Em seguida, é criado um objeto new_procs que irá monitorar a criação de novos processos no sistema. Ele usa o WMI para realizar essa tarefa.\
\
O código inicializa um contador chamado count como zero e cria (ou recria) um arquivo chamado "LISTA" para registrar os IDs de processo (PIDs) dos processos monitorados.\
\
Entra em um loop infinito que continuará monitorando processos em tempo real.\
\
A cada iteração do loop, o código obtém o próximo processo criado no sistema usando o objeto new_procs.\
\
Em seguida, o PID desse processo é registrado no arquivo "LISTA". O código verifica se count atingiu o valor 9 e, se isso ocorrer, adiciona o PID seguido de uma quebra de linha para iniciar uma nova linha no arquivo. Caso contrário, ele adiciona o PID seguido de uma vírgula para separar os PIDs.\
\
Finalmente, o código verifica se o script está sendo executado diretamente (não importado como um módulo) e, se for o caso, inicia a função process_monitor.



* dTrapRWS.py: \
Importações de bibliotecas Python: time, subprocess, psutil, atexit, watchdog, e uso de classes e funções relacionadas a essas bibliotecas. \
\
arquivos_alvo = ["bbdilha", "yydilha"]\
Essa lista contém os nomes dos arquivos que o código monitorará em busca de alterações. Esses são os arquivos que são suscetíveis a serem modificados por um ransomware. \
\
Função create_files_in_user_directories:\
Esta função cria os arquivos alvo ("bbdilha" e "yydilha") nas pastas "Documents," "Downloads," e "Desktop" do usuário. \
\
Função terminate_processes:\
Esta função é usada para encerrar processos específicos com base em seus PIDs. Ela é usada para encerrar processos maliciosos que podem estar tentando modificar os arquivos alvo. \
\
Função monitor_user_directories:\
Esta função monitora as pastas alvo ("Documents," "Downloads," e "Desktop") em busca de modificações nos arquivos alvo. Ela cria observadores para essas pastas e reage a eventos de modificação usando a classe personalizada MeuManipuladorDeEventos.\
\
Classe MeuManipuladorDeEventos:\
Esta é uma classe personalizada que herda de FileSystemEventHandler. Ela é usada para reagir a eventos de modificação de arquivos nas pastas alvo. Quando um arquivo alvo é modificado, esta classe verifica o tempo de execução, obtém a lista de PIDs gerados nos últimos 60 segundos e tenta encerrar esses processos.\
\
Função get_recent_pids:\
Esta função obtém uma lista de PIDs de processos que foram criados nos últimos 60 segundos, com base no conteúdo do arquivo "LISTA" onde os PIDs são registrados.\
\
Função get_first_last_pids:\
Esta função obtém o primeiro e o último PID de processos que foram criados nos últimos "intervalo_segundos" segundos. Ela é usada em conjunto com get_recent_pids.\
\
Função pids_extern:\
Esta função obtém os PIDs de processos externos usando a biblioteca psutil. Ela é usada para obter o PID do processo "get-pid.exe".\
\
Função get_pid:\
Esta função inicia o processo "get-pid.exe" e obtém seu PID. Ela é usada para rastrear o processo "get-pid.exe" e encerrá-lo posteriormente.\
\
Função kill_end:\
Esta função é usada para encerrar processos com base em seus PIDs, como o processo "get-pid.exe" quando o programa é encerrado.\
\
Função main:
Esta função é o ponto de entrada do programa. Ela cria os arquivos alvo, inicia o processo "get-pid.exe" e, em seguida, inicia o monitoramento das pastas alvo.


Backup (bckpRWS.py e seguranca-Backup.py)

* bckpRWS.py: \
Função criar_pasta:\
Esta função verifica se uma pasta especificada existe. Se não existir, ela a cria e imprime uma mensagem de confirmação. Se já existir, apenas imprime uma mensagem informando que a pasta já existe.\
\
Função listar_backups:\
Esta função lista os diretórios disponíveis (backups) dentro de uma pasta especificada e retorna uma lista com seus nomes. Se não houver backups, ela informa que nenhum backup foi encontrado.\
\
Função restaurar_backup:\
Esta função restaura um backup para uma pasta de destino. Ela remove todos os arquivos e pastas existentes na pasta de destino e, em seguida, copia os arquivos e pastas do backup para o destino.\
\
Função remove_readonly:\
Esta função é usada para remover a flag "somente leitura" dos arquivos e pastas no destino antes de removê-los.\
\
Função abrir_pasta:\
Esta função abre uma pasta no Explorador de Arquivos do Windows usando o comando explorer.\
\
Função realizar_backup:\
Esta função cria um backup copiando todos os arquivos e pastas de uma pasta de origem para uma pasta de destino usando shutil.copytree.\
\
Bloco if __name__ == "__main__":\
Este bloco é a parte principal do código que é executada quando o script é iniciado diretamente.\
\
Criação da pasta de backups:\
O código cria a pasta "C:\Backups" usando a função criar_pasta.\
\
Seleção da pasta a ser realizada o backup:\
O usuário é solicitado a inserir o caminho da pasta que deseja fazer backup.\
\
Verificação da existência da pasta selecionada:\
O código verifica se a pasta selecionada existe.\
\
Criação de um novo backup:\
Se a pasta de destino para o backup já existir, o usuário é questionado se deseja criar outro backup. Se sim, um novo diretório de backup é criado com um timestamp para evitar conflitos.\
\
Realização do backup:\
A função realizar_backup é chamada para criar o backup da pasta selecionada.\
\
Restauração do backup:\
O usuário é questionado se deseja restaurar o backup para a pasta de destino original.\
\
Listagem de backups disponíveis:\
Se a resposta for "sim", a função listar_backups é chamada para listar os backups disponíveis.\
\
Escolha do backup para restaurar:\
O usuário escolhe qual backup deseja restaurar com base em sua posição na lista.\
\
Restauração do backup selecionado:\
A função restaurar_backup é chamada para restaurar o backup selecionado para a pasta de destino original.\
\
Abertura da pasta de destino após a restauração:\
O usuário é questionado se deseja abrir a pasta de destino após a restauração. Se sim, a função abrir_pasta é chamada.

* seguranca-Backup.py:\
Este código em Python para Windows oferece funcionalidades para proteger e ocultar diretórios e arquivos em um sistema de arquivos. \
\
Função hide_directory_recursive:\
Esta função oculta um diretório e todos os seus subdiretórios e arquivos. Ela utiliza a biblioteca win32file para definir o atributo "oculto" em todos os elementos do diretório.\
\
Função unhide_directory_recursive:\
Esta função desoculta um diretório e todos os seus subdiretórios e arquivos, restaurando o atributo "normal" a eles.\
\
Função protect_files:\
Esta função remove permissões de escrita (atribuindo permissões somente de leitura) dos arquivos especificados. Isso pode ser usado para proteger arquivos contra modificações acidentais ou não autorizadas.
\
Função restore_permissions:\
Esta função restaura as permissões originais de escrita nos arquivos especificados, removendo as restrições impostas anteriormente.\
\
Bloco if __name__ == "__main__":\
Este bloco é a parte principal do código que é executada quando o script é iniciado diretamente.\
\
Entrada do caminho da pasta:\
O usuário é solicitado a inserir o caminho da pasta que deseja proteger, ocultar, proteger arquivos ou restaurar permissões.\
\
Escolha da opção:\
O usuário escolhe uma das opções disponíveis, que incluem ocultar o diretório e seus conteúdos, desocultar o diretório e seus conteúdos, proteger arquivos e restaurar permissões de arquivos.\
\
Execução da opção selecionada:\
Com base na opção escolhida pelo usuário, o código executa a função apropriada.
