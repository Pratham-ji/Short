document.addEventListener("DOMContentLoaded", () => {
   const startBtn = document.getElementById("start-btn");
   const loadingDiv = document.querySelector(".loading");
   const dotsDiv = document.getElementById("dots");
   let audioPlayer = new Audio();

   const startAssistant = async () => {
       try {
           // Show loading animation
           loadingDiv.style.display = "flex";
           dotsDiv.style.display = "none";

           // Fetch response from server
           const response = await fetch("/start_assistant", {
               method: "POST",
               headers: { "Content-Type": "application/json" },
           });

           if (!response.ok) {
               throw new Error(`Server Error: ${response.statusText}`);
           }

           const data = await response.json();
           console.log("AI Response:", data.response);

           if (data.audio) {
               // Play the audio response
               audioPlayer.src = "data:audio/mp3;base64," + data.audio;
               await audioPlayer.play();
               console.log("Audio playback started.");
           } else {
               // Show message if no audio is returned
               alert(data.response || "No response received from the assistant.");
           }
       } catch (err) {
           console.error("Error:", err.message);
           alert("An error occurred while processing your request. Please try again.");
       } finally {
           // Reset UI
           loadingDiv.style.display = "none";
           dotsDiv.style.display = "flex";
       }
   };

   startBtn.addEventListener("click", startAssistant);
});
