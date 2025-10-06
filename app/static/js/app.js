document.addEventListener("DOMContentLoaded", () => {
    const monitoredFoldersList = document.getElementById("monitored-folders-list");
    const folderPathInput = document.getElementById("folder-path");
    const addFolderBtn = document.getElementById("add-folder-btn");
    const scanNowBtn = document.getElementById("scan-now-btn");
    const jobsTableBody = document.querySelector("#jobs-table tbody");
    const logsContainer = document.getElementById("logs-container");
    const whisperModelInput = document.getElementById("whisper-model");
    const saveSettingsBtn = document.getElementById("save-settings-btn");

    const API_BASE_URL = "/api";

    // Fetch and display monitored folders
    async function fetchMonitoredFolders() {
        try {
            const response = await fetch(`${API_BASE_URL}/folders/`);
            const folders = await response.json();
            monitoredFoldersList.innerHTML = folders.map(f => `
                <div class="folder-item">
                    <input type="checkbox" id="folder-${f.id}" data-folder-id="${f.id}" ${f.monitoring_enabled ? "checked" : ""}>
                    <label for="folder-${f.id}">${f.path}</label>
                </div>
            `).join("");

            // Add event listeners to the new checkboxes
            document.querySelectorAll(".folder-item input[type='checkbox']").forEach(checkbox => {
                checkbox.addEventListener("change", async (event) => {
                    const folderId = event.target.dataset.folderId;
                    const monitoring_enabled = event.target.checked;
                    try {
                        await fetch(`${API_BASE_URL}/folders/${folderId}`, {
                            method: "PUT",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ monitoring_enabled }),
                        });
                    } catch (error) {
                        console.error("Error updating folder:", error);
                    }
                });
            });
        } catch (error) {
            console.error("Error fetching monitored folders:", error);
        }
    }

    // Add a new monitored folder
    addFolderBtn.addEventListener("click", async () => {
        const path = folderPathInput.value.trim();
        if (path) {
            try {
                await fetch(`${API_BASE_URL}/folders/`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ path }),
                });
                folderPathInput.value = "";
                fetchMonitoredFolders();
            } catch (error) {
                console.error("Error adding folder:", error);
            }
        }
    });

    // Fetch and display transcription jobs
    async function fetchJobs() {
        try {
            // This endpoint does not exist yet, will create it later
            const response = await fetch(`${API_BASE_URL}/jobs/`);
            const jobs = await response.json();
            jobsTableBody.innerHTML = jobs.map(job => `
                <tr>
                    <td>${job.file_name}</td>
                    <td>${job.file_path}</td>
                    <td>${job.status}</td>
                    <td>${new Date(job.date_added).toLocaleString()}</td>
                    <td>${job.date_completed ? new Date(job.date_completed).toLocaleString() : ""}</td>
                    <td>${job.error_message || ""}</td>
                </tr>
            `).join("");
        } catch (error) {
            console.error("Error fetching jobs:", error);
        }
    }

    // Trigger a scan
    scanNowBtn.addEventListener("click", async () => {
        try {
            await fetch(`${API_BASE_URL}/scan/`, { method: "POST" });
            fetchJobs(); // Refresh jobs after scan
        } catch (error) {
            console.error("Error triggering scan:", error);
        }
    });

    // Fetch and display logs
    async function fetchLogs() {
        try {
            const response = await fetch(`${API_BASE_URL}/logs/`);
            const logs = await response.json();
            logsContainer.innerHTML = logs.map(log => `
                <div>[${new Date(log.timestamp).toLocaleString()}] [${log.level}] ${log.message}</div>
            `).join("");
        } catch (error) {
            console.error("Error fetching logs:", error);
        }
    }

    // Fetch and display settings
    async function fetchSettings() {
        try {
            const response = await fetch(`${API_BASE_URL}/settings/`);
            const settings = await response.json();
            whisperModelInput.value = settings.whisper_model;
        } catch (error) {
            console.error("Error fetching settings:", error);
        }
    }

    // Save settings
    saveSettingsBtn.addEventListener("click", async () => {
        const whisper_model = whisperModelInput.value.trim();
        if (whisper_model) {
            try {
                await fetch(`${API_BASE_URL}/settings/`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ whisper_model }),
                });
                alert("Settings saved successfully!");
            } catch (error) {
                console.error("Error saving settings:", error);
                alert("Failed to save settings.");
            }
        }
    });

    // Initial data load
    fetchMonitoredFolders();
    fetchJobs();
    fetchLogs();
    fetchSettings();
    setInterval(fetchJobs, 5000); // Poll for job updates every 5 seconds
    setInterval(fetchLogs, 5000); // Poll for log updates every 5 seconds
});