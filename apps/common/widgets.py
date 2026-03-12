from django import forms


class LeafletLocationWidget(forms.TextInput):
    """
    Custom widget that displays a Leaflet map for picking lat,lng coordinates.
    Stores the value as "lat,lng" in a CharField.
    """
    template_name = 'widgets/leaflet_location.html'

    class Media:
        css = {
            'all': (
                'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
                'css/leaflet_location_widget.css',
            )
        }
        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'js/leaflet_location_widget.js',
        )

    def __init__(self, attrs=None, map_height='400px', default_center=None, default_zoom=12):
        self.map_height = map_height
        self.default_center = default_center or [41.2995, 69.2401]  # Tashkent
        self.default_zoom = default_zoom
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'map_height': self.map_height,
            'default_center': self.default_center,
            'default_zoom': self.default_zoom,
        })
        return context
