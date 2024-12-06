# Media Fetcher

A Python package for fetching media details from various platforms, including **Instagram**, **TikTok**, and more. It is designed to be lightweight, modular, and easy to integrate into other projects like Discord bots or web applications.

## Features

- Fetch metadata and media URLs for Instagram posts.
- Fetch metadata and video URLs for TikTok posts.
- Designed to support additional platforms in the future.
- Lightweight and reusable.

## Installation

Clone the repository and install the package manually using your preferred method, such as Poetry or pip.

## Usage

### Import Fetchers
Use the fetchers provided for supported platforms:

from media_fetcher.instagram import InstagramFetcher  
from media_fetcher.tiktok import TikTokFetcher  

### Example: Fetch Instagram Post
url = "https://www.instagram.com/p/example/"  
result = InstagramFetcher.fetch_post(url)  
print(result)  

### Example: Fetch TikTok Video
url = "https://www.tiktok.com/@example/video/123456789"  
result = TikTokFetcher.fetch_video(url)  
print(result)  

### Output Example
All fetchers return a dictionary with the status and URL. For example:

{  
    "url": "https://www.instagram.com/p/example/",  
    "status": "Success"  
}  

## Adding More Platforms

The package is designed to be extensible. To add support for more platforms, create a new fetcher module in the `media_fetcher` directory, following the existing structure.

## License

This project is licensed under the **Apache-2.0 License**.
