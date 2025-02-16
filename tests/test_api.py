"""
Unit tests for Smart Home System API.
Tests cover basic functionality, error handling, and input validation.
"""

import pytest
from api.api import (
    SmartHomeAPI, DeviceType, UserRole,
    SmartHomeError, UserError, HouseError, DeviceError,
    RoomType
)

def test_create_user():
    api = SmartHomeAPI()
    user = api.create_user("Test User", "test.user@example.com")
    assert user.name == "Test User"
    assert user.email == "test.user@example.com"

def test_create_user_invalid_email():
    api = SmartHomeAPI()
    with pytest.raises(UserError, match="Invalid email format"):
        api.create_user("Test User", "invalid-email")

def test_create_house():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    assert house.name == "My House"
    assert house.address == "123 Main St"
    assert house.id in api.houses

def test_create_house_invalid_name():
    api = SmartHomeAPI()
    with pytest.raises(HouseError, match="House name must be at least 2 characters"):
        api.create_house("", "Invalid", 0, 0)

def test_add_floor():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    assert floor in house.floors
    assert floor.name == "First Floor"

def test_add_room():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    room = api.add_room(house.id, floor.id, "Living Room")
    assert room in floor.rooms
    assert room.name == "Living Room"

def test_add_device():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    room = api.add_room(house.id, floor.id, "Living Room")
    device = api.add_device(house.id, floor.id, room.id, 
                          "temperature", "Temperature Sensor")
    assert device in room.devices
    assert device.name == "Temperature Sensor"
    assert device.type == DeviceType.TEMPERATURE

def test_add_device_invalid_type():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    room = api.add_room(house.id, floor.id, "Living Room")
    with pytest.raises(DeviceError, match="Invalid device type"):
        api.add_device(house.id, floor.id, room.id, "invalid_type", "Device")

def test_add_floor_invalid_name():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    with pytest.raises(HouseError, match="Floor name must be at least 2 characters"):
        api.add_floor(house.id, "")

def test_add_floor_invalid_house():
    api = SmartHomeAPI()
    with pytest.raises(HouseError, match="House not found"):
        api.add_floor("invalid_id", "First Floor")

def test_create_user_duplicate_email():
    api = SmartHomeAPI()
    api.create_user("Test User", "test.user@example.com")
    with pytest.raises(UserError, match="Email already registered"):
        api.create_user("Another User", "test.user@example.com")

def test_update_user_invalid_name():
    api = SmartHomeAPI()
    user = api.create_user("Test User", "test.user@example.com")
    with pytest.raises(UserError, match="User name must be at least 2 characters"):
        api.update_user(user.id, name="")

def test_update_user_invalid_email():
    api = SmartHomeAPI()
    user = api.create_user("Test User", "test.user@example.com")
    with pytest.raises(UserError, match="Invalid email format"):
        api.update_user(user.id, email="invalid-email")

def test_get_house_invalid_id():
    api = SmartHomeAPI()
    with pytest.raises(HouseError, match="House ID cannot be empty"):
        api.get_house("")

def test_add_floor_empty_name():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    with pytest.raises(HouseError, match="Floor name must be at least 2 characters"):
        api.add_floor(house.id, "")

def test_add_room_invalid_floor():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    with pytest.raises(HouseError, match="Floor not found"):
        api.add_room(house.id, "invalid_floor_id", "Living Room")

def test_add_device_name_too_short():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    room = api.add_room(house.id, floor.id, "Living Room")
    with pytest.raises(DeviceError, match="Device name must be at least 2 characters"):
        api.add_device(house.id, floor.id, room.id, "temperature", "")

def test_add_device_invalid_room():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    with pytest.raises(HouseError, match="Room not found"):
        api.add_device(house.id, floor.id, "invalid_room_id", "temperature", "Sensor")

def test_create_house_with_location():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    assert house.name == "My House"
    assert house.address == "123 Main St"
    assert house.location.latitude == 40.7128
    assert house.location.longitude == -74.0060

def test_add_room_with_type():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    room = api.add_room(house.id, floor.id, "Master Bedroom", 
                       room_type=RoomType.BEDROOM, size=20.5)
    assert room.name == "Master Bedroom"
    assert room.type == RoomType.BEDROOM
    assert room.size == 20.5

def test_update_device_invalid_id():
    api = SmartHomeAPI()
    house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)
    floor = api.add_floor(house.id, "First Floor")
    room = api.add_room(house.id, floor.id, "Living Room")
    with pytest.raises(DeviceError, match="Device ID cannot be empty"):
        api.update_device_status(house.id, floor.id, room.id, "", {}) 