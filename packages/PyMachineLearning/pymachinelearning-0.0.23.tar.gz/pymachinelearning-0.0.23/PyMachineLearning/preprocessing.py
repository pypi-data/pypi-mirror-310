################################################################################
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler, KBinsDiscretizer, StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.feature_selection import SelectFdr, SelectFpr, SelectKBest, SelectPercentile, f_regression, f_classif, mutual_info_classif, SequentialFeatureSelector
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA as PCA_sk
                          
################################################################################

class Imputer(BaseEstimator, TransformerMixin):

    def __init__(self, apply=True, method='simple_median', n_neighbors=4, n_nearest_features=4):
        self.apply = apply
        self.method = method
        self.n_neighbors = n_neighbors
        self.n_nearest_features = n_nearest_features

    def fit(self, X, y=None):

        if self.apply == True:

            if self.method in ['simple_mean', 'simple_median', 'simple_most_frequent']:
                 self.imputer_ = SimpleImputer(missing_values=np.nan, strategy='_'.join(self.method.split('_')[1:]))
            elif self.method == 'knn':
                 self.imputer_ = KNNImputer(n_neighbors=self.n_neighbors, weights="uniform")
            elif self.method in ['iterative_mean', 'iterative_median', 'iterative_most_frequent']:
                 # 'iterative_most_frequent' doesn't work as expected. It generates float values different from the uniques ones of the categorical variable on which it's applied.
                 self.imputer_ = IterativeImputer(initial_strategy='_'.join(self.method.split('_')[1:]), 
                                                  n_nearest_features=self.n_nearest_features, max_iter=25, random_state=123)
            else:
                 raise ValueError("Invalid method for imputation")
           
            self.imputer_.fit(X)
        return self

    def transform(self, X):
        
        if self.apply == True:
            X = self.imputer_.transform(X) # Output: numpy array
        return X

################################################################################
    
class Encoder(BaseEstimator, TransformerMixin):

    def __init__(self, method='ordinal', drop='first'): # drop=None to not remove any dummy
        self.method = method
        self.drop = drop

    def fit(self, X, y=None):

        if self.method == 'ordinal':
            self.encoder_ = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        elif self.method == 'one-hot':
            self.encoder_ = OneHotEncoder(drop=self.drop, handle_unknown='ignore', sparse_output=True)
        else:
            raise ValueError("Invalid method for encoding")
        
        self.encoder_.fit(X)
        return self

    def transform(self, X):
        
        if self.method == 'one-hot':
            # One-hot encoding gives an sparse matrix as output.
            # The output is transformed from sparse to dense matrix since this is usually required in sklearn.
            X = self.encoder_.transform(X).toarray() 
        else: 
            X = self.encoder_.transform(X)

        return X
    
    def get_feature_names_out(self, input_features=None):
        if self.method == 'one-hot':
            return self.encoder_.get_feature_names_out(input_features)
        else:
            return np.array(input_features)  # For ordinal encoding, return input features
        
################################################################################
    
class Scaler(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, method='standard'):
        
        self.apply = apply
        self.method = method

    def fit(self, X, y=None):
        
        if self.apply == True:
            if self.method == 'standard':
                self.scaler_ = StandardScaler(with_mean=True, with_std=True)
            elif self.method == 'min-max':
                self.scaler_ = MinMaxScaler(feature_range=(0, 1))
            self.scaler_.fit(X)

        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.scaler_.transform(X)
        return X 
    
################################################################################
    
class Discretizer(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, n_bins=3, strategy='quantile'):
        self.apply = apply
        self.n_bins = n_bins
        self.strategy = strategy

    def fit(self, X, y=None):
        
        if self.apply == True:
            self.discretizer_ = KBinsDiscretizer(encode='ordinal', n_bins=self.n_bins, strategy=self.strategy)
            self.discretizer_.fit(X)
        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.discretizer_.transform(X)
        return X 
    
################################################################################
    
