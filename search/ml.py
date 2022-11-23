import numpy as np
from keras.models import load_model
from django.conf import settings


class BeerModel:
    def __init__(self, model_path, style_names_path):
        self.model = load_model(model_path)
        print(f"loaded model from {model_path}")

        with open(style_names_path, "rt", encoding="utf8") as f:
            self.feature_style_names = f.read().splitlines()
        print(f"loaded style names from {style_names_path}")

    def predict(self, user_feature):
        if not (isinstance(user_feature, list) and len(user_feature) == 5):
            raise ValueError(f"Invalid user_feature : {user_feature}")

        # user_feature example : [0.2, 0.4, 0.6, 0.8, 1]

        data = np.array(user_feature).reshape(1, 5)
        ma_predict = self.model.predict(data)  # 범주형 결과
        final_ma_predict = np.argmax(ma_predict, axis=-1)  #수치형 결과
        index = final_ma_predict[0]
        return self.feature_style_names[index]


beer_model = BeerModel(settings.BEER_MODEL_PATH, settings.BEER_STYLE_NAMES_PATH)
