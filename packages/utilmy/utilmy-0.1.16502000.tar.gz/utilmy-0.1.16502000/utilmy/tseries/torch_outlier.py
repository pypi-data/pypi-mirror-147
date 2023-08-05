# -*- coding: utf-8 -*-
MNAME=""
HELP="""Copy of 06.time-series-anomaly-detection-ecg.ipynb
Original file is located at
    https://colab.research.google.com/drive/13z9d0puHSmFCVfHpTqEm5rKbaRNkdaac

# Time Series Anomaly Detection using LSTM Autoencoders with PyTorch in Python


!nvidia-smi
!pip install -qq arff2pandas
!pip install -q -U watermark
!pip install -qq -U pandas


!gdown --id 16MIleqoIr1vYxlGk4GKnGmrsCPuWkkpT
!unzip -qq ECG5000.zip


# Commented out IPython magic to ensure Python compatibility.
# %reload_ext watermark
# %watermark -v -p numpy,pandas,torch,arff2pandas
.

"""
import os, glob, sys, math, time, json, functools, random, yaml, gc, copy
from datetime import datetime
import seaborn as sns, pandas as pd, numpy as np
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.model_selection import train_test_split




from torch import nn, optim
import torch
import torch.nn.functional as F


#############################################################################################
from utilmy import log, log2

def help():
    """function help        """
    from utilmy import help_create
    print( HELP + help_create(MNAME) )



#############################################################################################
def test_all() -> None:
    """function test_all   to be used in test.py         """
    log(MNAME)
    test1()



