# import sys
# import torch
# import pandas as pd
# import numpy as np
# from torch.utils.data import DataLoader, TensorDataset
# import pkg_resources
# from .dataloader import DataProcessor
# from .model import CNNGRUClassificationModel  # 모델 클래스 명확히 지정

# class Predictor:
#     def __init__(self, device=None, model_path=None):
#         # device가 None이면 GPU가 가능한지 확인하여 자동 설정
#         self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device

#         # model_path가 None이면 기본 경로로 설정
#         if model_path is None:
#             model_path = pkg_resources.resource_filename('saferx', 'model2/model/final_model_converted.pth')

#         # seq_cols 및 target_cols 정의
#         self.seq_cols = [
#             'Daily_Entropy', 'Normalized_Daily_Entropy', 'Eight_Hour_Entropy', 'Normalized_Eight_Hour_Entropy',
#             'first_TOTAL_ACCELERATION', 'Location_Variability', 'last_TOTAL_ACCELERATION', 'mean_TOTAL_ACCELERATION',
#             'median_TOTAL_ACCELERATION', 'max_TOTAL_ACCELERATION', 'min_TOTAL_ACCELERATION', 'std_TOTAL_ACCELERATION',
#             'nunique_TOTAL_ACCELERATION', 'delta_CALORIES', 'first_HEARTBEAT', 'last_HEARTBEAT', 'mean_HEARTBEAT',
#             'median_HEARTBEAT', 'max_HEARTBEAT', 'min_HEARTBEAT', 'std_HEARTBEAT', 'nunique_HEARTBEAT',
#             'delta_DISTANCE', 'delta_SLEEP', 'delta_STEP', 'sex', 'age', 'place_Unknown', 'place_hallway', 'place_other', 'place_ward'
#         ]
#         self.target_cols = ['BPRS_change', 'YMRS_change', 'MADRS_change', 'HAMA_change']

#         # CNNGRUClassificationModel의 구조를 초기화하고 가중치를 로드
#         self.model = CNNGRUClassificationModel(input_dim=31, cnn_out_channels=256, cnn_kernel_size=4, gru_hidden_dim=64, output_dim=4, dropout_prob=0.5)
#         self.load_model(model_path)
#         self.model.to(self.device)
#         self.model.eval()

#     def load_model(self, model_path):
#         """
#         변환된 .pth 파일로부터 state_dict를 로드합니다.
#         """
#         # state_dict를 로드하여 모델에 적용
#         state_dict = torch.load(model_path, map_location=self.device)
#         self.model.load_state_dict(state_dict)

#     def preprocess_data(self, data_path):
#         data = pd.read_csv(data_path)
#         data = DataProcessor.preprocess_data(data)
#         data = DataProcessor.reset_week_numbers(data)
#         data = DataProcessor.transform_target(data)

#         max_length = DataProcessor.find_max_sequence_length_by_week(data, self.seq_cols)
#         results = DataProcessor.prepare_data_for_model_by_week(data, max_length, self.seq_cols, self.target_cols)
#         X_tensor, _ = DataProcessor.convert_results_to_tensors(results)
#         return DataLoader(TensorDataset(X_tensor), batch_size=16, shuffle=False)

#     def predict(self, data_loader):
#         predictions = []
#         with torch.no_grad():
#             for inputs in data_loader:
#                 inputs = inputs[0].to(self.device)
#                 outputs = self.model(inputs)
#                 binary_predictions = (outputs >= 0.5).cpu().numpy()
#                 predictions.extend(binary_predictions)

#         return np.array(predictions)

#     def save_predictions(self, predictions, output_path):
#         df = pd.DataFrame(predictions, columns=self.target_cols)
#         df.to_csv(output_path, index=False)
#         print(f'Predictions saved at {output_path}')
# import torch
# import pandas as pd
# from torch.utils.data import DataLoader, TensorDataset
# import pkg_resources
# from .dataloader import DataProcessor
# from .model import CNNGRUModel

