/**
 * CareerPrep AI - Voice Recording & Speech-to-Text Controller
 * Utilizes MediaRecorder API for audio capture and Web Speech API for real-time transcription.
 */

class VoiceRecorder {
  constructor(options = {}) {
    this.textAreaId = options.textAreaId || "answerText";
    this.audioPlayerId = options.audioPlayerId || "audioPreview";
    this.statusElemId = options.statusElemId || "voiceStatus";
    this.startBtnId = options.startBtnId || "startRecordBtn";
    this.stopBtnId = options.stopBtnId || "stopRecordBtn";
    this.playBtnId = options.playBtnId || "playRecordBtn";

    this.mediaRecorder = null;
    this.audioChunks = [];
    this.audioBlob = null;
    this.audioUrl = null;
    this.recognition = null;
    this.isRecording = false;

    this.initElements();
    this.initSpeechRecognition();
  }

  initElements() {
    this.textArea = document.getElementById(this.textAreaId);
    this.audioPlayer = document.getElementById(this.audioPlayerId);
    this.statusElem = document.getElementById(this.statusElemId);
    this.startBtn = document.getElementById(this.startBtnId);
    this.stopBtn = document.getElementById(this.stopBtnId);
    this.playBtn = document.getElementById(this.playBtnId);

    if (this.startBtn) this.startBtn.addEventListener("click", () => this.startRecording());
    if (this.stopBtn) this.stopBtn.addEventListener("click", () => this.stopRecording());
    if (this.playBtn) this.playBtn.addEventListener("click", () => this.playRecording());
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = "en-US";

      this.recognition.onresult = (event) => {
        let interimTranscript = "";
        let finalTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }

        if (this.textArea) {
          const baseText = this.textArea.dataset.initialText || "";
          this.textArea.value = (baseText + " " + finalTranscript + " " + interimTranscript).trim();
        }
      };

      this.recognition.onerror = (event) => {
        console.warn("Speech recognition warning:", event.error);
      };
    }
  }

  async startRecording() {
    this.audioChunks = [];
    if (this.textArea) {
      this.textArea.dataset.initialText = this.textArea.value;
    }

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        this.showStatus("Voice recording unsupported in this browser. Please use text answer.", "warning");
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        this.audioBlob = new Blob(this.audioChunks, { type: "audio/webm" });
        this.audioUrl = URL.createObjectURL(this.audioBlob);
        if (this.audioPlayer) {
          this.audioPlayer.src = this.audioUrl;
          this.audioPlayer.style.display = "block";
        }
        if (this.playBtn) this.playBtn.disabled = false;
        this.showStatus("Recording stopped. Audio ready for playback or submission.", "success");
      };

      this.mediaRecorder.start();
      this.isRecording = true;

      // Start Web Speech API transcription simultaneously
      if (this.recognition) {
        try {
          this.recognition.start();
        } catch (e) {
          // Ignore already-started errors
        }
      }

      // Update UI
      if (this.startBtn) this.startBtn.disabled = true;
      if (this.stopBtn) this.stopBtn.disabled = false;
      this.showStatus("🎤 Recording in progress... Speak clearly into your microphone.", "danger");

    } catch (err) {
      console.error("Microphone access error:", err);
      this.showStatus("Microphone permission denied or unavailable. You can answer using text.", "warning");
      if (this.startBtn) this.startBtn.disabled = false;
      if (this.stopBtn) this.stopBtn.disabled = true;
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      // Stop all audio tracks to release microphone
      this.mediaRecorder.stream.getTracks().forEach((track) => track.stop());
      this.isRecording = false;

      if (this.recognition) {
        try {
          this.recognition.stop();
        } catch (e) {}
      }

      if (this.startBtn) this.startBtn.disabled = false;
      if (this.stopBtn) this.stopBtn.disabled = true;
    }
  }

  playRecording() {
    if (this.audioPlayer && this.audioUrl) {
      this.audioPlayer.play();
    }
  }

  showStatus(message, type = "info") {
    if (!this.statusElem) return;
    this.statusElem.textContent = message;
    this.statusElem.className = `alert alert-${type}`;
    this.statusElem.style.display = "block";
  }

  getAudioBlob() {
    return this.audioBlob;
  }
}

window.VoiceRecorder = VoiceRecorder;
