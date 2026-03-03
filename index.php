<?php
// Enhanced Main Entry Point
// For security testing purposes only

// Enable error reporting for debugging (disable in production)
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

// Get timestamp
$timestamp = date('Y-m-d H:i:s');

// Generate or retrieve session ID
if (!isset($_SESSION['visitor_id'])) {
    $_SESSION['visitor_id'] = uniqid('visitor_', true);
    $_SESSION['first_visit'] = $timestamp;
    $_SESSION['visit_count'] = 1;
} else {
    $_SESSION['visit_count']++;
    $_SESSION['last_visit'] = $timestamp;
}

// Get referrer information
$referrer = $_SERVER['HTTP_REFERER'] ?? 'Direct';
$source = 'Unknown';

// Check where they came from
if (strpos($referrer, 'google.') !== false) {
    $source = 'Google Search';
} elseif (strpos($referrer, 'facebook.') !== false) {
    $source = 'Facebook';
} elseif (strpos($referrer, 'twitter.') !== false || strpos($referrer, 'x.com') !== false) {
    $source = 'Twitter/X';
} elseif (strpos($referrer, 'instagram.') !== false) {
    $source = 'Instagram';
} elseif (strpos($referrer, 'tiktok.') !== false) {
    $source = 'TikTok';
} elseif (strpos($referrer, 'youtube.') !== false) {
    $source = 'YouTube';
} elseif (strpos($referrer, 'bing.') !== false) {
    $source = 'Bing';
} elseif (strpos($referrer, 'yahoo.') !== false) {
    $source = 'Yahoo';
} elseif (strpos($referrer, 'duckduckgo.') !== false) {
    $source = 'DuckDuckGo';
} elseif (!empty($referrer) && $referrer != 'Direct') {
    $source = 'Other Website';
}

// Check for campaign parameters (UTM tracking)
$utm_source = $_GET['utm_source'] ?? null;
$utm_medium = $_GET['utm_medium'] ?? null;
$utm_campaign = $_GET['utm_campaign'] ?? null;
$utm_content = $_GET['utm_content'] ?? null;
$utm_term = $_GET['utm_term'] ?? null;

// Check for other tracking parameters
$ref = $_GET['ref'] ?? null;
$source_param = $_GET['source'] ?? null;
$campaign = $_GET['campaign'] ?? null;

// Log the visit in master log
$visitLog = $logDir . '/visits.log';
$visitData = [
    'timestamp' => $timestamp,
    'visitor_id' => $_SESSION['visitor_id'],
    'session_id' => session_id(),
    'visit_count' => $_SESSION['visit_count'],
    'ip' => $_SERVER['REMOTE_ADDR'],
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown',
    'referrer' => $referrer,
    'source' => $source,
    'landing_page' => $_SERVER['REQUEST_URI'],
    'query_string' => $_SERVER['QUERY_STRING'] ?? '',
    'utm' => [
        'source' => $utm_source,
        'medium' => $utm_medium,
        'campaign' => $utm_campaign,
        'content' => $utm_content,
        'term' => $utm_term
    ],
    'tracking_params' => [
        'ref' => $ref,
        'source' => $source_param,
        'campaign' => $campaign
    ],
    'method' => $_SERVER['REQUEST_METHOD'],
    'protocol' => $_SERVER['SERVER_PROTOCOL'],
    'port' => $_SERVER['SERVER_PORT']
];

// Append to visit log
file_put_contents($visitLog, json_encode($visitData) . "\n", FILE_APPEND);

// Also save to daily JSON file
$dailyDir = $logDir . '/visits/' . date('Y-m-d');
if (!file_exists($dailyDir)) {
    mkdir($dailyDir, 0777, true);
}

$dailyFile = $dailyDir . '/visits_' . date('Y-m-d_H') . '.json';
$dailyVisits = [];
if (file_exists($dailyFile)) {
    $dailyVisits = json_decode(file_get_contents($dailyFile), true) ?: [];
}
$dailyVisits[] = $visitData;
file_put_contents($dailyFile, json_encode($dailyVisits, JSON_PRETTY_PRINT));

// Check for mobile vs desktop
$isMobile = preg_match('/Mobile|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i', $_SERVER['HTTP_USER_AGENT'] ?? '');

// Store in session for later use
$_SESSION['visitor_data'] = [
    'first_visit' => $_SESSION['first_visit'],
    'visit_count' => $_SESSION['visit_count'],
    'source' => $source,
    'is_mobile' => $isMobile,
    'utm' => [
        'source' => $utm_source,
        'medium' => $utm_medium,
        'campaign' => $utm_campaign
    ]
];

// Optional: Set a cookie for tracking
setcookie('visitor_id', $_SESSION['visitor_id'], time() + (86400 * 30), '/'); // 30 days
setcookie('first_visit', $_SESSION['first_visit'], time() + (86400 * 30), '/');

// Determine which page to redirect to
$redirectTarget = '/index2.html'; // Default

// Check for A/B testing or different landing pages
if (isset($_GET['page'])) {
    // Allow override via URL parameter (for testing)
    $page = preg_replace('/[^a-zA-Z0-9_-]/', '', $_GET['page']);
    if (file_exists($page . '.html') || file_exists($page . '.php')) {
        $redirectTarget = '/' . $page . '.html';
    }
} elseif (isset($_SESSION['visit_count']) && $_SESSION['visit_count'] > 1) {
    // Returning visitor - maybe show a different page
    // You could redirect returning visitors to a special page
    // $redirectTarget = '/returning.html';
}

// Optional: Check if they came from a specific source and redirect accordingly
if ($source == 'Facebook' && $isMobile) {
    // Mobile users from Facebook
    // $redirectTarget = '/fb_mobile.html';
} elseif ($source == 'Google Search' && isset($_GET['q'])) {
    // Search traffic with keyword
    // Log the search keyword
    $searchQuery = $_GET['q'] ?? '';
    file_put_contents($logDir . '/search_keywords.log', date('Y-m-d H:i:s') . " - {$searchQuery}\n", FILE_APPEND);
}

// Optional: Add delay before redirect (to ensure IP logging completes)
// usleep(100000); // 0.1 second delay

// Optional: Log redirect
$redirectLog = $logDir . '/redirects.log';
file_put_contents($redirectLog, json_encode([
    'timestamp' => $timestamp,
    'visitor_id' => $_SESSION['visitor_id'],
    'redirect_to' => $redirectTarget,
    'from' => $_SERVER['REQUEST_URI']
]) . "\n", FILE_APPEND);

// Perform the redirect
header('Location: ' . $redirectTarget);

// Add tracking parameters to redirect URL if needed
if (isset($_GET['track']) && $_GET['track'] == '1') {
    $separator = (strpos($redirectTarget, '?') !== false) ? '&' : '?';
    $redirectTarget .= $separator . 'visitor=' . urlencode($_SESSION['visitor_id']);
    header('Location: ' . $redirectTarget);
}

// Exit to ensure no further code execution
exit;
?>