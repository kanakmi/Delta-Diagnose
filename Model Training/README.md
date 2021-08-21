## Building the Model

### Dataset
- In version 1.0 we had 251 Chest MRI Training Images (111-COVID, 70-Viral Pneumonia, 70-Normal) and 66 Test Images (26-COVID, 20-Viral Pneumonia, 20-Normal) from a Kaggle Dataset [(Link)](https://www.kaggle.com/pranavraikokte/covid19-image-dataset).
- In this version we combined the previous data with 1704 new Training Images (504-COVID, 576-Viral Pneumonia, 624-Normal) and 119 Test Images (32-COVID, 43-Viral Pneumonia, 44-Normal) from another Kaggle Dataset [(Link)](https://www.kaggle.com/sid321axn/covid-cxr-image-dataset-research).
- In the combined dataset we have 1955 Training Images and 185 Test Images.
<p align = 'center'>
  <img alt="Sample" height=40% src="https://i.ibb.co/Hrp0YyL/Screenshot-2021-08-08-105409.png" width="40%"/>
</p>

### Image Augmentation
We Horizontally Flipped the images and obtained 3910 total samples out of which 15% (587 samples) formed the Validation Set and rest (3323 samples) formed the Training Set.<br>

### Designing and Training the Model
- We designed a Sequential Model having 5 Convolutional Layers and 4 Dense Layers.
- The first layer started with 32 filters and kernel of 2x2.
- The number of filters are doubled at every next layer and kernel is is incremented by 1.
- We introduced some Max Pooling Layers after Convolutional Layers to avoid over-fitting and reduce Computational Costs.
- The Output from Covolutional Layer is Flattened and passed over to Dense Layers.
- We started with 512 neurons in the first Dense layer and reduced them to half over the next two Dense layers.
- Some Dropout Layers were also introduced throught the model to randomly ignore some of the neurons and reduce over-fitting.
- We used ReLU activation in all layers except output layer to reduce computation cost and introduce non-linearity.
- Finally the Output Layer was constructed containing 3 neurons (1 for each class) and softmax activation.

### Result
- The model with least Validation Loss was saved during the training and reloaded before obtaining the final results.
- The model was able to classify 99.45% of the samples correctly.
- The Precision and Recall is also good for all the classes.
