document.getElementById("scanBtn").onclick = async () => {
    const status = document.getElementById("status");
    const btn = document.getElementById("scanBtn");

    status.innerHTML = "Analyzing message...";
    btn.disabled = true;
    btn.style.opacity = "0.5";

    try {
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tabs[0]) throw new Error("No active tab");

        chrome.tabs.sendMessage(tabs[0].id, { action: "scanManual" }, (response) => {
            btn.disabled = false;
            btn.style.opacity = "1";

            if (chrome.runtime.lastError) {
                status.innerHTML = "<span style='color: #dc2626;'><b>CRITICAL:</b> Page needs refresh (F5) to link with ScamSense.</span>";
                return;
            }

            if (!response) {
                status.innerHTML = "<span style='color: #dc2626;'><b>Error:</b> No response from page.</span>";
                return;
            }

            switch (response.status) {
                case "alert_shown":
                    status.innerHTML = "<span style='color: #dc2626;'><b>⚠️ THREAT DETECTED!</b><br>Check bottom right for details.</span>";
                    break;
                case "low_risk":
                    let title = response.level.toUpperCase();
                    let color = "#16a34a"; // Green
                    if (response.category === "Conversational Message") {
                        title = "CONVERSATIONAL";
                        color = "#059669"; // Emerald Green
                    }

                    status.innerHTML = `<span style="color: ${color};"><b>✅ ${title}</b></span><br>
                                       <span style="font-size: 11px;">Category: ${response.category}</span><br>
                                       Risk Score: ${response.risk}%`;
                    break;
                case "no_content":
                    const url = tabs[0].url || "";
                    let msg = "Please select an email first.";
                    if (url.includes("web.whatsapp.com") || url.includes("web.telegram.org")) {
                        msg = "Please open a specific chat to scan.";
                    }
                    status.innerHTML = `<span style='color: #ea580c;'><b>⚠️ NO CONTENT</b><br>${msg}</span>`;
                    break;
                case "error":
                    status.innerHTML = "<span style='color: #dc2626;'><b>❌ SYSTEM ERROR</b><br>" + response.message + "</span>";
                    break;
                default:
                    status.innerHTML = "Unknown status: " + response.status;
            }
        });
    } catch (err) {
        btn.disabled = false;
        btn.style.opacity = "1";
        status.innerText = "Error: " + err.message;
    }
};
