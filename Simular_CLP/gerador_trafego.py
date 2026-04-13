# funcionando como cliente


from pymodbus.client import ModbusTcpClient
import time

print("Conectando ao CLP Virtual...")
# Conecta no IP local onde o nosso Servidor está rodando
cliente = ModbusTcpClient('127.0.0.1', port=502)

if cliente.connect():
    print("Conexão bem sucedida! Enviando comandos...\n")
    
    # Simula o envio de 3 comandos com um intervalo de 2 segundos entre eles
    for i in range(3):
        valor_falso = 100 + i
        print(f"Tentando escrever o valor {valor_falso} no registrador 10...")
        
        # O comando write_register gera o Function Code 6 (Escrita) que o seu IDS deve pegar!
        cliente.write_register(address=10, value=valor_falso, slave=1)
        time.sleep(2)
        
    cliente.close()
    print("\nFim da simulação de tráfego.")
else:
    print("Falha ao conectar no CLP.")