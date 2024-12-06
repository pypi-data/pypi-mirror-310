import requests
from typing import List, Union
from datetime import datetime
from base64 import b64decode

# Custom exception for Spiget API errors
class SpigetError(Exception):
    """Custom exception for Spiget API errors"""
    pass

# Types for Spiget API models
class BaseModel:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
            
    @staticmethod
    def decode_base64(text: str) -> str:
        """Decode base64 encoded text if present"""
        if text and isinstance(text, str):
            try:
                return b64decode(text).decode('utf-8')
            except:
                return text
        return text

class ResourceFile:
    def __init__(self, data: dict):
        self.type: str = data.get('type')
        self.size: float = data.get('size')
        self.size_unit: str = data.get('sizeUnit')
        self.url: str = data.get('url')
        self.external_url: str = data.get('externalUrl')

class Icon:
    def __init__(self, data: dict):
        self.url: str = data.get('url')
        self.data: str = data.get('data')

class ResourceRating:
    def __init__(self, data: dict):
        self.count: int = data.get('count')
        self.average: float = data.get('average')

class Author(BaseModel):
    def __init__(self, data: dict):
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.icon: Icon = Icon(data.get('icon', {})) if data.get('icon') else None

class Category(BaseModel):
    def __init__(self, data: dict):
        self.id: int = data.get('id')
        self.name: str = data.get('name')

class ResourceVersion(BaseModel):
    def __init__(self, data: dict):
        self.id: int = data.get('id')
        self.uuid: str = data.get('uuid')
        self.name: str = data.get('name')
        self.release_date: datetime = datetime.fromtimestamp(data.get('releaseDate', 0))
        self.downloads: int = data.get('downloads')
        self.rating: ResourceRating = ResourceRating(data.get('rating', {})) if data.get('rating') else None

class ResourceUpdate(BaseModel):
    def __init__(self, data: dict):
        self.id: int = data.get('id')
        self.resource: int = data.get('resource')
        self.title: str = data.get('title')
        self.description: str = self.decode_base64(data.get('description'))
        self.date: datetime = datetime.fromtimestamp(data.get('date', 0))
        self.likes: int = data.get('likes')

class ResourceReview(BaseModel):
    def __init__(self, data: dict):
        self.author: Author = Author(data.get('author', {})) if data.get('author') else None
        self.rating: ResourceRating = ResourceRating(data.get('rating', {})) if data.get('rating') else None
        self.message: str = self.decode_base64(data.get('message'))
        self.response_message: str = self.decode_base64(data.get('responseMessage'))
        self.version: str = data.get('version')
        self.date: datetime = datetime.fromtimestamp(data.get('date', 0))

class Resource(BaseModel):
    def __init__(self, data: dict):
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.tag: str = data.get('tag')
        self.contributors: str = data.get('contributors')
        self.likes: int = data.get('likes')
        self.file: ResourceFile = ResourceFile(data.get('file', {})) if data.get('file') else None
        self.tested_versions: List[str] = data.get('testedVersions', [])
        self.links: dict = data.get('links', {})
        self.rating: ResourceRating = ResourceRating(data.get('rating', {})) if data.get('rating') else None
        self.release_date: datetime = datetime.fromtimestamp(data.get('releaseDate', 0))
        self.update_date: datetime = datetime.fromtimestamp(data.get('updateDate', 0))
        self.downloads: int = data.get('downloads')
        self.external: bool = data.get('external', False)
        self.icon: Icon = Icon(data.get('icon', {})) if data.get('icon') else None
        self.premium: bool = data.get('premium', False)
        self.price: float = data.get('price')
        self.currency: str = data.get('currency')
        self.description: str = self.decode_base64(data.get('description'))
        self.documentation: str = self.decode_base64(data.get('documentation'))
        self.source_code_link: str = data.get('sourceCodeLink')
        self.donation_link: str = data.get('donationLink')

