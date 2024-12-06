# huddle01

`huddle01` is a Python client library designed to seamlessly integrate with the Huddle01 video conferencing platform. It provides developers with a straightforward interface to manage video calls, handle participants, and access various features of the Huddle01 API.

## Features

- **Easy Integration**: Simplifies the process of connecting Python applications with Huddle01.
- **Comprehensive API Coverage**: Access a wide range of functionalities offered by the Huddle01 platform.
- **Asynchronous Support**: Built with asynchronous programming in mind for efficient performance.
- **Extensible**: Designed to accommodate future enhancements and customizations.

## Installation

Ensure you have Python 3.12.7 or higher installed. You can install `huddle01` using pip:

```bash
pip install huddle01
```

To upgrade to the latest version:

```bash
pip install --upgrade huddle01
```


## Getting Started

Here's a basic example to initiate a video call:

```python
import asyncio
from huddle01 import HuddleClient

async def main():
    client = HuddleClient(api_key='YOUR_API_KEY')
    meeting = await client.create_meeting(topic='Async Team Sync')
    print(f"Join the meeting: {meeting.url}")

asyncio.run(main())
```

Replace `'YOUR_API_KEY'` with your actual Huddle01 API key.

## Documentation

Comprehensive documentation is available at [https://huddle01.readthedocs.io/](https://huddle01.readthedocs.io/), covering:

- **Authentication**: Setting up and managing API keys.
- **Meeting Management**: Creating, updating, and deleting meetings.
- **Participant Handling**: Adding, removing, and managing participants.
- **Advanced Features**: Utilizing recording, screen sharing, and more.


## Contact

For support or inquiries:

- **Email**: support@huddle01.com


Elevate your video conferencing capabilities with huddle01! 🚀