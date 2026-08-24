### AuditModel.php
```php
<?php

namespace App\Models;

use CodeIgniter\Model;

class AuditModel extends Model
{
    protected $table = 'audit_logs';
    protected $primaryKey = 'id';
    protected $allowedFields = ['user_id', 'action', 'endpoint', 'details', 'ip_address', 'user_agent', 'created_at'];
    protected $useTimestamps = false;

    public function log($action, $details = null)
    {
        $session = \Config\Services::session();
        $request = \Config\Services::request();

        $this->insert([
            'user_id'    => $session->get('user_id'),
            'action'     => $action,
            'endpoint'   => $request->getUri()->getPath(),
            'details'    => is_array($details) ? json_encode($details) : $details,
            'ip_address' => $request->getIPAddress(),
            'user_agent' => $request->getUserAgent()->getAgentString(),
            'created_at' => date('Y-m-d H:i:s')
        ]);
    }
}
```

### AutoRedact.php Helper (in app/Helpers/)
```php
<?php

if (!function_exists('redactSensitiveInfo')) {
    function redactSensitiveInfo(string $text): string
    {
        // Regex untuk NIK (16 digit angka)
        $text = preg_replace('/\b\d{16}\b/', '[REDACTED_NIK]', $text);

        // Regex untuk Nomor Telepon (contoh: 08xx-xxxx-xxxx atau +628xx-xxxx-xxxx)
        $text = preg_replace('/(?:\+62|0)(?:\\d{2,3}){1}[ -]?\\d{4}[ -]?\\d{4}|\+62(?:\\d{2,3}){1}[ -]?\\d{4}[ -]?\\d{4}/', '[REDACTED_PHONE]', $text);

        // Regex untuk Email
        $text = preg_replace('/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/', '[REDACTED_EMAIL]', $text);
        
        return $text;
    }
}
```

### Maintenance.php Command
```php
<?php

namespace App\Commands;

use CodeIgniter\CLI\BaseCommand;
use CodeIgniter\CLI\CLI;
use Config\Database;

class Maintenance extends BaseCommand
{
    protected $group       = 'App';
    protected $name        = 'app:maintenance';
    protected $description = 'Maintenance harian: cleanup audit log, backup DB, rotasi, reset kuota bulanan.';

    public function run(array $params)
    {
        CLI::write('=== POLRI LLM GATEWAY MAINTENANCE ===', 'yellow');
        CLI::write('Mulai: ' . date('Y-m-d H:i:s'));

        $this->cleanupAuditLogs();
        $this->backupDatabase();
        $this->rotateBackups();

        if (date('j') == 1) {
            $this->resetUserQuota();
        }

        CLI::write('Selesai: ' . date('Y-m-d H:i:s'), 'green');
    }

    protected function cleanupAuditLogs()
    {
        CLI::write('[1/4] Membersihkan audit log > 90 hari...', 'yellow');
        try {
            $db = Database::connect();
            $db->query("DELETE FROM audit_logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY)");
            CLI::write('      OK - ' . $db->affectedRows() . ' baris dihapus.', 'green');
        } catch (\Throwable $e) {
            CLI::error('      GAGAL: ' . $e->getMessage());
        }
    }

    protected function backupDatabase()
    {
        CLI::write('[2/4] Backup database...', 'yellow');
        $db        = Database::connect();
        $backupDir = WRITEPATH . 'backups';

        if (! is_dir($backupDir)) {
            mkdir($backupDir, 0775, true);
        }

        $backupFile = $backupDir . '/backup_' . date('Ymd_His') . '.sql';

        $command = sprintf(
            'mysqldump --user=%s --password=%s --host=%s --single-transaction --quick %s > %s 2>&1',
            escapeshellarg($db->username),
            escapeshellarg($db->password),
            escapeshellarg($db->hostname),
            escapeshellarg($db->database),
            escapeshellarg($backupFile)
        );

        exec($command, $output, $code);

        if ($code === 0 && file_exists($backupFile) && filesize($backupFile) > 0) {
            CLI::write('      OK - ' . $backupFile . ' (' . round(filesize($backupFile) / 1024, 2) . ' KB)', 'green');
        } else {
            CLI::error('      GAGAL: ' . implode(' ', $output));
        }
    }

    protected function rotateBackups()
    {
        CLI::write('[3/4] Rotasi backup (simpan 14 terakhir)...', 'yellow');
        $backupDir = WRITEPATH . 'backups';

        if (! is_dir($backupDir)) {
            CLI::write('      Skip - folder backup belum ada.', 'yellow');
            return;
        }

        $files = glob($backupDir . '/backup_*.sql');
        if ($files === false || count($files) <= 14) {
            CLI::write('      OK - ' . count($files ?: []) . ' backup, tidak perlu rotasi.', 'green');
            return;
        }

        usort($files, static fn ($a, $b) => filemtime($a) <=> filemtime($b));
        $deleted = 0;
        foreach (array_slice($files, 0, count($files) - 14) as $old) {
            if (@unlink($old)) {
                $deleted++;
            }
        }
        CLI::write('      OK - ' . $deleted . ' backup lama dihapus.', 'green');
    }

    protected function resetUserQuota()
    {
        CLI::write('[4/4] Reset kuota bulanan (tanggal 1)...', 'yellow');
        try {
            $db = Database::connect();
            $db->query("UPDATE users SET usage_count = 0");
            CLI::write('      OK - ' . $db->affectedRows() . ' user direset.', 'green');
        } catch (\Throwable $e) {
            CLI::error('      GAGAL: ' . $e->getMessage());
        }
    }
}
```

### `docker-compose.yml` fragment for `cron` service
```yaml
  cron:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: police-llm-cron
    command: cron -f
    volumes:
      - ./police-llm-gateway-ci4:/var/www/html
      - ./crontabs:/etc/cron.d
    depends_on:
      - db
    restart: unless-stopped
```

### `Dockerfile` fragment for `cron` setup
```dockerfile
# Install cron and mysql client
RUN apt-get update && apt-get install -y \
    cron \
    default-mysql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy crontab
COPY crontabs/police-llm-cron /etc/cron.d/police-llm-cron
RUN chmod 0644 /etc/cron.d/police-llm-cron

# CMD to start cron service
CMD service cron start && php-fpm
```

### `crontabs/police-llm-cron`
```bash
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Maintenance harian jam 03:00 (cleanup audit log, backup DB, rotasi, reset kuota tgl 1)
0 3 * * * root cd /var/www/html && php spark app:maintenance >> /var/www/html/writable/logs/maintenance.log 2>&1

# Newline wajib di akhir file crontab
```