import pymysql
from kafka import KafkaProducer
import json
import time
from datetime import datetime
import random
import ssl

productor = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("conectando a DB")
conexion = pymysql.connect(
    host='serverless-us-east4.sysp0000.db2.skysql.com',
    port=4049,
    user='dbpgf00710410',
    password='4wHnZv3Id4rjbe=ZCu0^v',
    database='dyjdb',
    ssl={"cert_reqs": ssl.CERT_NONE} 
)
cursor = conexion.cursor()
print("conexion exitosa")
print("iniciando")

for i in range(1, 4):
    now = datetime.now()
    fecha_actual = now.strftime('%Y-%m-%d %H:%M:%S')
    mes = now.month
    ano = now.year
    
    id_punto_venta = 1
    nit = f"102030{i}02"
    razon_social = f"Cliente {i}"
    num_fact = random.randint(10000, 99999)
    num_aut = f"100000{random.randint(100000, 999999)}"
    total_fact = round(random.uniform(50.0, 1500.0), 2)
    importe_ice = 0
    importe_exento = 0
    importe_neto = round(total_fact * 0.87, 2)
    debito_fiscal = round(total_fact * 0.13, 2)
    codigo_control = "A1-B2-C3-D4"
    id_rubro = 1
    tipo = random.choice([1, 2])

    #sql
    sql_insert = """
        INSERT INTO venta (
            idpuntoVenta, nitCliente, razonSocial, numFact, numAut, 
            fechaCliente, totalFact, importeIce, importeExento, importeNeto, 
            debitoFiscal, codigoControl, mes, ano, idrubro, tipo
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    valores = (
        id_punto_venta, nit, razon_social, num_fact, num_aut, 
        fecha_actual, total_fact, importe_ice, importe_exento, importe_neto, 
        debito_fiscal, codigo_control, mes, ano, id_rubro, tipo
    )
    
    try:
        # Guardar en BD
        cursor.execute(sql_insert, valores)
        conexion.commit()
        print(f"{total_fact}registrada")
    except Exception as e:
        print(f"Error BD: {e}")
        continue
    mensaje_kafka = {
        "fecha": fecha_actual,
        "nit": nit,
        "cliente": razon_social,
        "monto": total_fact,
        "sucursal": "Sede Potosi"
    }
    
    productor.send('transacciones_contables', value=mensaje_kafka)
    print("enviando")
    
    time.sleep(3) 

productor.flush()
cursor.close()
conexion.close()
print("Finalizado.")