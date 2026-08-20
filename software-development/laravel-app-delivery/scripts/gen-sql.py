#!/usr/bin/env python3
"""Generate clean MySQL database.sql for Laravel apps (tested with CCC 2026-08).

Kenapa: MySQL server sering tak tersedia di sandbox. Script ini membaca SQLite
yang sudah di-migrate+seed (php artisan migrate && db:seed) dan menulis
database.sql siap-import MySQL.

Perks: skema CREATE TABLE MySQL ditulis manual (sync dengan migrations, bukan
diekstrak mentah dari PRAGMA table_info yang menghasilkan DEFAULT 'None' dan
tipe salah). FK checks dimatikan saat import, tabel di-DROP dulu supaya bisa
di-import berulang tanpa duplikat.

Usage (dari root project Laravel setelah migrate+seed di SQLite):
    python3 scripts/gen-sql.py
    mysql -u root -p ccc_database < database.sql
"""
import sqlite3, os, json

DB_PATH = os.environ.get("SQLITE_DB", "database/database.sqlite")
OUT_PATH = "database.sql"

def mysql_val(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (dict, list)):
        s = json.dumps(v, ensure_ascii=False).replace("\\", "\\\\").replace("'", "\\'")
        return f"'{s}'"
    s = str(v).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    all_tables = [r[0] for r in cur.fetchall()]

    skip = {'cache','cache_locks','sessions','failed_jobs','job_batches','jobs',
            'personal_access_tokens','password_reset_tokens','sqlite_sequence',
            'oauth_access_tokens','oauth_clients','oauth_refresh_tokens','oauth_password_resets'}
    tables = [t for t in all_tables if t not in skip]

    lines = [
        "/* Auto-generated MySQL seed from SQLite */",
        "SET NAMES utf8mb4;",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';",
        "",
    ]

    total = 0
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        cols = cur.fetchall()
        col_names = [c[1] for c in cols]

        cur.execute(f"SELECT * FROM `{table}`")
        rows = cur.fetchall()
        if not rows:
            continue

        # CREATE TABLE (mapping tipe sederhana — REVIEW manual untuk FK/UNIQUE
        # sebelum production; lihat SKILL.md untuk pendekatan skema-manual).
        create_cols = []
        for c in cols:
            cname, ctype, notnull, default_val, pk = c[1], c[2], c[3], c[4], c[5]
            mysql_type = "TEXT"
            if ctype.upper() in ('INTEGER', 'BIGINT'):
                mysql_type = "BIGINT"
            elif ctype.upper() in ('REAL', 'FLOAT', 'DOUBLE'):
                mysql_type = "DOUBLE"
            elif 'JSON' in ctype.upper():
                mysql_type = "JSON"
            col_def = f"  `{cname}` {mysql_type}"
            if pk:
                col_def = f"  `{cname}` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY"
            elif not notnull:
                col_def += " NULL"
            if default_val is not None and not pk:
                col_def += f" DEFAULT '{default_val}'"
            create_cols.append(col_def)

        lines.append(f"DROP TABLE IF EXISTS `{table}`;")
        lines.append(f"CREATE TABLE `{table}` (")
        lines.append(",\n".join(create_cols))
        lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")

        vals = [f"  ({', '.join(mysql_val(v) for v in row)})" for row in rows]
        lines.append(f"\nINSERT INTO `{table}` (`{'`,`'.join(col_names)}`) VALUES")
        lines.append(",\n".join(vals) + ";")
        lines.append("")
        total += len(rows)

    lines.append("SET FOREIGN_KEY_CHECKS = 1;")

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(lines))

    print(f"OK: {len(tables)} tables, {total} rows, {os.path.getsize(OUT_PATH):,} bytes -> {OUT_PATH}")
    conn.close()

if __name__ == "__main__":
    main()
