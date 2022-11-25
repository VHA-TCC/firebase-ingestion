import base64
import json
import functions_framework

from firestore import Firestore
from telemetry import Telemetry, EngineSpeed, FuelTank, Speed, GeoLocalization

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def load_data(cloud_event):
   # Print out the data from Pub/Sub, to prove that it worked
   telemetry_data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8'))

   vehicle_id = telemetry_data.get("vin")

   if vehicle_id is None:
      return { "error": 'Could not find vehicle id inside telemetry data.' }, 400

   telemetry = Telemetry(engineSpeed=EngineSpeed(unit=telemetry_data.get("rpm", {}).get("unit"),
                                                 value=float(telemetry_data.get("rpm", {}).get("value"))),
                         fuelTank=FuelTank(unit="%",
                                           value=telemetry_data.get("fuelLevel", 0)),
                         location=GeoLocalization(latitude=float(telemetry_data.get("geolocation", {}).get("lat")),
                                                  longitude=float(telemetry_data.get("geolocation", {}).get("lng"))),
                         speed=Speed(unit=telemetry_data.get("speed", {}).get("unit"),
                                     value=float(telemetry_data.get("speed", {}).get("value"))),
                         vehicle_id=vehicle_id)
   
   firestore = Firestore()
   firestore.upsert(collection="telemetry",
                    document=vehicle_id,
                    data=telemetry.get_data())
   
   return { "created": True }, 201
