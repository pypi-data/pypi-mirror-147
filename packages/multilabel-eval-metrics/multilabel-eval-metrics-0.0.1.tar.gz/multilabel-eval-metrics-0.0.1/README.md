## Evaluation metrics for multi-label classification models
This toolkit is used to focus on different evaluation metrics that can be used for evaluating the performance of a multilabel classifier. 

### Intro

The evaluation metrics for multi-label classification can be broadly classified into two categories:

- Example-Based Evaluation Metrics
- Label Based Evaluation Metrics.

### Metrics

Exact Match Ratio (EMR)
1/0 Loss
Hamming Loss
Example-Based Accuracy
Example-Based Precision
Label Based Metrics
Macro Averaged Accuracy
Macro Averaged Precision
Macro Averaged Recall
Micro Averaged Accuracy
Micro Averaged Precision
Micro Averaged Recall
α- Evaluation Score

[Reference](https://medium.datadriveninvestor.com/a-survey-of-evaluation-metrics-for-multilabel-classification-bb16e8cd41cd)

### Examples

```python
from multilabel_eval_metrics import *
import numpy as np
if __name__=="__main__":
    y_true = np.array([[0, 1], [1, 1], [1, 1], [0, 1], [1, 0]])
    y_pred = np.array([[1, 1], [1, 0], [1, 1], [0, 1], [1, 0]])
    print(y_true)
    print(y_pred)
    result=MultiLabelMetrics(y_true,y_pred).get_metric_summary(show=True)
```

### License

The `multilabel-eval-metrics` toolkit is provided by [Donghua Chen](https://github.com/dhchenx) with MIT License.

