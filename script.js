const generateBtn = document.getElementById("generateBtn");

generateBtn.addEventListener("click", async () => {
    const promptInput = document.getElementById("prompt").value;
    const languageInput = document.getElementById("language").value;
    const loadingDiv = document.getElementById("loading");
    const audioContainer = document.getElementById("audio-container");
    const audioPlayer = document.getElementById("audioPlayer");
    const textContainer = document.getElementById("translated-text-container");
    const translatedTextEl = document.getElementById("translatedText");

    if (!promptInput.trim()) {
        alert("Enter a prompt first!");
        return;
    }

    // Reset UI for loading state
    generateBtn.disabled = true;
    loadingDiv.style.display = "block";
    audioContainer.style.display = "none";
    textContainer.style.display = "none";
    translatedTextEl.innerText = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: promptInput,
                language: languageInput
            })
        });

        // Parse the response as JSON (it now contains text + audio data)
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Generation failed");
        }

        // 1. Display the translated text
        translatedTextEl.innerText = data.translated_text;
        textContainer.style.display = "block";

        // 2. Play the audio using the base64 string
        audioPlayer.src = "data:audio/mp3;base64," + data.audio_base64;
        audioContainer.style.display = "block";
        loadingDiv.style.display = "none";

    } catch (error) {
        console.error(error);
        alert("Error: " + error.message);
        loadingDiv.style.display = "none";
    }

    generateBtn.disabled = false;
});