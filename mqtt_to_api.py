import paho.mqtt.client as mqtt
import json
import requests

BROKER_IP = "192.168.100.2"
BROKER_PORT = 1883
MQTT_USER = "root"
MQTT_PASS = "dietpi"

TOPICO = "casa/sala/bme280"


API_URL = "http://127.0.0.1:5000/api/enviar_leitura"  


def enviar_para_api(temperatura, umidade, pressao, sensor_id=1):
    """Envia os dados recebidos do MQTT para a API externa Flask"""
    try:
        payload = {
            "temperatura": temperatura,
            "umidade": umidade,
            "pressao": pressao,
            "sensorID": sensor_id
        }

        resposta = requests.post(API_URL, json=payload)

        print("➡️ Enviando para API:", payload)
        print("⬅️ Resposta API:", resposta.json())

    except Exception as e:
        print("❌ Erro ao enviar para API:", e)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✔ Conectado ao broker MQTT!")
        client.subscribe(TOPICO)
        print(f"📡 Inscrito no tópico: {TOPICO}")
    else:
        print(f"❌ Falha na conexão! Código: {rc}")


def on_message(client, userdata, msg):
    try:
        mensagem = msg.payload.decode()
        print(f"📨 Mensagem recebida: {mensagem}")

        dados = json.loads(mensagem)

        temperatura = dados.get("temperatura")
        umidade = dados.get("umidade")
        pressao = dados.get("pressao")
        sensor_id = dados.get("sensorID", 1)

        if temperatura is None or umidade is None or pressao is None:
            print("⚠ Pacote incompleto. Ignorando.")
            return

        enviar_para_api(temperatura, umidade, pressao, sensor_id)

    except json.JSONDecodeError:
        print("⚠ Mensagem não está em formato JSON!")


client = mqtt.Client()

if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, BROKER_PORT, 60)

client.loop_forever()
