"""Configuration settings for the application."""

# Excel processing configuration
CONFIG = {
    'REQUIRED_COLUMNS': ['Nombre'],
    'OUTPUT_COLUMNS': [
        'First Name', 'Last Name', 'Email', 'Student ID', 
        'Section', 'Team', 'Remarks'
    ],
    'DEFAULT_FILENAME': 'processed_students.xlsx'
}

# JavaScript for handling logout
LOGOUT_JS = """
<script>
    function closeTab() {
        // Try to close the tab
        window.close();
        
        // If the tab doesn't close, redirect to a blank page
        setTimeout(function() {
            window.location.href = 'about:blank';
        }, 100);
    }
</script>
"""