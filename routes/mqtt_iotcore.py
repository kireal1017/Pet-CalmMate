from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def send_mqtt_message(topic, message): #mqtt전송 API
    client = AWSIoTMQTTClient("nyangmeong-device")
    client.configureEndpoint("a3vvk9g700ik4i-ats.iot.ap-northeast-2.amazonaws.com", 8883)
    client.configureCredentials(
        "certs/AmazonRootCA1.pem",
        "certs/private.pem.key",
        "certs/certificate.pem.crt"
    )

    print("Connecting to AWS IoT Core...")
    client.connect()
    print("Connected!")

    print(f"Publishing to {topic}: {message}")
    client.publish(topic, message, 1)
    print("Done.")