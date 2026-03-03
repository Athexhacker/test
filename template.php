<?php
// Enhanced Template Redirector
// For security testing purposes only

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Start session for tracking
session_start();

// Include the enhanced IP logger
include 'ip.php';

// Create logs directory if it doesn't exist
$logDir = 'security_test_logs';
if (!file_exists($logDir)) {
    mkdir($logDir, 0777, true);
}

// Create template-specific log directory
$templateDir = $logDir . '/template_redirects';
if (!file_exists($templateDir)) {
    mkdir($templateDir, 0777, true);
}

// Get timestamp
$timestamp = date('Y-m-d H:i:s');

// Get the template name from the filename
$templateName = basename($_SERVER['PHP_SELF'], '.php');

// Generate or retrieve session ID
if (!isset($_SESSION['visitor_id'])) {
    $_SESSION['visitor_id'] = uniqid('visitor_', true);
    $_SESSION['first_visit'] = $timestamp;
    $_SESSION['visit_count'] = 1;
} else {
    $_SESSION['visit_count']++;
    $_SESSION['last_visit'] = $timestamp;
}

// Get all parameters
$getParams = $_GET;
$campaign = $getParams['campaign'] ?? 'default';
$source = $getParams['source'] ?? 'direct';
$medium = $getParams['medium'] ?? 'unknown';
$content = $getParams['content'] ?? null;
$term = $getParams['term'] ?? null;

// Determine redirect path
$baseRedirect = 'forwarding_link/index2.html';
$redirectPath = $baseRedirect;

// Check if we should use a different template based on parameters
if (isset($getParams['template'])) {
    $template = preg_replace('/[^a-zA-Z0-9_-]/', '', $getParams['template']);
    if (file_exists("forwarding_link/{$template}.html") || file_exists("forwarding_link/{$template}.php")) {
        $redirectPath = "forwarding_link/{$template}.html";
    }
}

// Check for mobile version
$isMobile = preg_match('/Mobile|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i', $_SERVER['HTTP_USER_AGENT'] ?? '');
if ($isMobile && isset($getParams['mobile_template'])) {
    $mobileTemplate = preg_replace('/[^a-zA-Z0-9_-]/', '', $getParams['mobile_template']);
    if (file_exists("forwarding_link/mobile/{$mobileTemplate}.html")) {
        $redirectPath = "forwarding_link/mobile/{$mobileTemplate}.html";
    }
}

// Add query parameters to redirect if needed
if (!empty($getParams) && !isset($getParams['no_track'])) {
    $queryParams = [];
    
    // Preserve important tracking parameters
    $preserveParams = ['campaign', 'source', 'medium', 'content', 'term', 'ref', 'visitor_id'];
    foreach ($preserveParams as $param) {
        if (isset($getParams[$param])) {
            $queryParams[$param] = $getParams[$param];
        }
    }
    
    // Add visitor ID for tracking
    $queryParams['visitor'] = $_SESSION['visitor_id'];
    $queryParams['template'] = $templateName;
    
    // Build query string
    if (!empty($queryParams)) {
        $separator = (strpos($redirectPath, '?') !== false) ? '&' : '?';
        $redirectPath .= $separator . http_build_query($queryParams);
    }
}

// Comprehensive logging
$logData = [
    'timestamp' => $timestamp,
    'template_name' => $templateName,
    'visitor_id' => $_SESSION['visitor_id'],
    'session_id' => session_id(),
    'visit_count' => $_SESSION['visit_count'],
    'ip' => $_SERVER['REMOTE_ADDR'],
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown',
    'is_mobile' => $isMobile,
    'campaign' => $campaign,
    'source' => $source,
    'medium' => $medium,
    'content' => $content,
    'term' => $term,
    'all_params' => $getParams,
    'redirect_to' => $redirectPath,
    'base_redirect' => $baseRedirect,
    'referrer' => $_SERVER['HTTP_REFERER'] ?? 'Direct',
    'request_uri' => $_SERVER['REQUEST_URI'],
    'query_string' => $_SERVER['QUERY_STRING'] ?? ''
];

// 1. Save to template-specific log
$templateLogFile = $templateDir . '/' . $templateName . '_' . date('Y-m-d') . '.log';
file_put_contents($templateLogFile, json_encode($logData) . "\n", FILE_APPEND);

