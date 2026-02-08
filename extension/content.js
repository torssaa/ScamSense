/**
 * ScamSense Content Script (Final Robust Version)
 * Implements automatic "Blind Extraction" for Outlook and Gmail.
 * No user highlighting required.
 */

console.log("ScamSense: Robust Content Script Loaded");

async function getExtractionData() {
    const host = window.location.hostname;
    let data = { sender: "Detected Message", content: "" };

    // Platform-specific targeted extraction
    // Platform-specific targeted extraction
    if (host.includes("web.whatsapp.com")) {
        const activeChat = document.querySelector("#main");
        if (activeChat) {
            // Get all message rows (in and out)
            const rows = activeChat.querySelectorAll("div[role='row']");

            // Extract text from the last 15 messages
            data.content = Array.from(rows).slice(-15).map(row => {
                const messageNode = row.querySelector(".message-in, .message-out");
                if (!messageNode) return "";

                // Try selectable text first (most reliable for content)
                const copyable = messageNode.querySelector(".copyable-text span");
                if (copyable) return copyable.innerText;

                // Fallback: Get all text in the bubble (captions, system messages)
                return messageNode.innerText;
            }).filter(t => t && t.trim().length > 0).join("\n");

            const header = document.querySelector("header [title]");
            data.sender = header ? header.title : "WhatsApp Contact";
            return data;
        }
    }

    if (host.includes("web.telegram.org")) {
        // Telegram has two versions (K and A), support both
        const validSelectors = [".Message", ".message", ".bubble"];
        const bubbles = document.querySelectorAll(validSelectors.join(","));

        if (bubbles.length > 0) {
            data.content = Array.from(bubbles).slice(-15).map(b => {
                // Try to find the specific text content div
                const textDiv = b.querySelector(".text-content, .message-text");
                return textDiv ? textDiv.innerText : b.innerText;
            }).filter(t => t && t.trim().length > 0).join("\n");

            // Try multiple header selectors for Telegram K/A
            const header = document.querySelector(".chat-info .title, .chat-title, .top .peer-title");
            data.sender = header ? header.innerText : "Telegram Contact";
            return data;
        }
    }

    const startTime = Date.now();
    console.log("ScamSense: Extraction started...");

    // Recursive search for the largest text block (fallback for Outlook/Gmail)
    function findMainContent(root) {
        let maxText = "";

        // Target areas for Outlook and Gmail
        const targetSelectors = [
            ".allowTextSelection",
            "#readPane_content_container",
            "[role='main']",
            ".a3s",
            ".gs"
        ];

        for (let selector of targetSelectors) {
            const el = root.querySelector(selector);
            if (el && el.innerText.trim().length > maxText.length) {
                maxText = el.innerText.trim();
            }
        }

        return maxText;
    }

    try {
        data.content = findMainContent(document);

        // Try to find sender from common header areas
        const senderSelectors = ["span.gD", "[data-name]", ".C_Oka", ".G3", ".owR", "header [title]", "span[email]"];
        for (let sel of senderSelectors) {
            const el = document.querySelector(sel);
            if (el && el.innerText.trim()) {
                data.sender = el.innerText.trim();
                break;
            }
        }
    } catch (e) {
        console.error("ScamSense: Extraction error", e);
    }

    console.log(`ScamSense: Extraction finished in ${Date.now() - startTime}ms. Content length: ${data.content.length}`);
    return data;
}

