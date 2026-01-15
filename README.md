# Computer Vision Playground

An interactive tool for exploring computer vision concepts like convolution, filters, and kernels.

## Installation

```bash
uv sync
```

## Run App

```bash
make dev
make run
```

## `/src` Code Structure

The codebase is organized into two main directories to separate business logic from presentation:

### `src/core/` - Business Logic

Contains the core convolution and image processing logic with no UI dependencies.

- **`image_data.py`** - Image representation as a 2D grid of pixel values (0-255)
- **`filter_config.py`** - Kernel configuration (size, type, values) and position tracking
- **`filter_calculator.py`** - Filter operations (currently mean/average filter)

These modules handle all the math and data transformations. They can be tested and used independently of the UI.

### `src/ui/` - User Interface

Contains all Qt/PySide6 widgets and visual components.

- **`main_window.py`** - Main application window coordinating all 6 sections
- **`pixel_grid_widget.py`** - Displays image as an interactive grid of pixels
- **`kernel_grid_widget.py`** - Interactive grid for editing kernel values
- **`control_panel.py`** - Control panel for settings and navigation
- **`work_section_widget.py`** - Displays step-by-step filter calculations

The UI layer uses the core classes to perform calculations and visualize results. Changes to the UI don't affect the underlying algorithms.

### Entry Points

- **`main.py`** - Application entry point
- **`dev_runner.py`** - Development mode with auto-restart on file changes