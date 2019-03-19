
import app
import segment as Segment

seg = Segment.SegmentDisplay()

def on_message(client, obj, msg):
            print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	    print("====")
	    seg.numberDisplay_dec(float(str(msg.payload)))



client = app.MQTTClient("mqtt://bszhbvxe:c98S4q4Bpifl@m24.cloudmqtt.com:19448")
client.connect(on_message)
client.subscribeToTopic("temp")

