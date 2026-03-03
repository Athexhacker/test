<?php
// Enhanced IP and Device Info Collector
// For security testing purposes only

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Create logs directory if it doesn't exist
$logDir = 'security_test_logs';
if (!file_exists($logDir)) {
    mkdir($logDir, 0777, true);
}

// Create IP logs subdirectory
$ipDir = $logDir . '/ip_info';
if (!file_exists($ipDir)) {
    mkdir($ipDir, 0777, true);
}

// Get timestamp
$timestamp = date('Y-m-d H:i:s');
$dateFile = date('Y-m-d'); // For daily files
$dateTimeForFile = date('Ymd_His');

// Get real IP address with proxy detection
function getRealIP() {
    $ip = $_SERVER['REMOTE_ADDR'];
    
    // Check for proxy IPs
    $proxyHeaders = [
        'HTTP_CLIENT_IP',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_CF_CONNECTING_IP', // Cloudflare
        'HTTP_X_REAL_IP' // Nginx proxy
    ];
    
    foreach ($proxyHeaders as $header) {
        if (!empty($_SERVER[$header])) {
            $ips = explode(',', $_SERVER[$header]);
            $ip = trim($ips[0]); // Get first IP in list
            break;
        }
    }
    
    return $ip;
}

$ip = getRealIP();

// Get all available headers
$allHeaders = getallheaders();
$headers = [];
foreach ($allHeaders as $name => $value) {
    $headers[$name] = $value;
}

// Get browser and device info from User-Agent
$userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';

// Parse User-Agent for device info (basic)
function parseUserAgent($ua) {
    $info = [
        'browser' => 'Unknown',
        'browser_version' => 'Unknown',
        'os' => 'Unknown',
        'device' => 'Desktop',
        'is_mobile' => false
    ];
    
    // Check for mobile
    if (preg_match('/Mobile|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i', $ua)) {
        $info['is_mobile'] = true;
        $info['device'] = 'Mobile';
    }
    
    // Check for tablet
    if (preg_match('/iPad|Tablet|Android(?!.*Mobile)/i', $ua)) {
        $info['device'] = 'Tablet';
    }
    
    // Detect OS
    if (preg_match('/Windows NT ([\d.]+)/i', $ua, $matches)) {
        $info['os'] = 'Windows ' . $matches[1];
    } elseif (preg_match('/Mac OS X ([\d_]+)/i', $ua, $matches)) {
        $info['os'] = 'macOS ' . str_replace('_', '.', $matches[1]);
    } elseif (preg_match('/Android ([\d.]+)/i', $ua, $matches)) {
        $info['os'] = 'Android ' . $matches[1];
    } elseif (preg_match('/iOS ([\d_]+)/i', $ua, $matches)) {
        $info['os'] = 'iOS ' . str_replace('_', '.', $matches[1]);
    } elseif (preg_match('/Linux/i', $ua)) {
        $info['os'] = 'Linux';
    }
    
    // Detect Browser
    if (preg_match('/Chrome\/([\d.]+)/i', $ua, $matches) && !preg_match('/Edg/i', $ua)) {
        $info['browser'] = 'Chrome';
        $info['browser_version'] = $matches[1];
    } elseif (preg_match('/Firefox\/([\d.]+)/i', $ua, $matches)) {
        $info['browser'] = 'Firefox';
        $info['browser_version'] = $matches[1];
    } elseif (preg_match('/Safari\/([\d.]+)/i', $ua, $matches) && !preg_match('/Chrome/i', $ua)) {
        $info['browser'] = 'Safari';
        $info['browser_version'] = $matches[1];
    } elseif (preg_match('/Edg\/([\d.]+)/i', $ua, $matches)) {
        $info['browser'] = 'Edge';
        $info['browser_version'] = $matches[1];
    } elseif (preg_match('/MSIE ([\d.]+)/i', $ua, $matches)) {
        $info['browser'] = 'Internet Explorer';
        $info['browser_version'] = $matches[1];
    }
    
    return $info;
}

