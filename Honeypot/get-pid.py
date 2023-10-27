# Path -> C:\Users\UserFelipe\output
# Registra ID de novos Processos
import wmi

#  Captura novos PID em tempo real 
def process_monitor():   
   objCom = wmi.WMI()
   new_procs = objCom.watch_for(notification_type="Creation", wmi_class="Win32_Process")
   count = 0
   with open("LISTA", "w") as output:
       output.close()
       
   while True:
    processo = new_procs()
    with open ("LISTA", "a") as output:
        if count == 9:
            output.write(f"{processo.ProcessId},\n")
            count = 0

        else: 
            output.write(f"{processo.ProcessId},")
            count += 1

if __name__ == "__main__":
    process_monitor()