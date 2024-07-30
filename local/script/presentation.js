const text1 = document.getElementById('text1');
const text2 = document.getElementById('text2');

const fullText1 = "Ich bin dein Südtirol Versteher und du kannst mir etwas diktieren. Ich versuche es auf Deutsch zu transkribieren. Deine Daten werden nicht gepeichert, müssen aber an openAI zur Verarbeitung gesendet werden. Formuliere deinen Text höflich und sympathisch - ob es geklappt hat, sieht du unten in der Bewertung. Viel Spass!";

const initialText1 = fullText1.split(' ').slice(0, 5).join(' ') + '...';

text1.innerText = initialText1;

text1.addEventListener('mouseover', () => {
    text1.innerText = fullText1;
});

text1.addEventListener('mouseout', () => {
    text1.innerText = initialText1;
});
