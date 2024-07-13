import json
import time
import random
from datetime import datetime

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from constants import PUBLISH_TOPIC, RABBITMQ_HOST, RABBITMQ_SERVER_PORT


def main():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(RABBITMQ_HOST, RABBITMQ_SERVER_PORT)

    mqttc.loop_start()

    while True:
        try:
            status = random.randint(0, 6)
            message = json.dumps(
                {"status": status, "created_at": datetime.now().isoformat()}
            )

            publish.single(PUBLISH_TOPIC, message, hostname="localhost")

        except KeyboardInterrupt:
            mqttc.disconnect()
            mqttc.loop_stop()

        time.sleep(1)


if __name__ == "__main__":
    main()
