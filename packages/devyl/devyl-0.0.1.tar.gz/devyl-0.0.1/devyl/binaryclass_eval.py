import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.metrics import log_loss, confusion_matrix, roc_auc_score, roc_curve

#list for metrics scoring
score= []
xtest_ = []
ytest_ = []

#plot the confusion matrix
def cm(algo, xtest, ytest): #it need the model variable after fitting the data
    disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(ytest, algo.predict(xtest)),
                           display_labels=algo.classes_)
    xtest_ = xtest
    ytest_ = ytest
    disp.plot()
    plt.show() 