# SocialNet XML Parser

A professional desktop application for parsing, validating, formatting, and visualizing social network data stored in XML format.

## Features

- **XML Parsing**: Load and parse social network XML files
- **Validation**: Validate XML structure and data integrity
- **Formatting**: Prettify and format XML files
- **Data Analysis**: Parse user data, calculate statistics
- **Error Checking**: Comprehensive data integrity validation
- **Graph Visualization**: Visualize social network as directed graphs
- **JSON Export**: Export parsed data to JSON format
- **Code Viewer**: View XML code in a syntax-highlighted read-only window

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python -m socialnet_parser.main
```

Or from the package root:
```bash
python -m socialnet_parser
```

## Project Structure

```
socialnet_parser/
├── socialnet_parser/          # Main package
│   ├── controllers/          # Business logic layer
│   │   ├── xml_controller.py
│   │   ├── data_controller.py
│   │   └── graph_controller.py
│   ├── ui/                   # User interface layer
│   │   ├── main_window.py
│   │   ├── code_viewer_window.py
│   │   └── graph_visualization_window.py
│   └── main.py               # Application entry point
├── tests/                     # Unit tests
├── resources/                 # Static resources
│   ├── samples/              # Sample XML files
│   └── images/               # Image assets
├── data/                      # Output data directory
├── docs/                      # Documentation
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- **Controllers**: Handle all business logic (XML operations, data processing, graph building)
- **UI**: Handle all presentation and user interaction
- **Main**: Simple entry point that initializes and runs the application

## License

MIT License

