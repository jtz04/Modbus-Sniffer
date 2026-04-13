import os
import pandas as pd
from scapy.all import TCP, IP, sniff, load_contrib
from datetime import datetime

# carregar o modulo de protocolo modbus para que o scapy possa reconhecer os pacotes modbus
load_contrib('modbus')

#importar as classes de request e response do modbus para analisar os pacotes
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse

# lista para armazenar os logs dos pacotes capturados
logs_ids = []

# função para analisar os pacotes capturados
def analisa_pkt_modbus(pkt):
    #checagem de segurnaa para verificar se o pacote tem a camada IP e TCP
    if pkt.haslayer(IP) and pkt[TCP]:

        #checagem para verificar se o pacote é do Modbus TCP (porta 502)
        if pkt[TCP].dport == 502 or pkt[TCP].sport == 502:

            #extrair IPs
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

            # Converte o horário do pacote (timestamp) para algo legível
            horario = datetime.fromtimestamp(pkt.time).strftime('%Y-%m-%d %H:%M:%S')

            tipo = None
            codigo_funcao = None
            is_modbus_valid = False  # Flag para indicar se é um pacote Modbus válido

            # identificar se é uma requisicao ou resposta do Modbus
            
            if pkt.haslayer(ModbusADURequest):
                tipo = "Request"
                codigo_funcao = pkt[ModbusADURequest].funcCode
                is_modbus_valid = True
            elif pkt.haslayer(ModbusADUResponse):
                tipo = "Response"
                codigo_funcao = pkt[ModbusADUResponse].funcCode
                is_modbus_valid = True
            else:
                print(f"[{horario}] Pacote TCP na porta 502, mas não é Modbus válido: {src_ip} -> {dst_ip}")

            # Criar e salvar registro apenas se for Modbus válido
            if is_modbus_valid:
                registro = {
                    "Horario": horario,
                    "IP_Origem": src_ip,
                    "IP_Destino": dst_ip,
                    "Tipo": tipo,
                    "Funcao": codigo_funcao
                }
                logs_ids.append(registro)
                print(f"[{horario}] Capturado: {src_ip} -> {dst_ip} | Funcao: {codigo_funcao}")
            
        print("Pacote Modbus TCP detectado:")

        #exibir um resumo do pacote
        print(pkt.summary())

# numero de pacotes 
qtde_pkts = 10
print("---- Iniciando captura de trafego Modbus: ----")
print(f" Aguardando trafego na porta 502... (Capturando {qtde_pkts} pacotes...) \n ")

sniff(iface="Software Loopback Interface 1", filter="tcp port 502", prn=analisa_pkt_modbus, count=qtde_pkts)
#sniff é uma função do scapy que captura pacotes da rede.
#iface especifica a interface de rede a ser monitorada declarada como "lo" no linux e "Software Loopback Interface 1" no windows para monitorar o tráfego local (loopback). 
#filter é um filtro de captura para limitar os pacotes capturados
#prn é uma função de callback que é chamada para cada pacote capturado
#count especifica o número de pacotes a serem capturados antes de parar a captura


# tratamento dos logs capturados para salvar em um arquivo CSV e exibir a tabela final
print(f"--- Captura finalizada. Gerando DataFrame ---")

csv_file = "logs_modbus.csv" 
df_logs = pd.DataFrame(logs_ids) #gerar um DataFrame a partir da lista de logs capturados

if df_logs.empty: #verificar se o DataFrame está vazio (sem logs capturados)
    print("Nenhum log Modbus válido capturado. O arquivo CSV não foi alterado.")
    
else: #salvar os logs em um arquivo CSV. Se o arquivo já existir, os novos logs serão adicionados ao final do arquivo sem sobrescrever os dados existentes.
    write_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
    df_logs.to_csv(csv_file, sep=";", index=False, mode="a", header=write_header)
    print(f"Logs salvos em '{csv_file}' (adicionados ao fim do arquivo).")

print("\nTabela final de Logs:")
print(df_logs.to_string())

