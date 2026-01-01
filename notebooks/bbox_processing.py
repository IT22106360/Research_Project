OCR_W = 2480  # width used during OCR
OCR_H = 3508  # height used during OCR

def rescale_box(box, src_w, src_h, dst_w, dst_h):
    x1, y1, x2, y2 = box
    return [
        int(x1 / src_w * dst_w),
        int(y1 / src_h * dst_h),
        int(x2 / src_w * dst_w),
        int(y2 / src_h * dst_h),
    ]

bboxes_px = [rescale_box(b, OCR_W, OCR_H, W, H) for b in bboxes]

OCR_W = 2480  # width used during OCR
OCR_H = 3508  # height used during OCR

def rescale_box(box, src_w, src_h, dst_w, dst_h):
    x1, y1, x2, y2 = box
    return [
        int(x1 / src_w * dst_w),
        int(y1 / src_h * dst_h),
        int(x2 / src_w * dst_w),
        int(y2 / src_h * dst_h),
    ]

bboxes_px = [rescale_box(b, OCR_W, OCR_H, W, H) for b in bboxes]

def clamp_pixel_box(box, width, height):
    x1, y1, x2, y2 = box
    return [
        max(0, min(x1, width)),
        max(0, min(y1, height)),
        max(0, min(x2, width)),
        max(0, min(y2, height)),
    ]

bboxes_px = [clamp_pixel_box(b, W, H) for b in bboxes_px]

def normalize_box(box, width, height):
    x1, y1, x2, y2 = box
    return [
        int(1000 * x1 / width),
        int(1000 * y1 / height),
        int(1000 * x2 / width),
        int(1000 * y2 / height),
    ]

bboxes_norm = [normalize_box(b, W, H) for b in bboxes_px]

def clamp_norm_box(box):
    return [max(0, min(v, 1000)) for v in box]

bboxes_norm = [clamp_norm_box(b) for b in bboxes_norm]

def fix_bboxes(bboxes, image, ocr_size=None):
    H, W, _ = image.shape

    if ocr_size:
        ow, oh = ocr_size
        bboxes = [rescale_box(b, ow, oh, W, H) for b in bboxes]

    bboxes = [clamp_pixel_box(b, W, H) for b in bboxes]

    for b in bboxes:
        assert b[0] < b[2] and b[1] < b[3]

    bboxes_norm = [normalize_box(b, W, H) for b in bboxes]
    bboxes_norm = [clamp_norm_box(b) for b in bboxes_norm]

    return bboxes, bboxes_norm

