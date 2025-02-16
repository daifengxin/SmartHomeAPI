#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Smart Home System API Implementation
Provides functionality for managing houses, floors, rooms and devices
with focus on input validation and error handling.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
import uuid


class SmartHomeError(Exception):
    """Base exception class for Smart Home System"""
    pass


class UserError(SmartHomeError):
    """Exception raised for user-related errors"""
    pass


class HouseError(SmartHomeError):
    """Exception raised for house-related errors"""
    pass


class DeviceError(SmartHomeError):
    """Exception raised for device-related errors"""
    pass


class UserRole(Enum):
    """User roles in the system"""
    ADMIN = "admin"
    REGULAR = "regular"


class RoomType(Enum):
    """Available room types"""
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"
    KITCHEN = "kitchen"
    LIVING_ROOM = "living_room"
    OTHER = "other"


class DeviceType(Enum):
    """Supported device types"""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LIGHT = "light"
    SECURITY_CAMERA = "security_camera"
    DOOR_LOCK = "door_lock"
    OTHER = "other"


@dataclass
class Location:
    """Geographic location data"""
    latitude: float
    longitude: float


@dataclass
class User:
    """User data structure"""
    id: str
    name: str
    email: str
    role: UserRole

    def __init__(self, name: str, email: str, role: UserRole = UserRole.REGULAR):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role


@dataclass
class Device:
    """Device data structure"""
    id: str
    type: DeviceType
    name: str
    status: Dict

    def __init__(self, device_type: DeviceType, name: str):
        self.id = str(uuid.uuid4())
        self.type = device_type
        self.name = name
        self.status = {}


