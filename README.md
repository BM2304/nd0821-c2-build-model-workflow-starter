# ML Pipeline for Short-Term Rental Prices in NYC
End-to-end ml pipeline for estimating the typical price for a given property based 
on the price of similar properties in NYC. 

Link to Github: [https://github.com/BM2304/nd0821-c2-build-model-workflow-starter](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter)
Link to W&B: [https://wandb.ai/bm23/nyc_airbnb](https://wandb.ai/bm23/nyc_airbnb)
### Create environment
Make sure to have conda installed and ready, then create a new environment using the ``environment.yml``
file provided in the root of the repository and activate it:

```bash
> conda env create -f environment.yml
> conda activate nyc_airbnb_dev
```
### Get API key for Weights and Biases
Let's make sure we are logged in to Weights & Biases. Get your API key from W&B by going to 
[https://wandb.ai/authorize](https://wandb.ai/authorize) and click on the + icon (copy to clipboard), 
then paste your key into this command:

```bash
> wandb login [your API key]
```

You should see a message similar to:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[your username]/.netrc
```
### The configuration
As usual, the parameters controlling the pipeline are defined in the ``config.yaml`` file defined in
the root of the starter kit.


### Running the entire pipeline or just a selection of steps
In order to run the pipeline when you are developing, you need to be in the root of the starter kit, 
then you can execute as usual:

```bash
>  mlflow run .
```
This will run the entire pipeline.

When developing it is useful to be able to run one step at the time. Say you want to run only
the ``download`` step. The `main.py` is written so that the steps are defined at the top of the file, in the 
``_steps`` list, and can be selected by using the `steps` parameter on the command line:

```bash
> mlflow run . -P steps=download
```
If you want to run the ``download`` and the ``basic_cleaning`` steps, you can similarly do:
```bash
> mlflow run . -P steps=download,basic_cleaning
```
You can override any other parameter in the configuration file using the Hydra syntax, by
providing it as a ``hydra_options`` parameter. For example, say that we want to set the parameter
modeling -> random_forest -> n_estimators to 10 and etl->min_price to 50:

```bash
> mlflow run . \
  -P steps=download,basic_cleaning \
  -P hydra_options="modeling.random_forest.n_estimators=10 etl.min_price=50"
```


- `download`: downloads the data (get_data). [MLproject](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter/blob/master/components/get_data/MLproject)
- `basic_cleaning`: remove outliers and null values [MLproject](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter/blob/master/src/basic_cleaning/MLproject)
- `data_check`: run data checks like distribution and expected columns [MLproject](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter/blob/master/src/data_check/MLproject)
- `data_split`: segrgate the data (splits the data) [MLproject](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter/blob/master/components/train_val_test_split/MLproject)
- `train_random_forest`: train random forest and upload fitted model [MLproject](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter/blob/master/src/train_random_forest/MLproject)
- `test_regression_model`: test a trained model on new test data [MLproject](https://github.com/BM2304/nd0821-c2-build-model-workflow-starter/blob/master/components/test_regression_model/MLproject)

### Train the model on a new data sample

```
> mlflow run https://github.com/BM2304/nd0821-c2-build-model-workflow-starter.git \
             -v [the version you want to use, like 1.0.1] \
             -P hydra_options="etl.sample='sample2.csv'"
```

## License

[License](LICENSE.txt)
