from batch_normalization_folding.TensorFlow.tf_bn_fold import fold_tensorflow_model
import tensorflow as tf
from typing import Any
import sys

def fold_batchnormalization_layers(
		model:Any,
		verbose:bool
	)->(Any, str):
	"""
	Performs the update of the model for batch norm folding
	"""
	if (isinstance(model,tf.keras.Model) 
		and not isinstance(model,tf.keras.Sequential)):
		return fold_tensorflow_model(
			model=model,
			verbose=verbose)
	else:
		print(f'\rRequested model type is not supported yet.'
			f' Type is {type(model)}.')
		return model, 'failed'