@dataclass
class Room:
    """Room data structure with type classification"""
    id: str
    name: str
    type: RoomType
    floor: int
    size: float  # in square meters
    devices: List[Device]

    def __init__(self, name: str, room_type: RoomType = RoomType.OTHER, floor: int = 1, size: float = 0.0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = room_type
        self.floor = floor
        self.size = size
        self.devices = []


@dataclass
class Floor:
    """Floor data structure"""
    id: str
    name: str
    floor_number: int
    rooms: List[Room]

    def __init__(self, name: str, floor_number: int = 1):
        self.id = str(uuid.uuid4())
        self.name = name
        self.floor_number = floor_number
        self.rooms = []


@dataclass
class House:
    """House data structure with location tracking"""
    id: str
    name: str
    address: str
    location: Location
    owner_id: str
    floors: List[Floor]

    def __init__(self, name: str, address: str, location: Location):
        self.id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.location = location
        self.owner_id = ""
        self.floors = []


class SmartHomeAPI:
    """Smart Home System API

    This API provides functionality to manage houses, floors, rooms and devices.
    It focuses on input validation and error handling without actual database
    or device implementations.

    Features:
    - User management (create, get, update)
    - House management (create, get, update, delete)
    - Floor management (add, get)
    - Room management (add, get)
    - Device management (add, get, update status)
    """

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.houses: Dict[str, House] = {}
    
    def _validate_input(self, value: str, min_length: int, field_name: str, is_email: bool = False) -> None:
        """Validate input string

        Args:
            value: String to validate
            min_length: Minimum required length
            field_name: Name of the field for error message
            is_email: Whether to validate email format

        Raises:
            UserError: If validating user input
            HouseError: If validating house input
            DeviceError: If validating device input
        """
        error_class = SmartHomeError
        if field_name.startswith("User"):
            error_class = UserError
        elif field_name.startswith("House") or field_name.startswith("Floor") or field_name.startswith("Room"):
            error_class = HouseError
        elif field_name.startswith("Device"):
            error_class = DeviceError

        if not value or len(value.strip()) < min_length:
            raise error_class(f"{field_name} must be at least {min_length} characters")
        if is_email and not '@' in value:
            raise UserError("Invalid email format")  # Email validation always raises UserError

    def _validate_id(self, id_str: str, entity_type: str) -> None:
        """Validate ID format and existence"""
        error_class = SmartHomeError
        if entity_type.startswith("User"):
            error_class = UserError
        elif entity_type.startswith("House") or entity_type.startswith("Floor") or entity_type.startswith("Room"):
            error_class = HouseError
        elif entity_type.startswith("Device"):
            error_class = DeviceError

        if not id_str:
            raise error_class(f"{entity_type} ID cannot be empty")
        if not isinstance(id_str, str):
            raise error_class(f"Invalid {entity_type} ID format")

    # User operations
    def create_user(self, name: str, email: str) -> User:
        """Create a new user"""
        self._validate_input(name, 2, "User name")
        self._validate_input(email, 5, "Email", is_email=True)
        
        if any(user.email == email for user in self.users.values()):
            raise UserError("Email already registered")
            
        user = User(name, email)
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User:
        """Get user by ID"""
        self._validate_id(user_id, "User")
        user = self.users.get(user_id)
        if not user:
            raise UserError("User not found")
        return user
    
    def update_user(self, user_id: str, name: str = None, email: str = None) -> User:
        """Update user information"""
        user = self.get_user(user_id)
        
        if name is not None:
            self._validate_input(name, 2, "User name")
            user.name = name
            
        if email is not None:
            self._validate_input(email, 5, "Email", is_email=True)
            if any(u.email == email and u.id != user_id for u in self.users.values()):
                raise UserError("Email already registered")
            user.email = email
            
        return user
    
    # House operations
    def create_house(self, name: str, address: str, latitude: float, longitude: float) -> House:
        """Create a new house with location

        Args:
            name: Name of the house
            address: House address
            latitude: Geographic latitude
            longitude: Geographic longitude

        Returns:
            House: Created house object

        Raises:
            HouseError: If validation fails
        """
        self._validate_input(name, 2, "House name")
        self._validate_input(address, 5, "House address")
        
        location = Location(latitude, longitude)
        house = House(name, address, location)
        self.houses[house.id] = house
        return house
    
    def get_house(self, house_id: str) -> House:
        """Get house by ID

        Args:
            house_id: House identifier

        Returns:
            House: Found house object

        Raises:
            HouseError: If house not found
        """
        if not house_id:
            raise HouseError("House ID cannot be empty")
        if house_id not in self.houses:
            raise HouseError("House not found")
        return self.houses[house_id]
    
    def update_house_name(self, house_id: str, new_name: str) -> None:
        """Update house name

        Args:
            house_id: House identifier
            new_name: New name for the house

        Raises:
            HouseError: If validation fails or house not found
        """
        self._validate_input(new_name, 2, "House name")
        house = self.get_house(house_id)
        house.name = new_name

    def delete_house(self, house_id: str) -> None:
        """Delete a house

        Args:
            house_id: House identifier

        Raises:
            HouseError: If house not found
        """
        if house_id not in self.houses:
            raise HouseError(f"House {house_id} not found")
        del self.houses[house_id]

    def add_floor(self, house_id: str, floor_name: str, floor_number: int = 1) -> Floor:
        """Add a floor to a house"""
        self._validate_input(floor_name, 2, "Floor name")
        
        house = self.get_house(house_id)
        floor = Floor(floor_name, floor_number)
        house.floors.append(floor)
        return floor

    def add_room(self, house_id: str, floor_id: str, room_name: str, 
                room_type: RoomType = RoomType.OTHER, size: float = 0.0) -> Room:
        """Add a room to a floor

        Args:
            house_id: House identifier
            floor_id: Floor identifier
            room_name: Name of the room
            room_type: Type of room (bedroom, bathroom, etc.)
            size: Room size in square meters

        Returns:
            Room: Created room object

        Raises:
            HouseError: If validation fails
        """
        self._validate_input(room_name, 2, "Room name")
        self._validate_id(house_id, "House")
        self._validate_id(floor_id, "Floor")
        
        if size < 0:
            raise HouseError("Room size cannot be negative")
        
        house = self.get_house(house_id)
        floor = next((f for f in house.floors if f.id == floor_id), None)
        if not floor:
            raise HouseError("Floor not found")
        
        room = Room(room_name, room_type, floor.floor_number, size)
        floor.rooms.append(room)
        return room

    def add_device(self, house_id: str, floor_id: str, room_id: str, 
                  device_type: str, device_name: str) -> Device:
        """Add a device to a room

        Args:
            house_id: House identifier
            floor_id: Floor identifier
            room_id: Room identifier
            device_type: Type of device (temperature/humidity)
            device_name: Name of the device

        Raises:
            DeviceError: If device validation fails
            HouseError: If house/floor/room not found
        """
        self._validate_input(device_name, 2, "Device name")
        
        try:
            device_type_enum = DeviceType(device_type)
        except ValueError:
            raise DeviceError(f"Invalid device type: {device_type}")

        self._validate_id(house_id, "House")
        self._validate_id(floor_id, "Floor")
        self._validate_id(room_id, "Room")
        
        house = self.get_house(house_id)
        floor = next((f for f in house.floors if f.id == floor_id), None)
        if not floor:
            raise HouseError("Floor not found")
        
        room = next((r for r in floor.rooms if r.id == room_id), None)
        if not room:
            raise HouseError("Room not found")

        device = Device(device_type_enum, device_name)
        room.devices.append(device)
        return device

    def update_device_status(self, house_id: str, floor_id: str, 
                            room_id: str, device_id: str, status: Dict) -> Device:
        """Update device status

        Args:
            house_id: House identifier
            floor_id: Floor identifier
            room_id: Room identifier
            device_id: Device identifier
            status: New device status

        Returns:
            Updated device

        Raises:
            DeviceError: If device not found or status invalid
            HouseError: If house/floor/room not found
        """
        if not device_id:
            raise DeviceError("Device ID cannot be empty")
        
        self._validate_id(house_id, "House")
        self._validate_id(floor_id, "Floor")
        self._validate_id(room_id, "Room")

        # Find device
        house = self.get_house(house_id)
        floor = next((f for f in house.floors if f.id == floor_id), None)
        if not floor:
            raise HouseError("Floor not found")
        
        room = next((r for r in floor.rooms if r.id == room_id), None)
        if not room:
            raise HouseError("Room not found")
        
        device = next((d for d in room.devices if d.id == device_id), None)
        if not device:
            raise DeviceError("Device not found")

        device.status.update(status)
        return device 