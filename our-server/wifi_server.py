import asyncio, json, time
import picar_4wd as fc
from picar_4wd.adc import ADC
from websockets.server import serve

HOST = "100.95.25.48" # RPi IP address
# HOST = "127.0.0.1"
PORT = 65432

async def parseData(websocket):
	async for message in websocket:
		print(message)
		data = json.loads(message)

		if ("request" not in data) or (data["request"] != "move" and data["request"] != "sensor_data"):
			await websocket.send(json.dumps({"error": "Invalid message"}))
			continue

		if data["request"] == "move":
			if "type" not in data:
				await websocket.send(json.dumps({"error": "Invalid message"}))
				continue
			
			if data["type"] == "forward":
				print("forward")
				fc.forward(50)
			elif data["type"] == "backward":
				print("backward")
				fc.backward(50)
			elif data["type"] == "left":
				print("left")
				fc.turn_left(50)
			elif data["type"] == "right":
				print("right")
				fc.turn_right(50)
			elif data["type"] == "stop":
				print("stop")
				fc.stop()
			
			await websocket.send(json.dumps({"status": "ok", "data": None}))

		elif data["request"] == "sensor_data":
			await websocket.send(json.dumps({"status": "ok", "data": {
				"speed": fc.speed_val(),
				"servo": fc.get_distance_at(0),
				"power": power_read(),
				"grayscale": fc.get_grayscale_list()
			}}))
		
		else:
			await websocket.send(json.dumps({"status": "unknown"}))
		
		await asyncio.sleep(0.01)

def power_read():
    power_read_pin = ADC('A4')
    power_val = power_read_pin.read()
    power_val = power_val / 4095.0 * 3.3
    # print(power_val)
    power_val = power_val * 3
    power_val = round(power_val, 2)
    return power_val

async def main():
	async with serve(parseData, HOST, PORT):
		await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())