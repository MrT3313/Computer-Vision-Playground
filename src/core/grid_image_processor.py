import cv2
import easyocr


class GridImageProcessor:
    def __init__(self):
        # Initialize EasyOCR reader for English text recognition with GPU acceleration
        self.reader = easyocr.Reader(['en'], gpu=True)
    
    def process_image(self, image_path: str) -> tuple[bool, tuple[int, list[list[int]]] | None, str]:
        """
        Process an image containing a grid of numbers and extract the values.
        
        Returns:
            tuple: (success: bool, data: tuple[grid_size, grid_data] | None, message: str)
        """
        try:
            # Load the image from file
            img = cv2.imread(image_path)
            if img is None:
                return (False, None, "Failed to load image file")
            
            # Convert image to grayscale for processing
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            # Apply binary thresholding using Otsu's method to separate grid lines from background
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Create morphological kernels for detecting horizontal and vertical lines
            # Horizontal kernel: wide and thin to detect horizontal lines
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width // 40, 1))
            # Vertical kernel: thin and tall to detect vertical lines
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height // 120))
            
            # Detect horizontal lines using morphological opening followed by dilation
            horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
            horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=2)
            
            # Detect vertical lines using morphological opening followed by dilation
            vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
            vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=2)
            
            # Create projections to find line positions
            # Horizontal projection: sum pixels along each row to find horizontal lines
            h_projection = cv2.reduce(horizontal_lines, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32F).flatten()
            # Vertical projection: sum pixels along each column to find vertical lines
            v_projection = cv2.reduce(vertical_lines, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32F).flatten()
            
            # Set thresholds for detecting line positions (50% of maximum projection value)
            h_threshold = h_projection.max() * 0.5
            v_threshold = v_projection.max() * 0.5
            
            # Find candidate positions for horizontal lines
            h_candidates = []
            for i, val in enumerate(h_projection):
                if val > h_threshold:
                    h_candidates.append((i, val))
            
            # Find candidate positions for vertical lines
            v_candidates = []
            for i, val in enumerate(v_projection):
                if val > v_threshold:
                    v_candidates.append((i, val))
            
            # Verify that grid lines were detected
            if len(h_candidates) == 0 or len(v_candidates) == 0:
                return (False, None, f"Failed to detect grid lines (found {len(h_candidates)} horizontal, {len(v_candidates)} vertical candidates)")
            
            # Sort candidates by projection strength (descending)
            h_candidates.sort(key=lambda x: x[1], reverse=True)
            v_candidates.sort(key=lambda x: x[1], reverse=True)
            
            # Filter horizontal line positions to remove duplicates that are too close
            h_positions = []
            min_h_spacing = height // 30  # Minimum spacing between lines
            for pos, val in h_candidates:
                if not h_positions:
                    h_positions.append(pos)
                else:
                    # Check if this position is too close to any existing position
                    too_close = any(abs(pos - existing) < min_h_spacing for existing in h_positions)
                    if not too_close:
                        h_positions.append(pos)
            h_positions.sort()  # Sort positions from top to bottom
            
            # Filter vertical line positions to remove duplicates that are too close
            v_positions = []
            min_v_spacing = width // 30  # Minimum spacing between lines
            for pos, val in v_candidates:
                if not v_positions:
                    v_positions.append(pos)
                else:
                    # Check if this position is too close to any existing position
                    too_close = any(abs(pos - existing) < min_v_spacing for existing in v_positions)
                    if not too_close:
                        v_positions.append(pos)
            v_positions.sort()  # Sort positions from left to right
            
            # Verify minimum number of lines detected
            if len(h_positions) < 2:
                return (False, None, f"Failed to detect horizontal grid lines (found {len(h_positions)} lines, need at least 2)")
            
            if len(v_positions) < 2:
                return (False, None, f"Failed to detect vertical grid lines (found {len(v_positions)} lines, need at least 2)")
            
            # Calculate expected grid dimensions
            expected_grid_size = len(h_positions) - 1  # Number of cells = number of lines - 1
            detected_v_size = len(v_positions) - 1
            
            # Handle grid mismatch by attempting to estimate missing vertical lines
            if detected_v_size != expected_grid_size:
                if len(v_positions) > 1:
                    # Calculate average spacing between lines
                    avg_h_spacing = (h_positions[-1] - h_positions[0]) / max(1, len(h_positions) - 1) if len(h_positions) > 1 else 0
                    avg_v_spacing = (v_positions[-1] - v_positions[0]) / max(1, len(v_positions) - 1)
                    
                    if avg_h_spacing > 0:
                        # Estimate number of vertical cells based on horizontal spacing
                        estimated_v_cells = int((v_positions[-1] - v_positions[0]) / avg_h_spacing) + 1
                        
                        # If estimation is close and spacing is reasonable, reconstruct vertical positions
                        if abs(estimated_v_cells - expected_grid_size) <= 1 and avg_h_spacing > 10:
                            v_positions_filtered = [v_positions[0]]
                            for i in range(1, expected_grid_size + 1):
                                estimated_pos = int(v_positions[0] + i * avg_h_spacing)
                                v_positions_filtered.append(estimated_pos)
                            v_positions = sorted(v_positions_filtered)
                        else:
                            return (False, None, f"Grid mismatch: {expected_grid_size} rows but {detected_v_size} columns detected. Horizontal spacing: {avg_h_spacing:.1f}px, Vertical spacing: {avg_v_spacing:.1f}px")
                    else:
                        return (False, None, f"Grid is not square: detected {expected_grid_size} rows and {detected_v_size} columns")
                else:
                    return (False, None, f"Grid is not square: detected {expected_grid_size} rows and {detected_v_size} columns")
            
            # Verify we still have minimum number of lines after filtering
            if len(h_positions) < 2:
                return (False, None, f"Failed to detect horizontal grid lines (found {len(h_positions)} lines, need at least 2)")
            
            if len(v_positions) < 2:
                return (False, None, f"Failed to detect vertical grid lines (found {len(v_positions)} lines, need at least 2)")
            
            # Calculate final grid dimensions
            num_rows = len(h_positions) - 1
            num_cols = len(v_positions) - 1
            
            # Verify grid is square
            if num_rows != num_cols:
                return (False, None, f"Grid is not square: detected {num_rows} rows and {num_cols} columns")
            
            # Verify grid size is within valid range
            if num_rows < 3 or num_rows > 20:
                return (False, None, f"Grid size {num_rows}x{num_rows} is outside valid range (3-20)")
            
            # Initialize grid data structure
            grid_size = num_rows
            grid_data = []
            ocr_failures = 0  # Counter for OCR failures
            ocr_failure_details = []  # List of failure details for error reporting
            total_cells = grid_size * grid_size
            
            # Extract values from each cell using OCR
            for row_idx in range(grid_size):
                row_data = []
                # Calculate vertical bounds for this row
                y_start = h_positions[row_idx]
                y_end = h_positions[row_idx + 1] if row_idx + 1 < len(h_positions) else height
                
                for col_idx in range(grid_size):
                    # Calculate horizontal bounds for this column
                    x_start = v_positions[col_idx]
                    x_end = v_positions[col_idx + 1] if col_idx + 1 < len(v_positions) else width
                    
                    # Extract cell image
                    cell_img = gray[y_start:y_end, x_start:x_end]
                    
                    # Handle empty cells
                    if cell_img.size == 0:
                        row_data.append(0)
                        ocr_failures += 1
                        ocr_failure_details.append(f"Cell ({row_idx}, {col_idx}): empty")
                        continue
                    
                    # Apply binary thresholding to cell image for better OCR accuracy
                    _, cell_binary = cv2.threshold(cell_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    
                    # Add padding around cell to improve OCR recognition
                    padding = 5
                    cell_img_padded = cv2.copyMakeBorder(
                        cell_binary, padding, padding, padding, padding,
                        cv2.BORDER_CONSTANT, value=0
                    )
                    
                    # Perform OCR on the cell image
                    results = self.reader.readtext(cell_img_padded)
                    
                    # Process OCR results
                    cell_value = None
                    ocr_text = None
                    if results:
                        # Get the recognized text
                        text = results[0][1].strip()
                        ocr_text = text
                        # Apply common OCR error corrections
                        text = text.replace('O', '0').replace('o', '0')  # O -> 0
                        text = text.replace('l', '1').replace('I', '1')  # l, I -> 1
                        text = text.replace('S', '5').replace('s', '5')  # S -> 5
                        text = text.replace('Z', '2').replace('z', '2')  # Z -> 2
                        # Keep only digits
                        text = ''.join(c for c in text if c.isdigit())
                        
                        # Convert to integer and validate range
                        if text:
                            try:
                                value = int(text)
                                if 0 <= value <= 255:  # Valid pixel value range
                                    cell_value = value
                            except ValueError:
                                pass
                    
                    # Handle OCR failures by defaulting to 0
                    if cell_value is None:
                        ocr_failures += 1
                        ocr_text_display = f"'{ocr_text}'" if ocr_text else "no text"
                        ocr_failure_details.append(f"Cell ({row_idx}, {col_idx}): OCR read {ocr_text_display}")
                        row_data.append(0)
                    else:
                        row_data.append(cell_value)
                
                grid_data.append(row_data)
            
            # Calculate OCR failure rate
            failure_rate = ocr_failures / total_cells if total_cells > 0 else 1.0
            # If failure rate is too high (>30%), return error
            if failure_rate > 0.3:
                failure_msg = f"OCR failed for {ocr_failures}/{total_cells} cells ({failure_rate*100:.1f}%). "
                failure_msg += f"First few failures: {', '.join(ocr_failure_details[:5])}"
                if len(ocr_failure_details) > 5:
                    failure_msg += f" ... and {len(ocr_failure_details) - 5} more"
                return (False, None, failure_msg)
            
            # Return success with warning if some OCR failures occurred
            if ocr_failures > 0:
                success_msg = f"Successfully extracted {total_cells - ocr_failures}/{total_cells} values"
                return (True, (grid_size, grid_data), success_msg)
            
            # Return success with no warnings
            return (True, (grid_size, grid_data), "Successfully processed image")
            
        except Exception as e:
            # Catch any unexpected errors and return failure
            return (False, None, f"Error during processing: {str(e)}")