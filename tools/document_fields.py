#!/usr/bin/env python3
"""Insert auto-derived doc comments above undocumented record fields.

Reads the exact `WARNING [types.bal:(line:col,...)] undocumented field 'name'`
locations from a `bal build` run and inserts a `# <description>` line above
each one. Descriptions are mechanically derived from the field name (splitting
camelCase/PascalCase and expanding common SAP Business One abbreviations such
as Whs -> Warehouse, Qty -> Quantity), not sourced from SAP documentation,
since SAP's own Service Layer metadata carries no field-level descriptions to
draw from.

Usage: python3 tools/document_fields.py <connector-dir> [<connector-dir> ...]
Each <connector-dir> is a path like ballerina/banking.
"""
import re
import subprocess
import sys
from pathlib import Path

ABBREVIATIONS = {
    "whs": "warehouse", "qty": "quantity", "amt": "amount", "num": "number",
    "pct": "percent", "fc": "foreign currency", "sc": "system currency",
    "lc": "local currency", "bp": "business partner", "doc": "document",
    "cust": "customer", "vend": "vendor", "curr": "currency",
    "desc": "description", "ref": "reference", "addr": "address",
    "acct": "account", "grp": "group", "cd": "code", "id": "ID",
    "url": "URL", "vat": "VAT", "gl": "general ledger",
    "ar": "accounts receivable", "ap": "accounts payable",
    "po": "purchase order", "so": "sales order", "uom": "unit of measure",
    "wt": "withholding tax", "sn": "serial number", "wh": "warehouse",
    "dfs": "distribution", "no": "number", "info": "information",
    "org": "organization", "bom": "bill of materials",
}

WARNING_RE = re.compile(
    r"WARNING \[(?P<file>[^:]+):\((?P<line>\d+):\d+,\d+:\d+\)\] "
    r"undocumented field '(?P<field>[^']+)'"
)

WORD_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z0-9]+|[A-Z0-9]+")


def describe(field_name: str) -> str:
    name = field_name.lstrip("'")
    if name.startswith("U_"):
        rest = name[2:]
        return f"User-defined field: {describe(rest)[0].lower()}{describe(rest)[1:]}"
    words = WORD_RE.findall(name)
    if not words:
        return f"The `{name}` field."
    phrase_parts = []
    for w in words:
        lw = w.lower()
        if lw in ABBREVIATIONS:
            phrase_parts.append(ABBREVIATIONS[lw])
        elif w.isupper() and len(w) > 1:
            phrase_parts.append(w)
        else:
            phrase_parts.append(lw)
    phrase = " ".join(phrase_parts)
    phrase = phrase[0].upper() + phrase[1:]
    return f"{phrase} field."


def get_warnings(connector_dir: Path):
    result = subprocess.run(
        ["bal", "build", str(connector_dir)],
        capture_output=True, text=True, timeout=300,
    )
    warnings = []
    for line in result.stdout.splitlines() + result.stderr.splitlines():
        m = WARNING_RE.search(line)
        if m:
            warnings.append((int(m.group("line")), m.group("field")))
    return warnings


def patch_file(bal_file: Path, warnings):
    lines = bal_file.read_text().splitlines(keepends=True)
    # Process bottom-to-top so earlier line numbers stay valid.
    for line_no, field_name in sorted(set(warnings), key=lambda x: -x[0]):
        idx = line_no - 1
        target = lines[idx]
        indent = target[: len(target) - len(target.lstrip(" "))]
        desc = describe(field_name)
        # Doc comments must precede annotations, not follow them: walk up
        # past any consecutive `@...` annotation lines immediately above
        # the field before inserting the `#` doc comment line.
        insert_at = idx
        while insert_at > 0 and lines[insert_at - 1].lstrip().startswith("@"):
            insert_at -= 1
        lines.insert(insert_at, f"{indent}# {desc}\n")
    bal_file.write_text("".join(lines))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        connector_dir = Path(arg)
        name = connector_dir.name
        print(f"=== {name} ===")
        warnings = get_warnings(connector_dir)
        by_file = {}
        for line_no, field_name in warnings:
            by_file.setdefault("types.bal", []).append((line_no, field_name))
        if not by_file:
            print("  no undocumented fields")
            continue
        for fname, warns in by_file.items():
            bal_file = connector_dir / fname
            print(f"  patching {bal_file} ({len(warns)} fields)")
            patch_file(bal_file, warns)


if __name__ == "__main__":
    main()