$uaInfo = parseUserAgent($userAgent);

// Get geolocation data from IP (using multiple services)
function getGeoLocation($ip) {
    // Skip for local IPs
    if ($ip == '127.0.0.1' || $ip == '::1' || strpos($ip, '192.168.') === 0 || strpos($ip, '10.') === 0) {
        return ['error' => 'Local IP', 'ip' => $ip];
    }
    
    // Try ip-api.com first (free, no API key needed)
    try {
        $response = file_get_contents("http://ip-api.com/json/{$ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting");
        if ($response) {
            $data = json_decode($response, true);
            if ($data['status'] == 'success') {
                return $data;
            }
        }
    } catch (Exception $e) {
        // Fallback to next service
    }
    
    // Try ipapi.co as backup
    try {
        $response = file_get_contents("https://ipapi.co/{$ip}/json/");
        if ($response) {
            return json_decode($response, true);
        }
    } catch (Exception $e) {
        // Return basic info
        return [
            'ip' => $ip,
            'error' => 'Could not fetch geolocation'
        ];
    }
    
    return ['ip' => $ip, 'error' => 'Could not fetch geolocation'];
}

$geoData = getGeoLocation($ip);

// Get server info
$serverInfo = [
    'request_time' => $timestamp,
    'request_method' => $_SERVER['REQUEST_METHOD'],
    'request_uri' => $_SERVER['REQUEST_URI'],
    'query_string' => $_SERVER['QUERY_STRING'] ?? '',
    'https' => isset($_SERVER['HTTPS']) ? 'Yes' : 'No',
    'server_protocol' => $_SERVER['SERVER_PROTOCOL'],
    'server_port' => $_SERVER['SERVER_PORT'],
    'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown',
    'document_root' => $_SERVER['DOCUMENT_ROOT'] ?? 'Unknown',
    'script_filename' => $_SERVER['SCRIPT_FILENAME'] ?? 'Unknown'
];

// Check for VPN/Proxy
$vpnDetected = false;
if (isset($geoData['proxy']) && $geoData['proxy'] === true) {
    $vpnDetected = true;
}
if (isset($geoData['hosting']) && $geoData['hosting'] === true) {
    $vpnDetected = true;
}
if (isset($geoData['mobile']) && $geoData['mobile'] === true) {
    // This is a mobile connection, not necessarily VPN
}

// Compile all data
$ipData = [
    'timestamp' => $timestamp,
    'ip' => $ip,
    'headers' => $headers,
    'user_agent' => $userAgent,
    'browser_info' => $uaInfo,
    'geo_location' => $geoData,
    'server_info' => $serverInfo,
    'vpn_detected' => $vpnDetected,
    'referer' => $_SERVER['HTTP_REFERER'] ?? 'Direct',
    'accept_language' => $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'Unknown',
    'accept_encoding' => $_SERVER['HTTP_ACCEPT_ENCODING'] ?? 'Unknown',
    'connection_type' => $_SERVER['HTTP_CONNECTION'] ?? 'Unknown'
];

// 1. Save to JSON file (detailed)
$jsonFile = $ipDir . '/ip_' . $dateTimeForFile . '_' . preg_replace('/[^0-9.]/', '', $ip) . '.json';
file_put_contents($jsonFile, json_encode($ipData, JSON_PRETTY_PRINT));

// 2. Save to daily CSV (for easy analysis)
$csvFile = $ipDir . '/ip_log_' . $dateFile . '.csv';
$isNewFile = !file_exists($csvFile);
$fp = fopen($csvFile, 'a');

if ($isNewFile) {
    fputcsv($fp, [
        'Timestamp',
        'IP',
        'Country',
        'City',
        'ISP',
        'Browser',
        'OS',
        'Device',
        'VPN/Proxy',
        'Referer',
        'User Agent'
    ]);
}

