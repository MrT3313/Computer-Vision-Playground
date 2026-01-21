from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io


class FormulaDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Store the current filter selection (e.g., "Mean", "Custom", etc.)
        self._filter_selection = "Mean"
        # Store the current filter type (e.g., "Cross-Correlation", "Convolution")
        self._filter_type = "Cross-Correlation"
        self._setup_ui()
    
    def _setup_ui(self):
        # Create vertical layout for the formula display
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Add 10px padding on all sides
        
        # Create label to display the rendered formula image
        self._formula_label = QLabel()
        self._formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the formula image
        layout.addWidget(self._formula_label)
        
        # Render the initial formula
        self._render_formula()
    
    def set_filter(self, filter_name: str) -> None:
        # Update the filter selection and re-render the corresponding formula
        self._filter_selection = filter_name
        self._render_formula()
    
    def set_filter_type(self, filter_type: str) -> None:
        # Update the filter type and re-render the corresponding formula
        self._filter_type = filter_type
        self._render_formula()

    
    def _render_formula(self) -> None:
        # Generate the appropriate LaTeX formula based on filter selection
        if self._filter_selection == "Mean":
            formula = self._create_mean_formula()
        elif self._filter_selection == "Gaussian":
            # Gaussian filter always uses cross-correlation (implementation doesn't support filter_type)
            formula = self._create_gaussian_formula()
        elif self._filter_selection == "Custom":
            formula = self._create_custom_formula()
        else:
            # Fallback message for unsupported filter types
            formula = "No formula available"
        
        # Convert LaTeX formula to a QPixmap image and display it
        pixmap = self._latex_to_pixmap(formula)
        self._formula_label.setPixmap(pixmap)
    
    def _create_mean_formula(self) -> str:
        # Return the LaTeX string for the mean filter formula
        # G(i,j) = output pixel at position (i,j)
        # (2k+1)^2 = kernel area (total number of elements)
        # F(u+i, v+j) = input pixel values within kernel window
        return r'$G(i,j) = \frac{1}{(2k + 1)^2} \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} F(u+i, v+j)$'
    
    def _create_gaussian_formula(self) -> str:
        # Return the LaTeX string for the Gaussian filter formula
        # Gaussian filter always uses cross-correlation (symmetric kernels make convolution equivalent)
        return r'$G[i, j] = \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} H[u, v] \cdot F[i + u, j + v]$'
    
    def _create_custom_formula(self) -> str:
        # Return the LaTeX string for the custom filter formula
        # Different formula based on Cross-Correlation vs Convolution
        if self._filter_type == "Convolution":
            # Convolution: G[i,j] = sum H[u,v] F[i-u, j-v]
            return r'$G[i, j] = \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} H[u, v] \cdot F[i - u, j - v]$'
        else:
            # Cross-Correlation: G[i,j] = sum H[u,v] F[i+u, j+v]
            return r'$G[i, j] = \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} H[u, v] \cdot F[i + u, j + v]$'
    
    def _latex_to_pixmap(self, latex_str: str) -> QPixmap:
        # Convert a LaTeX formula string to a QPixmap image using matplotlib
        
        # Create a matplotlib figure with white background
        fig = Figure(figsize=(8, 1), facecolor='white')
        # Create a canvas for rendering the figure
        canvas = FigureCanvasAgg(fig)
        # Add a subplot and disable axes (we only want the formula, not a plot)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Render the LaTeX text centered in the figure
        ax.text(0.5, 0.5, latex_str, 
                horizontalalignment='center',  # Center horizontally
                verticalalignment='center',  # Center vertically
                fontsize=12,  # Set font size
                transform=ax.transAxes)  # Use axes coordinates (0-1 range)
        
        # Draw the canvas to render the formula
        canvas.draw()
        
        # Save the rendered figure to a BytesIO buffer as PNG
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)  # Reset buffer position to beginning
        
        # Close the matplotlib figure to free memory
        plt.close(fig)
        
        # Load the PNG data into a QImage
        img = QImage()
        img.loadFromData(buf.read())
        
        # Convert QImage to QPixmap and return
        return QPixmap.fromImage(img)
    
    def sizeHint(self) -> QSize:
        # Return the preferred size for this widget
        return QSize(600, 80)
