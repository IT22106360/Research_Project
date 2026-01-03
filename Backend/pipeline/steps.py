import cv2
import numpy as np

def illumination_correction(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def denoise(img):
    return cv2.fastNlMeansDenoisingColored(
        img, None,
        h=6, hColor=6,
        templateWindowSize=7,
        searchWindowSize=21
    )

def blur_score(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def resize_if_needed(img, min_height=900):
    h, w = img.shape[:2]
    if h < min_height:
        scale = min_height / h
        img = cv2.resize(
            img,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC  # text-safe
        )
    return img

def adaptive_sharpen(img):
    score = blur_score(img)

    if score < 80:
        alpha = 1.8
    elif score < 150:
        alpha = 1.4
    else:
        return img  # already sharp enough

    blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=1.0)
    return cv2.addWeighted(img, alpha, blurred, -(alpha - 1), 0)

def preprocess_for_ocr(img):
    img = illumination_correction(img)
    img = denoise(img)
    img = resize_if_needed(img)
    img = adaptive_sharpen(img)

    return img

def run_tesseract_ocr(preprocessed_img, image_id="web_image"):
    """
    Input:
        preprocessed_img: OpenCV BGR image
    Output:
        OCR JSON with text + word boxes
    """

    # Convert BGR → RGB (Tesseract expects RGB)
    rgb = cv2.cvtColor(preprocessed_img, cv2.COLOR_BGR2RGB)

    # OCR config (OCR-friendly)
    custom_config = r"--oem 3 --psm 6"

    data = pytesseract.image_to_data(
        rgb,
        config=custom_config,
        output_type=pytesseract.Output.DICT
    )

    words = []
    full_text = []

    H, W = rgb.shape[:2]

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        conf = int(data["conf"][i])

        if text == "" or conf < 40:
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        words.append({
            "text": text,
            "confidence": conf,
            "bbox": [x, y, x + w, y + h]  # pixel coords
        })

        full_text.append(text)

    return {
        "image_id": image_id,
        "ocr_text": " ".join(full_text),
        "words": words,
        "ocr_width": W,
        "ocr_height": H
    }
