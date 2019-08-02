from sklearn_crfsuite import metrics

actual = []
actual_temp = []

with open("dev.col") as f:
    for l in f:
        if l != "\n":
            pos = l.split("\t")[1].strip()
            actual_temp.append(pos)
        else:
            actual.append(actual_temp)
            actual_temp = []

predicted = []
predicted_temp = []

with open("dev-predicted.col") as f:
    for l in f:
        if l != "\n":
            pos = l.split("\t")[1].strip()
            predicted_temp.append(pos)
        else:
            predicted.append(predicted_temp)
            predicted_temp = []


print(metrics.flat_classification_report(
    actual, predicted, digits=3
    ))