def test1():
  """ lSTM Auto-encoder
  Example
  -------
    In this tutorial, you learned how to create an LSTM Autoencoder with PyTorch and use it to detect heartbeat anomalies in ECG data.
  
    - [Read  tutorial](https://www.curiousily.com/posts/time-series-anomaly-detection-using-lstm-autoencoder-with-pytorch-in-python/)
    - [Run  notebook in your browser (Google Colab)](https://colab.research.google.com/drive/1_J2MrBSvsJfOcVmYAN2-WSp36BtsFZCa)
    - [Read  Getting Things Done with Pytorch book](https://github.com/curiousily/Getting-Things-Done-with-Pytorch)
  
    You learned how to:
  
    - Prepare a dataset for Anomaly Detection from Time Series Data
    - Build an LSTM Autoencoder with PyTorch
    - Train and evaluate your model
    - Choose a threshold for anomaly detection
    - Classify unseen examples as normal or anomaly
  
    While our Time Series data is univariate (have only 1 feature),  code should work for multivariate datasets (multiple features) with little or no modification. Feel free to try it!
  
    ## References
  
    - [Sequitur - Recurrent Autoencoder (RAE)](https://github.com/shobrook/sequitur)
    - [Towards Never-Ending Learning from Time Series Streams](https://www.cs.ucr.edu/~eamonn/neverending.pdf)
    - [LSTM Autoencoder for Anomaly Detection](https://towardsdatascience.com/lstm-autoencoder-for-anomaly-detection-e1f4f2ee7ccf)
  """


  sns.set(style='whitegrid', palette='muted', font_scale=1.2)
  HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#ADFF02", "#8F00FF"]
  sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))
  rcParams['figure.figsize'] = 12, 8


  RANDOM_SEED = 42
  np.random.seed(RANDOM_SEED)
  torch.manual_seed(RANDOM_SEED)


  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


  #######  Input data  ###########################################################################
  """combine  training and test data into a single data frame. 
     This will give us more data to train our Autoencoder. also shuffle it:"""
  from arff2pandas import a2p
  with open('ECG5000_TRAIN.arff') as f:
    train = a2p.load(f)

  with open('ECG5000_TEST.arff') as f:
    test = a2p.load(f)

  df = train.append(test)
  df = df.sample(frac=1.0)


  """have 5,000 examples. Each row represents a single heartbeat record. Let's name  possible classes:"""
  CLASS_NORMAL = 1
  class_names = ['Normal','R on T','PVC','SP','UB']

  new_columns = list(df.columns)
  new_columns[-1] = 'target'
  df.columns = new_columns


  """## Exploratory Data Analysis
  """
  df.target.value_counts()
  ax = sns.countplot(df.target)
  ax.set_xticklabels(class_names);


  """ normal class, has by far,  most examples. This is great because use it to train our model.
  
  Let's have a look at an averaged (smood out with one standard deviation on top and bottom of it) Time Series for each class:
  """
  classes = df.target.unique()

  fig, axs = plt.subplots(nrows=len(classes) // 3 + 1, ncols=3, sharey=True, figsize=(14, 8))
  for i, cls in enumerate(classes):
    ax = axs.flat[i]
    data = df[df.target == cls] \
      .drop(labels='target', axis=1) \
      .mean(axis=0) \
      .to_numpy()
    plot_time_series_class(data, class_names[i], ax)

  fig.delaxes(axs.flat[-1])
  fig.tight_layout();




  """ normal class has a distinctly different pattern than all or classes. Maybe our model will be able to detect anomalies?
  
  ## LSTM Autoencoder
   [Autoencoder's](https://en.wikipedia.org/wiki/Autoencoder) job is to get some input data, pass it through  model, and obtain a reconstruction of  input.  reconstruction should match  input as much as possible.  trick is to use a small number of parameters, so your model learns a compressed representation of  data.
  In a sense, Autoencoders try to learn only  most important features (compressed version) of  data. Here, have a look at how to feed Time Series data to an Autoencoder. use a couple of LSTM layers (hence  LSTM Autoencoder) to capture  temporal dependencies of  data.
  To classify a sequence as normal or an anomaly, pick a threshold above which a heartbeat is considered abnormal.
  
  
  ### Reconstruction Loss
  When training an Autoencoder,  objective is to reconstruct  input as best as possible. 
  This is done by minimizing a loss function (just like in supervised learning). 
  This function is known as *reconstruction loss*. Cross-entropy loss and Mean squared error are common examples.
  
  
  ## Anomaly Detection in ECG Data
  use normal heartbeats as training data for our model and record  *reconstruction loss*. But first, need to prepare  data:
  
  
  ### Data Preprocessing
  Let's get all normal heartbeats and drop  target (class) column:
  """

  normal_df = df[df.target == str(CLASS_NORMAL)].drop(labels='target', axis=1)

  """merge all or classes and mark m as anomalies:"""
  anomaly_df = df[df.target != str(CLASS_NORMAL)].drop(labels='target', axis=1)



  train_df, val_df = train_test_split(normal_df, test_size=0.15, random_state=RANDOM_SEED)
  val_df, test_df  = train_test_split(val_df, test_size=0.33, random_state=RANDOM_SEED)


  """Each Time Series will be converted to a 
     2D Tensor in  shape *sequence length* x *number of features* (140x1 in our case).
  """

  train_dataset, seq_len, n_features = create_dataset(train_df)
  val_dataset, _, _          = create_dataset(val_df)
  test_normal_dataset, _, _  = create_dataset(test_df)
  test_anomaly_dataset, _, _ = create_dataset(anomaly_df)



  """Our Autoencoder passes  input through  Encoder and Decoder."""
  model = modelRecurrentAutoencoder(seq_len, n_features, 128)
  model = model.to(device)


  """
  using a batch size of 1 (our model sees only 1 sequence at a time). 
  minimizing  [L1Loss](https://pytorch.org/docs/stable/nn.html#l1loss), 
  which measures  MAE (mean absolute error). Why?  reconstructions seem to be better than with MSE (mean squared error).
  """
  model, history = model_train(model, train_dataset, val_dataset, n_epochs=150
                               )


  ax = plt.figure().gca()
  ax.plot(history['train'])
  ax.plot(history['val'])
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['train', 'test'])
  plt.title('Loss over training epochs')
  plt.show();


  MODEL_PATH = 'model.pth'
  torch.save(model, MODEL_PATH)



  ############################################################################
  # """Uncomment  next lines, if you want to download and load  pre-trained model:"""
  # !gdown --id 1jEYx5wGsb7Ix8cZAw3l5p5pOwHs3_I9A
  # model = torch.load('model.pth')
  # model = model.to(device)

  """## Choosing a threshold
  With our model at hand, can have a look at  reconstruction error on  training set.
   Let's start by writing a helper function to get predictions from our model:
  """



  """Our function goes through each example in  dataset and records  predictions and losses."""
  _, losses = model_predict(model, train_dataset)

  sns.distplot(losses, bins=50, kde=True);
  THRESHOLD = 26



  """## Evaluation
  Using  threshold, can turn  problem into a simple binary classification task:
  
  - If  reconstruction loss for an example is below  threshold, classify it as a *normal* heartbeat
  - Alternatively, if  loss is higher than  threshold, classify it as an anomaly
  
  ### Normal hearbeats
  Let's check how well our model does on normal heartbeats. use  normal heartbeats from  test set (our model haven't seen those):
  """

  predictions, pred_losses = model_predict(model, test_normal_dataset)
  sns.distplot(pred_losses, bins=50, kde=True);

  """count  correct predictions:"""
  correct = sum(l <= THRESHOLD for l in pred_losses)
  print(f'Correct normal predictions: {correct}/{len(test_normal_dataset)}')


  """### Anomalies
  do  same with  anomaly examples, but ir number is much higher. get a subset that has  same size as  normal heartbeats:
  """

  anomaly_dataset = test_anomaly_dataset[:len(test_normal_dataset)]


  """Now can take  predictions of our model for  subset of anomalies:"""
  predictions, pred_losses = model_predict(model, anomaly_dataset)
  sns.distplot(pred_losses, bins=50, kde=True);


  """Finally, can count  number of examples above  threshold (considered as anomalies):"""
  correct = sum(l > THRESHOLD for l in pred_losses)
  print(f'Correct anomaly predictions: {correct}/{len(anomaly_dataset)}')


  """have very good results. 
  In  real world, you can tweak  threshold depending on what kind of errors you want to tolerate. 
  In this case, you might want to have more false positives (normal heartbeats considered as anomalies) 
  than false negatives (anomalies considered as normal).
  #### Looking at Examples  
  can overlay  real and reconstructed Time Series values to see how close y are. 
  do it for some normal and anomaly cases:
  """
  for i, data in enumerate(test_normal_dataset[:6]):
    plot_prediction(data, model, title='Normal', ax=axs[0, i])

  for i, data in enumerate(test_anomaly_dataset[:6]):
    plot_prediction(data, model, title='Anomaly', ax=axs[1, i])

  fig.tight_layout();





