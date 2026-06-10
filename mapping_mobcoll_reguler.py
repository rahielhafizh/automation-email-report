import re
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from typing import Optional

ASSET_DIR = Path(__file__).parent / "asset"
INPUT_FILE = ASSET_DIR / "Mapping-PIC.xlsx"
OUTPUT_FILE = ASSET_DIR / "Mapping-Result.xlsx"

DEGREE_MAP: dict[str, str] = {
    "ST": "S.T",
    "SP": "S.P",
    "SAB": "S.A.B",
    "SKOM": "S.Kom",
    "S KOM": "S.Kom",
    "SKom": "S.Kom",
    "SPD": "S.Pd",
    "S PD": "S.Pd",
    "SE": "S.E",
    "SH": "S.H",
    "SI": "S.I",
    "SIP": "S.IP",
    "SSOS": "S.Sos",
    "SAK": "S.Ak",
    "MM": "M.M",
    "MT": "M.T",
    "MBA": "M.B.A",
    "MSI": "M.Si",
    "MSC": "M.Sc",
    "AMD": "A.Md",
}

DEGREE_KEYS_UPPER: frozenset[str] = frozenset(
    k.upper().replace(" ", "") for k in DEGREE_MAP
)

DEGREE_TOKENS_SORTED = sorted(DEGREE_MAP.keys(), key=len, reverse=True)
DEGREE_PATTERN = re.compile(
    r"[,\s]+(" + "|".join(re.escape(d) for d in DEGREE_TOKENS_SORTED) + r")\s*$",
    re.IGNORECASE,
)

INLINE_DEGREE_PATTERN = re.compile(
    r"\s+([A-Z]{2,5})\s*$",
)


def format_abbreviation(token: str) -> str:
    upper = token.upper()
    canonical = DEGREE_MAP.get(upper) or DEGREE_MAP.get(token)
    return canonical if canonical else ".".join(upper)


PREFIX_ABBREV: dict[str, str] = {
    "MUHAMMAD": "M.",
    "MUHAMAD": "M.",
    "MOCHAMMAD": "M.",
    "MOHAMMAD": "M.",
    "MOCHAMAD": "M.",
    "MOHAMAD": "M.",
    "MOH": "M.",
}

BARE_M_PREFIX = re.compile(r"^M$", re.IGNORECASE)

CITY_SUFFIXES: frozenset[str] = frozenset(
    {
        "BKL",
        "SMD",
        "SMG",
        "TBN",
        "NR",
        "KB",
        "MDN",
        "JKT",
        "SBY",
        "BGR",
        "CKR",
        "TSM",
        "CRB",
        "TGR",
        "DPK",
        "BDG",
        "SLO",
        "YGY",
        "MLG",
        "SDA",
        "PTK",
        "BPN",
        "MKS",
        "MDO",
        "AMQ",
        "BTM",
        "PLG",
        "LPG",
        "PBR",
        "PDG",
        "MES",
        "ACH",
        "ABG",
    }
)

BALINESE_COMPOUND: frozenset[str] = frozenset(
    {
        "I MADE",
        "I WAYAN",
        "I KADEK",
        "I GEDE",
        "I PUTU",
        "I KOMANG",
        "I NGURAH",
        "I KETUT",
        "NI LUH",
        "NI MADE",
        "NI WAYAN",
        "NI KADEK",
        "NI KETUT",
        "NI KOMANG",
        "NI PUTU",
        "IDA BAGUS",
        "IDA AYU",
    }
)

BALINESE_SINGLE: frozenset[str] = frozenset({"I", "NI", "IDA", "ANAK", "DEWA", "DESAK"})


def extract_comma_degree(raw: str) -> tuple[str, Optional[str]]:
    match = DEGREE_PATTERN.search(raw)
    if not match:
        return raw, None
    token_raw = match.group(1)
    token_key = token_raw.upper().replace(" ", "")
    pure_name = raw[: match.start()].strip().rstrip(",").strip()
    normalised = format_abbreviation(token_key)
    return pure_name, normalised


def extract_inline_degree(
    tokens_u: list[str], tokens_o: list[str]
) -> tuple[list[str], list[str], Optional[str]]:
    if not tokens_u:
        return tokens_u, tokens_o, None
    last_u = tokens_u[-1].upper()
    if (
        re.fullmatch(r"[A-Z]{2,5}", last_u)
        and last_u in DEGREE_KEYS_UPPER
        and last_u not in CITY_SUFFIXES
    ):
        degree = format_abbreviation(last_u)
        return tokens_u[:-1], tokens_o[:-1], degree
    return tokens_u, tokens_o, None


def strip_city_suffix(upper: list[str], orig: list[str]) -> tuple[list[str], list[str]]:
    if upper and upper[-1] in CITY_SUFFIXES:
        return upper[:-1], orig[:-1]
    return upper, orig