# class Predictor:
#     def __init__(self, device=None, model_path=None):
#         self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device
#         # model_path = model_path or pkg_resources.resource_filename('saferx', 'model2/model/final_model_converted.pth')
#         model_path = model_path or pkg_resources.resource_filename('saferx', 'model2/model/model.pth')
#         self.seq_cols = [
#             'Daily_Entropy', 'Normalized_Daily_Entropy', 'Eight_Hour_Entropy', 'Normalized_Eight_Hour_Entropy',
#             'first_TOTAL_ACCELERATION', 'Location_Variability', 'last_TOTAL_ACCELERATION', 'mean_TOTAL_ACCELERATION',
#             'median_TOTAL_ACCELERATION', 'max_TOTAL_ACCELERATION', 'min_TOTAL_ACCELERATION', 'std_TOTAL_ACCELERATION',
#             'nunique_TOTAL_ACCELERATION', 'delta_CALORIES', 'first_HEARTBEAT', 'last_HEARTBEAT', 'mean_HEARTBEAT',
#             'median_HEARTBEAT', 'max_HEARTBEAT', 'min_HEARTBEAT', 'std_HEARTBEAT', 'nunique_HEARTBEAT',
#             'delta_DISTANCE', 'delta_SLEEP', 'delta_STEP', 'sex', 'age', 'place_Unknown', 'place_hallway', 'place_other', 'place_ward'
#         ]

#         # self.model = CNNGRUClassificationModel(input_dim=31, cnn_out_channels=256, cnn_kernel_size=4, gru_hidden_dim=64, output_dim=4, dropout_prob=0.5)
#         self.model  = CNNGRUModel(input_dim=31,cnn_out_channels=256, cnn_kernel_size=4, gru_hidden_dim=64, output_dim=4, dropout_prob=0.5)
#         self.load_model(model_path)
#         self.model.to(self.device)
#         self.model.eval()

#     def load_model(self, model_path):
#         state_dict = torch.load(model_path, map_location=self.device)
#         self.model.load_state_dict(state_dict)

#     def preprocess_data(self, data_path):
#         data = pd.read_csv(data_path)
#         data = DataProcessor.preprocess_data(data)
#         data = DataProcessor.reset_week_numbers(data)

#         max_length = DataProcessor.find_max_sequence_length_by_week(data, self.seq_cols)
#         results = DataProcessor.prepare_data_for_model_by_week(data, max_length, self.seq_cols)
#         X_tensor = DataProcessor.convert_results_to_tensors(results)
#         return DataLoader(TensorDataset(X_tensor), batch_size=16, shuffle=False)

#     def predict(self, data_loader):
#         """
#         데이터 로더를 사용하여 예측 점수를 계산합니다.
#         """
#         scores = []
#         with torch.no_grad():
#             for inputs in data_loader:
#                 inputs = inputs[0].to(self.device)
#                 outputs = self.model(inputs)  # 모델 출력 그대로 사용
#                 scores.extend(outputs.cpu().numpy())  # 점수 리스트에 추가

