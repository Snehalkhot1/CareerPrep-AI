/**
 * CareerPrep AI - Mock Interview Console Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  const timerElem = document.getElementById("interviewTimer");
  let secondsElapsed = 0;
  let timerInterval = null;

  // Initialize Interview Timer
  if (timerElem) {
    timerInterval = setInterval(() => {
      secondsElapsed++;
      const minutes = Math.floor(secondsElapsed / 60);
      const seconds = secondsElapsed % 60;
      timerElem.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    }, 1000);
  }

  // Initialize Voice Recorder
  let recorder = null;
  if (typeof VoiceRecorder !== "undefined") {
    recorder = new VoiceRecorder({
      textAreaId: "answerText",
      audioPlayerId: "audioPreview",
      statusElemId: "voiceStatus",
      startBtnId: "startRecordBtn",
      stopBtnId: "stopRecordBtn",
      playBtnId: "playRecordBtn",
    });
  }

  // Handle Form Submission with Optional Audio Blob
  const answerForm = document.getElementById("interviewAnswerForm");
  if (answerForm) {
    answerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById("submitAnswerBtn");
      const answerText = document.getElementById("answerText").value.trim();

      if (!answerText) {
        alert("Please provide an answer before proceeding (either by voice or by typing).");
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = "⏳ Evaluating Answer...";
      }

      const formData = new FormData(answerForm);
      formData.append("duration_seconds", secondsElapsed);

      // Attach audio blob if recorded
      if (recorder && recorder.getAudioBlob()) {
        formData.append("audio_file", recorder.getAudioBlob(), "answer.webm");
      }

      try {
        const response = await fetch(answerForm.action, {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        if (data.redirect) {
          window.location.href = data.redirect;
        } else if (data.success) {
          // If next question exists, reload to display next question
          window.location.reload();
        } else {
          alert(data.error || "An error occurred submitting your answer.");
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = "➡ Submit Answer";
          }
        }
      } catch (err) {
        console.error("Submission error:", err);
        // Fallback: standard form submit
        answerForm.submit();
      }
    });
  }
});