function showAlert(result) {
    const existing = document.getElementById("scamsense-alert");
    if (existing) existing.remove();

    const alertDiv = document.createElement("div");
    alertDiv.id = "scamsense-alert";

    // Aggressively protect the alert container from site CSS
    alertDiv.style.cssText = `
        all: initial !important;
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        width: 370px !important;
        max-width: calc(100vw - 40px) !important;
        height: auto !important;
        max-height: calc(100vh - 40px) !important;
        min-height: 100px !important;
        z-index: 2147483647 !important;
        background-color: white !important;
        border-radius: 16px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
        font-family: "Segoe UI", Tahoma, sans-serif !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        animation: scamIn 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) !important;
        box-sizing: border-box !important;
        border: 1px solid #e5e7eb !important;
    `;

    const accent = result.risk_score >= 85 ? '#dc2626' : '#f97316';

    alertDiv.innerHTML = `
        <div style="all: initial; background: ${accent}; color: white; padding: 10px 15px; font-weight: 900; display: flex; justify-content: space-between; align-items: center; letter-spacing: 1px; flex-shrink: 0; position: sticky; top: 0; z-index: 1000; font-family: 'Segoe UI', sans-serif; box-sizing: border-box; width: 100%;">
            <span style="font-size: 13px;">🛡️ SCAMSENSE ALERT</span>
            <button id="scamsense-close-x" style="all: initial; background: none; border: none; color: white; font-size: 28px; cursor: pointer; padding: 5px; line-height: 0.8; display: flex; align-items: center; justify-content: center; min-width: 36px; min-height: 36px; font-weight: bold; font-family: Arial, sans-serif;">&times;</button>
        </div>
        <div style="all: initial; padding: 15px; overflow-y: auto; flex: 1; display: block; font-family: 'Segoe UI', sans-serif; box-sizing: border-box; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase;">Risk Probability</span>
                <span style="font-size: 32px; font-weight: 900; color: ${accent};">${result.risk_score}%</span>
            </div>
            <div style="margin-bottom: 6px; font-size: 14px;"><strong>Type:</strong> ${result.category}</div>
            <div style="margin-bottom: 6px; font-size: 14px;"><strong>Emotion:</strong> ${result.sentiment}</div>
            <div style="height: 1px; background: #e5e7eb; margin: 10px 0;"></div>
            <div id="scamsense-explanation-text" style="background: #f9fafb; padding: 12px; border-radius: 8px; border-left: 5px solid ${accent}; font-size: 13px; color: #374151; line-height: 1.4; margin-bottom: 15px; display: -webkit-box; -webkit-line-clamp: 8; -webkit-box-orient: vertical; overflow: hidden; max-height: 12em; font-family: 'Segoe UI', sans-serif; box-sizing: border-box;">
                ${result.explanation}
            </div>
            <div style="background: #111827; padding: 12px; border-radius: 8px; color: white; font-size: 13px; line-height: 1.4; font-family: 'Segoe UI', sans-serif; box-sizing: border-box;">
                <strong style="color: ${accent}; text-transform: uppercase; font-size: 11px; display: block; margin-bottom: 4px;">Recommended Action:</strong>
                ${result.recommended_action}
            </div>
        </div>
        <style>
            @keyframes scamIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
            #scamsense-alert div::-webkit-scrollbar { width: 8px; }
            #scamsense-alert div::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
            #scamsense-alert div::-webkit-scrollbar-thumb { background: #888; border-radius: 10px; }
            #scamsense-alert div::-webkit-scrollbar-thumb:hover { background: #555; }
        </style>
    `;

    document.body.appendChild(alertDiv);

    // Use a very specific selection to ensure the click works
    const closeBtn = alertDiv.querySelector("#scamsense-close-x");
    if (closeBtn) {
        closeBtn.onclick = (e) => {
            e.stopPropagation();
            alertDiv.remove();
        };
    }

    // Keep it open longer, but focus on the close button
    setTimeout(() => { if (alertDiv.parentNode) alertDiv.remove(); }, 60000);
}

// Manual listener (used by popup)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scanManual") {
        getExtractionData().then(data => {
            if (!data.content || data.content.length < 10) {
                sendResponse({ status: "no_content" });
                return;
            }

            chrome.runtime.sendMessage({ action: "analyzeContent", data: data }, (response) => {
                if (response?.status === "success") {
                    showAlert(response.result);
                    sendResponse({
                        status: response.result.risk_score >= 25 ? "alert_shown" : "low_risk",
                        risk: response.result.risk_score,
                        level: response.result.risk_level,
                        category: response.result.category
                    });
                } else {
                    sendResponse({ status: "error", message: response?.message || "Internal communication error" });
                }
            });
        });
        return true;
    }
});
