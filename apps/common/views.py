from django.contrib import admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from urllib.parse import urljoin
from drf_yasg.utils import swagger_auto_schema
from .models import TinyMCEImage
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


@csrf_exempt
@login_required
@swagger_auto_schema(schema=None, auto_schema=None)
def upload_image(request):
    """Handle image uploads from TinyMCE editor."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    if not uploaded_file.content_type.startswith('image/'):
        return JsonResponse({'error': 'File is not an image'}, status=400)
    
    image = TinyMCEImage(title=uploaded_file.name)
    image.image = uploaded_file
    image.save()
    
    # Get the absolute URL by combining the site URL with the media URL
    site_url = request.build_absolute_uri('/').rstrip('/')
    relative_url = image.image.url
    
    # Ensure we have an absolute URL
    if relative_url.startswith('/'):
        # Already a root-relative URL, just add the site domain
        absolute_url = f"{site_url}{relative_url}"
    else:
        # Combine with the site URL
        absolute_url = urljoin(site_url, relative_url)
    
    # Return the absolute URL to the image
    return JsonResponse({
        'location': absolute_url,  # Absolute URL for TinyMCE
        'success': True
    })


@method_decorator(csrf_exempt, name='dispatch')
class APIDocumentationView(TemplateView):
    template_name = 'api_documentation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current host for API testing
        context['api_base_url'] = f"{self.request.scheme}://{self.request.get_host()}/api"
        
        # API sections with endpoints
        context['api_sections'] = [
            {
                'id': 'sozlamalar',
                'title': 'Sozlamalar',
                'description': 'Sayt asosiy sozlamalari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/settings/',
                        'description': 'Asosiy sozlamalar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/footer/',
                        'description': 'Footer ma\'lumotlari',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/contact/',
                        'description': 'Aloqa ma\'lumotlari',
                        'params': []
                    }
                ]
            },
            {
                'id': 'tadbirlar',
                'title': 'Tadbirlar',
                'description': 'Forum tadbirlari',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/events/',
                        'description': 'Barcha tadbirlar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/events/{slug}/',
                        'description': 'Tadbir tafsilotlari (kun tartibi, spikerlar, media)',
                        'params': [{'name': 'slug', 'type': 'string', 'required': True}]
                    }
                ]
            },
            {
                'id': 'kontent',
                'title': 'Kontent',
                'description': 'Yangiliklar, FAQ, izohlar va boshqa',
                'endpoints': [
                    {
                        'method': 'GET',
                        'path': '/news/',
                        'description': 'Yangiliklar ro\'yxati',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/supporters/',
                        'description': 'Qo\'llab-quvvatlovchilar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/sponsors/',
                        'description': 'Homiylar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/faqs/',
                        'description': 'Ko\'p so\'raladigan savollar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/comments/',
                        'description': 'Izohlar',
                        'params': []
                    },
                    {
                        'method': 'GET',
                        'path': '/past-forums/',
                        'description': 'O\'tgan forumlar',
                        'params': []
                    }
                ]
            },
            {
                'id': 'formalar',
                'title': 'Formalar',
                'description': 'Ariza va so\'rov yuborish',
                'endpoints': [
                    {
                        'method': 'POST',
                        'path': '/forms/presentation/',
                        'description': 'Taqdimot bilan chiqish arizasi',
                        'params': [
                            {'name': 'full_name', 'type': 'string', 'required': True},
                            {'name': 'position', 'type': 'string', 'required': True},
                            {'name': 'organization_name', 'type': 'string', 'required': True},
                            {'name': 'phone', 'type': 'string', 'required': True},
                            {'name': 'email', 'type': 'string', 'required': True},
                            {'name': 'organization_website', 'type': 'string', 'required': False},
                            {'name': 'presentation_topic', 'type': 'string', 'required': True},
                            {'name': 'pdf_file', 'type': 'file', 'required': False},
                        ]
                    },
                    {
                        'method': 'POST',
                        'path': '/forms/partner/',
                        'description': 'Forum hamkoriga aylaning arizasi',
                        'params': [
                            {'name': 'organization_name', 'type': 'string', 'required': True},
                            {'name': 'contact_person', 'type': 'string', 'required': True},
                            {'name': 'phone', 'type': 'string', 'required': True},
                            {'name': 'email', 'type': 'string', 'required': True},
                        ]
                    },
                    {
                        'method': 'POST',
                        'path': '/forms/certificate-check/',
                        'description': 'Sertifikatni tekshirish',
                        'params': [
                            {'name': 'full_name', 'type': 'string', 'required': True},
                            {'name': 'certificate_number', 'type': 'string', 'required': True},
                        ]
                    }
                ]
            }
        ]
        
        return context