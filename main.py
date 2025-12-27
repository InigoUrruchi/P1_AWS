from mqtt_client import mqtt_client
from test_mqtt import meshtastic
from threading import Thread

def main():
    #Instanciar clases
    client_mqtt = mqtt_client()
    client_meshtastic = meshtastic()

    #Incializar hilos
    thread_mqtt = Thread(target=client_mqtt.loop_forever)
    thread_mesh = Thread(target=client_meshtastic.run)

    #Iniciar hilos
    thread_mqtt.start()
    thread_mesh.start()

if __name__ == "__main__":
    main()