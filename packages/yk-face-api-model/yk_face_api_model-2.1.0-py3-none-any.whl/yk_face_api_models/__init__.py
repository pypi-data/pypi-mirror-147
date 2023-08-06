"""
Import models used in controller.
"""
from .process_request_config import ProcessRequestConfig
from .identify_request import IdentifyRequest, IdentifyRequestSchema
from .template_request import TemplateRequest, TemplateRequestSchema
from .verify_id_request import VerifyIdRequest, VerifyIdRequestSchema
from .verify_request import VerifyRequest, VerifyRequestSchema
from .process_request import ProcessRequest, ProcessRequestSchema
from .verify_images import VerifyImages, VerifyImagesSchema
from .process_multiple_request import ProcessMultipleRequest, ProcessMultipleRequestSchema
from .rename_gallery_request import RenameGalleryRequest, RenameGalleryRequestSchema