#############################################################################################################
class modelEncoder(nn.Module):
  """ *Encoder* uses two LSTM layers to compress  Time Series data input.

  Next, decode  compressed representation using a *Decoder*:
  """
  def __init__(self, seq_len, n_features, embedding_dim=64):
    super(modelEncoder, self).__init__()

    self.seq_len, self.n_features = seq_len, n_features
    self.embedding_dim, self.hidden_dim = embedding_dim, 2 * embedding_dim

    self.rnn1 = nn.LSTM(
      input_size=n_features,
      hidden_size=self.hidden_dim,
      num_layers=1,
      batch_first=True
    )

    self.rnn2 = nn.LSTM(
      input_size=self.hidden_dim,
      hidden_size=embedding_dim,
      num_layers=1,
      batch_first=True
    )

  def forward(self, x):
    x = x.reshape((1, self.seq_len, self.n_features))

    x, (_, _) = self.rnn1(x)
    x, (hidden_n, _) = self.rnn2(x)

    return hidden_n.reshape((self.n_features, self.embedding_dim))




class modelDecoder(nn.Module):
  """Our Decoder contains two LSTM layers and an output layer that gives  final reconstruction.
  #
  # Time to wrap everything into an easy to use module:
  """
  def __init__(self, seq_len, input_dim=64, n_features=1):
    super(modelDecoder, self).__init__()

    self.seq_len, self.input_dim = seq_len, input_dim
    self.hidden_dim, self.n_features = 2 * input_dim, n_features

    self.rnn1 = nn.LSTM(
      input_size=input_dim,
      hidden_size=input_dim,
      num_layers=1,
      batch_first=True
    )

    self.rnn2 = nn.LSTM(
      input_size=input_dim,
      hidden_size=self.hidden_dim,
      num_layers=1,
      batch_first=True
    )

    self.output_layer = nn.Linear(self.hidden_dim, n_features)

  def forward(self, x):
    x = x.repeat(self.seq_len, self.n_features)
    x = x.reshape((self.n_features, self.seq_len, self.input_dim))

    x, (hidden_n, cell_n) = self.rnn1(x)
    x, (hidden_n, cell_n) = self.rnn2(x)
    x = x.reshape((self.seq_len, self.hidden_dim))

    return self.output_layer(x)




