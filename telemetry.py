from dataclasses import dataclass, asdict

@dataclass
class EngineSpeed:
   unit: str
   value: int

@dataclass
class FuelTank:
   unit: str
   value: int

@dataclass
class GeoLocalization:
   latitude: float
   longitude: float

@dataclass
class Speed:
   unit: str
   value: int

@dataclass
class Telemetry:
   engineSpeed: EngineSpeed
   fuelTank: FuelTank
   location: GeoLocalization
   speed: Speed
   vehicle_id: str

   def get_data(self):
      return asdict(self)