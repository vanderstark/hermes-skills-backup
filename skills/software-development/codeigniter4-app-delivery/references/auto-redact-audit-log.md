# Auto-Redact & Audit Log (Polri LLM Gateway)

Dokumentasi implementasi fitur keamanan untuk instansi pemerintah.

## 1. Audit Log Table
```sql
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100),
    endpoint VARCHAR(255),
    details TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    created_at DATETIME
);
```

## 2. AuditModel Pattern
Tiap aksi sensitif (send prompt, login, edit kasus) wajib memanggil `AuditModel::log()`
sebelum atau sesudah eksekusi:

```php
// Di Controller:
$this->auditModel->log('Prompt Sent', ['prompt' => $text, 'tool' => $osint]);
```

## 3. Auto-Redact PII (NIK/Telp/Email)
Pola filter sensitif yang WAJIB diterapkan pada HASIL LLM sebelum dikirim ke UI/database.

```php
private function redactSensitiveInfo(string $text): string
{
    // NIK (16 digit)
    $text = preg_replace('/\b\d{16}\b/', '[REDACTED_NIK]', $text);
    // Phone
    $text = preg_replace('/(?:\+62|0)(?:\d{2,3}){1}[ -]?\d{4}[ -]?\d{4}/', '[REDACTED_PHONE]', $text);
    // Email
    $text = preg_replace('/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/', '[REDACTED_EMAIL]', $text);
    return $text;
}
```
Selalu panggil `redactSensitiveInfo()` tepat setelah `llmResult` didapat dari API/Service.
