import numpy as np
import scipy.fft
from scipy.signal import find_peaks
from typing import List


def compute_slope(x: np.array, y: np.array) -> float:
    Y = np.zeros((y.shape[-1], 1))
    B = np.ones((x.shape[-1], 2))
    Y[:, 0] = y
    B[:, 0] = x
    k = np.linalg.inv(np.transpose(B)@B)@np.transpose(B)@Y
    k1 = k[0, 0]
    return k1


def sdd_threshold_selection(img: np.array, n_fit: int) -> List[float]:
    """


    Reference: Z.Z. Wang, "A new approach for Segmentation and Quantification of Cells or Nanoparticles," IEEE T IND INFORM, 2016
    Args:
        img (np.array): Input image [0...255], shape should be [w,h,1] or [w,h]
        n_fit (int): approximation order for the derriative estimation

    Returns:
        List[float]: list with threshholds
    """

    # Step 1. The gray-scale values of the image
    # are rearranged in the interval [1,255] and
    # its normalized histogram distribution P(x)
    image = np.around(img)
    image = np.clip(image, 1, 255)
    Ns = np.amax(image).astype(int)
    Ns1 = max(np.amin(image), 1).astype(int)
    hist1, _ = np.histogram(image, bins=255, range=(0, 255))
    hist1 = hist1/np.amax(hist1)

    # Step 2. The normalized histogram distribution
    # is filtered in the frequency domain.

    fhist = scipy.fft.fft(hist1)
    fhist[10: (np.amax(fhist.shape)-10)] = 0
    ahist = scipy.fft.ifft(fhist)
    hist = np.abs(ahist)/np.amax(np.abs(ahist))
    hist[0:Ns1] = 0
    hist[Ns:255] = 0

    # Step 3. To compute the slope difference

    N = n_fit
    hl = np.zeros([np.amax(hist.shape)])
    sd = np.zeros_like(hist)

    for i in range(N, np.amax(hist.shape)-N):
        Y = hist[i-N:i]
        X = np.arange(i-N, i)
        k1 = compute_slope(np.array(X), np.array(Y))

        Y = hist[i:i+N]
        X = np.arange(i, i+N)
        k2 = compute_slope(np.array(X), np.array(Y))
        sd[i] = k1-k2

    sd = sd/np.amax(sd)

    peaks = np.where(sd > 0, sd, 0)
    valleys = np.where(sd < 0, -sd, 0)
    peak_intensity, _ = find_peaks(peaks)
    valley_intensity, _ = find_peaks(valleys)

    #max_peak_ind = np.argmax(peaks[peak_intensity])
    th_cand = valley_intensity[valley_intensity > peak_intensity[0]]
    th_cand = th_cand[th_cand < peak_intensity[-1]]

    return th_cand
