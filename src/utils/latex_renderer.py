from PySide6.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io


def render_latex_to_pixmap(latex_str: str, figsize: tuple[float, float] = (8, 1), dpi: int = 100) -> QPixmap:
    """
    Convert a LaTeX formula string to a QPixmap image using matplotlib.
    
    Args:
        latex_str: LaTeX formula string to render
        figsize: Figure size as (width, height) in inches
        dpi: Resolution in dots per inch
        
    Returns:
        QPixmap containing the rendered formula
    """
    fig = Figure(figsize=figsize, facecolor='white')
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    ax.text(0.5, 0.5, latex_str, 
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=12,
            transform=ax.transAxes)
    
    canvas.draw()
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0, facecolor='white')
    buf.seek(0)
    
    plt.close(fig)
    
    img = QImage()
    img.loadFromData(buf.read())
    
    return QPixmap.fromImage(img)
