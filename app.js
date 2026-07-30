const emotions = {
    joy: {
        icon: "✦",
        color: "#c9ef82",
        description: "A bright, uplifting emotional state."
    },
    love: {
        icon: "♡",
        color: "#f49bb6",
        description: "Warmth, connection, and affection are present."
    },
    anger: {
        icon: "✹",
        color: "#ff876b",
        description: "A strong signal of frustration or opposition."
    },
    fear: {
        icon: "◒",
        color: "#b6a2ff",
        description: "Concern, uncertainty, or apprehension is present."
    },
    sadness: {
        icon: "☾",
        color: "#82baf0",
        description: "A quieter, reflective emotional state."
    },
    surprise: {
        icon: "✺",
        color: "#f7cd71",
        description: "An unexpected turn has caught attention."
    }
};

const labels = [
    "Sadness",
    "Joy",
    "Love",
    "Anger",
    "Fear",
    "Surprise"
];

const apiOrder = [
    "sadness",
    "joy",
    "love",
    "anger",
    "fear",
    "surprise"
];

const input = document.querySelector("#emotionInput");
const count = document.querySelector("#charCount");
const spectrum = document.querySelector("#spectrum");
const button = document.querySelector("#analyzeButton");

function render(result) {

    const emotion = result.emotion.toLowerCase();
    const data = emotions[emotion];

    document.querySelector("#emotionIcon").textContent = data.icon;
    document.querySelector("#emotionIcon").style.background =
        data.color + "33";
    document.querySelector("#emotionIcon").style.color =
        data.color;

    document.querySelector("#primaryEmotion").textContent =
        emotion.charAt(0).toUpperCase() + emotion.slice(1);

    document.querySelector("#emotionDescription").textContent =
        data.description;

    document.querySelector("#confidence").textContent =
        result.confidence.toFixed(2) + "%";

    if (result.confidence >= 90)
        document.querySelector("#certainty").textContent =
            "Very High certainty";
    else if (result.confidence >= 75)
        document.querySelector("#certainty").textContent =
            "High certainty";
    else if (result.confidence >= 60)
        document.querySelector("#certainty").textContent =
            "Moderate certainty";
    else
        document.querySelector("#certainty").textContent =
            "Low certainty";

    spectrum.innerHTML = "";

    apiOrder.forEach((emotionName, index) => {

        const score = result.scores[emotionName];

        const row = document.createElement("div");
        row.className = "emotion-bar";

        row.innerHTML = `
            <span>${labels[index]}</span>

            <div class="bar-track">
                <div
                    class="bar-fill"
                    style="
                        width:0;
                        background:${
                            emotionName === emotion
                                ? data.color
                                : "#7c7891"
                        };
                    ">
                </div>
            </div>

            <b>${score.toFixed(2)}%</b>
        `;

        spectrum.appendChild(row);

        requestAnimationFrame(() => {
            row.querySelector(".bar-fill").style.width =
                score + "%";
        });

    });

}

async function analyzeText() {

    const text = input.value.trim();

    if (!text)
        return;

    button.disabled = true;
    button.innerHTML = "Reading <span>⌁</span>";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            }
        );

        if (!response.ok)
            throw new Error("Backend returned an error.");

        const result = await response.json();

        render(result);

    }
    catch (err) {

        alert(
            "Unable to connect to the Emotion Signal backend.\n\n" +
            "Make sure app.py is running."
        );

        console.error(err);

    }
    finally {

        button.disabled = false;
        button.innerHTML = "Read emotion <span>→</span>";

    }

}

button.addEventListener(
    "click",
    analyzeText
);

input.addEventListener(
    "input",
    () => {
        count.textContent =
            `${input.value.length} / 500`;
    }
);

document.querySelectorAll("[data-example]").forEach(button => {

    button.addEventListener("click", () => {

        input.value = button.dataset.example;

        input.dispatchEvent(new Event("input"));

        input.focus();

    });

});

const modal = document.querySelector("#modal");
const loginButton = document.querySelector("#loginButton");

if (modal && loginButton) {

    loginButton.onclick = () =>
        modal.classList.add("open");

    document.querySelector("#closeModal").onclick = () =>
        modal.classList.remove("open");

    modal.onclick = e => {

        if (e.target === modal)
            modal.classList.remove("open");

    };

    document.querySelector("#loginForm").onsubmit = e => {

        e.preventDefault();

        modal.classList.remove("open");

        const toast = document.querySelector("#toast");

        toast.textContent =
            "Welcome to your Emotion Signal workspace";

        toast.classList.add("show");

        setTimeout(() => {

            toast.classList.remove("show");

        }, 3000);

    };

}

count.textContent =
    `${input.value.length} / 500`;

render({
    emotion: "joy",
    confidence: 96.8,
    scores: {
        sadness: 1.2,
        joy: 96.8,
        love: 24.5,
        anger: 0.8,
        fear: 1.1,
        surprise: 8.4
    }
});
