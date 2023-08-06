# Decision Score Histogram
A new histogram-based approach for visualizing anomaly detection algorithm performance and prediction confidence.

## Background
Performance visualization of anomaly detection algorithms is an 
essential aspect of anomaly and intrusion detection systems. 
It allows analysts to highlight trends and outliers in anomaly 
detection models results to gain intuitive understanding of detection
models. This work presents a new way of visualizing anomaly 
detection algorithm results using a histogram. 

### Importance of the Visualization Approach

- provides a better understanding
of detection algorithms performance by revealing the exact 
proportions of true positives, true negatives, false positives, 
and false negatives of detection algorithms. 
- provides insights into the strengths and weaknesses of detection
algorithms performance on different aspects of a datasets unlike 
previous approaches that rely on only positive and negative 
decision scores. 
- can be applied to performance visualization and analysis of 
supervised machine learning techniques involving 
binary classification of imbalanced datasets.


## Usage
Below is an example of how to use this histogram.

**Input:**
- decision_scores: Decision/Anomaly scores of detection or binary  
classification algorithm  --> input to class object
- ground_truth: binary class labels of normal (+1) and anomalous (-1)
data instances  -->  input to class object
- fig_name (Optional: string): name for saving output plot; default is 'hist_plot'  --> input to hist_plot method
- **Input data type**: ```list, numpy array, pandas DataFrame, pandas Series```

**Output:**
- Histogram visualization of true positives, true negatives, false
positives and false negatives with their prediction confidences.

**General use case**
``` python
from hist_score import AnomalyScoreHist
fig = AnomalyScoreHist(decision_scores, ground_truth)
fig.plot_hist(fig_name)
```
**Note**: The data class convention used in this work is:
- 1: represents normal class
- -1: represents the anomalous class

The code can also handle supervised binary predictions whereby 1: class A and -1: class B.

### Example

```python
from hist_score import AnomalyScoreHist

fig = AnomalyScoreHist(test_dec, test['class'])
fig.plot_hist('IF_histogram')
```
where ```test_dec``` is the decision score output of isolation forest 
detection algorithm on test set 2 of [TLIGHT dataset](https://github.com/emmanuelaboah/TLIGHT-SYSTEM/tree/main/Dataset)
and ```test['class']```
is the class label (1, -1).

![hist visualization](images/img1.png)


## References
Users can refer to our paper below for further insight and 
examples:
- Aboah Boateng E, Bruce JW. Unsupervised Machine Learning 
Techniques for Detecting PLC Process Control Anomalies. Journal of Cybersecurity and Privacy. 
2022; 2(2):220-244. https://doi.org/10.3390/jcp2020012

