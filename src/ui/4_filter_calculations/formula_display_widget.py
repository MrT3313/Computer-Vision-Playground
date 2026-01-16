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
        self._filter_type = "Mean"
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self._formula_label = QLabel()
        self._formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._formula_label)
        
        self._render_formula()
    
    def set_filter(self, filter_name: str) -> None:
        self._filter_type = filter_name
        self._render_formula()

    
    def _render_formula(self) -> None:
        if self._filter_type == "Mean":
            formula = self._create_mean_formula()
        else:
            formula = "No formula available"
        
        pixmap = self._latex_to_pixmap(formula)
        self._formula_label.setPixmap(pixmap)
    
    def _create_mean_formula(self) -> str:
        return r'$G(i,j) = \frac{1}{(2k + 1)^2} \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} F(u+i, v+j)$'
    
    def _latex_to_pixmap(self, latex_str: str) -> QPixmap:
        fig = Figure(figsize=(8, 1), facecolor='white')
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
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        
        plt.close(fig)
        
        img = QImage()
        img.loadFromData(buf.read())
        
        return QPixmap.fromImage(img)
    
    def sizeHint(self) -> QSize:
        return QSize(600, 80)
