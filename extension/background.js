/**
 * ScamSense Background Service Worker
 * Handles API calls to bypass Content Security Policy (CSP) restrictions.
 */

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "analyzeContent") {
        console.log("Background: Received analysis request");

        fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender: request.data.sender || "Unknown",
                content: request.data.content
            })
        })
            .then(response => {
                if (!response.ok) throw new Error("Backend reachable but returned error " + response.status);
                return response.json();
            })
            .then(result => {
                console.log("Background: Analysis success", result);
                sendResponse({ status: "success", result: result });
            })
            .catch(error => {
                console.error("Background: Fetch error", error);
                sendResponse({ status: "error", message: error.message });
            });

        return true; // Keep channel open for async response
    }
});
