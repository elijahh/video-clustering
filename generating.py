# generate dataset by applying random transformations to videos
# mix random frames from primary source and some from secondary

import cv2
import ffms
import random
from processing import *


P = 400 # number of frames from primary source
S = 100 # number of frames from secondary source


# parameters for temp video to generate
TEMPFILE = 'temp.avi'
FOURCC = cv2.cv.CV_FOURCC('X', 'V', 'I', 'D')
FPS = 20.0
SIZE = (640, 480)


def deriveBag(primary, secondary, algo):
    writer = cv2.VideoWriter()
    if writer.open(TEMPFILE, FOURCC, FPS, SIZE):
        generateVideoFromSeed(writer, primary, P)
        generateVideoFromSeed(writer, secondary, S)
        return processVideo(TEMPFILE, algo)


def generateVideoFromSeed(writer, f, p):
    vs = ffms.VideoSource(f)
    vs.set_output_format([ffms.get_pix_fmt('bgr24')])
    numFramesInSource = len(vs.track.frame_info_list)
    for i in range(p):
        print "Grabbing frame {0}/{1} from {2}".format(i, p-1, f)
        frame = vs.get_frame(random.randrange(0, numFramesInSource))
        frame = np.reshape(frame.planes[0], (frame.EncodedHeight, frame.EncodedWidth, 3))
        # TODO: apply transform/filter to image
        frame = cv2.resize(frame, SIZE)
        writer.write(frame)
