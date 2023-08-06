import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.metrics import log_loss, confusion_matrix, roc_auc_score, roc_curve

class binary:
    def __init__(self, algo, xtest, ytest, xtrain, ytrain):
        score = []
        self.xtest = xtest
        self.ytest = ytest
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.score = score
        self.algo = algo

    #plot the confusion matrix
    def plot_confusionmatrix(self): #it need the model variable after fitting the data
        #prediction from testing dataset
        test_predict = self.algo.predict(self.xtest)
        
        #plot confusion matrix
        cm = confusion_matrix(self.ytest, test_predict)

        self.test_predict = test_predict
        self.cm = cm

        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=self.algo.classes_)
        disp.plot()
        plt.show() 

    # Roc Curve Characterics
    def auc_plot(self):
        plt.title("Area Under Curve")
        plt.plot(self.fpr_test, self.tpr_test, label="AUC Test="+str(self.roctest))
        plt.plot(self.fpr_train, self.tpr_train, label="AUC Train="+str(self.roctrain))
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.legend(loc=4)
        plt.grid(True)
        plt.show()
    
    #metrix function 
    def print_score(self, name): #algo = model, name = string of the model name
        predtrain = self.algo.predict(self.xtrain)
        
        #confussion matrix percentage
        tn, fp, fn, tp = self.cm.ravel()
        tst = self.ytest.count()
        cmatrix = ((tn + tp)/tst)*100    

        #accuracy score
        acctest = (accuracy_score(self.ytest, self.test_predict))*100
        acctrain = (accuracy_score(self.ytrain, predtrain))*100

        #log loss
        logtest = log_loss(self.ytest,self.test_predict)
        logtrain = log_loss(self.ytrain,predtrain)
                
        #classification report
        precision1 = (tp / (tp+fp))*100
        precision0 = (tn/(tn+fn))*100
        recall1 = (tp/(tp+fn))*100
        recall0 = (tn/(tn+fp))*100
        f1 = 2*(precision1 * recall1)/(precision1 + recall1)    

        #calculate roc_auc_score
        test_prob = self.algo.predict_proba(self.xtest)[::,1]
        train_prob = self.algo.predict_proba(self.xtrain)[::,1]
        roctest = roc_auc_score(self.ytest, test_prob)
        roctrain = roc_auc_score(self.ytrain, train_prob)
        fpr_test, tpr_test, _ = roc_curve(self.ytest,  test_prob)
        fpr_train, tpr_train, _ = roc_curve(self.ytrain,  train_prob)


        self.score.append([name, cmatrix, acctest, acctrain, logtest, logtrain, precision1, precision0, recall1, recall0, f1, self.roctest, self.roctrain])
         
        self.test_prob = test_prob
        self.train_prob = train_prob
        self.roctest = roctest
        self.roctrain = roctrain
        self.fpr_test = fpr_test
        self.tpr_test = tpr_test
        self.fpr_train = fpr_train
        self.tpr_train = tpr_train
               
        #print metrics score
        print("Confusion Matrix Accuracy Score = {:.2f}%\n".format(cmatrix))
        print("Accuracy Score: Training -> {:.2f}% Testing -> {:.2f}%\n".format(acctrain, acctest))
        print("Log Loss Training-> {} Testing -> {}\n".format(logtrain, logtest))
        print('Precision class 1: {:.2f}%\nPrecision class 0: {:.2f}%'.format(precision1, precision0))
        print('Recall class 1: {:.2f}%\nRecall class 0: {:.2f}%'.format(recall1, recall0))
        print('F1: {:.2f}%'.format(f1)) 
        print('ROC AUC Training-> {:.2f}% Testing-> {:.2f}%'.format(self.roctrain, self.roctest))
    
    #evaluation table
    def compare(self):
        print(self.score)