# Main class for interacting with the Spiget API
class Spiget:
    BASE_URL = "https://api.spiget.org/v2"
    
    def __init__(self, user_agent: str = "Python-Spiget-Wrapper"):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent
        })

    def _make_request(self, endpoint: str, method: str = "GET", params: dict = None, data: dict = None) -> Union[dict, list]:
        """Make a request to the Spiget API"""
        response = self.session.request(
            method=method,
            url=f"{self.BASE_URL}{endpoint}",
            params=params,
            json=data
        )
        
        if response.status_code == 404:
            raise SpigetError("Resource not found")
        elif response.status_code != 200:
            raise SpigetError(f"API request failed with status code {response.status_code}")
            
        return response.json()

    # Status endpoints
    def get_status(self) -> dict:
        """Get the API status"""
        return self._make_request("/status")

    # Resource endpoints
    def get_resources(self, size: int = 10, page: int = 1, sort: str = None, fields: List[str] = None) -> List[Resource]:
        """Get a list of available resources"""
        params = {
            "size": size,
            "page": page,
            "sort": sort,
            "fields": ",".join(fields) if fields else None
        }
        data = self._make_request("/resources", params=params)
        return [Resource(item) for item in data]

    def get_resource(self, resource_id: int) -> Resource:
        """Get a resource by its ID"""
        data = self._make_request(f"/resources/{resource_id}")
        return Resource(data)

    def get_resource_versions(self, resource_id: int, size: int = 10, page: int = 1) -> List[ResourceVersion]:
        """Get versions of a resource"""
        params = {"size": size, "page": page}
        data = self._make_request(f"/resources/{resource_id}/versions", params=params)
        return [ResourceVersion(item) for item in data]

    def get_resource_version(self, resource_id: int, version_id: Union[int, str]) -> ResourceVersion:
        """Get a specific resource version"""
        data = self._make_request(f"/resources/{resource_id}/versions/{version_id}")
        return ResourceVersion(data)

    def get_resource_latest_version(self, resource_id: int) -> ResourceVersion:
        """Get the latest resource version"""
        data = self._make_request(f"/resources/{resource_id}/versions/latest")
        return ResourceVersion(data)

    def get_resource_updates(self, resource_id: int, size: int = 10, page: int = 1) -> List[ResourceUpdate]:
        """Get updates of a resource"""
        params = {"size": size, "page": page}
        data = self._make_request(f"/resources/{resource_id}/updates", params=params)
        return [ResourceUpdate(item) for item in data]

    def get_resource_reviews(self, resource_id: int, size: int = 10, page: int = 1) -> List[ResourceReview]:
        """Get reviews of a resource"""
        params = {"size": size, "page": page}
        data = self._make_request(f"/resources/{resource_id}/reviews", params=params)
        return [ResourceReview(item) for item in data]

    def get_resource_author(self, resource_id: int) -> Author:
        """Get the resource author"""
        data = self._make_request(f"/resources/{resource_id}/author")
        return Author(data)

    # Author endpoints
    def get_authors(self, size: int = 10, page: int = 1) -> List[Author]:
        """Get a list of available authors"""
        params = {"size": size, "page": page}
        data = self._make_request("/authors", params=params)
        return [Author(item) for item in data]

    def get_author(self, author_id: int) -> Author:
        """Get details about an author"""
        data = self._make_request(f"/authors/{author_id}")
        return Author(data)

    def get_author_resources(self, author_id: int, size: int = 10, page: int = 1) -> List[Resource]:
        """Get an author's resources"""
        params = {"size": size, "page": page}
        data = self._make_request(f"/authors/{author_id}/resources", params=params)
        return [Resource(item) for item in data]

    # Category endpoints
    def get_categories(self, size: int = 10, page: int = 1) -> List[Category]:
        """Get a list of categories"""
        params = {"size": size, "page": page}
        data = self._make_request("/categories", params=params)
        return [Category(item) for item in data]

    def get_category(self, category_id: int) -> Category:
        """Get details about a category"""
        data = self._make_request(f"/categories/{category_id}")
        return Category(data)

    def get_category_resources(self, category_id: int, size: int = 10, page: int = 1) -> List[Resource]:
        """Get the resources in a category"""
        params = {"size": size, "page": page}
        data = self._make_request(f"/categories/{category_id}/resources", params=params)
        return [Resource(item) for item in data]

    # Search endpoints
    def search_resources(self, query: str, field: str = None, size: int = 10, page: int = 1) -> List[Resource]:
        """Search resources"""
        params = {"size": size, "page": page, "field": field}
        data = self._make_request(f"/search/resources/{query}", params=params)
        return [Resource(item) for item in data]

    def search_authors(self, query: str, field: str = None, size: int = 10, page: int = 1) -> List[Author]:
        """Search authors"""
        params = {"size": size, "page": page, "field": field}
        data = self._make_request(f"/search/authors/{query}", params=params)
        return [Author(item) for item in data]

# Class for handling Spiget webhooks
class WebhookHandler:
    def __init__(self, session: requests.Session):
        self.session = session

    def _make_request(self, endpoint: str, method: str = "GET", params: dict = None, data: dict = None) -> Union[dict, list]:
        """Make a request to the Spiget API"""
        response = self.session.request(
            method=method,
            url=f"{Spiget.BASE_URL}{endpoint}",
            params=params,
            json=data
        )
        
        if response.status_code == 404:
            raise SpigetError("Resource not found")
        elif response.status_code != 200:
            raise SpigetError(f"API request failed with status code {response.status_code}")
            
        return response.json()

    def get_webhook_events(self) -> dict:
        """Get a list of available webhook events"""
        return self._make_request("/webhook/events")

    def register_webhook(self, url: str, events: List[str]) -> dict:
        """Register a new webhook"""
        data = {
            "url": url,
            "events": events
        }
        return self._make_request("/webhook/register", method="POST", data=data)

    def get_webhook_status(self, webhook_id: str) -> dict:
        """Get the status of a webhook"""
        return self._make_request(f"/webhook/status/{webhook_id}")

    def delete_webhook(self, webhook_id: str, secret: str) -> dict:
        """Delete a webhook"""
        return self._make_request(f"/webhook/delete/{webhook_id}/{secret}", method="DELETE")
