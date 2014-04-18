# generate dataset by applying random transformations to videos
# mix random frames from primary source and some from secondary

import cv2
import ffms
import random
from processing import *


P = 0.5 # percentage of primary source to mix
S = 0.01 # percentage of secondary source to mix


# parameters for temp video to generate
TEMPFILE = 'temp.avi'
FOURCC = cv2.cv.CV_FOURCC('X', 'V', 'I', 'D')
FPS = 20.0
SIZE = (640, 480)


def deriveBag(primary, secondary, algo):
    writer = cv2.VideoWriter()
    writer.open(TEMPFILE, FOURCC, FPS, SIZE)
    generateVideoFromSeed(writer, primary, P)
    generateVideoFromSeed(writer, secondary, S)
    writer.release()
    return processVideo(TEMPFILE, algo)


def generateVideoFromSeed(writer, f, p):
    vs = ffms.VideoSource(f)
    vs.set_output_format([ffms.get_pix_fmt('bgra')])
    numFramesInSource = len(vs.track.frame_info_list)
    numFramesToGrab = int(p * numFramesInSource)
    for i in range(numFramesToGrab):
        frame = vs.get_frame(random.randrange(0, numFramesInSource)).planes[0]
        # format for opencv for video writing
        # (strip alpha values [SLOW - is there better pix_fmt?] and reshape)
        image = [frame[j] for j in range(len(frame)) if (j + 1) % 4 != 0]
        image = np.reshape(image, (frame.EncodedHeight, frame.EncodedWidth, 3))
        # TODO: apply transform/filter to image
        writer.write(image)
