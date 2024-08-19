const fullTextout =
  "Ich bin dein Commoning .... ";
const fullText =
  "Ich bin dein Commoning Versteher und du kannst hier deine Überlegungen zu Themen rund ums Commoning einsprechen. Ich werde diese transkribieren, eine kurze Reflexion schreiben und dann bewerten, wie sehr der Text den Idealen des Commonings entspricht.";

const initialText = fullTextout;
text1.innerText = fullTextout;

// Set the initial height to ensure smooth first transition
text1.style.height = "17px";

let timeoutId;

text1.addEventListener("mouseover", () => {
  clearTimeout(timeoutId);
  text1.innerText = fullText;

  // Get the full height of the content
  const fullHeight = text1.scrollHeight + "px";

  // Set the height to the current height first (for smooth animation)
  text1.style.height = text1.offsetHeight + "px";

  // Trigger a reflow to apply the current height before changing it
  text1.offsetHeight; // This forces a reflow, necessary for the transition

  // Now, set the height to the full height, which will trigger the transition
  text1.style.height = fullHeight;
});

text1.addEventListener("mouseout", () => {
  // Set the height back to the initial height
  text1.style.height = "17px";

  timeoutId = setTimeout(() => {
    text1.innerText = initialText;
  }, 725);
});
