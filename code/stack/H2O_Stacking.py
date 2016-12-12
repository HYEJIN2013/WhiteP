import h2o
from h2o.estimators.glm import H2OGeneralizedLinearEstimator



def make_Z(models):
	'''
	Takes a list of models and creates level-one data
	'''

	# Map over base learners
	cvpreds_list = map(lambda model: get_cvpreds(model), models)
	model_ids = map(lambda model: model.model_id, models)

	# cbind all the cvpred cols
	Z = reduce(lambda x,y: x.cbind(y), cvpreds_list)
	Z.columns = model_ids

	return Z


def get_cvpreds(model):

	V = model.nfolds
	family = "binomial"
	#cvpred_list =  model._model_json['output']['cross_validation_predictions']
	if family == "binomial":
		cvpred_fold_list = map(lambda v: h2o.get_frame(model._model_json['output']['cross_validation_predictions'][v]['name'])[2], range(V))
	elif family == "gaussian":
		# TO DO: Check that this is working
		cvpred_fold_list = map(lambda v: h2o.get_frame(model._model_json['output']['cross_validation_predictions'][v]['name'])[0], range(V))
	else:
		print "TO DO: Multinomial"
	# once we change the constructor, the following command should work...
	#cvpred_sparse = h2o.H2OFrame(cvpred_list)
	cvpred_sparse = reduce(lambda x,y: x.cbind(y), cvpred_fold_list)

	# Rowsum across folds (columns) to get cvpreds
	cvpreds = cvpred_sparse.apply(fun=lambda row: row.sum(), axis=1)

	return cvpreds


def stack(models,
	metalearner,
	response_frame,
	cvpreds_frame=None,
	seed=1,
	keep_levelone_data=True):
	''' Given a set of cross-validated models, stack them into 
	a Super Learner ensemble using the specified metalearner.
	- models: list of H2O models trained and xval with same folds
	- metalearner: an untrained H2O model (with)
	- response_frame: H2OFrame of the response with a single column
	- cvpreds_frame: An H2OFrame object containing the cross-validation holdout predictions for each of the base learners.
	'''

	# Add the rest of the functionality
	# Add a bunch of tests to make sure data types are correct

	# Create levelone frame
	Z = make_Z(models)
	levelone = Z.cbind(response_frame)
	levelone.set_name(col=Z.ncol, name='y')
	#this updates columns, but does not update the actual colnames??

	metalearner.train(x=Z.columns, y='y', training_frame=levelone)

	return metalearner
	# TO DO: Update this return object of class H2OSuperLearner/H2OEnsemble/H2OStack


def metapredict(models, metafit, test_data):
	'''
	Generate the predictions on the base learners and metalearner.
	'''
	
	# Generate preds for the base learners
	pred_list = map(lambda model: model.predict(test_data), models)
	if (metafit.family == 'binomial'):  #this will only work for binomial, need to update
		pred_cols = map(lambda pp: pp[2], pred_list)
	elif (metafit.family == 'gaussian'):
		pred_cols = map(lambda pp: pp[0], pred_list)
	else:
		print "Multinomial not yet implemented"

	basepred = reduce(lambda x,y: x.cbind(y), pred_cols)
	basepred.columns = map(lambda model: model.model_id, models) # names of the models (design-matrix-for-metalearner names)

	# Using the base learner predictions
	pred = metafit.predict(test_data=basepred)
	
	# This is currently not implemented, use sklearn auc utility function now
	#perf = metafit.model_performance(test_data=basepred)
	#perf.auc()

	#return perf, pred, basepred
	return pred, basepred


# TO DO: Update this
# Probably we should return only the SuperLearner predictions
# rather than a 2-element list containing preds and basepreds
#def predict(H2OSuperLearner, test_data):
#	'''
#	Generate the Super Learner predictions.
#	'''
