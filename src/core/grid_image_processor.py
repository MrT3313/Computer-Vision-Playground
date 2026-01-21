import cv2
import easyocr
from typing import Tuple


class GridImageProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=True)
    
    def process_image(self, image_path: str) -> tuple[bool, tuple[int, list[list[int]]] | None, str]:
        try:
            img = cv2.imread(image_path)
            if img is None:
                return (False, None, "Failed to load image file")
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            h_positions, v_positions = self._detect_grid_lines(gray, height, width)
            if h_positions is None or v_positions is None:
                return (False, None, "Failed to detect grid lines")
            
            grid_size, grid_data = self._extract_cell_values(gray, h_positions, v_positions)
            if grid_size is None:
                return (False, None, "Failed to extract grid values")
            
            validation_result = self._validate_grid(grid_size, grid_data)
            if not validation_result[0]:
                return validation_result
            
            return (True, (grid_size, grid_data), validation_result[1])
            
        except Exception as e:
            return (False, None, f"Error during processing: {str(e)}")
    
    def _detect_grid_lines(self, gray: cv2.Mat, height: int, width: int) -> tuple[list[int] | None, list[int] | None]:
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width // 40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height // 120))
        
        horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=2)
        
        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=2)
        
        h_projection = cv2.reduce(horizontal_lines, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32F).flatten()
        v_projection = cv2.reduce(vertical_lines, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32F).flatten()
        
        h_threshold = h_projection.max() * 0.5
        v_threshold = v_projection.max() * 0.5
        
        h_candidates = [(i, val) for i, val in enumerate(h_projection) if val > h_threshold]
        v_candidates = [(i, val) for i, val in enumerate(v_projection) if val > v_threshold]
        
        if len(h_candidates) == 0 or len(v_candidates) == 0:
            return (None, None)
        
        h_candidates.sort(key=lambda x: x[1], reverse=True)
        v_candidates.sort(key=lambda x: x[1], reverse=True)
        
        h_positions = self._filter_line_positions(h_candidates, height // 30, height)
        v_positions = self._filter_line_positions(v_candidates, width // 30, width)
        
        if len(h_positions) < 2 or len(v_positions) < 2:
            return (None, None)
        
        expected_grid_size = len(h_positions) - 1
        detected_v_size = len(v_positions) - 1
        
        if detected_v_size != expected_grid_size:
            v_positions = self._estimate_missing_lines(v_positions, h_positions, expected_grid_size, height, width)
            if v_positions is None:
                return (None, None)
        
        if len(h_positions) < 2 or len(v_positions) < 2:
            return (None, None)
        
        return (h_positions, v_positions)
    
    def _filter_line_positions(self, candidates: list[tuple[int, float]], min_spacing: int, dimension: int) -> list[int]:
        positions = []
        for pos, val in candidates:
            if not positions:
                positions.append(pos)
            else:
                too_close = any(abs(pos - existing) < min_spacing for existing in positions)
                if not too_close:
                    positions.append(pos)
        positions.sort()
        return positions
    
    def _estimate_missing_lines(self, v_positions: list[int], h_positions: list[int], 
                                 expected_size: int, height: int, width: int) -> list[int] | None:
        if len(v_positions) <= 1:
            return None
        
        avg_h_spacing = (h_positions[-1] - h_positions[0]) / max(1, len(h_positions) - 1) if len(h_positions) > 1 else 0
        avg_v_spacing = (v_positions[-1] - v_positions[0]) / max(1, len(v_positions) - 1)
        
        if avg_h_spacing > 0:
            estimated_v_cells = int((v_positions[-1] - v_positions[0]) / avg_h_spacing) + 1
            
            if abs(estimated_v_cells - expected_size) <= 1 and avg_h_spacing > 10:
                v_positions_filtered = [v_positions[0]]
                for i in range(1, expected_size + 1):
                    estimated_pos = int(v_positions[0] + i * avg_h_spacing)
                    v_positions_filtered.append(estimated_pos)
                return sorted(v_positions_filtered)
            else:
                return None
        return None
    
    def _extract_cell_values(self, gray: cv2.Mat, h_positions: list[int], v_positions: list[int]) -> tuple[int | None, list[list[int]] | None]:
        num_rows = len(h_positions) - 1
        num_cols = len(v_positions) - 1
        
        if num_rows != num_cols:
            return (None, None)
        
        if num_rows < 3 or num_rows > 20:
            return (None, None)
        
        grid_size = num_rows
        grid_data = []
        ocr_failures = 0
        ocr_failure_details = []
        total_cells = grid_size * grid_size
        
        for row_idx in range(grid_size):
            row_data = []
            y_start = h_positions[row_idx]
            y_end = h_positions[row_idx + 1] if row_idx + 1 < len(h_positions) else gray.shape[0]
            
            for col_idx in range(grid_size):
                x_start = v_positions[col_idx]
                x_end = v_positions[col_idx + 1] if col_idx + 1 < len(v_positions) else gray.shape[1]
                
                cell_img = gray[y_start:y_end, x_start:x_end]
                
                if cell_img.size == 0:
                    row_data.append(0)
                    ocr_failures += 1
                    ocr_failure_details.append(f"Cell ({row_idx}, {col_idx}): empty")
                    continue
                
                cell_value = self._process_ocr_cell(cell_img, row_idx, col_idx)
                if cell_value is None:
                    ocr_failures += 1
                    ocr_failure_details.append(f"Cell ({row_idx}, {col_idx}): OCR failed")
                    row_data.append(0)
                else:
                    row_data.append(cell_value)
            
            grid_data.append(row_data)
        
        failure_rate = ocr_failures / total_cells if total_cells > 0 else 1.0
        if failure_rate > 0.3:
            failure_msg = f"OCR failed for {ocr_failures}/{total_cells} cells ({failure_rate*100:.1f}%). "
            failure_msg += f"First few failures: {', '.join(ocr_failure_details[:5])}"
            if len(ocr_failure_details) > 5:
                failure_msg += f" ... and {len(ocr_failure_details) - 5} more"
            return (None, None)
        
        if ocr_failures > 0:
            return (grid_size, grid_data)
        
        return (grid_size, grid_data)
    
    def _process_ocr_cell(self, cell_img: cv2.Mat, row_idx: int, col_idx: int) -> int | None:
        _, cell_binary = cv2.threshold(cell_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        padding = 5
        cell_img_padded = cv2.copyMakeBorder(
            cell_binary, padding, padding, padding, padding,
            cv2.BORDER_CONSTANT, value=0
        )
        
        results = self.reader.readtext(cell_img_padded)
        
        if not results:
            return None
        
        text = results[0][1].strip()
        text = text.replace('O', '0').replace('o', '0')
        text = text.replace('l', '1').replace('I', '1')
        text = text.replace('S', '5').replace('s', '5')
        text = text.replace('Z', '2').replace('z', '2')
        text = ''.join(c for c in text if c.isdigit())
        
        if text:
            try:
                value = int(text)
                if 0 <= value <= 255:
                    return value
            except ValueError:
                pass
        
        return None
    
    def _validate_grid(self, grid_size: int, grid_data: list[list[int]]) -> tuple[bool, str]:
        if grid_size < 3 or grid_size > 20:
            return (False, f"Grid size {grid_size}x{grid_size} is outside valid range (3-20)")
        
        total_cells = grid_size * grid_size
        extracted_count = sum(1 for row in grid_data for val in row if val is not None and val != 0)
        
        if extracted_count == total_cells:
            return (True, "Successfully processed image")
        else:
            return (True, f"Successfully extracted {extracted_count}/{total_cells} values")
