## Adaptive Pooling Options

#### Adaptive Sum Pooling
- Sums all values in each region
- Similar to average pooling but without dividing by num elements
- Not often used directly but could be helpful in cases where cumulative response is relevant.
---
#### Adaptive Min Pooling
- Selects the **minimum value** in each region --> Captures the weakest activation in each spatial region.
- Useful when suppression or low-value feature importance is looked at
- Downside: often disregards useful strong signals; prone to noise

---
#### Adaptive Log-Sum-Exp Pooling (LSE Pooling)**
- Computes a softmax-weighted average of the feature values
    - Parameter β controls the smoothness of the pooling.
        - When β→∞, behaves like max pooling.
        - When β=1, behaves like average pooling.
- Effective for learning the pooling behavior based on data.

---
#### Adaptive Mixed Pooling
- Combines **average pooling** and **max pooling** by weighting their contributions
- Useful when both strong activations and global context are important.
- Offers more flexibility in capturing feature representations.

---
#### Attention Pooling
- dynamically decide which spatial locations or channels are most important.
    - Outputs are computed as a weighted sum of activations.

---
### **Summary Comparison

| **Method**                   | **Aggregation**                  | **Advantages**                                 | **Disadvantages**                            |
| ---------------------------- | -------------------------------- | ---------------------------------------------- | -------------------------------------------- |
| Adaptive Average Pooling     | Average of values in each region | Stable gradients, smooth output                | May lose critical high activations           |
| Adaptive Max Pooling         | Maximum value in each region     | Retains key features, robust to noise          | Ignores global trends, sensitive to outliers |
| Adaptive Log-Sum-Exp Pooling | Softmax-weighted aggregation     | Balances max and average pooling               | Slightly more computationally expensive      |
| Adaptive Mixed Pooling       | Weighted average and max         | Combines strengths of average and max          | Requires tuning or learning of the weight    |
| Attention Pooling            | Learnable attention weights      | Focus on most important regions dynamically    | Requires additional computational overhead   |
