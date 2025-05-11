import unittest
from PIL import Image
import io
from cv import predict
class TestPredict(unittest.TestCase):
    def setUp(self):
        # Load the test image and convert to bytes
        self.test_image_path ='./tests/test_image2.png'
        with open(self.test_image_path, 'rb') as f:
            self.test_bytes = f.read()
    def test_predict_class_name(self):
        # Call predict function with image bytes
        result = predict(self.test_bytes)
        # Assert the result is a non-empty string (class name)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        print(f"Predicted class name: {result}")
if __name__ == "__main__":
    unittest.main()