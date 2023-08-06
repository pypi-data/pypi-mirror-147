import tensorflow as tf

def get_lambda_args(
		cpt:int,
		model:tf.keras.Model):
	return model.get_config()['layers'][cpt]['inbound_nodes'][0][-1]['y']

def retrieve_layer_cpt(
		model:tf.keras.Model,
		layer_name:str
	)->int:
	"""
	"""
	for cpt, layer in enumerate(model.layers):
		if layer.name==layer_name:
			return cpt

def call_lambda_layer(
		layer_input:tf.Variable,
		model:tf.keras.Model,
		layer:tf.keras.layers.Layer,
		layer_cpt:int
	)->tf.Variable:
	"""
	this function deals with lambda layers
	the issue is : lambda layers often use parameters
	that are neither weights nor variable and are 
	only accessible in the mdoel config
	"""
	if (not isinstance(layer, tf.keras.layers.Lambda)
		and not ('lambda' in type(layer).__name__.lower())):
		output=layer(layer_input)
		return output
	if layer_cpt==-1:
		layer_cpt=retrieve_layer_cpt(
			model=model,
			layer_name=layer.name)
	y=get_lambda_args(
		cpt=layer_cpt,
		model=model)
	output=layer(layer_input, y)
	return output