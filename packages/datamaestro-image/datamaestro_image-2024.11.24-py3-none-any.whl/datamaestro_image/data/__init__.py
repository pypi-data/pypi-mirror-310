from datamaestro.data import Base
from datamaestro.data.ml import Supervised
from experimaestro import Param
from datamaestro.definitions import argument, datatasks, datatags
from datamaestro.data.tensor import IDX


class Images(Base):
    pass


class IDXImage(IDX, Images):
    pass


@datatasks("image classification")
@datatags("images")
class ImageClassification(Supervised):
    """Image classification dataset"""

    pass


@argument("images", Images)
@argument("labels", Base)
@datatasks("image classification")
@datatags("images")
class LabelledImages(Base):
    """Image classification dataset

    Attributes:

        images: The images of the dataset
        labels: The labels associated with each image
    """

    images: Param[Images]
    labels: Param[Base]
