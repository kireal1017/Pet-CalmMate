from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from uuid import uuid4

def send_mqtt_message(topic, message):
    client = AWSIoTMQTTClient(f"nyangmeong-device-{uuid4().hex[:6]}")

    client.configureEndpoint("a3vvk9g700ik4i-ats.iot.ap-northeast-2.amazonaws.com", 8883)
    client.configureCredentials(
        "certs/AmazonRootCA1.pem",
        "certs/private.pem.key",
        "certs/certificate.pem.crt"
    )

    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)

    print("Connecting to AWS IoT Core...")
    client.connect()
    print("Connected!")

    print(f"Publishing to {topic}: {message}")
    client.publish(topic, message, 1)
    print("Done.")

    client.disconnect()
    print("Disconnected.")