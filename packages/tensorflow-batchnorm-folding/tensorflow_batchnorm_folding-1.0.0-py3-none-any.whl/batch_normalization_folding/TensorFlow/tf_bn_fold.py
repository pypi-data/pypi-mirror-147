from batch_normalization_folding.TensorFlow.back_forth import (
	check_layer)
from batch_normalization_folding.TensorFlow.modify_bn_graph import (
	remove_folded_layers)
from batch_normalization_folding.TensorFlow.add_biases import (
	complete_model,
	check_if_need_completion)
from batch_normalization_folding.TensorFlow.update_fold_weights import (
	fold_weights)
from batch_normalization_folding.TensorFlow.deep_copy import deep_copy_a_model
from typing import Dict
import tensorflow as tf

def get_graph_as_dict(
		model:tf.keras.Model
	)->Dict[str,list]:
	"""
	This function returns a dictionnary of the layers and their corresponding
	input layers.
	"""
	network_dict = {model.layers[0].name:[]}
	for layer in model.layers:
		for node in layer._outbound_nodes:
			layer_name = node.outbound_layer.name
			if layer_name not in network_dict:
				network_dict.update(
					{layer_name: [layer.name]})
			else:
				if layer.name not in  network_dict[layer_name]:
					network_dict[layer_name].append(layer.name)
	return network_dict

def reverse_graph(
		graph:Dict[str,list]
	)->Dict[str,list]:
	"""
	This function fetches the output layers of each layer of the DNN
	"""
	output_dict={}
	for key_1 in list(graph.keys()):
		for key_2 in graph[key_1]:
			if key_2 not in output_dict:
				output_dict.update(
						{key_2: [key_1]})
			else:
				if key_1 not in output_dict[key_2]:
					output_dict[key_2].append(key_1)
	output_dict[list(graph.keys())[-1]]=[]
	return output_dict

def fold_tensorflow_model(
		model:tf.keras.Model,
		verbose:bool
	)->(tf.keras.Model, str):
	"""
	In this functio nwe fold the model
	But we also update the batchnorm statistics adequately
	"""
	model_to_fold=deep_copy_a_model(model=model)
	backward_graph=get_graph_as_dict(model=model_to_fold)
	forward_graph=reverse_graph(graph=backward_graph)
	fold_dict={}
	unfolded_layers=0
	for layer in model_to_fold.layers:
		if isinstance(layer, tf.keras.layers.BatchNormalization):
			foldeable, roots, leaves, forward=check_layer(
				model=model_to_fold,
				layer=layer,
				forward_graph=forward_graph,
				backward_graph=backward_graph)
			if foldeable:
				fold_dict[layer.name]=(roots, leaves, forward)
			else:
				unfolded_layers+=1
	layers_to_complete=check_if_need_completion(
		model=model, 
		fold_dict=fold_dict)
	if verbose:
		print('\r+'+'-'*36+'+')
		print(f'| {model.name.center(34)} |')
		print('\r+'+'-'*36+'+')
		print(f'| BN layers folded         | '
			f'{f"{len(fold_dict)}".center(7):<7} |')
		print(f'| BN layers not folded     | '
			f'{f"{unfolded_layers}".center(7):<7} |')
		print('+'+'-'*36+'+')
	if len(layers_to_complete)!=0:
		model_to_fold=complete_model(
			model=model_to_fold,
			layers_to_complete=layers_to_complete)
	fold_weights(
		model=model_to_fold,
		fold_dict=fold_dict)
	model_to_fold=remove_folded_layers(
		model=model_to_fold,
		backward_graph=backward_graph,
		fold_dict=fold_dict)
	return model_to_fold, f'{len(fold_dict)}/{unfolded_layers}'