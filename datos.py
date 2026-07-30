from kafka import KafkaConsumer
import json

consumidor = KafkaConsumer(
    'transacciones_contables',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='grupo_gerencia',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
print("ACTIVO ")
print("Ecuchando\n")

try:
    for mensaje in consumidor:
        datos = mensaje.value
        print(f" nuevo registro")
        print(f" Cliente: {datos['cliente']} (NIT: {datos['nit']})")
        print(f" Monto: Bs. {datos['monto']}")
        print(f" Hora: {datos['fecha']}")
        print("-" * 50)
except KeyboardInterrupt:
    print("Cerrando escucha.")
finally:
    consumidor.close()