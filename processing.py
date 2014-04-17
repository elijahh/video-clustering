import ffms
from hashing import * # M, N, algos defined here


# TODO: experiment with various sizes, interpolations (resizers)
def processVideo(filename, algo):
    vs = ffms.VideoSource(filename)
    vs.set_output_format([ffms.get_pix_fmt('gray')], width=M, height=N, resizer=ffms.FFMS_RESIZER_BILINEAR)
    hashes = []
    for framenum in vs.track.keyframes:
        frame = vs.get_frame(framenum).planes[0].reshape((M, N))
        hashes += [algo(frame)]
    return hashes
