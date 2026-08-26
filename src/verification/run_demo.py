import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from verification.verifier import verify_report

class FakeDoc:
    def __init__(self, title, summary):
        self.title = title
        self.summary = summary

report = "CNNs use filters to detect features in images. Bananas are a good source of potassium. Convolutional layers reduce the spatial size of feature maps."

docs = [
    FakeDoc("Convolutional neural network", "CNNs use convolutional filters to extract features from images and reduce spatial dimensions through pooling layers."),
    FakeDoc("Nutrition facts", "Bananas contain potassium, vitamin B6, and fiber."),
]

results = verify_report(report, docs)
for r in results:
    print(f"[{r['confidence']}] ({r['score']}) {r['claim']}")
    print(f"   -> Best match: {r['source']}\n")