document.addEventListener('DOMContentLoaded', function() {
    const loadingDiv = document.querySelector('.loading');
    const dotsDiv = document.getElementById('dots');
  let recognition;
    let audioPlayer = new Audio();
     if('webkitSpeechRecognition' in window) {

        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
          console.log("Speech recognition started");
          loadingDiv.style.display = 'flex';
          dotsDiv.style.display = 'none';
        };

         recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
             fetch('/process_text', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
              },
             body: JSON.stringify({ text: transcript })
          })
          .then(response => response.json())
          .then(data => {
               console.log(data.response);
               audioPlayer.src = 'data:audio/mp3;base64,' + data.audio;
              audioPlayer.play();
               loadingDiv.style.display = 'none';
               dotsDiv.style.display = 'flex';
          })
        .catch(error => {
               console.error('Error:', error);
              loadingDiv.style.display = 'none';
              dotsDiv.style.display = 'flex';
           });
       };

     recognition.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        loadingDiv.style.display = 'none';
         dotsDiv.style.display = 'flex';
     };

  if(welcomeAudio) {
        audioPlayer.src = 'data:audio/mp3;base64,' + welcomeAudio;
        audioPlayer.play();
   }

  dotsDiv.addEventListener('click', () => {
     loadingDiv.style.display = 'flex';
     dotsDiv.style.display = 'none';
       recognition.start();
      });

     } else {
        loadingDiv.textContent = "Speech recognition is not supported in this browser."
        dotsDiv.style.display = 'flex';
    }
});
