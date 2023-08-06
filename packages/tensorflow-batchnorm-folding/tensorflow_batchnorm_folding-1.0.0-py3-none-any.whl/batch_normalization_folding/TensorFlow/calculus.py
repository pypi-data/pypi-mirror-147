import numpy as np

def fold_leaf_backward_conv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	new_W=(W / np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]]))
	gamma=np.tile(np.expand_dims(gamma, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	beta=np.tile(np.expand_dims(beta, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	mu=np.tile(np.expand_dims(mu, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	sigma=np.tile(np.expand_dims(sigma, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	new_b=b - np.sum(beta * W, axis = (0,1,2)) + np.sum(
		W*gamma*(mu / np.sqrt(sigma + 1.e-3)), axis = (0,1,2))
	return (new_W, new_b)

def fold_leaf_backward_dense(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W / np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=0),
		[W.shape[0], 1]))
	new_b=b - np.sum(beta * W, axis = 0) + np.sum(
		W*gamma*(mu / np.sqrt(sigma + 1.e-3)), axis = 0)
	return (new_W, new_b)

def fold_leaf_backward_depthwiseconv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W / np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, 1]))
	gamma=np.tile(np.expand_dims(gamma, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	beta=np.tile(np.expand_dims(beta, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	mu=np.tile(np.expand_dims(mu, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	sigma=np.tile(np.expand_dims(sigma, axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]])
	new_b=b - np.sum(beta * W, axis = (0,1,3)) + np.sum(
		W*gamma*(mu / np.sqrt(sigma + 1.e-3)), axis = (0,1,3))
	return (new_W, new_b)

def fold_leaf_backward_bn(
		gamma_:np.ndarray,
		beta_:np.ndarray,
		mu_:np.ndarray,
		sigma_:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_gamma=gamma_*np.sqrt(sigma + 1.e-3)/np.sqrt(sigma + 1.e-3) / gamma
	new_beta=beta_ + gamma_ * (mu*consec[1] - mu_)/np.sqrt(sigma_ + 1.e-3)
	new_mu=beta*consec[1]
	new_sigma=np.ones(shape=sigma_.shape) - 1.e-3
	return (new_gamma, new_beta, new_mu, new_sigma)

def fold_root_backward_conv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W * np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,2)),
		[W.shape[0], W.shape[1], W.shape[2], 1]))
	new_b=(gamma * (b - mu) / np.sqrt(sigma + 1.e-3)) + beta
	return (new_W, new_b)

def fold_root_backward_dense(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W * np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=0),
		[W.shape[0], 1]))
	new_b=(gamma * (b - mu) / np.sqrt(sigma + 1.e-3)) + beta
	return (new_W, new_b)

def fold_root_backward_depthwiseconv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W * np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]]))
	new_b=(gamma * (b - mu) / np.sqrt(sigma + 1.e-3)) + beta
	return (new_W, new_b)

def fold_root_backward_bn(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=gamma * (W / (sigma + 1.e-3))
	new_b=gamma * (b - mu) / (sigma + 1.e-3) + beta
	return (new_W, new_b)

def fold_leaf_forward_conv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W / np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,2)),
		[W.shape[0], W.shape[1], W.shape[2], 1]))
	new_b=(gamma * (b + mu) / np.sqrt(sigma + 1.e-3)) - beta
	return (new_W, new_b)

def fold_leaf_forward_depthwiseconv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W / np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, 1]))
	new_b=(gamma * (b + mu) / np.sqrt(sigma + 1.e-3)) - beta
	return (new_W, new_b)

def fold_leaf_forward_dense(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W / np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=0),
		[W.shape[0], 1]))
	new_b=(gamma * (b + mu) / np.sqrt(sigma + 1.e-3)) - beta
	return (new_W, new_b)

def fold_leaf_forward_bn(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	return (new_W, new_b)

def fold_root_forward_conv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W * np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, W.shape[3]]))	
	new_b=b + np.sum(np.tile(
		np.expand_dims(beta,axis=(0,1,3)), 
		[W.shape[0], W.shape[1], 1, W.shape[3]]) 
		* W, axis = (0,1,2)) - np.sum(
		W*np.tile(np.expand_dims(gamma*(mu / np.sqrt(sigma + 1.e-3)),
		axis=(0,1,3)), [W.shape[0], W.shape[1], 1, W.shape[3]]), 
		axis = (0,1,2))
	return (new_W, new_b)

def fold_root_forward_depthwiseconv(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W * np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=(0,1,3)),
		[W.shape[0], W.shape[1], 1, 1]))
	new_b=b + np.sum(beta * W, axis = (0,1,3)) - np.sum(
		W*gamma*(mu / np.sqrt(sigma + 1.e-3)), axis = (0,1,3))
	return (new_W, new_b)

def fold_root_forward_dense(
		W:np.ndarray,
		b:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	new_W=(W * np.tile(
		np.expand_dims(gamma / np.sqrt(sigma + 1.e-3), axis=1),
		[1, W.shape[1]]))
	new_b=b + np.sum(np.tile(np.expand_dims(beta,axis=1),
		[1, W.shape[1]]) * W, axis = 0) - np.sum(
		W*np.tile(np.expand_dims(gamma*(mu / np.sqrt(sigma + 1.e-3)),
		axis=1), [1, W.shape[1]]), axis = 0)
	return (new_W, new_b)

def fold_root_forward_bn(
		gamma_:np.ndarray,
		beta_:np.ndarray,
		mu_:np.ndarray,
		sigma_:np.ndarray,
		gamma:np.ndarray,
		beta:np.ndarray,
		mu:np.ndarray,
		sigma:np.ndarray
	)->(np.ndarray,np.ndarray):
	"""
	"""
	return (new_W, new_b)