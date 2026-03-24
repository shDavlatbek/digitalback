import base64
import hashlib
import hmac
from typing import Optional, Dict, Any
from urllib.parse import quote
from django.conf import settings


class SimpleImgproxyUrlBuilder:
    """
    Imgproxy URL builder with optional signing support.

    When IMGPROXY_KEY and IMGPROXY_SALT are set in Django settings (hex-encoded),
    generates signed URLs: /{signature}/processing_options/plain/source_url

    Otherwise falls back to insecure mode: /insecure/processing_options/plain/source_url

    Reference: https://docs.imgproxy.net/usage/signing_url
    """

    def __init__(self, base_url: str = None, key: str = None, salt: str = None):
        self.base_url = (base_url or getattr(settings, 'IMGPROXY_BASE_URL', 'http://localhost:8080')).rstrip('/')

        key_hex = key or getattr(settings, 'IMGPROXY_KEY', None)
        salt_hex = salt or getattr(settings, 'IMGPROXY_SALT', None)

        if key_hex and salt_hex:
            self.key = bytes.fromhex(key_hex)
            self.salt = bytes.fromhex(salt_hex)
        else:
            self.key = None
            self.salt = None

    def _sign(self, path: str) -> str:
        """Sign path using HMAC SHA256 with key and salt, return URL-safe base64."""
        digest = hmac.new(self.key, msg=self.salt + path.encode(), digestmod=hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
        
    def build_url(
        self,
        source_url: str,
        resize: str = None,
        width: int = None,
        height: int = None,
        resize_type: str = 'fit',
        enlarge: bool = False,
        quality: int = None,
        format: str = 'webp',
        **kwargs
    ) -> str:
        """
        Build imgproxy URL in insecure mode.
        
        Args:
            source_url: Source image URL
            resize: Custom resize string (e.g., "rs:fit:128:128:0")
            width: Image width
            height: Image height
            resize_type: fit, fill, crop, force
            enlarge: Allow enlargement (0 or 1)
            quality: Image quality (1-100)
            format: Output format (webp, jpg, png, avif)
            **kwargs: Additional processing options
            
        Returns:
            Complete imgproxy URL
        """
        options = []
        
        # Resize option
        if resize:
            options.append(resize)
        elif width or height:
            w = width or 0
            h = height or 0
            enlarge_flag = 1 if enlarge else 0
            options.append(f"rs:{resize_type}:{w}:{h}:{enlarge_flag}")
        
        # Quality
        if quality:
            options.append(f"q:{quality}")
            
        # Additional options
        for key, value in kwargs.items():
            if value is not None:
                options.append(f"{key}:{value}")

        # Build path (everything after base_url)
        processing_options = "/".join(options) if options else ""
        path_parts = []

        if processing_options:
            path_parts.append(processing_options)

        encoded_source = base64.urlsafe_b64encode(source_url.encode()).rstrip(b'=').decode()

        # Append format as extension on encoded source URL instead of as a processing option
        if format:
            encoded_source += f".{format}"
        path_parts.append(encoded_source)
        path = "/" + "/".join(path_parts)

        if self.key and self.salt:
            signature = self._sign(path)
        else:
            signature = "insecure"

        return f"{self.base_url}/{signature}{path}"


# Global instance
imgproxy = SimpleImgproxyUrlBuilder()


# Convenience functions for common use cases
def build_imgproxy_url(source_url: str, **kwargs) -> str:
    """Build imgproxy URL with options."""
    return imgproxy.build_url(source_url, **kwargs)


def get_thumbnail_url(source_url: str, size: int = 200, quality: int = 85) -> str:
    """Get square thumbnail URL."""
    return imgproxy.build_url(
        source_url,
        width=size,
        height=size,
        resize_type='fill',
        quality=quality
    )


def get_responsive_url(source_url: str, width: int, quality: int = 85) -> str:
    """Get responsive image URL for specific width."""
    return imgproxy.build_url(
        source_url,
        width=width,
        resize_type='fit',
        quality=quality
    )


# Preset configurations for common sizes
PRESET_SIZES = {
    'thumb_small': {'width': 150, 'height': 150, 'resize_type': 'fill'},
    'thumb_medium': {'width': 300, 'height': 300, 'resize_type': 'fill'},
    'thumb_large': {'width': 500, 'height': 500, 'resize_type': 'fill'},
    'list_small': {'width': 200, 'height': 150, 'resize_type': 'fill'},
    'list_medium': {'width': 400, 'height': 300, 'resize_type': 'fill'},
    'banner_mobile': {'width': 768, 'height': 400, 'resize_type': 'fill'},
    'banner_desktop': {'width': 1920, 'height': 600, 'resize_type': 'fill'},
    'avatar_small': {'width': 100, 'height': 100, 'resize_type': 'fill'},
    'avatar_medium': {'width': 200, 'height': 200, 'resize_type': 'fill'},
}


def get_preset_url(source_url: str, preset: str, quality: int = 85) -> str:
    """Get URL using predefined preset."""
    if preset not in PRESET_SIZES:
        raise ValueError(f"Unknown preset: {preset}")
    
    options = PRESET_SIZES[preset].copy()
    options['quality'] = quality
    
    return imgproxy.build_url(source_url, **options)


# ──────────────────────────────────────────────
# DRF Serializer Field
# ──────────────────────────────────────────────

from rest_framework import serializers as drf_serializers


class ImgproxyImageField(drf_serializers.ImageField):
    """Serializer field that wraps image URLs through imgproxy."""

    def __init__(self, *args, imgproxy_options=None, **kwargs):
        self.imgproxy_options = imgproxy_options or {}
        self.imgproxy_options.setdefault('format', 'webp')
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if not value:
            return None

        request = self.context.get('request')
        if request:
            original_url = request.build_absolute_uri(value.url)
        else:
            original_url = value.url

        return {
            'original': original_url,
            'optimized': build_imgproxy_url(f"local:///{value.name}", **self.imgproxy_options),
        }