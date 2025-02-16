# Smart Home System API

EC530 Assignment implementation focusing on API design and error handling.

## Features

- User Management: Create, get, and update users
- House Management: Create, get, update, and delete houses
- Room Management: Add and manage rooms with types
- Device Management: Add devices and monitor status

## Project Structure
- `api/api.py`: Core API implementation
- `tests/test_api.py`: Unit tests
- `.github/workflows/test.yml`: CI configuration

## Setup & Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## API Example
```python
from api.api import SmartHomeAPI, DeviceType, RoomType

# Initialize API
api = SmartHomeAPI()

# Create a house
house = api.create_house("My House", "123 Main St", 40.7128, -74.0060)

# Add a floor
floor = api.add_floor(house.id, "First Floor")

# Add a room
room = api.add_room(house.id, floor.id, "Living Room", 
                   room_type=RoomType.LIVING_ROOM)

# Add a device
device = api.add_device(house.id, floor.id, room.id, 
                       "temperature", "Temperature Sensor")
```

## API Documentation

### User Management
- `create_user(name: str, email: str) -> User`
  - Creates a new user
  - Validates email format and uniqueness
  - Returns User object

- `get_user(user_id: str) -> User`
  - Retrieves user by ID
  - Throws UserError if not found

- `update_user(user_id: str, name: str = None, email: str = None) -> User`
  - Updates user information
  - Validates new data
  - Returns updated User object

### House Management
[类似的文档格式继续...]

### Data Structures
```python
@dataclass
class User:
    id: str
    name: str
    email: str
    role: UserRole

@dataclass
class House:
    id: str
    name: str
    address: str
    location: Location
    owner_id: str
    floors: List[Floor]
```