class modelRecurrentAutoencoder(nn.Module):
  """### LSTM Autoencoder

  ![Autoencoder](https://lilianweng.github.io/lil-log/assets/images/autoencoder-architecture.png)
  *Sample Autoencoder Architecture [Image Source](https://lilianweng.github.io/lil-log/2018/08/12/from-autoencoder-to-beta-vae.html)*

   general Autoencoder architecture consists of two components.
       An *Encoder* that compresses  input and a *Decoder* that tries to reconstruct it.

  use  LSTM Autoencoder from this [GitHub repo](https://github.com/shobrook/sequitur)
  with some small tweaks. Our model's job is to reconstruct Time Series data.
  """
  def __init__(self, seq_len, n_features, embedding_dim=64, device='cpu'):
    super(modelRecurrentAutoencoder, self).__init__()

    self.encoder = modelEncoder(seq_len, n_features, embedding_dim).to(device)
    self.decoder = modelDecoder(seq_len, embedding_dim, n_features).to(device)

  def forward(self, x):
    x = self.encoder(x)
    x = self.decoder(x)

    return x


def create_dataset(df):

  sequences = df.astype(np.float32).to_numpy().tolist()

  dataset = [torch.tensor(s).unsqueeze(1).float() for s in sequences]

  n_seq, seq_len, n_features = torch.stack(dataset).shape

  return dataset, seq_len, n_features


def model_predict(model, dataset, device='cpu'):
  predictions, losses = [], []
  loss_calc = nn.L1Loss(reduction='sum').to(device)
  with torch.no_grad():
    model = model.eval()
    for seq_true in dataset:
      seq_true = seq_true.to(device)
      seq_pred = model(seq_true)

      loss = loss_calc(seq_pred, seq_true)

      predictions.append(seq_pred.cpu().numpy().flatten())
      losses.append(loss.item())
  return predictions, losses



def model_train(model, train_dataset, val_dataset, n_epochs, device='cpu'):
  optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
  loss_calc = nn.L1Loss(reduction='sum').to(device)
  history   = dict(train=[], val=[])

  best_model_wts = copy.deepcopy(model.state_dict())
  best_loss = 10000.0

  for epoch in range(1, n_epochs + 1):
    model = model.train()

    train_losses = []
    for seq_true in train_dataset:
      optimizer.zero_grad()

      seq_true = seq_true.to(device)
      seq_pred = model(seq_true)

      loss = loss_calc(seq_pred, seq_true)
      loss.backward()
      optimizer.step()
      train_losses.append(loss.item())


    val_losses = []
    model      = model.eval()
    with torch.no_grad():
      for seq_true in val_dataset:
        seq_true = seq_true.to(device)
        seq_pred = model(seq_true)
        loss     = loss_calc(seq_pred, seq_true)
        val_losses.append(loss.item())

    train_loss = np.mean(train_losses)
    val_loss = np.mean(val_losses)

    history['train'].append(train_loss)
    history['val'].append(val_loss)

    if val_loss < best_loss:
      best_loss = val_loss
      best_model_wts = copy.deepcopy(model.state_dict())

    print(f'Epoch {epoch}: train loss {train_loss} val loss {val_loss}')

  model.load_state_dict(best_model_wts)
  return model.eval(), history






if 'utils':
  def plot_time_series_class(data, class_name, ax, n_steps=10):
    time_series_df = pd.DataFrame(data)

    smooth_path = time_series_df.rolling(n_steps).mean()
    path_deviation = 2 * time_series_df.rolling(n_steps).std()

    under_line = (smooth_path - path_deviation)[0]
    over_line = (smooth_path + path_deviation)[0]

    ax.plot(smooth_path, linewidth=2)
    ax.fill_between(
      path_deviation.index,
      under_line,
      over_line,
      alpha=.125
    )
    ax.set_title(class_name)


  def plot_prediction(data, model, title, ax):
    predictions, pred_losses = model_predict(model, [data])

    ax.plot(data, label='true')
    ax.plot(predictions[0], label='reconstructed')
    ax.set_title(f'{title} (loss: {np.around(pred_losses[0], 2)})')
    ax.legend()
    fig, axs = plt.subplots(
      nrows=2,
      ncols=6,
      sharey=True,
      sharex=True,
      figsize=(22, 8)
    )