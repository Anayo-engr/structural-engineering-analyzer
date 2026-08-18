/* =========================================================
   STRUCTURAL ENGINEERING ANALYZER
   FRONTEND JAVASCRIPT
========================================================= */

const API_BASE_URL = "http://127.0.0.1:8000";

/* =========================================================
   DOM ELEMENTS
========================================================= */

const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

const beamForm = document.getElementById("beam-form");
const beamResult = document.getElementById("beam-result");
const beamResultContent = document.getElementById("beam-result-content");

const columnForm = document.getElementById("column-form");
const columnResult = document.getElementById("column-result");
const columnResultContent = document.getElementById("column-result-content");

/* =========================================================
   API STATUS
========================================================= */

async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        const data = await response.json();

        if (data.status === "healthy") {
            statusDot.classList.add("online");
            statusDot.classList.remove("offline");
            statusText.textContent = "API Online";
        } else {
            throw new Error("API unhealthy");
        }

    } catch (error) {
        statusDot.classList.remove("online");
        statusDot.classList.add("offline");
        statusText.textContent = "API Offline";
    }
}

/* =========================================================
   HELPER FUNCTIONS
========================================================= */

function getNumber(id) {
    return Number(document.getElementById(id).value);
}

function formatValue(value) {
    if (typeof value === "number") {
        return Number.isInteger(value)
            ? value
            : Number(value.toFixed(3));
    }

    if (value === null || value === undefined) {
        return "-";
    }

    return value;
}

function formatLabel(key) {
    return key
        .replace(/_/g, " ")
        .replace(/\b\w/g, character => character.toUpperCase());
}

function displayResults(container, result) {
    container.innerHTML = "";

    const content = document.createElement("div");
    content.className = "result-content";

    const grid = document.createElement("div");
    grid.className = "result-grid";

    Object.entries(result).forEach(([key, value]) => {

        if (typeof value === "object" && value !== null) {
            const nested = document.createElement("div");
            nested.className = "result-item";

            nested.innerHTML = `
                <span class="result-label">
                    ${formatLabel(key)}
                </span>
                <span class="result-value">
                    ${escapeHtml(JSON.stringify(value))}
                </span>
            `;

            grid.appendChild(nested);
            return;
        }

        const item = document.createElement("div");
        item.className = "result-item";

        item.innerHTML = `
            <span class="result-label">
                ${formatLabel(key)}
            </span>
            <span class="result-value">
                ${escapeHtml(String(formatValue(value)))}
            </span>
        `;

        grid.appendChild(item);
    });

    content.appendChild(grid);
    container.appendChild(content);
}

function displayError(container, message) {
    container.innerHTML = `
        <div class="result-error">
            <strong>Calculation Error</strong>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

function escapeHtml(value) {
    return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/* =========================================================
   BEAM CALCULATOR
========================================================= */

beamForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const button = beamForm.querySelector(".primary-button");

    button.disabled = true;
    button.textContent = "Calculating...";

    beamResult.classList.remove("hidden");

    beamResultContent.innerHTML = `
        <div class="result-content">
            Calculating beam...
        </div>
    `;

    const requestData = {
        beam_width: getNumber("beam-width"),
        overall_depth: getNumber("overall-depth"),
        concrete_cover: getNumber("concrete-cover"),
        main_bar_diameter: getNumber("main-bar-diameter"),
        dead_load: getNumber("dead-load"),
        live_load: getNumber("live-load"),
        span: getNumber("beam-span"),
        concrete_strength: getNumber("concrete-strength"),
        steel_strength: getNumber("steel-strength"),
        link_diameter: getNumber("link-diameter")
    };

    try {

        const response = await fetch(
            `${API_BASE_URL}/calculate/beam`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail
                    ? JSON.stringify(data.detail)
                    : "Beam calculation failed."
            );
        }

        displayResults(beamResultContent, data);

    } catch (error) {

        displayError(
            beamResultContent,
            error.message || "Unable to connect to the API."
        );

    } finally {

        button.disabled = false;
        button.textContent = "Calculate Beam";
    }
});

/* =========================================================
   COLUMN CALCULATOR
========================================================= */

columnForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const button = columnForm.querySelector(".primary-button");

    button.disabled = true;
    button.textContent = "Calculating...";

    columnResult.classList.remove("hidden");

    columnResultContent.innerHTML = `
        <div class="result-content">
            Calculating column...
        </div>
    `;

    const requestData = {
        column_width: getNumber("column-width"),
        column_depth: getNumber("column-depth"),
        column_height: getNumber("column-height"),
        concrete_cover: getNumber("column-cover"),
        axial_load: getNumber("column-load"),
        concrete_strength: getNumber("column-concrete-strength"),
        steel_strength: getNumber("column-steel-strength")
    };

    try {

        const response = await fetch(
            `${API_BASE_URL}/calculate/column`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail
                    ? JSON.stringify(data.detail)
                    : "Column calculation failed."
            );
        }

        displayResults(columnResultContent, data);

    } catch (error) {

        displayError(
            columnResultContent,
            error.message || "Unable to connect to the API."
        );

    } finally {

        button.disabled = false;
        button.textContent = "Calculate Column";
    }
});

/* =========================================================
   FORM RESET
========================================================= */

beamForm.addEventListener("reset", function () {
    setTimeout(() => {
        beamResult.classList.add("hidden");
        beamResultContent.innerHTML = "";
    }, 0);
});

columnForm.addEventListener("reset", function () {
    setTimeout(() => {
        columnResult.classList.add("hidden");
        columnResultContent.innerHTML = "";
    }, 0);
});

/* =========================================================
   INITIAL API CHECK
========================================================= */

checkApiStatus();
