[![publish](https://github.com/Mark7888/pyspiget/actions/workflows/publish.yml/badge.svg?event=push)](https://github.com/Mark7888/pyspiget/actions/workflows/publish.yml)
[![Downloads](https://static.pepy.tech/badge/pyspiget)](https://pepy.tech/project/pyspiget)

# Python Spiget API Wrapper

A modern Python wrapper for the [Spiget API](https://spiget.org/), providing easy access to Spigot resources, authors, and categories.

## Installation

```bash
pip install pyspiget
```

## Quick Start

```python
from spiget import Spiget

# Initialize the client
api = Spiget(user_agent="MyApp/1.0.0")

# Get a resource
resource = api.get_resource(1234)
print(f"Resource name: {resource.name}")

# Search for resources
resources = api.search_resources("worldedit")
for resource in resources:
    print(f"Found: {resource.name}")
```

## API Reference

### Main Classes

#### `Spiget`

The main class for interacting with the Spiget API.

```python
api = Spiget(user_agent="MyApp/1.0.0")
```

#### `WebhookHandler`

Handles webhook-related operations for the Spiget API.

```python
webhook_handler = WebhookHandler(api.session)
```

### Data Models

All models inherit from `BaseModel` which provides basic dictionary to object conversion.

#### `Resource`
Represents a Spigot resource (plugin, mod, etc.)

Properties:
- `id`: Resource ID
- `name`: Resource name
- `tag`: Resource tag
- `contributors`: List of contributors
- `likes`: Number of likes
- `file`: ResourceFile object
- `tested_versions`: List of tested Minecraft versions
- `links`: Dictionary of related links
- `rating`: ResourceRating object
- `release_date`: Release datetime
- `update_date`: Last update datetime
- `downloads`: Number of downloads
- `external`: Whether the resource is external
- `icon`: Icon object
- `premium`: Whether the resource is premium
- `price`: Resource price (if premium)
- `currency`: Price currency
- `description`: Resource description
- `documentation`: Resource documentation
- `source_code_link`: Link to source code
- `donation_link`: Link to donation page

#### `ResourceFile`
Represents a resource's downloadable file.

Properties:
- `type`: File type
- `size`: File size
- `size_unit`: Size unit
- `url`: Download URL
- `external_url`: External download URL

#### `ResourceVersion`
Represents a specific version of a resource.

Properties:
- `id`: Version ID
- `uuid`: Version UUID
- `name`: Version name
- `release_date`: Release datetime
- `downloads`: Number of downloads
- `rating`: ResourceRating object

#### `ResourceUpdate`
Represents an update post for a resource.

Properties:
- `id`: Update ID
- `resource`: Resource ID
- `title`: Update title
- `description`: Update description
- `date`: Update datetime
- `likes`: Number of likes

#### `ResourceReview`
Represents a review for a resource.

Properties:
- `author`: Author object
- `rating`: ResourceRating object
- `message`: Review message
- `response_message`: Author's response
- `version`: Version reviewed
- `date`: Review datetime

#### `Author`
Represents a resource author.

Properties:
- `id`: Author ID
- `name`: Author name
- `icon`: Icon object

#### `Category`
Represents a resource category.

Properties:
- `id`: Category ID
- `name`: Category name

### Methods

#### Resource Methods

```python
# Get multiple resources
resources = api.get_resources(size=10, page=1, sort=None, fields=None)

# Get a single resource
resource = api.get_resource(resource_id=1234)

# Get resource versions
versions = api.get_resource_versions(resource_id=1234, size=10, page=1)

# Get specific version
version = api.get_resource_version(resource_id=1234, version_id="1.0.0")

# Get latest version
latest = api.get_resource_latest_version(resource_id=1234)

# Get resource updates
updates = api.get_resource_updates(resource_id=1234, size=10, page=1)

# Get resource reviews
reviews = api.get_resource_reviews(resource_id=1234, size=10, page=1)

# Get resource author
author = api.get_resource_author(resource_id=1234)
```

#### Author Methods

```python
# Get multiple authors
authors = api.get_authors(size=10, page=1)

# Get single author
author = api.get_author(author_id=1234)

# Get author's resources
resources = api.get_author_resources(author_id=1234, size=10, page=1)
```

#### Category Methods

```python
# Get all categories
categories = api.get_categories(size=10, page=1)

# Get single category
category = api.get_category(category_id=1234)

# Get category resources
resources = api.get_category_resources(category_id=1234, size=10, page=1)
```

#### Search Methods

```python
# Search resources
resources = api.search_resources(query="worldedit", field=None, size=10, page=1)

# Search authors
authors = api.search_authors(query="sk89q", field=None, size=10, page=1)
```

#### Webhook Methods

```python
# Get available webhook events
events = webhook_handler.get_webhook_events()

# Register a webhook
webhook = webhook_handler.register_webhook(
    url="https://example.com/webhook",
    events=["resource-update", "new-resource"]
)

# Get webhook status
status = webhook_handler.get_webhook_status(webhook_id="abc123")

# Delete webhook
webhook_handler.delete_webhook(webhook_id="abc123", secret="webhook_secret")
```

## Error Handling

The wrapper includes a custom `SpigetError` exception that is raised when API requests fail:

```python
from spiget import Spiget, SpigetError

api = Spiget()

try:
    resource = api.get_resource(99999999)
except SpigetError as e:
    print(f"API error: {e}")
```

## Credits

This wrapper is built for the [Spiget API](https://spiget.org/) created by the [SpiGetOrg team](https://github.com/SpiGetOrg).

## License

MIT License - see LICENSE file for details
