from typing import List, Dict, Any
from skl2onnx.common.data_types import FloatTensorType, StringTensorType,DoubleTensorType, Int64TensorType,Int32TensorType,BooleanTensorType
import numpy as np
from enum import Enum
from copy import deepcopy
import json
import os
import PIL

class ModelifyInputs:
    def __init__(self):
        self.sample = None

    def add_sample(self, sample):
        self.sample = sample
        
class InputType(Enum):

    def __new__(cls, value, numpy_type, onnx_type ):
        t = object.__new__(cls)
        t._value_ = value
        t._numpy_type = numpy_type
        t._onnx_type = onnx_type
        return t

    
    integer = (1, np.dtype("int32"), Int32TensorType([None, 1]))
    # double = (2, np.dtype("float64"), DoubleTensorType([None, 1])) # onnx doesnt support DoubleTensorType yet
    long = (3, np.dtype("int64"), Int64TensorType([None, 1]))
    float = (4, np.dtype("float32"), FloatTensorType([None, 1]))
    string = (5, np.dtype("str"), StringTensorType([None, 1]))
    boolean = (6, np.dtype("bool"), BooleanTensorType([None, 1]))

    def __repr__(self):
        return self.name

    def to_numpy(self) -> np.dtype:
        return self._numpy_type

    def to_onnx(self):
        return self._onnx_type
    
    
class Column(object):
    def __init__(self, name, input_type):
        self.name = name
        try:
            self.input_type = InputType[input_type] if isinstance(input_type, str) else input_type
        except KeyError:
            raise Exception("Unsupported type '{0}', expected inputs: {1}".format(input_type, [i.name for i in InputType]))
        if not isinstance(self.input_type, InputType):
            raise TypeError("Expected InputType")
        
    def to_dict(self):
        return {"name": self.name, "type": self.input_type.name}


class Image(ModelifyInputs):
    def __init__(self, width:int, height:int, channel=3):
        self.type = "IMAGE"
        self.width = width
        self.height = height
        self.channel = channel
        super().__init__()

    def to_list(self):
        return [{"width": self.width,  "height": self.height, "channel": self.channel}]

    def read_image(self, image_url: str, format="RGB"):
        try:
            image = PIL.Image.open(image_url).convert(format)
            return image
        except Exception as ex:
            print(str(ex), has_pii=True)

    def get_input_for_model(self, preprocess=False, image_source=None):
        if image_source is None:
            if self.sample is None:
                raise Exception("No sample image provided")
            image_source = os.path.join(os.getcwd(), self.sample)
        if self.channel == 1:
            img = self.read_image(image_source, format="L")
        else:
            img = self.read_image(image_source)
        if not preprocess:
            img = np.array(img.resize((self.width, self.height)))
            img = img / 255.0
            img = img.astype(np.float32)
            img = np.expand_dims(img, 0)   
        return img 

    
class Tabular(ModelifyInputs):
    def __init__(self, inputs: List[Column]):
        self.type = "TABULAR"
        if not (
            all(map(lambda x: isinstance(x, Column), inputs))
        ):
            raise Exception(
                "List should include Column"
            )

        self.inputs = inputs
    
    def convert_onnx(self):
        result = list(map(lambda x: (x.name,x.input_type.to_onnx()), self.inputs))

        result = []
        selector = None
        for input in self.inputs:
            if selector != input.input_type:
                selector = input.input_type
                onnx_input_name = f"{input.input_type.name}_{len(result)}"
                onnx_type = deepcopy(input.input_type.to_onnx())
                result.append((onnx_input_name, onnx_type ))
            else:
                result[-1][1].shape[1] += 1

        return result

    def to_json(self) -> str:
        return json.dumps([x.to_dict() for x in self.inputs])

    def to_list(self) -> List[Dict[str, Any]]:
        return [x.to_dict() for x in self.inputs]

       