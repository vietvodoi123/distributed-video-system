import re

# --- La Mã ---
ROMAN_MAP = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
def roman_to_int(s: str) -> int:
    s = s.upper()
    total = 0
    prev = 0
    for ch in reversed(s):
        val = ROMAN_MAP.get(ch, 0)
        if val < prev:
            total -= val
        else:
            total += val
        prev = val
    return total

# --- Hán ---
HAN_MAP = {"零":0,"〇":0,"一":1,"二":2,"两":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
UNIT_MAP = {"十":10,"百":100,"千":1000,"万":10000,"亿":100000000}

def chinese_to_number(ch: str) -> int:
    """
    Chuyển chuỗi số chữ Hán sang int.
    - Nếu có ký tự đơn vị (十/百/千/万/亿) → dùng unit-based parsing.
    - Nếu không có đơn vị nhưng có chữ số Hán (ví dụ 二零四) → xử lý theo vị trí (positional).
    """
    ch = (ch or "").strip()
    if not ch:
        return 0

    # Nếu có bất kỳ ký tự đơn vị nào thì dùng unit-based parsing
    if any(c in UNIT_MAP for c in ch):
        total, section, number = 0, 0, 0
        for c in ch:
            if c in HAN_MAP:
                number = HAN_MAP[c]
            elif c in UNIT_MAP:
                unit = UNIT_MAP[c]
                if unit == 10000 or unit == 100000000:
                    # xử lý 万 / 亿: gộp section rồi nhân
                    section = (section + number) * unit
                    total += section
                    section, number = 0, 0
                else:
                    section += (number or 1) * unit
                    number = 0
            elif c.isdigit():
                # cho trường hợp mix chữ số Ả Rập trong chuỗi
                number = number * 10 + int(c)
            else:
                # bỏ qua ký tự lạ
                pass
        return total + section + number

    else:
        # positional style: 二零四 => 2 0 4 => 204
        total = 0
        seen_any = False
        for c in ch:
            if c in HAN_MAP:
                total = total * 10 + HAN_MAP[c]
                seen_any = True
            elif c.isdigit():
                total = total * 10 + int(c)
                seen_any = True
            else:
                # bỏ qua ký tự lạ
                pass
        return total if seen_any else 0

# --- Extract ---
def extract_chapter_number(title: str) -> int | None:
    """
    Trích số chương từ title.
    Trả về int nếu tìm được, None nếu không match.
    """
    if not title:
        return None

    pattern = (
        r"(?:第\s*([一二三四五六七八九十百千万零〇两\dIVXLCDM]+)\s*(?:章|话|卷|节|篇|回|集|段|部|册))"
        r"|(?:Chương\s+([IVXLCDM\d一二三四五六七八九十百千万零〇两]+))"
        r"|(?:\b(\d{1,4})\b)"  # NEW: bắt số dạng 004, 14, 24,...
    )

    m = re.search(pattern, title, re.I)
    if not m:
        return None

    num_str = m.group(1) or m.group(2) or m.group(3)

    if not num_str:
        return None

    num_str = num_str.strip().lstrip("第")

    # Ưu tiên số Ả Rập
    if num_str.isdigit():
        return int(num_str)

    # La Mã
    if re.fullmatch(r"[IVXLCDM]+", num_str, re.I):
        return roman_to_int(num_str)

    # Chữ Hán
    value = chinese_to_number(num_str)
    return value if value != 0 or ("零" in num_str or "〇" in num_str) else None
