// Leaflet Location Widget - utility JS
// The main initialization logic is in the widget template itself
// This file can be used for shared utilities if needed

(function () {
    'use strict';

    // Ensure Leaflet is loaded
    if (typeof L === 'undefined') {
        console.warn('Leaflet library not loaded. Map widgets may not work.');
    }
})();
