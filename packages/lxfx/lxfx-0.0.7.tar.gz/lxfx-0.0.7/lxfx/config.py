import json
import os

class XFXConfig:
    """
    This class generates the configuration data for the XFX model.
    Configure the model that is going to be instantiated by the XFX class. This can be either of the following:
    1. FxFCModel
    2. FxFCEncoder
    3. FxFCDecoder
    4. FxFCAutoEncoder
    Specify the model type by the model_type parameter in the XFX class and the class shall
    automatically load the appropriate configuration data and model for that type.
    If the project directory specified is already an XFX project then it is loaded as a project with
    existing configurations, models and all information saved during the previous runs.
    """
    def __init__(self, dump_dir = None, config_file_path = None):
        self.dump_dir = dump_dir
        self.config_file_path = config_file_path
        self.config_dict = {
            "FCBlock": {
                "in_features": None,
                "hidden_size": None,
                "out_size": None,
                "nature": "lstm",
                "dropout": 0.2,
                "num_layers": 1,
                "bidirectional": False,
                "activation": "tanh",
                "use_batch_norm": False,
                "pass_block_hidden_state": False
            },
            "FxFCModel": {
                "num_features": None,
                "block_type": "lstm",
                "out_features": 1,
                "units": None,
                "comment0": "The length of the units array is equal to the number or fxfc blocks",
                "num_layers": 1,
                "is_encoder": False,
                "encoder_latent_dim": None,
                "is_decoder": False,
                "comment1": "The number of out_units MUST be equal to the number of units",
                "out_units": None,
                "comment2": "Once the out_units is set then pass_block_hidden_states must be false beucase the first layer shall have a hidden state whose shape is different from the next layer's hidden state shape",
                "activation": "tanh",
                "bidirectional": False,
                "pass_states": False,
                "comment": "use_batch_norm is a MUST if the data is forex data",
                "use_batch_norm": False,
                "pass_block_hidden_state": False,
                "decoder_out_features": None
            },
            "FxFCEncoder": {
                "num_features": None,
                "block_type": None,
                "units": None,
                "out_units": None,
                "num_layers": 1,
                "activation": "tanh",
                "latent_dim": None,
                "use_batch_norm": False,
                "bidirectional": False
            },
            "FxFCDecoder": {
                "latent_dim": None,
                "target_features": 1,
                "block_type": None,
                "units": None,
                "out_units": None,
                "num_layers": 1,
                "activation": "tanh",
                "use_batch_norm": False,
                "initialize_weights": False,
                "initializer_method": None
            },
            "FxFCAutoEncoder": {
                "num_features": None,
                "target_features": 1,
                "future_pred_length": 1,
                "block_types": ["lstm", "lstm"],
                "comment0": "The current configuration requires that the hidden size of the last layer of the encoder and the first layer of the decoder are the same.",
                "units": [None, None],
                "comment1": "Once the out_units is set then pass_block_hidden_states must be false beucase the first layer shall have a hidden state whose shape is different from the next layer's hidden state shape",
                "out_units": [None, None],
                "num_layers": [1, 1],
                "activations": ["tanh", "tanh"],
                "latent_dim": 32,
                "dropout": [0.2, 0.2],
                "bidirectional": [False, False],
                "use_batch_norm": [False, False],
                "pass_states": [True, True],
                "pass_block_hidden_state": [False, False],
                "is_attentive": False
            },
            "TimeSeriesDatasetManager": {
                "file_path": None,
                "future_pred_length": 1,
                "targetIndices": None,
                "target_names": None,
                "drop_names": None,
                "date_col": None,
                "sequence_length": 5,
                "test_sequence_length": 2,
                "is_autoregressive": False,
                "stride": 1,
                "scaler_feature_range": [0, 1],
                "transform": None,
                "use_default_scaler": True,
                "split_criterion": [0.7, 0.15, 0.15],
                "batchsize": None,
                "is_fx": False,
                "transform_targets": True,
                "index_col": None,
                "manual_seed": None,
                "test_stride": None
            },
            "ModelTrainer": {
                "loss_fn": None,
                "optmizer": None,
                "epochs": 3,
                "accuracy_fn": None,
                "lr": 0.001,
                "project_path": None,
                "is_logging": True,
                "resume": False,
                "targets_transformed": False
            },
            "TensorInitializer": {
                "method": None
            }
        }

    def get_config_dict(self):
        return self.config_dict

    def dump_config_file(self): # Write the dictionary to a JSON file
        filepath = "config.json"
        if self.dump_dir:
            filepath = os.path.join(self.dump_dir, filepath)
        elif self.config_file_path:
            filepath = self.config_file_path
        with open(filepath, 'w') as json_file:
            json.dump(self.config_dict, json_file, indent=4)
