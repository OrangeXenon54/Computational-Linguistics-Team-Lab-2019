Naive Bayes baseline classifier for Parts of Speech tagging
=============================================================

This folder contains a baseline implementation of naive bayes classifier for Parts of Speech (POS) tagging. The project is implemented in Python.


### Dependencies

For computation

      numpy

For visualization

      matplotlib
      sklearn
      
### Train the model

Use ClassifierTrain.py to train and generate the model. Change the paths into appropriate directories. This will generate multiple training checkpoints.
              
              ClassifierTrain.py
              ---------------------------
              
              #resource paths
              TRAINING_PATH = "training data file path"
                       

### Generate prediction usiong model

Once the training has been done, use ClassifierTest.py to test the model. Change the paths into appropriate directory.

              ClassifierTest.py
              --------------------------
              
              #resource paths
              MODEL_PATH = "model file path"
              TAG_COUNT_PATH = "tag count file path(generated with model)"
              TEST_PATH = 'test data file path'
              RESULT_PATH = 'output of the prediction file path(will be generated)'
              
### Evalute the model prediction

To generate the evaluation of the model (Micro and Macro average precision, Recall, fscore), use this Evaluation.py Change the paths into appropriate directory.

              Evaluation.py
              -----------------------------
              
              
              ORIGINAL_LABEL_PATH = "Test file with original label"
              PREDICTED_LABEL_PATH = "test file with predicted label"
              
Use ConfusionMatrics.py to generate the confusion matrics.

<p align="center">
  <img src="https://github.com/OrangeXenon54/Group-13-Computational-Linguistics-Team-Lab-2019/blob/master/Naive%20Bayes%20final/Figure_1.png" width="500" title="hover text">
</p>
       
              
          
