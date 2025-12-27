import json
import paho.mqtt.client as mqtt
from datetime import datetime
from logger import Logger 

class mqtt_client(mqtt.Client):

    def __init__(self):
        # Configuración del cliente MQTT
        self.BROKER = "broker.emqx.io"  # Cambia esto por tu broker MQTT
        self.PORT = 1883  # Puerto del broker MQTT
        self.TOPICS = ["sensor/data/sen55", "sensor/data/gas_sensor"]  # Temas a los que se suscribirá el cliente

        self.logger = Logger("sensor")

    # Callback cuando se establece la conexión con el broker
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            for topic in self.TOPICS:
                self.client.subscribe(topic)
                print(f"Suscrito al tema '{topic}'")
        else:
            print(f"Error de conexión, código: {rc}")

    # Callback cuando se recibe un mensaje en los temas suscritos
    def on_message(self,client, userdata, msg):
        print(f"Mensaje recibido en el tema '{msg.topic}':")
        print(msg.payload.decode("utf-8"))

        try:
            # Decodificar y convertir el mensaje de JSON a diccionario
            payload = json.loads(msg.payload.decode("utf-8"))
            data = json.dumps(payload, indent=4) # Mostrar el mensaje formateado
            if Logger:
                self.logger.write_log(data)
            else:
                print("No se pudo inicializar el logger.")

            print(data)

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")

    # Bucle principal para mantener la conexión y escuchar mensajes    
    def loop_forever(self):
        # Crear un cliente MQTT
        self.client = mqtt.Client()

        # Asignar las funciones de callback
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Conectar al broker MQTT
        self.client.connect(self.BROKER, self.PORT, 60)

        # Bucle principal para mantener la conexión y escuchar mensajes
        print("Esperando mensajes... Presiona Ctrl+C para salir")
        try:
            self.client.loop_forever()  # Mantener el cliente en ejecución
        except KeyboardInterrupt:
            print("Desconectando del broker...")
            self.client.disconnect()
def main():
    client = mqtt_client()
    client.loop_forever()
    

if __name__ == "__main__":
    main()
