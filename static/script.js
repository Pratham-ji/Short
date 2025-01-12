document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const startBtn = document.getElementById("start-btn");
    const loadingDiv = document.querySelector(".loading");
    const dotsDiv = document.getElementById("dots");
    let audioPlayer = new Audio();
    let recordingTimeout;

    if (!startBtn || !loadingDiv || !dotsDiv) {
        console.error("Missing key elements in the DOM.");
        return;
    }

    startBtn.style.width = "300px";
    startBtn.style.height = "300px";
    startBtn.style.borderRadius = "50%";

    dotsDiv.addEventListener("mouseover", () => {
        startBtn.classList.add("show");
    });

    dotsDiv.addEventListener("mouseleave", () => {
        if (loadingDiv.style.display === "none" || !loadingDiv.style.display) {
            startBtn.classList.remove("show");
        }
    });


    const startAssistant = async () => {
        console.log("Start button clicked.");
        loadingDiv.style.display = "flex";
        dotsDiv.style.display = "none";

        // Set timeout to stop recording
        recordingTimeout = setTimeout(() => {
           stopRecording("Recording timed out");
       }, 5000);


        try {
            const response = await fetch("/start_assistant", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

             if (!response.ok) {
                const errorData = await response.json();
                 throw new Error(`Server Error: ${response.status} - ${errorData.response || response.statusText}`);
             }
            const data = await response.json();
            console.log("AI Response:", data.response);

            if (data.audio) {
                audioPlayer.src = "data:audio/mp3;base64," + data.audio;
                await audioPlayer.play();
                console.log("Audio playback started.");
            }
             else {
                 console.warn("No audio received from the assistant.");
                 alert(data.response || "No response received from the assistant.");
             }
        }
         catch (err) {
            console.error("Error:", err.message);
            alert(`An error occurred while processing your request. Please try again. Error Details: ${err.message}`);
          }
        finally {
            clearTimeout(recordingTimeout);
            loadingDiv.style.display = "none";
            dotsDiv.style.display = "flex";
            console.log("UI reset complete.");
        }
    };

       function stopRecording(message) {
          console.log(message);
      }

    startBtn.addEventListener("click", startAssistant);
});
