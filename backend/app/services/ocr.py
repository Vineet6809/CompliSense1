"""Real CPU OCR, loaded only on first use. No cloud keys or fake fallback text."""

import importlib.util
from pathlib import Path


class OCRUnavailableError(RuntimeError):
    pass


class OCRService:
    def __init__(self):
        self.engine = None

    @property
    def available(self) -> bool:
        return importlib.util.find_spec("rapidocr_onnxruntime") is not None

    def scan(self, path: Path) -> dict:
        if not self.available:
            raise OCRUnavailableError("OCR is not installed. Install backend/requirements.txt and restart the API.")
        import cv2
        from rapidocr_onnxruntime import RapidOCR

        if self.engine is None:
            self.engine = RapidOCR(intra_op_num_threads=2, inter_op_num_threads=1)
        image = cv2.imread(str(path))
        if image is None:
            raise ValueError("The saved image could not be read. Upload the photograph again.")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        reflection_score = float(cv2.countNonZero((gray >= 245).astype("uint8")) / gray.size)
        warnings = []
        if blur_score < 60:
            warnings.append("The image has little sharp detail. Check focus and recapture if text is blurred.")
        if min(image.shape[:2]) < 500:
            warnings.append("Low image resolution may hide small declarations. Use a closer, sharper photograph.")
        if reflection_score > 0.08:
            warnings.append("Bright glare covers part of the label. Recheck any extracted value against a non-reflective photograph.")
        results, _ = self.engine(image)
        lines = []
        for box, text, confidence in results or []:
            lines.append(
                {
                    "text": str(text),
                    "confidence": round(float(confidence), 4),
                    "box": [[float(x), float(y)] for x, y in box],
                }
            )
        if not lines:
            warnings.append("No text was recognized. Absence of OCR text is not proof that a declaration is missing.")
        average_confidence = round(sum(line["confidence"] for line in lines) / len(lines), 3) if lines else 0.0
        if lines and average_confidence < 0.65:
            warnings.append("OCR confidence is low across the detected text. Treat extracted declarations as review candidates.")
        return {
            "lines": lines,
            "ocr_text": "\n".join(line["text"] for line in lines),
            "quality": {
                "warnings": warnings,
                "blur_score": round(blur_score, 2),
                "reflection_score": round(reflection_score, 3),
                "ocr_confidence": average_confidence,
                "review_required": bool(warnings),
            },
        }
