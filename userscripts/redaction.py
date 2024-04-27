import cv2
import fitz
import numpy as np

pdf = fitz.open("./test.pdf")  # open as pdf

for page in pdf.pages():

    page.clean_contents()
    images = page.get_images()
    len_images = len(images)

    if len_images == 0:
        continue

    print("Page number: ", page.number + 1)
    for i, img in enumerate(page.get_images()):

        # colors for redaction box
        yellow = (1, 1, 0)
        black = (0, 0, 0)
        pix = fitz.Pixmap(pdf, img[0]).tobytes()
        pix = cv2.imdecode(np.asarray(bytearray(pix), dtype="uint8"), cv2.IMREAD_COLOR)

        cv2.imshow("image", pix)
        print(f"Image {i}/{len_images} - Redact? (y/N): ")

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        redact = input()
        print("")

        if redact != "y" and redact != "Y":
            continue

        box = page.get_image_bbox(img[7])
        page.add_redact_annot(box, "REDACTED", align=fitz.TEXT_ALIGN_CENTER, fill=black, text_color=yellow)

    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

pdf.save("./redact.pdf", garbage=3, deflate=True)