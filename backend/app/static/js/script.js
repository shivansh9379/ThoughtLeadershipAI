const input = document.querySelector("#message");
const button = document.querySelector("#send-btn");
const messages = document.querySelector(".messages");

const topicInput = document.querySelector("#topic-input");
const audienceInput = document.querySelector("#audience-input");
const generateButton = document.querySelector("#generate-btn");


/* =========================================
   MARKDOWN
========================================= */

marked.setOptions({
    breaks: true,
    gfm: true
});


/* =========================================
   SCROLL
========================================= */

function scrollBottom() {

    messages.scrollTop = messages.scrollHeight;

}


/* =========================================
   ESCAPE HTML
========================================= */

function escapeHTML(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

}


/* =========================================
   ADD USER MESSAGE
========================================= */

function addUserMessage(text) {

    messages.insertAdjacentHTML(
        "beforeend",
        `
        <div class="user-message">
            ${escapeHTML(text)}
        </div>
        `
    );

    scrollBottom();

}


/* =========================================
   ADD AI MESSAGE
========================================= */

function addAIMessage(text) {

    const formatted = marked.parse(text);

    messages.insertAdjacentHTML(
        "beforeend",
        `
        <div class="ai-message markdown-body">
            ${formatted}
        </div>
        `
    );

    if (window.hljs) {

        document
            .querySelectorAll("pre code")
            .forEach((block) => {

                hljs.highlightElement(block);

            });

    }

    scrollBottom();

}


/* =========================================
   THINKING
========================================= */

function showThinking(message = "Thinking...") {

    messages.insertAdjacentHTML(
        "beforeend",
        `
        <div class="ai-message" id="thinking">
            <span class="loader"></span>
            ${message}
        </div>
        `
    );

    scrollBottom();

}


function removeThinking() {

    const thinking = document.querySelector("#thinking");

    if (thinking) {
        thinking.remove();
    }

}


/* =========================================
   NORMAL CHAT
========================================= */

async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    addUserMessage(text);

    input.value = "";

    input.disabled = true;
    button.disabled = true;

    showThinking("Thinking...");

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data = await response.json();

        removeThinking();

        addAIMessage(
            data.reply || "Sorry, I couldn't generate a response."
        );


    } catch (error) {

        removeThinking();

        addAIMessage(
            "❌ Something went wrong. Please try again."
        );

        console.error(error);

    }


    input.disabled = false;
    button.disabled = false;

    input.focus();

    scrollBottom();

}


/* =========================================
   GENERATE THOUGHT LEADERSHIP
========================================= */

async function generateArticle() {

    const topic = topicInput.value.trim();
    const audience = audienceInput.value.trim();


    if (!topic) {

        alert("Please enter a topic.");

        topicInput.focus();

        return;

    }


    if (!audience) {

        alert("Please enter the target audience.");

        audienceInput.focus();

        return;

    }


    generateButton.disabled = true;

    topicInput.disabled = true;
    audienceInput.disabled = true;


    showThinking(
        "🔎 Researching → 💡 Finding insights → ✍️ Writing → 🔍 Reviewing → ✨ Humanizing..."
    );


    try {

        const response = await fetch(
            "/generate-content",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    topics: topic,

                    audience: audience

                })

            }
        );


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data = await response.json();


        removeThinking();


        if (!data.success) {

            addAIMessage(
                `❌ **Pipeline failed**\n\n` +
                `Stage: \`${data.stage || "unknown"}\`\n\n` +
                `${data.error || "Unknown error."}`
            );

            return;

        }


        const finalArticle = data.final_article;


        if (!finalArticle) {

            addAIMessage(
                "❌ The pipeline completed but no final article was returned."
            );

            return;

        }


        let output = "";


        if (finalArticle.title) {

            output += `# ${finalArticle.title}\n\n`;

        }


        if (finalArticle.subtitle) {

            output += `*${finalArticle.subtitle}*\n\n`;

        }


        output += finalArticle.article || "";


        if (
            finalArticle.key_takeaways &&
            finalArticle.key_takeaways.length
        ) {

            output += "\n\n## Key Takeaways\n\n";

            finalArticle.key_takeaways.forEach(
                (item) => {

                    output += `- ${item}\n`;

                }
            );

        }


        if (finalArticle.recommended_cta) {

            output +=
                "\n\n## Recommended CTA\n\n" +
                finalArticle.recommended_cta;

        }


        addAIMessage(output);


    } catch (error) {

        removeThinking();

        addAIMessage(
            `❌ **Generation failed**\n\n${error.message}`
        );

        console.error(error);

    }


    generateButton.disabled = false;

    topicInput.disabled = false;
    audienceInput.disabled = false;

}


/* =========================================
   BUTTON EVENTS
========================================= */

button.addEventListener(
    "click",
    sendMessage
);


generateButton.addEventListener(
    "click",
    generateArticle
);


/* =========================================
   ENTER KEY — CHAT
========================================= */

input.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


/* =========================================
   ENTER KEY — TOPIC
========================================= */

topicInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            generateArticle();

        }

    }
);


/* =========================================
   ENTER KEY — AUDIENCE
========================================= */

audienceInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            generateArticle();

        }

    }
);