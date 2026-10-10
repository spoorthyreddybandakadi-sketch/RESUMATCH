let resumeText = "";

async function uploadResume(file) {
    if (!file) {
        return;
    }

    const uploadStatus = document.getElementById("uploadStatus");
    uploadStatus.textContent = "Uploading resume...";

    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Resume upload failed.");
        }

        resumeText = result.resume_text || result.text || "";

        uploadStatus.textContent =
            "✓ Resume uploaded: " + file.name;

    } catch (error) {
        console.error("Upload error:", error);
        uploadStatus.textContent = "Resume upload failed.";
        alert("Could not upload resume. Check the Terminal for errors.");
    }
}


async function analyzeResume() {
    const jobDescription =
        document.getElementById("jobDescription").value.trim();

    if (!resumeText) {
        alert("Please upload your PDF resume first.");
        return;
    }

    if (!jobDescription) {
        alert("Please enter a job description.");
        return;
    }

    const analyzeButton = document.querySelector(".analyze-btn");
    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    try {
        const response = await fetch("/match", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resume_text: resumeText,
                job_description: jobDescription
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Analysis failed.");
        }

        // Display match percentage
        const score = Number(result.match_score);

        document.getElementById("matchScore").textContent =
            Number.isFinite(score) ? score.toFixed(2) + "%" : "N/A";

        // Safely handle skills returned by the backend
        const matchingSkills = Array.isArray(result.matching_skills)
            ? result.matching_skills
            : [];

        const missingSkills = Array.isArray(result.missing_skills)
            ? result.missing_skills
            : [];

        document.getElementById("matchingSkills").textContent =
            matchingSkills.length > 0
                ? matchingSkills.join(", ")
                : "No matching skills found.";

        document.getElementById("missingSkills").textContent =
            missingSkills.length > 0
                ? missingSkills.join(", ")
                : "No missing skills found.";
        const suggestions = Array.isArray(result.suggestions)
    ? result.suggestions
    : [];

const suggestionsList = document.getElementById("suggestionsList");

suggestionsList.replaceChildren();

if (suggestions.length > 0) {
    suggestions.forEach(function (item) {
        const li = document.createElement("li");
        li.textContent = item;
        suggestionsList.appendChild(li);
    });
} else {
    const li = document.createElement("li");
    li.textContent = "No suggestions available.";
    suggestionsList.appendChild(li);
}        

        // Show results
        document.getElementById("resultsSection").style.display = "block";

        document.getElementById("resultsSection").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        console.error("Analysis error:", error);
        alert("Analysis failed. Check the browser console for details.");
    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Resume →";
    }
}