def protected_prefix_length(upper_tokens: list[str]) -> int:
    if len(upper_tokens) >= 2:
        two = upper_tokens[0] + " " + upper_tokens[1]
        if two in BALINESE_COMPOUND:
            return 2
    if upper_tokens and (upper_tokens[0] in BALINESE_SINGLE or upper_tokens[0] == "M."):
        return 1
    return 0


PROTECTED_SINGLES: frozenset[str] = frozenset({"I", "M."})


def format_token(token: str, is_protected: bool = False) -> str:
    if "." in token:
        return token
    upper = token.upper()
    if len(token) == 1 and token.isalpha():
        if is_protected or upper in PROTECTED_SINGLES:
            return upper
        return upper + "."
    return token.title()


def clean_name(value) -> str:
    raw = str(value).strip() if pd.notna(value) else ""
    if not raw:
        return ""

    raw = re.sub(r"\s{2,}", " ", raw).strip().rstrip(".,")

    pure, degree = extract_comma_degree(raw)

    tokens_u = pure.upper().split()
    tokens_o = pure.split()
    if not tokens_u:
        return ""

    tokens_u, tokens_o = strip_city_suffix(tokens_u, tokens_o)
    if not tokens_u:
        return ""

    if degree is None:
        tokens_u, tokens_o, degree = extract_inline_degree(tokens_u, tokens_o)

    if not tokens_u:
        return ""

    if tokens_u[0] in PREFIX_ABBREV:
        tokens_u[0] = PREFIX_ABBREV[tokens_u[0]]
        tokens_o[0] = tokens_u[0]
    elif BARE_M_PREFIX.match(tokens_u[0]) and len(tokens_u) > 1:
        tokens_u[0] = "M."
        tokens_o[0] = "M."

    prefix_len = protected_prefix_length(tokens_u)

    keep_full = prefix_len + 2

    if len(tokens_u) <= keep_full:
        result = " ".join(format_token(t) for t in tokens_u)
    else:
        full_part = " ".join(format_token(t) for t in tokens_u[:keep_full])
        letters = [t[0].upper() for t in tokens_u[keep_full:] if t and t[0].isalpha()]
        initials = ".".join(letters)
        result = f"{full_part} {initials}" if initials else full_part

    return f"{result}, {degree}" if degree else result


def clean_branch_id(value) -> str:
    raw = str(value) if pd.notna(value) else ""
    digits = re.sub(r"[^0-9]", "", raw).strip()
    return digits.zfill(4) if digits else ""


def clean_area(value) -> str:
    raw = str(value).strip() if pd.notna(value) else ""
    stripped = re.sub(r"^[\d\W_]+\s*", "", raw)
    collapsed = re.sub(r"\s{2,}", " ", stripped).strip()
    return collapsed.upper()


HEADER_FILL = PatternFill("solid", start_color="1F4E79", end_color="1F4E79")
ALT_ROW_FILL = PatternFill("solid", start_color="D6E4F0", end_color="D6E4F0")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=10)
BODY_FONT = Font(name="Arial", size=10)
CENTER = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


def apply_worksheet_style(ws, col_count: int) -> None:
    for col in range(1, col_count + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = THIN_BORDER

    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        fill = ALT_ROW_FILL if row_idx % 2 == 0 else PatternFill()
        for cell in row:
            cell.font = BODY_FONT
            cell.fill = fill
            cell.border = THIN_BORDER
            cell.alignment = LEFT

    for col in range(1, col_count + 1):
        col_letter = get_column_letter(col)
        max_len = max(
            (
                len(str(ws.cell(row=r, column=col).value or ""))
                for r in range(1, ws.max_row + 1)
            ),
            default=10,
        )
        ws.column_dimensions[col_letter].width = min(max_len + 4, 45)

    ws.freeze_panes = "A2"


def load_source(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")
    return pd.read_excel(file_path, dtype=str)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    col_names = list(result.columns)

    if len(col_names) > 2:
        result[col_names[2]] = result[col_names[2]].map(clean_branch_id)

    if len(col_names) > 3:
        result[col_names[3]] = result[col_names[3]].map(clean_area)

    if len(col_names) > 6:
        result[col_names[6]] = result[col_names[6]].map(clean_name)

    if len(col_names) > 10:
        result[col_names[10]] = result[col_names[10]].map(clean_name)

    return result


def write_output(df: pd.DataFrame, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(file_path, index=False, sheet_name="Result")

    wb = load_workbook(file_path)
    ws = wb.active
    apply_worksheet_style(ws, len(df.columns))
    wb.save(file_path)


def run() -> None:
    df_raw = load_source(INPUT_FILE)
    df_clean = transform(df_raw)
    write_output(df_clean, OUTPUT_FILE)
    print(f"[DONE] {len(df_clean)} rows written → {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