#         return scores
import torch
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
import pkg_resources
from .dataloader import DataProcessor
from .model import CNNGRUModel
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Predictor:
    def __init__(self, device=None, model_path=None, scaler=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device
        model_path = model_path or pkg_resources.resource_filename('saferx', 'model2/model/model.pth')

        # Feature and target columns
        self.seq_cols = [
          'Daily_Entropy', 'Normalized_Daily_Entropy', 'Eight_Hour_Entropy',
       'Normalized_Eight_Hour_Entropy', 'first_TOTAL_ACCELERATION','Location_Variability',
       'last_TOTAL_ACCELERATION', 'mean_TOTAL_ACCELERATION',
       'median_TOTAL_ACCELERATION', 'max_TOTAL_ACCELERATION',
       'min_TOTAL_ACCELERATION', 'std_TOTAL_ACCELERATION',
       'nunique_TOTAL_ACCELERATION', 'delta_CALORIES', 'first_HEARTBEAT', 'last_HEARTBEAT',
       'mean_HEARTBEAT', 'median_HEARTBEAT', 'max_HEARTBEAT', 'min_HEARTBEAT',
       'std_HEARTBEAT', 'nunique_HEARTBEAT', 'delta_DISTANCE', 'delta_SLEEP',
       'delta_STEP','sex', 'age', 'place_Unknown', 'place_hallway',
       'place_other', 'place_ward'
        ]
        self.target_cols = ['BPRS_sum', 'YMRS_sum', 'MADRS_sum', 'HAMA_sum']

         # Include target columns in seq_cols if not already included
        for col in self.target_cols:
            if col not in self.seq_cols:
                self.seq_cols.append(col)


        # Initialize the model with input_dim dynamically set to len(self.seq_cols)
        self.model = CNNGRUModel(
            input_dim=35,
            cnn_out_channels=256,
            cnn_kernel_size=4,
            gru_hidden_dim=64,
            output_dim=len(self.target_cols),
            dropout_prob=0.5
        )
        self.load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

        # Define the scaler
        self.scaler = scaler or MinMaxScaler(feature_range=(-1, 1))
    def load_model(self, model_path):
        """
        Load the model state_dict from the .pth file.
        """
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)

    def preprocess_data(self, data_path):
        """
        Preprocess the input data and fit the scaler.
        """
        data = pd.read_csv(data_path)
        data = DataProcessor.preprocess_data(data)
        print("Processed columns:", data.columns.tolist())

        # Ensure seq_cols match with available data columns
        available_cols = data.columns.tolist()
        missing_cols = [col for col in self.seq_cols if col not in available_cols]
        if missing_cols:
            raise ValueError(f"Missing columns in data: {missing_cols}")

        # Identify numeric features and fit the scaler
        numeric_features = self.seq_cols
        self.scaler.fit(data[numeric_features])  # Fit the scaler
        data[numeric_features] = self.scaler.transform(data[numeric_features])  # Apply scaling

        # Reset week numbers and prepare data
        data = DataProcessor.reset_week_numbers(data)
        max_length = DataProcessor.find_max_sequence_length_by_week(data, self.seq_cols)
        results = DataProcessor.prepare_data_for_model_by_week(data, max_length, self.seq_cols)
        X_tensor = DataProcessor.convert_results_to_tensors(results)
        return DataLoader(TensorDataset(X_tensor), batch_size=16, shuffle=False)
    def predict_with_rescaling_and_clipping(self, data_loader):
        """
        Perform prediction, rescale, and clip the values within target ranges.
        """
        # Ensure scaler is fitted before using
        if not hasattr(self.scaler, "data_min_"):
            raise ValueError("Scaler has not been fitted. Ensure preprocess_data() is called before this method.")

        # Define target ranges
        target_ranges = {
            'BPRS_sum': (0, 108),
            'YMRS_sum': (0, 60),
            'MADRS_sum': (0, 60),
            'HAMA_sum': (0, 50)
        }

        # Perform predictions
        self.model.eval()
        predictions = []
        with torch.no_grad():
            for inputs in data_loader:
                inputs = inputs[0].to(self.device)
                outputs = self.model(inputs)
                predictions.extend(outputs.cpu().numpy())

        predictions = np.array(predictions)

        # Create a full feature array for inverse transformation
        num_features = len(self.seq_cols)  # scaler input dim
        predictions_full = np.zeros((predictions.shape[0], num_features))

        # Place predictions into their respective target column positions
        target_indices = [self.seq_cols.index(col) for col in self.target_cols]
        for i, idx in enumerate(target_indices):
            predictions_full[:, idx] = predictions[:, i]

        # Inverse transform predictions
        predictions_rescaled_full = self.scaler.inverse_transform(predictions_full)
        predictions_rescaled = predictions_rescaled_full[:, target_indices]

        # Clip predictions within target ranges
        for i, target_name in enumerate(self.target_cols):
            min_val, max_val = target_ranges[target_name]
            predictions_rescaled[:, i] = np.clip(predictions_rescaled[:, i], min_val, max_val)

        return predictions_rescaled
