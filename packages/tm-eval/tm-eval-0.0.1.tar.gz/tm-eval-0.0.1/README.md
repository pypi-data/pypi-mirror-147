## Topic Modeling Evaluation
A toolkit to quickly evaluate model goodness over number of topics

### Metrics
Coherence measure to be used. 

- Fastest method - 'u_mass', 'c_uci' also known as `c_pmi`. 

- For 'u_mass' corpus should be provided, if texts is provided, it will be converted to corpus using the dictionary. 

- For 'c_v', 'c_uci' and 'c_npmi' `texts` should be provided (`corpus` isn't needed)

### Examples

Example 1: estimate metrics for one topic model with specific number of topics
```python
from tm_eval import *
# load a dictionary with document key and its term list split by ','.
input_file = "datasets/covid19_symptoms.pickle"
output_folder = "outputs"
model_name = "symptom"
num_topics = 10
# run
results = evaluate_all_metrics_from_lda_model(input_file=input_file, 
                                              output_folder=output_folder,
                                              model_name=model_name, 
                                              num_topics=num_topics)
print(results)
```
Example 2: find model goodness change over number of topics
```python
from tm_eval import *
if __name__=="__main__":
    # start configure
    # load a dictionary (key,value) with document id as key and its term list combined by ',' as value.
    input_file = "datasets/covid19_symptoms.pickle"
    output_folder = "outputs"
    model_name = "symptom"
    start=2
    end=5
    # end configure
    # run and explore

    list_results = explore_topic_model_metrics(input_file=input_file, 
                                               output_folder=output_folder,
                                               model_name=model_name,
                                               start=start,
                                               end=end)
    # summarize results
    show_topic_model_metric_change(list_results,save=True,
                                   save_path=f"{output_folder}/metrics.csv")

    # plot metric changes
    plot_tm_metric_change(csv_path=f"{output_folder}/metrics.csv",
                          save=True,save_folder=output_folder)
```

### Output results

![c_v](https://dhchenx.github.io/projects/tm-eval/c_v.jpg)

![u_mass](https://dhchenx.github.io/projects/tm-eval/u_mass.jpg)

![c_npmi](https://dhchenx.github.io/projects/tm-eval/c_npmi.jpg)

![c_uci](https://dhchenx.github.io/projects/tm-eval/c_uci.jpg)

### License

The `tm-eval` toolkit is provided by [Donghua Chen](https://github.com/dhchenx) with MIT License.

### References
1. [Topic Modeling in Python: Latent Dirichlet Allocation (LDA)](https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0)
2. [Evaluate Topic Models: Latent Dirichlet Allocation (LDA)](https://towardsdatascience.com/evaluate-topic-model-in-python-latent-dirichlet-allocation-lda-7d57484bb5d0)