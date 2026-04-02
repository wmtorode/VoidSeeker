import os
import os.path
import logging
import logging.handlers
import traceback
import platform
import time
import PIL
import pytesseract

from sqlalchemy.orm import sessionmaker

from libvoidseeker import *


INT_MAX_LOG_SIZE = 1024 * 1024 * 5  # ~5MB size
LOG_DIR = '/opt/voidseekerLog/'
STORE_DIR = '/opt/voidseekerStore/ocr/'
LOG_FILE = LOG_DIR + 'ocrlog.txt'
OCR_LOOP_DELAY = 5

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.isdir(STORE_DIR):
    os.makedirs(STORE_DIR)

LOGGER = logging.getLogger("voidseeker-ocr")
LOGGER.setLevel(logging.INFO)
obj_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=INT_MAX_LOG_SIZE, backupCount=5)
obj_handler.setLevel(logging.INFO)
obj_formatter = logging.Formatter('%(name)-18s %(levelname)-8s %(funcName)-25s %(asctime)-25s %(message)s')
obj_handler.setFormatter(obj_formatter)

LOGGER.addHandler(obj_handler)

if TEST_MODE.lower() == "yes":
    LOGGER.setLevel(logging.DEBUG)
    obj_handler.setLevel(logging.DEBUG)
    OCR_LOOP_DELAY = 2


class OCRServer:

    def __init__(self):
        self.sessionMaker = sessionmaker()
        self.sessionMaker.configure(bind=ENGINE)
        self.session = self.sessionMaker()
        self.logger = LOGGER
        self.logger.info("OCRServer initialized")

    def startSqlTransaction(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.session.commit()

    def processRequest(self, request: OcrRequest):

        data = OCRData()
        data.fromJson(request.requestJson)

        for image in data.images:
            try:
                self.logger.info("OCR Request: " + image)
                imagePath = os.path.join(STORE_DIR, image)
                if os.path.exists(imagePath):
                    image = PIL.Image.open(imagePath)
                    text = pytesseract.image_to_string(image)
                    data.results.append(text.lower())
                else:
                    self.logger.error("Image not found: " + imagePath)
                    data.results.append("")
            except (TypeError, PIL.UnidentifiedImageError):
                self.logger.warning(f"Unsupported image format for image: {image}")
                data.results.append("")
        result = OcrResult()
        result.serverId = request.serverId
        result.userId = request.userId
        result.ocrResultJson = data.toJson()
        result.channelId = request.channelId
        self.session.add(result)
        self.session.delete(request)

    def run(self):
        while True:
            try:
                time.sleep(OCR_LOOP_DELAY)
                self.startSqlTransaction()

                ocrRequests = self.session.query(OcrRequest).all()  # type: List[OcrRequest]
                for ocrRequest in ocrRequests: # type: OcrRequest
                    self.processRequest(ocrRequest)
                self.session.commit()
            except:
                self.logger.error("OCR Server Exception:")
                trace = traceback.format_exc()
                lst_trace = trace.split('\n')
                for line in lst_trace:
                    self.logger.critical(line)


server = OCRServer()
server.run()