class FeaturesSelector(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, method='Fdr', cv=3, k=5, percentile=50, n_neighbors=7, alpha=0.05, n_jobs=None):
        self.apply = apply
        self.method = method
        self.cv = cv # number of folds in cross_val_score for forward/backward algorithms.
        self.k = k # number of features to keep in SelectKBest. 
        self.percentile = percentile # percent of features to keep in SelectPercentile.
        self.n_neighbors = n_neighbors # used in forward/backward KNN.
        self.alpha = alpha
        self.n_jobs = n_jobs

    def fit(self, X, y):
        
        if self.apply == True:

            if self.method == 'Fdr_f_reg':
                self.features_selector_ = SelectFdr(f_regression, alpha=self.alpha)
            elif self.method == 'Fpr_f_reg':
                self.features_selector_ = SelectFpr(f_regression, alpha=self.alpha)
            elif self.method == 'KBest_f_reg':
                self.features_selector_ = SelectKBest(f_regression, k=self.k)
            elif self.method == 'Percentile_f_reg':
                self.features_selector_ = SelectPercentile(f_regression, percentile=self.percentile)  
            elif self.method == 'Fdr_f_class':
                self.features_selector_ = SelectFdr(f_classif, alpha=self.alpha)
            elif self.method == 'Fpr_f_class':
                self.features_selector_ = SelectFpr(f_classif, alpha=self.alpha)
            elif self.method == 'KBest_f_class':
                self.features_selector_ = SelectKBest(f_classif, k=self.k)
            elif self.method == 'Percentile_f_class':
                self.features_selector_ = SelectPercentile(f_classif, percentile=self.percentile)  
            elif self.method == 'KBest_mutual_class':
                self.features_selector_ = SelectKBest(mutual_info_classif, k=self.k)
            elif self.method == 'Percentile_mutual_class':
                self.features_selector_ = SelectPercentile(mutual_info_classif, percentile=self.percentile)

            elif self.method == 'forward_linear_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=LinearRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_linear_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=LinearRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'forward_knn_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsRegressor(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_knn_reg':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsRegressor(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs) 
            elif self.method == 'forward_knn_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsClassifier(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_knn_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=KNeighborsClassifier(n_neighbors=self.n_neighbors),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs) 
            elif self.method == 'forward_logistic':
                self.features_selector_ = SequentialFeatureSelector(estimator=LogisticRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_logistic':
                self.features_selector_ = SequentialFeatureSelector(estimator=LogisticRegression(),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'backward_trees_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=DecisionTreeClassifier(max_depth=4),
                                                                    n_features_to_select='auto',
                                                                    direction='backward', cv=self.cv, n_jobs=self.n_jobs)
            elif self.method == 'forward_trees_class':
                self.features_selector_ = SequentialFeatureSelector(estimator=DecisionTreeClassifier(max_depth=4),
                                                                    n_features_to_select='auto',
                                                                    direction='forward', cv=self.cv, n_jobs=self.n_jobs)
            else:
                raise ValueError("Invalid method for features selector")
        
            self.features_selector_.fit(X, y)
        
        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.features_selector_.transform(X)
        return X  
    
################################################################################

class PCA(BaseEstimator, TransformerMixin):

    def __init__(self, apply=False, n_components=2, random_state=123):
        
        self.apply = apply
        self.n_components = n_components
        self.random_state = random_state

    def fit(self, X, y=None):
        
        if self.apply == True:
            self.PCA_ = PCA_sk(n_components=self.n_components, random_state=self.random_state)
            self.PCA_.fit(X)

        return self
    
    def transform(self, X):
        
        if self.apply == True:
            X = self.PCA_.transform(X)
        return X 

################################################################################

'''
class ToPandas(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        """
        Transformer to convert NumPy array back to pandas DataFrame.
        
        Parameters:
        - columns: The list of column names to assign to the DataFrame
        """
        self.columns = columns

    def fit(self, X, y=None):
        """
        No fitting necessary for this transformer.
        """
        return self

    def transform(self, X):
        """
        Convert the NumPy array X to a pandas DataFrame with the given columns.
        
        Parameters:
        - X: NumPy array to convert to DataFrame
        
        Returns:
        - pandas DataFrame with the specified column names
        """
        return pd.DataFrame(X, columns=self.columns)
'''

################################################################################

def set_original_name_prot_attr_after_one_hot(prot_attr, X_pd):
    col0 = f'{prot_attr}_0'
    col1 = f'{prot_attr}_1'
    if col0 in X_pd.columns: # drop_first=False in one-hot encoding
        X_pd.drop(col0, axis=1)
    if col1 in X_pd.columns:              
        X_pd = X_pd.rename(columns={col1: prot_attr}) # rename col1 by prot_attr
    return X_pd

class ColumnTransformerToPandas(BaseEstimator, TransformerMixin):

    def __init__(self, column_transformer, prot_attr=None, prot_attr_index=True):
        """
        Transformer to convert NumPy array back to pandas DataFrame.
        
        Parameters:
        - column_transformer: The fitted ColumnTransformer from which to extract feature names dynamically.
        - quant_predictors: The original quant predictor names
        """
        self.column_transformer = column_transformer
        self.prot_attr = prot_attr
        self.prot_attr_index = prot_attr_index

    def fit(self, X, y=None):
        self.column_transformer.fit(X, y)
        return self

    def transform(self, X):

        self.quant_predictors = self.column_transformer.get_params()['transformers'][0][2]
        self.cat_predictors = self.column_transformer.get_params()['transformers'][1][2]
        
        try: # If a encoder is used, try, if not, pass.
            # Updating cat_predictors (only changes if one-hot is used)
            self.cat_predictors = self.column_transformer.named_transformers_['cat']['encoder'].encoder_.get_feature_names_out(self.cat_predictors).tolist()
        except:
            pass
        
        # Combine the quant and cat feature names
        predictors = self.quant_predictors + self.cat_predictors
        
        # Transforming X applying column_transformer
        X = self.column_transformer.transform(X)

        # Convert the transformed NumPy array to a DataFrame with the correct column names
        X_pd = pd.DataFrame(X, columns=predictors)
        
        # If one-hot is used the sensitive variable has a new name ('{prot_attr}_1'), so the original name is imposed
        # prot_attr is suppose to be a binary variable here
        if self.prot_attr is not None:

            # Recovering the original name of the prot_attr
            X_pd = set_original_name_prot_attr_after_one_hot(self.prot_attr, X_pd)

            # Setting the prot_attr as index (required by fairness post-processors)
            if self.prot_attr_index == True:
                X_pd.index = X_pd[self.prot_attr]
               
        return X_pd
    
################################################################################
    

################################################################################
    

################################################################################
    

################################################################################