    #!/usr/bin/env python3
    import sys
    import json
    import pytesseract
    from PIL import Image
    import os
    import re

    def normalize(text):
        return re.sub(r'\s+', ' ', text).strip().lower()

    def extract_tahun_lulus(text):
        lines = text.split('\n')
        for line in reversed(lines):
            if 'kabupaten' in line or 'kota' in line:
                year = re.search(r'(20\d{2})', line)
                if year:
                    return year.group(1)
        return None

    def ocr_image(path):
        img = Image.open(path)
        img = img.convert('L')
        img = img.point(lambda x: 0 if x < 140 else 255)

        text = pytesseract.image_to_string(img, lang='ind+eng')
        text_lower = text.lower()

        result = {
            "raw_text": text_lower
        }

        # =====================
        # NISN
        # =====================
        nisn_match = re.search(r'\b\d{10}\b', text_lower)
        if nisn_match:
            result["nisn"] = nisn_match.group()

        # =====================
        # Nama
        # =====================
        lines = [l.strip() for l in text_lower.split('\n') if l.strip()]
        for i, line in enumerate(lines):
            if 'dengan' in line and 'menyatakan' in line:
                if i + 1 < len(lines):
                    result["nama"] = normalize(lines[i+1])
                    break

        # =====================
        # Tahun Lulus (FIX)
        # =====================
        tahun_lulus = extract_tahun_lulus(text_lower)
        if tahun_lulus:
            result["tahun_lulus"] = tahun_lulus

        # =====================
        # Sekolah
        # =====================
        for line in lines:
            if 'satuan pendidikan' in line or 'saluan pendidikan' in line:
                result["sekolah"] = normalize(
                    line.replace('satuan pendidikan','')
                        .replace('saluan pendidikan','')
                        .replace(':','')
                )
                break

        return result

    if __name__ == "__main__":
        phone = sys.argv[1]
        file_path = sys.argv[2]

        if not os.path.exists(file_path):
            print(json.dumps({"error": "File not found"}))
            sys.exit(1)

        data = ocr_image(file_path)
        data["phone"] = phone
        data["file_path"] = file_path

        print(json.dumps(data))
