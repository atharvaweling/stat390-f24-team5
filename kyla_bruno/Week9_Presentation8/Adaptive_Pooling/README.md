# Adaptive Pooling Methods and Improvements

Results suggest Adaptive Mixed Pooling is the best for mapping our differently sized input images to a fix output size. Max pooling alone seems to be the best alternative. Within both, performance can be improved with additional convolutional layers, droupout methods, regularization (L2), learning rate adjustments, and not defining a kernel (let the model use default behavior of determining best kernel based on input).

#### Suggestions for Next Quarter
Ways to improve feature extraction and pooling layer adaptability (in order of what I think may work best):
- Use attention mechanisms to guide the pooling process, focusing on the most relevant spatial regions (aka combine the pooling with an attention map)
- Apply pooling at multiple scales and then combine through conactenation or additional pooling (should help capture both fine and coarse-grained features)
    - mixed pooling on subregions, then aggregate the results (using weighted sum, attention mechanism, or smth else)
- In addition to mixed pooling, use dilated convlutions to enhance receptive fields before pooling. and/or preserve unpooled features using residual connections to later fuse with the pooled outputs. 
- Apply regularization to prevent pooling weights from being overly biased towards max or average.
- Apply mixed pooling within each level of a spatial pyramid (Spatial Pyramid Pooling) and aggregate across levels for multi-scale representations
- Instead of using pre-defined or auto-defined kernel, make a secondary neural network to predict the optimal kernel size for pooling layers

There are many different directions to go with this. I think this O-shape prediction problem may do better with different settings (conv layers, pooling options, etc.) than our tissue data. So it may be better to refine these results and try out different methods using the data we plan to use this on. 

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
### Summary Comparison

| **Method**                   | **Aggregation**                  | **Advantages**                                 | **Disadvantages**                            |
| ---------------------------- | -------------------------------- | ---------------------------------------------- | -------------------------------------------- |
| Adaptive Average Pooling     | Average of values in each region | Stable gradients, smooth output                | May lose critical high activations           |
| Adaptive Max Pooling         | Maximum value in each region     | Retains key features, robust to noise          | Ignores global trends, sensitive to outliers |
| Adaptive Log-Sum-Exp Pooling | Softmax-weighted aggregation     | Balances max and average pooling               | Slightly more computationally expensive      |
| Adaptive Mixed Pooling       | Weighted average and max         | Combines strengths of average and max          | Requires tuning or learning of the weight    |
| Attention Pooling            | Learnable attention weights      | Focus on most important regions dynamically    | Requires additional computational overhead   |
