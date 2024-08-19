config = {
    "myopenkey": "YOUR_API_KEY",
    "modelname": "gpt-4o",
    "jsonbuild": """
            Analysiere den folgenden Text auf Deutsch und gib die Ergebnisse in einem strukturierten Json Format zurück ohne einen markdown viewer. Das Ergebnis sollte die folgenden Komponenten enthalten:

            "Transcript": Der Text sollte vollständig wiedergegeben werden.
            "Eindruck": Reflektiere den Inhalt und wie gut der Text die Werte des Commoning widerspiegelt. Beurteile, welche Aspekte des Textes besonders der Logik des Commoning entsprechen und welche möglicherweise im Widerspruch stehen.
            "Gemeinschaft": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie stark die Verbundenheit der Menschen im Text dargestellt wird (0 = sehr egoistisch, 100 = sehr gemeinschaftssinnig).
            "Vertrauen": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie vertrauenswürdig der Text wirkt (0 = sehr misstrauisch, 100 = sehr vertrauenswürdig).
            "Gegenseitig": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie einladend und offen der Text für Kollaboration ist (0 = sehr abweisend, 100 = sehr einladend).
            "Nachhaltig": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie bewusst der Text mit Ressourcen umgeht (0 = sehr verschwenderisch, 100 = sehr bewusst und sparsam).
            "Inklusion": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie inklusiv der Text ist (0 = ausgrenzend, 100 = einschließend).
            "Kommerziell": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie sehr der Text profitorientiertes Wirtschaften ausdrückt (0 = bedürfnisorientiert, 100 = profitorientiert).
            "SozialesMiteinander": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie sehr der Text Zusammenarbeit und Förderung von Beziehungen unterstützt (0 = asozial, 100 = sehr sozial).
            "GleichrangigeSelbstOrganisation": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie sehr der Text das Aushandeln auf Augenhöhe fördert (0 = hierarchisch, 100 = gleichrangig).
            "SorgendesSelbstbestimmtes Wirtschaften": Gib eine Bewertung zwischen 0 und 100 ab, die ausdrückt, wie sehr der Text sorgendes und selbstbestimmtes Wirtschaften unterstützt (0 = fremdbestimmt, 100 = selbstbestimmt und bedürfnisorientiert). 
            
            Der User Text ist: 
            """
}
