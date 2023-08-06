# Movies View Estimator

This project tries to predict the number of views a movie might have received by considering the movie Rating and
the Rating Count.

What makes these project so amazing is that it uses a very small database to train a 
Linear Regression Model.

It accepts that it is linear data.

**The pro for this solution:**
- It is easy to understand
- Simple to build
- Very fast to train
- Very small project to maintain

**The cons for this solution:**

- Too simple
- It might not present a good prediction result
- Small dataset used to train


Another good ways to handle this problem would use  **k-nearest neighbors** algorithm.
It is a good fit for the issue.

**The pro for this solution:**
- It is easy to understand
- Simple to build
- Very small project to maintain

**The cons for this solution:**
- if the project goes bigger and more data is provided the model is computationally expensive
- Sensitive to noise
- Expensive to predict

# How to install:

It uses python 3.8

```python
pip install moviesViewEstimator
```

# How to use:

```python
import pandas as pd
from model import LinearRegressionModel

# if you want to know how many views a movie with rate 8.2 and almost 90 thousand rate count you need to pass a pandas
# dataframe, which is the format accepted by the model
predict_dataframe = pd.DataFrame([[8.2, 89224]]) # rate 8.2 and almost 90 thousand rate count
predict_dataframe.columns = ['Rating', 'Rating Count'] # setting the columns names

model = LinearRegressionModel()
print(model.predict(predict_dataframe))
```
```python
[2460651]
```

The predictions tell us that a movie of Rating 8.2 and a Rating Count of almost 90 thousand,
would have almost 2.5 million views.

# Documentation:

For more information you can check the [documentation](https://joaopeuko.github.io/moviesViewEstimator/)