// 2. Save to campaign-specific log
if ($campaign != 'default') {
    $campaignDir = $logDir . '/campaigns';
    if (!file_exists($campaignDir)) {
        mkdir($campaignDir, 0777, true);
    }
    $campaignFile = $campaignDir . '/' . preg_replace('/[^a-zA-Z0-9_-]/', '', $campaign) . '_' . date('Y-m-d') . '.log';
    file_put_contents($campaignFile, json_encode($logData) . "\n", FILE_APPEND);
}

// 3. Save to daily JSON for analysis
$dailyDir = $logDir . '/template_analytics/' . date('Y-m-d');
if (!file_exists($dailyDir)) {
    mkdir($dailyDir, 0777, true);
}

$hourlyFile = $dailyDir . '/hour_' . date('H') . '.json';
$hourlyData = [];
if (file_exists($hourlyFile)) {
    $hourlyData = json_decode(file_get_contents($hourlyFile), true) ?: [];
}
$hourlyData[] = $logData;
file_put_contents($hourlyFile, json_encode($hourlyData, JSON_PRETTY_PRINT));

// 4. Update analytics summary
updateAnalytics($logDir, $templateName, $campaign, $source, $isMobile);

// Store in session for later use
if (!isset($_SESSION['templates_visited'])) {
    $_SESSION['templates_visited'] = [];
}
$_SESSION['templates_visited'][] = [
    'template' => $templateName,
    'timestamp' => $timestamp,
    'redirect_to' => $redirectPath
];

// Optional: Add delay for tracking (useful for conversion tracking)
if (isset($getParams['delay'])) {
    $delay = intval($getParams['delay']);
    if ($delay > 0 && $delay <= 5) { // Max 5 seconds
        sleep($delay);
    }
}

// Optional: Set cookies for tracking
setcookie('last_template', $templateName, time() + 86400, '/');
setcookie('last_campaign', $campaign, time() + 86400, '/');
setcookie('visitor_id', $_SESSION['visitor_id'], time() + (86400 * 30), '/');

// Log the redirect
$redirectLog = $logDir . '/all_redirects.log';
file_put_contents($redirectLog, json_encode([
    'timestamp' => $timestamp,
    'visitor_id' => $_SESSION['visitor_id'],
    'template' => $templateName,
    'from' => 'template.php',
    'to' => $redirectPath,
    'campaign' => $campaign
]) . "\n", FILE_APPEND);

// Perform the redirect
header('Location: ' . $redirectPath);

// Optional: If this is an AJAX request, return JSON instead
if (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && 
    strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest') {
    header('Content-Type: application/json');
    echo json_encode([
        'success' => true,
        'redirect' => $redirectPath,
        'visitor_id' => $_SESSION['visitor_id'],
        'template' => $templateName,
        'campaign' => $campaign
    ]);
    exit;
}

// Exit to ensure no further code execution
exit;

/**
 * Update analytics summary
 */
function updateAnalytics($logDir, $templateName, $campaign, $source, $isMobile) {
    $analyticsFile = $logDir . '/template_analytics/summary_' . date('Y-m-d') . '.json';
    
    $analytics = [];
    if (file_exists($analyticsFile)) {
        $analytics = json_decode(file_get_contents($analyticsFile), true);
    }
    
    // Initialize counters
    if (!isset($analytics[$templateName])) {
        $analytics[$templateName] = [
            'total' => 0,
            'campaigns' => [],
            'sources' => [],
            'mobile' => 0,
            'desktop' => 0,
            'hourly' => array_fill(0, 24, 0)
        ];
    }
    
    // Update counters
    $analytics[$templateName]['total']++;
    $analytics[$templateName]['campaigns'][$campaign] = ($analytics[$templateName]['campaigns'][$campaign] ?? 0) + 1;
    $analytics[$templateName]['sources'][$source] = ($analytics[$templateName]['sources'][$source] ?? 0) + 1;
    $analytics[$templateName][$isMobile ? 'mobile' : 'desktop']++;
    $analytics[$templateName]['hourly'][intval(date('H'))]++;
    
    file_put_contents($analyticsFile, json_encode($analytics, JSON_PRETTY_PRINT));
}
?>