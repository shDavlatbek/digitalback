(function () {
    'use strict';

    function toggleMediaFields(row) {
        var typeSelect = row.querySelector('select[name$="-type"]');
        if (!typeSelect) return;

        var fileInput = row.querySelector('[class*="field-file"], .field-file');
        var urlInput = row.querySelector('[class*="field-url"], .field-url');

        // For tabular inlines, fields are in <td> cells
        if (!fileInput && !urlInput) {
            var cells = row.querySelectorAll('td');
            cells.forEach(function (td) {
                var input = td.querySelector('input, select');
                if (!input) return;
                var name = input.getAttribute('name') || '';
                if (name.endsWith('-file') || name.endsWith('-file_0')) {
                    fileInput = td;
                } else if (name.endsWith('-url')) {
                    urlInput = td;
                }
            });
        }

        var val = typeSelect.value;

        if (fileInput) {
            fileInput.style.display = (val === 'video' || val === 'image' || val === 'file') ? '' : 'none';
        }
        if (urlInput) {
            urlInput.style.display = (val === 'video') ? '' : 'none';
        }

        // If type is video: show both file and url (can use either)
        // If type is image or file: show file, hide url
        if (val === 'image' || val === 'file') {
            if (urlInput) urlInput.style.display = 'none';
            if (fileInput) fileInput.style.display = '';
        } else if (val === 'video') {
            if (urlInput) urlInput.style.display = '';
            if (fileInput) fileInput.style.display = '';
        }
    }

    function initToggle() {
        // Find all inline rows
        var inlineGroups = document.querySelectorAll('.inline-related, .dynamic-eventmedia_set, .dynamic-newsmedia_set, tr.form-row, tr.has_original, tr.empty-form');
        inlineGroups.forEach(function (row) {
            toggleMediaFields(row);
        });

        // Also look in tabular inline tbody
        document.querySelectorAll('.tabular .module tbody tr').forEach(function (row) {
            toggleMediaFields(row);
        });

        // Listen for changes on type selects
        document.addEventListener('change', function (e) {
            if (e.target && e.target.name && e.target.name.endsWith('-type')) {
                var row = e.target.closest('tr') || e.target.closest('.inline-related');
                if (row) toggleMediaFields(row);
            }
        });
    }

    // Run on DOMContentLoaded and also when new inlines are added
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initToggle);
    } else {
        initToggle();
    }

    // For dynamically added inlines (adminsortable2 or Django's "Add another" button)
    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            mutation.addedNodes.forEach(function (node) {
                if (node.nodeType === 1) {
                    var rows = node.querySelectorAll ? node.querySelectorAll('tr, .inline-related') : [];
                    rows.forEach(function (row) {
                        toggleMediaFields(row);
                    });
                    // Also check if the node itself is a row
                    if (node.tagName === 'TR' || (node.classList && node.classList.contains('inline-related'))) {
                        toggleMediaFields(node);
                    }
                }
            });
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
