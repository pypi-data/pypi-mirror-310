"""
Metadata describing the various libraries.
"""

LIBS = {
    'duino_bus': {
        'description':
        'Bus/Packet interface for communicating with Arduino devices',
    },
    'duino_cli': {
        'description': 'Command Line Interface for Arduino Projects',
        'is_lib': False,
    },
    'duino_led': {
        'description': 'Some LED Abstractions'
    },
    'duino_littlefs': {
        'description': 'A CLI Plugin for LittleFS filesystems',
    },
    'duino_log': {
        'description': 'A logging abstraction',
    },
    'duino_makefile': {
        'description': 'Common Makefile rules',
    },
    'duino_util': {
        'description': 'Common Utility functions',
    },
    'duino_vscode_settings': {
        'description': 'Generate VSCode c_cpp_properties.json file',
        'has_badge': False,
        'is_lib': False,
    }
}
