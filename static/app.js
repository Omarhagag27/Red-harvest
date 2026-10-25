
const form = document.getElementById("download-form");
const mediaType = document.getElementById("media-type");
const qualityField = document.getElementById("quality-field");

const downloadButton = document.getElementById("download-button");
const buttonText = document.getElementById("button-text");
const spinner = document.getElementById("spinner");
const statusBox = document.getElementById("status");

const progressContainer = document.getElementById("progress-container");
const progressLabel = document.getElementById("progress-label");
const progressPercent = document.getElementById("progress-percent");
const progressTrack = document.getElementById("progress-track");
const progressFill = document.getElementById("progress-fill");
const progressDetails = document.getElementById("progress-details");

mediaType.addEventListener("change", () => {
    qualityField.classList.toggle(
        "hidden",
        mediaType.value === "audio"
    );
});

function showStatus(message, type) {
    statusBox.textContent = message;
    statusBox.className = `status ${type}`;
}

function setLoading(loading) {
    downloadButton.disabled = loading;
    spinner.classList.toggle("hidden", !loading);
    buttonText.textContent = loading ? "Downloading..." : "Download";
}

function resetProgress() {
    progressContainer.classList.remove("hidden");
    progressFill.style.width = "0%";
    progressFill.classList.remove("complete");
    progressPercent.textContent = "0%";
    progressLabel.textContent = "Starting download...";
    progressDetails.textContent = "";
    progressTrack.setAttribute("aria-valuenow", "0");
}

function updateProgress(job) {
    const percent = Number.isFinite(job.percent)
        ? Math.max(0, Math.min(100, job.percent))
        : null;

    if (percent !== null) {
        progressFill.style.width = `${percent}%`;
        progressPercent.textContent = `${Math.round(percent)}%`;
        progressTrack.setAttribute("aria-valuenow", String(Math.round(percent)));
    } else {
        progressPercent.textContent = "";
    }

    const labels = {
        starting: "Preparing download...",
        downloading: "Downloading...",
        processing: "Processing media...",
        completed: "Download complete",
        failed: "Download failed"
    };

    progressLabel.textContent =
        labels[job.status] || "Working...";

    const details = [];

    if (job.filename) {
        details.push(job.filename);
    }

    if (typeof job.speed === "number") {
        details.push(`${(job.speed / 1024 / 1024).toFixed(2)} MB/s`);
    }

    if (typeof job.eta === "number" && job.status === "downloading") {
        details.push(`About ${job.eta}s remaining`);
    }

    progressDetails.textContent = details.join(" · ");

    if (job.status === "completed") {
        progressFill.style.width = "100%";
        progressPercent.textContent = "100%";
        progressTrack.setAttribute("aria-valuenow", "100");
        progressFill.classList.add("complete");
    }
}

async function pollProgress(jobId) {
    while (true) {
        const response = await fetch(
            `/progress/${encodeURIComponent(jobId)}`
        );

        const job = await response.json();

        if (!response.ok) {
            throw new Error(job.error || "Could not retrieve progress.");
        }

        updateProgress(job);

        if (job.status === "completed") {
            const result = job.result || {};
            showStatus(
                `Download completed: ${result.title || "Media"}\n` +
                `Saved to: ${result.download_dir || "Download directory"}`,
                "success"
            );
            return;
        }

        if (job.status === "failed") {
            throw new Error(job.error || "Download failed.");
        }

        // Wait one second before checking again.
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
        url: document.getElementById("url").value.trim(),
        media_type: mediaType.value,
        quality: document.getElementById("quality").value,
        download_dir:
            document.getElementById("download-dir").value.trim() || null,
        playlist: document.getElementById("playlist").checked
    };

    if (!data.url) {
        showStatus("Please enter a media URL.", "error");
        return;
    }

    setLoading(true);
    resetProgress();
    showStatus("Starting download...", "loading");

    try {
        const response = await fetch("/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not start download.");
        }

        await pollProgress(result.job_id);

    } catch (error) {
        progressLabel.textContent = "Download stopped";
        showStatus(error.message || "An unexpected error occurred.", "error");

    } finally {
        setLoading(false);
    }
});
