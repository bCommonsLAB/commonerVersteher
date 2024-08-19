document.addEventListener("DOMContentLoaded", () => {
  const dropArea = document.querySelector(".drag-image"),
    dragText = dropArea.querySelector("h6"),
    input = dropArea.querySelector("input"),
    loadingScreen = document.getElementById("loading-screen"),
    statusElement = document.getElementById("status"),
    userTextElement = document.getElementById("user-text"),
    openPopupBtn = document.getElementById("open-popup"),
    closePopupBtn = document.getElementById("close-popup"),
    popupContainer = document.getElementById("popup-container"),
    browseButton = dropArea.querySelector("button");

  let file;

  function showLoading() {
    loadingScreen.style.display = "flex";
  }

  function hideLoading() {
    loadingScreen.style.display = "none";
  }

  function openPopup() {
    popupContainer.style.display = "flex";
    popupContainer.classList.remove("slideOut");
    popupContainer.classList.add("slideIn");
  }

  function closePopup() {
    popupContainer.classList.remove("slideIn");
    popupContainer.classList.add("slideOut");
    popupContainer.addEventListener(
      "animationend",
      () => {
        if (popupContainer.classList.contains("slideOut")) {
          popupContainer.style.display = "none";
        }
      },
      { once: true }
    );
  }

  function viewFile() {
    let fileType = file.type;
    let validExtensions = ["audio/mpeg"];
    if (validExtensions.includes(fileType)) {
      closePopup();
      showLoading();
      sendFileToServer(file);
    } else {
      alert("This is not an MP3 File!");
      dropArea.classList.remove("active");
      dragText.textContent = "Drag & Drop to Upload MP3 File";
    }
  }

  function sendFileToServer(file) {
    const formData = new FormData();
    formData.append("audio", file);

    fetch("http://localhost:5000/transcribe", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        hideLoading();
        if (data.error) {
          statusElement.innerText = "Fehler bei der Analyse: " + data.error;
          console.error("Analyse Fehler:", data.error);
        } else {
          if (userTextElement) userTextElement.value = data.transcript || "";
          statusElement.innerText = "Analyse beendet";
        }
      })
      .catch((error) => {
        hideLoading();
        statusElement.innerText = "Fehler bei der Analyse";
        console.error(error);
      });
  }

  input.addEventListener("change", function () {
    file = this.files[0];
    dropArea.classList.add("active");
    viewFile();
  });

  dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload MP3 File";
  });

  dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    file = event.dataTransfer.files[0];
    dropArea.classList.remove("active");
    viewFile();
  });

  browseButton.addEventListener("click", () => {
    input.click();
  });

  openPopupBtn.addEventListener("click", openPopup);
  closePopupBtn.addEventListener("click", closePopup);

  window.addEventListener("click", (event) => {
    if (event.target == popupContainer) {
      closePopup();
    }
  });
});
