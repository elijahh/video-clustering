import ffms
from hashing import * # M, N, algos defined here


def processVideo(filename, algo):
    vs = ffms.VideoSource(filename)
    vs.set_output_format([ffms.get_pix_fmt('gray')], width=M, height=N, resizer=ffms.FFMS_RESIZER_FAST_BILINEAR)
    hashes = u''
    for framenum in vs.track.keyframes:
        print "Hashing frame {0}/{1}".format(framenum, vs.track.keyframes[-1])
        frame = vs.get_frame(framenum).planes[0].reshape((M, N))
        hashes += str(algo(frame)) + ' '
    return hashes