fputcsv($fp, [
    $timestamp,
    $ip,
    $geoData['country'] ?? 'Unknown',
    $geoData['city'] ?? 'Unknown',
    $geoData['isp'] ?? 'Unknown',
    $uaInfo['browser'] . ' ' . $uaInfo['browser_version'],
    $uaInfo['os'],
    $uaInfo['device'],
    $vpnDetected ? 'Yes' : 'No',
    $_SERVER['HTTP_REFERER'] ?? 'Direct',
    substr($userAgent, 0, 100) // Truncate for CSV
]);

fclose($fp);

// 3. Save to simple text log (original format but enhanced)
$txtFile = $ipDir . '/ip_simple_' . $dateFile . '.txt';
$txtLog = fopen($txtFile, 'a');

fwrite($txtLog, "=== New Visitor: {$timestamp} ===\r\n");
fwrite($txtLog, "IP: {$ip}\r\n");
fwrite($txtLog, "Location: " . ($geoData['city'] ?? 'Unknown') . ", " . ($geoData['country'] ?? 'Unknown') . "\r\n");
fwrite($txtLog, "ISP: " . ($geoData['isp'] ?? 'Unknown') . "\r\n");
fwrite($txtLog, "Browser: " . $uaInfo['browser'] . " " . $uaInfo['browser_version'] . "\r\n");
fwrite($txtLog, "OS: " . $uaInfo['os'] . "\r\n");
fwrite($txtLog, "Device: " . $uaInfo['device'] . "\r\n");
fwrite($txtLog, "VPN/Proxy: " . ($vpnDetected ? 'Yes' : 'No') . "\r\n");
fwrite($txtLog, "Referer: " . ($_SERVER['HTTP_REFERER'] ?? 'Direct') . "\r\n");
fwrite($txtLog, "User Agent: {$userAgent}\r\n");
fwrite($txtLog, "----------------------------------------\r\n\r\n");

fclose($txtLog);

// 4. Also save to master log (for integration with other scripts)
$masterLog = $logDir . '/master_ip_log.json';
$masterData = [];
if (file_exists($masterLog)) {
    $masterData = json_decode(file_get_contents($masterLog), true) ?: [];
}
$masterData[] = $ipData;
if (count($masterData) > 1000) {
    array_shift($masterData); // Keep last 1000 entries
}
file_put_contents($masterLog, json_encode($masterData, JSON_PRETTY_PRINT));

// 5. If this is an AJAX request, return JSON
if (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && 
    strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest') {
    header('Content-Type: application/json');
    echo json_encode([
        'success' => true,
        'message' => 'IP logged successfully',
        'data' => [
            'ip' => $ip,
            'country' => $geoData['country'] ?? 'Unknown',
            'city' => $geoData['city'] ?? 'Unknown',
            'isp' => $geoData['isp'] ?? 'Unknown'
        ]
    ]);
    exit();
}

// 6. Optional: Display info as image (for stealth)
if (isset($_GET['image'])) {
    // Create a 1x1 transparent pixel
    header('Content-Type: image/png');
    echo base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==');
    exit();
}

// 7. Optional: Display info as HTML (for testing)
if (isset($_GET['debug'])) {
    echo "<!DOCTYPE html>";
    echo "<html><head><title>IP Logger Debug</title>";
    echo "<style>body{background:#1a1a1a;color:#fff;font-family:monospace;padding:20px;}";
    echo "pre{background:#333;padding:15px;border-radius:5px;border-left:3px solid #FFD700;}</style>";
    echo "</head><body>";
    echo "<h1>🔍 IP Logger Debug Info</h1>";
    echo "<pre>" . htmlspecialchars(json_encode($ipData, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES)) . "</pre>";
    echo "<p><small>Logged at: $timestamp</small></p>";
    echo "</body></html>";
    exit();
}

// Default behavior: return 1x1 pixel (for tracking pixels)
header('Content-Type: image/png');
echo base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==');
exit();
?>