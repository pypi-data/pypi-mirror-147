#### Written by
#### John Park 
#### LR Tuner 
#### 1. Find range of LR using line search
#### 2. model fit method to obtain validation and training losses 
import tensorflow as tf

class LRSearch(tf.keras.optimizers.schedules.LearningRateSchedule):
    
  def __init__(
      self,
      initial_learning_rate, #integer
      maximal_learning_rate,
      step_size,
      name="LRsearch"):
    
    super(LRSearch, self).__init__() #what does this do???

    self.initial_learning_rate = initial_learning_rate
    self.maximal_learning_rate = maximal_learning_rate
    self.step_size = step_size
    self.name = name

  def __call__(self, step):
     with tf.name_scope(self.name or "LRsearch") as name:
      initial_learning_rate = tf.convert_to_tensor(
          self.initial_learning_rate, name="initial_learning_rate")
      dtype = initial_learning_rate.dtype
      maximal_learning_rate = tf.cast(self.maximal_learning_rate, dtype)
      step_size = tf.cast(self.step_size, dtype)
      x = tf.cast(step, dtype)
      
      return initial_learning_rate * 10 ** ( tf.experimental.numpy.log10(maximal_learning_rate/initial_learning_rate) * x / step_size)
        # this should be changed to np.exp ** (tf.log(...))


class LossHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.history2 = {'loss':[],'val_loss':[]}

    def on_batch_end(self, batch, logs={}):
        self.history2['loss'].append(logs.get('loss'))

    def on_epoch_end(self, epoch, logs={}):
        self.history2['val_loss'].append(logs.get('val_loss'))

class SaveBatchLoss(tf.keras.callbacks.Callback):
    def on_train_batch_end(self, batch, logs=None):

        batch_end_loss.append(logs['loss'])

class LossAndErrorPrintingCallback(tf.keras.callbacks.Callback):
    def on_train_batch_end(self, batch, logs=None):
        print(
            "Up to batch {}, the average loss is {:7.2f}.".format(batch, logs["loss"])
        )

    def on_test_batch_end(self, batch, logs=None):
        print(
            "Up to batch {}, the average loss is {:7.2f}.".format(batch, logs["loss"])
        )


class Search_LR(tf.keras.Model):
  
  def __init__(
      self,
      train_ds, #integer
      validation_ds,
      initial_learning_rate,
      maximum_learning_rate,
      STEPS_PER_EPOCH,
      ModelObj,
      name="Search_LR"):
    
    super(Search_LR, self).__init__() #what does this do???

    self.tr_ds = train_ds
    self.vali_ds = validation_ds
    self.iLR = initial_learning_rate
    self.mLR = maximum_learning_rate
    self.model = ModelObj
    self.name = name
    self.spEpoch = STEPS_PER_EPOCH
    self.LRschedule = LRSearch(
      initial_learning_rate = self.iLR,
      maximal_learning_rate = self.mLR,
      step_size =  self.spEpoch,
      name = 'LRSearch'
      )

  def __call__(self,N_incre, callbackclass=LossHistory()):
    #how can function take callbackclass as argument??
    #batch_end_loss = list() 

    historylog = callbackclass
    
    history = self.model.fit(
      self.tr_ds, 
      epochs= N_incre,
      steps_per_epoch = int(self.spEpoch/N_incre), #Change this to round - up
      validation_data = self.vali_ds,
      callbacks = [historylog],
      verbose=1)

    return history, historylog
