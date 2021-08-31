import torchvision.transforms.functional as TF
import torch.nn.functional as F
from model.model import UNet
from PIL import Image
import numpy as np
import random
import torch

BINARY_MODEL_WEIGHTS = 'model/weights/binary.pth'
MULTILABEL_MODEL_WEIGHTS = 'model/weights/multilabel.pth'

class ModelUtils():
    def __init__(self):
        # define models
        self.binary_model = UNet(n_channels=2, n_classes=1)
        self.multilabel_model = UNet(n_channels=2, n_classes=7)

        # use model on the right device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.binary_model.to(device=self.device)
        self.multilabel_model.to(device=self.device)

        # load weights
        self.binary_model.load_state_dict(torch.load(BINARY_MODEL_WEIGHTS, map_location=self.device))
        self.multilabel_model.load_state_dict(torch.load(MULTILABEL_MODEL_WEIGHTS, map_location=self.device))

    def _get_mask(self, model, image):
        model.eval()

        img = self._process_image(image)

        img = img.unsqueeze(0)
        img = img.to(device=self.device, dtype=torch.float32)

        with torch.no_grad():
            output = model(img)
            if model.n_classes > 1:
                probs = F.softmax(output, dim=1)
            else:
                probs = torch.sigmoid(output)
            probs = probs.squeeze(0)
            full_mask = probs.squeeze().cpu().numpy()
        return full_mask > 0.5

    def _process_image(self, image):
        angle = 0
        dx, dy = 0, 0
        scale = 1
        shear = 0

        image[0] = TF.affine(Image.fromarray(image[0]), angle=angle, translate=[dx, dy], scale=scale, shear=shear)
        image[1] = TF.affine(Image.fromarray(image[1]), angle=angle, translate=[dx, dy], scale=scale, shear=shear)

        image = torch.tensor(image)
        image = TF.normalize(image, mean=[image[0].mean(), image[1].mean()], std=[image[0].std(), image[1].std()])

        # noise = 0.1 * torch.randn(2, 512, 512)
        
        return image

    def binary_pred(self, image):
        return self._get_mask(self.binary_model, image)

    def multilabel_pred(self, image):
        return np.argmax(self._get_mask(self.multilabel_model, image), axis=0)
