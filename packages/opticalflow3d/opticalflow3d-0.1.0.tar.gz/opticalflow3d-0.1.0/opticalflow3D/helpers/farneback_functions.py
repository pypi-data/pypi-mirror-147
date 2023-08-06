import math

import numpy as np
from numba import cuda
import cupy as cp
from cupyx.scipy import ndimage
import cupyx


def make_abc_fast(signal, spatial_size, sigma_k=0.15):
    # spatial_size = spatial_size | 1 # ensure the value is odd
    sigma = sigma_k * (spatial_size - 1)

    n = int((spatial_size - 1) / 2)
    a = np.exp(-(np.arange(-n, n + 1, dtype=np.float32) ** 2) / (2 * sigma ** 2))

    # Set up applicability and basis functions
    applicability = np.multiply.outer(np.multiply.outer(a, a), a)
    z, y, x = np.mgrid[-n:n + 1, -n:n + 1, -n:n + 1]

    basis = np.stack((np.ones(x.shape), x, y, z, x * x, y * y, z * z, x * y, x * z, y * z), axis=3)
    nb = basis.shape[3]

    # Compute the inverse metric
    # can be shortened by only calculating those values that matter
    q = np.zeros((nb, nb), dtype=np.float32)
    for i in range(nb):
        for j in range(i, nb):
            q[i, j] = np.sum(basis[..., i] * applicability * basis[..., j])
            q[j, i] = q[i, j]

    del basis, applicability, x, y, z
    qinv = np.linalg.inv(q)

    # convolutions in z
    kernel_0 = cp.array(a)
    kernel_1 = cp.array(np.arange(-n, n + 1, dtype=np.float32) * a)
    kernel_2 = cp.array(np.arange(-n, n + 1, dtype=np.float32) ** 2 * a)

    conv_z0 = cupyx.scipy.ndimage.correlate1d(signal, kernel_0, axis=0)
    conv_z1 = cupyx.scipy.ndimage.correlate1d(signal, kernel_1, axis=0)
    conv_z2 = cupyx.scipy.ndimage.correlate1d(signal, kernel_2, axis=0)

    # convolutions in y
    conv_z0y0 = cupyx.scipy.ndimage.correlate1d(conv_z0, kernel_0, axis=1)
    conv_z0y1 = cupyx.scipy.ndimage.correlate1d(conv_z0, kernel_1, axis=1)
    conv_z0y2 = cupyx.scipy.ndimage.correlate1d(conv_z0, kernel_2, axis=1)
    del conv_z0

    conv_z1y0 = cupyx.scipy.ndimage.correlate1d(conv_z1, kernel_0, axis=1)
    conv_z1y1 = cupyx.scipy.ndimage.correlate1d(conv_z1, kernel_1, axis=1)
    del conv_z1

    conv_z2y0 = cupyx.scipy.ndimage.correlate1d(conv_z2, kernel_0, axis=1)
    del conv_z2

    # convolutions in x
    conv_z0y0x0 = cupyx.scipy.ndimage.correlate1d(conv_z0y0, kernel_0, axis=2)
    b_0 = qinv[1, 1] * cupyx.scipy.ndimage.correlate1d(conv_z0y0, kernel_1, axis=2)
    a_00 = qinv[4, 4] * cupyx.scipy.ndimage.correlate1d(conv_z0y0, kernel_2, axis=2) + qinv[4, 0] * conv_z0y0x0
    del conv_z0y0

    b_1 = qinv[2, 2] * cupyx.scipy.ndimage.correlate1d(conv_z0y1, kernel_0, axis=2)
    a_01 = qinv[7, 7] * cupyx.scipy.ndimage.correlate1d(conv_z0y1, kernel_1, axis=2) / 2
    del conv_z0y1

    a_11 = qinv[5, 5] * cupyx.scipy.ndimage.correlate1d(conv_z0y2, kernel_0, axis=2) + qinv[5, 0] * conv_z0y0x0
    del conv_z0y2

    b_2 = qinv[3, 3] * cupyx.scipy.ndimage.correlate1d(conv_z1y0, kernel_0, axis=2)
    a_02 = qinv[8, 8] * cupyx.scipy.ndimage.correlate1d(conv_z1y0, kernel_1, axis=2) / 2
    del conv_z1y0

    a_12 = qinv[9, 9] * cupyx.scipy.ndimage.correlate1d(conv_z1y1, kernel_0, axis=2) / 2
    del conv_z1y1

    a_22 = qinv[6, 6] * cupyx.scipy.ndimage.correlate1d(conv_z2y0, kernel_0, axis=2) + qinv[6, 0] * conv_z0y0x0
    del conv_z2y0, conv_z0y0x0

    return b_0, b_1, b_2, a_00, a_01, a_02, a_11, a_12, a_22


@cuda.jit
def update_matrices(b1_0, b1_1, b1_2, a1_00, a1_01, a1_02, a1_11, a1_12, a1_22,
                    b2_0, b2_1, b2_2, a2_00, a2_01, a2_02, a2_11, a2_12, a2_22,
                    vx, vy, vz, border,
                    h0, h1, h2, g00, g01, g02, g11, g12, g22):
    z, y, x = cuda.grid(3)

    r = cuda.local.array(shape=(9,), dtype=np.float32)
    for j in range(9):
        r[j] = 0.0

    border_size = len(border) - 1
    depth, length, width = vx.shape

    if z < depth and y < length and x < width:
        dx = vx[z, y, x]
        dy = vy[z, y, x]
        dz = vz[z, y, x]

        fx = x + dx
        fy = y + dy
        fz = z + dz

        x1 = int(math.floor(fx))
        y1 = int(math.floor(fy))
        z1 = int(math.floor(fz))

        fx -= x1
        fy -= y1
        fz -= z1

        ## interpolate values
        if 0 <= x1 and 0 <= y1 and 0 <= z1 and x1 < (width - 1) and y1 < (length - 1) and z1 < (depth - 1):
            a000 = (1.0 - fx) * (1.0 - fy) * (1.0 - fz)
            a001 = fx * (1.0 - fy) * (1.0 - fz)
            a010 = (1.0 - fx) * fy * (1.0 - fz)
            a100 = (1.0 - fx) * (1.0 - fy) * fz
            a011 = fx * fy * (1.0 - fz)
            a101 = fx * (1.0 - fy) * fz
            a110 = (1.0 - fx) * fy * fz
            a111 = fx * fy * fz

            r[0] = a000 * b2_0[z1, y1, x1] + \
                   a001 * b2_0[z1, y1, x1 + 1] + \
                   a010 * b2_0[z1, y1 + 1, x1] + \
                   a100 * b2_0[z1 + 1, y1, x1] + \
                   a011 * b2_0[z1, y1 + 1, x1 + 1] + \
                   a101 * b2_0[z1 + 1, y1, x1 + 1] + \
                   a110 * b2_0[z1 + 1, y1 + 1, x1] + \
                   a111 * b2_0[z1 + 1, y1 + 1, x1 + 1]

            r[1] = a000 * b2_1[z1, y1, x1] + \
                   a001 * b2_1[z1, y1, x1 + 1] + \
                   a010 * b2_1[z1, y1 + 1, x1] + \
                   a100 * b2_1[z1 + 1, y1, x1] + \
                   a011 * b2_1[z1, y1 + 1, x1 + 1] + \
                   a101 * b2_1[z1 + 1, y1, x1 + 1] + \
                   a110 * b2_1[z1 + 1, y1 + 1, x1] + \
                   a111 * b2_1[z1 + 1, y1 + 1, x1 + 1]

            r[2] = a000 * b2_2[z1, y1, x1] + \
                   a001 * b2_2[z1, y1, x1 + 1] + \
                   a010 * b2_2[z1, y1 + 1, x1] + \
                   a100 * b2_2[z1 + 1, y1, x1] + \
                   a011 * b2_2[z1, y1 + 1, x1 + 1] + \
                   a101 * b2_2[z1 + 1, y1, x1 + 1] + \
                   a110 * b2_2[z1 + 1, y1 + 1, x1] + \
                   a111 * b2_2[z1 + 1, y1 + 1, x1 + 1]

            r[3] = a000 * a2_00[z1, y1, x1] + \
                   a001 * a2_00[z1, y1, x1 + 1] + \
                   a010 * a2_00[z1, y1 + 1, x1] + \
                   a100 * a2_00[z1 + 1, y1, x1] + \
                   a011 * a2_00[z1, y1 + 1, x1 + 1] + \
                   a101 * a2_00[z1 + 1, y1, x1 + 1] + \
                   a110 * a2_00[z1 + 1, y1 + 1, x1] + \
                   a111 * a2_00[z1 + 1, y1 + 1, x1 + 1]

            r[4] = a000 * a2_01[z1, y1, x1] + \
                   a001 * a2_01[z1, y1, x1 + 1] + \
                   a010 * a2_01[z1, y1 + 1, x1] + \
                   a100 * a2_01[z1 + 1, y1, x1] + \
                   a011 * a2_01[z1, y1 + 1, x1 + 1] + \
                   a101 * a2_01[z1 + 1, y1, x1 + 1] + \
                   a110 * a2_01[z1 + 1, y1 + 1, x1] + \
                   a111 * a2_01[z1 + 1, y1 + 1, x1 + 1]

            r[5] = a000 * a2_02[z1, y1, x1] + \
                   a001 * a2_02[z1, y1, x1 + 1] + \
                   a010 * a2_02[z1, y1 + 1, x1] + \
                   a100 * a2_02[z1 + 1, y1, x1] + \
                   a011 * a2_02[z1, y1 + 1, x1 + 1] + \
                   a101 * a2_02[z1 + 1, y1, x1 + 1] + \
                   a110 * a2_02[z1 + 1, y1 + 1, x1] + \
                   a111 * a2_02[z1 + 1, y1 + 1, x1 + 1]

            r[6] = a000 * a2_11[z1, y1, x1] + \
                   a001 * a2_11[z1, y1, x1 + 1] + \
                   a010 * a2_11[z1, y1 + 1, x1] + \
                   a100 * a2_11[z1 + 1, y1, x1] + \
                   a011 * a2_11[z1, y1 + 1, x1 + 1] + \
                   a101 * a2_11[z1 + 1, y1, x1 + 1] + \
                   a110 * a2_11[z1 + 1, y1 + 1, x1] + \
                   a111 * a2_11[z1 + 1, y1 + 1, x1 + 1]

            r[7] = a000 * a2_12[z1, y1, x1] + \
                   a001 * a2_12[z1, y1, x1 + 1] + \
                   a010 * a2_12[z1, y1 + 1, x1] + \
                   a100 * a2_12[z1 + 1, y1, x1] + \
                   a011 * a2_12[z1, y1 + 1, x1 + 1] + \
                   a101 * a2_12[z1 + 1, y1, x1 + 1] + \
                   a110 * a2_12[z1 + 1, y1 + 1, x1] + \
                   a111 * a2_12[z1 + 1, y1 + 1, x1 + 1]

            r[8] = a000 * a2_22[z1, y1, x1] + \
                   a001 * a2_22[z1, y1, x1 + 1] + \
                   a010 * a2_22[z1, y1 + 1, x1] + \
                   a100 * a2_22[z1 + 1, y1, x1] + \
                   a011 * a2_22[z1, y1 + 1, x1 + 1] + \
                   a101 * a2_22[z1 + 1, y1, x1 + 1] + \
                   a110 * a2_22[z1 + 1, y1 + 1, x1] + \
                   a111 * a2_22[z1 + 1, y1 + 1, x1 + 1]

            r[3] = (a1_00[z, y, x] + r[3]) * 0.5
            r[4] = (a1_01[z, y, x] + r[4]) * 0.25
            r[5] = (a1_02[z, y, x] + r[5]) * 0.25
            r[6] = (a1_11[z, y, x] + r[6]) * 0.5
            r[7] = (a1_12[z, y, x] + r[7]) * 0.25
            r[8] = (a1_22[z, y, x] + r[8]) * 0.5
        else:
            r[3] = a1_00[z, y, x]
            r[4] = a1_01[z, y, x] * 0.5
            r[5] = a1_02[z, y, x] * 0.5
            r[6] = a1_11[z, y, x]
            r[7] = a1_12[z, y, x] * 0.5
            r[8] = a1_22[z, y, x]

        r[0] = ((b1_0[z, y, x] - r[0]) * 0.5) + (r[3] * dx + r[4] * dy + r[5] * dz)

        r[1] = ((b1_1[z, y, x] - r[1]) * 0.5) + (r[4] * dx + r[6] * dy + r[7] * dz)

        r[2] = (b1_2[z, y, x] - r[2]) * 0.5 + (r[5] * dx + r[7] * dy + r[8] * dz)

        scale = border[min(x, border_size)] * \
                border[min(y, border_size)] * \
                border[min(z, border_size)] * \
                border[min(width - x - 1, border_size)] * \
                border[min(length - y - 1, border_size)] * \
                border[min(depth - z - 1, border_size)]

        for j in range(9):
            r[j] = r[j] * scale

        g00[z, y, x] = r[3] * r[3] + r[4] * r[4] + r[5] * r[5]
        g01[z, y, x] = r[3] * r[4] + r[4] * r[6] + r[5] * r[7]
        g02[z, y, x] = r[3] * r[5] + r[4] * r[7] + r[5] * r[8]
        g11[z, y, x] = r[4] * r[4] + r[6] * r[6] + r[7] * r[7]
        g12[z, y, x] = r[4] * r[5] + r[6] * r[7] + r[7] * r[8]
        g22[z, y, x] = r[5] * r[5] + r[7] * r[7] + r[8] * r[8]

        h0[z, y, x] = r[3] * r[0] + r[4] * r[1] + r[5] * r[2]
        h1[z, y, x] = r[4] * r[0] + r[6] * r[1] + r[7] * r[2]
        h2[z, y, x] = r[5] * r[0] + r[7] * r[1] + r[8] * r[2]


@cuda.jit
def calculate_error(h0, h1, h2, g00, g01, g02, g11, g12, g22,
                    flowx, flowy, flowz, error):
    z, y, x = cuda.grid(3)

    depth, length, width = flowx.shape

    if z < depth and y < length and x < width:
        error[z, y, x] = (h0[z, y, x] ** 2 + h1[z, y, x] ** 2 + h2[z, y, x] ** 2) - \
                         (flowx[z, y, x] * (g00[z, y, x] * h0[z, y, x] + g01[z, y, x] * h1[z, y, x] + g02[z, y, x] * h2[z, y, x]) +
                          flowy[z, y, x] * (g01[z, y, x] * h0[z, y, x] + g11[z, y, x] * h1[z, y, x] + g12[z, y, x] * h2[z, y, x]) +
                          flowz[z, y, x] * (g02[z, y, x] * h0[z, y, x] + g12[z, y, x] * h1[z, y, x] + g22[z, y, x] * h2[z, y, x]))


@cuda.jit
def update_flow(h0, h1, h2, g00, g01, g02, g11, g12, g22,
                  flowx, flowy, flowz):
    # M is in format [[g00, g01, g02], and [[h0],
    #                 [g01, g11, g12],      [h1],
    #                 [g02, g12, g22]]      [h2]]
    z, y, x = cuda.grid(3)

    depth, length, width = flowx.shape

    if z < depth and y < length and x < width:
        det = g00[z, y, x] * (g11[z, y, x] * g22[z, y, x] - g12[z, y, x] * g12[z, y, x]) - \
              g01[z, y, x] * (g01[z, y, x] * g22[z, y, x] - g02[z, y, x] * g12[z, y, x]) + \
              g02[z, y, x] * (g01[z, y, x] * g12[z, y, x] - g02[z, y, x] * g11[z, y, x])

        flowx[z, y, x] = (h0[z, y, x] * (g11[z, y, x] * g22[z, y, x] - g12[z, y, x] * g12[z, y, x]) -
                          g01[z, y, x] * (h1[z, y, x] * g22[z, y, x] - h2[z, y, x] * g12[z, y, x]) +
                          g02[z, y, x] * (h1[z, y, x] * g12[z, y, x] - h2[z, y, x] * g11[z, y, x])) / det
        flowy[z, y, x] = (g00[z, y, x] * (h1[z, y, x] * g22[z, y, x] - h2[z, y, x] * g12[z, y, x]) -
                          h0[z, y, x] * (g01[z, y, x] * g22[z, y, x] - g02[z, y, x] * g12[z, y, x]) +
                          g02[z, y, x] * (g01[z, y, x] * h2[z, y, x] - g02[z, y, x] * h1[z, y, x])) / det
        flowz[z, y, x] = (g00[z, y, x] * (g11[z, y, x] * h2[z, y, x] - g12[z, y, x] * h1[z, y, x]) -
                          g01[z, y, x] * (g01[z, y, x] * h2[z, y, x] - g02[z, y, x] * h1[z, y, x]) +
                          h0[z, y, x] * (g01[z, y, x] * g12[z, y, x] - g02[z, y, x] * g11[z, y, x])) / det


def gaussian_kernel_1d(sigma, radius=None):
    if radius is None:
        radius = math.ceil(2 * sigma)

    output_kernel = np.mgrid[-radius:radius + 1]
    output_kernel = np.exp((-(1 / 2) * (output_kernel ** 2)) / (sigma ** 2))
    output_kernel = output_kernel / np.sum(output_kernel)

    return output_kernel


def gaussian_pyramid_3d(image, sigma=1, scale=0.5):
    kernel = cp.asarray(gaussian_kernel_1d(sigma), dtype=cp.float32)
    radius = math.ceil(2 * sigma)

    # gaussian smoothing
    image = cupyx.scipy.ndimage.convolve(image, cp.reshape(kernel, (2 * radius + 1, 1, 1)), mode="reflect")
    image = cupyx.scipy.ndimage.convolve(image, cp.reshape(kernel, (1, 2 * radius + 1, 1)), mode="reflect")
    image = cupyx.scipy.ndimage.convolve(image, cp.reshape(kernel, (1, 1, 2 * radius + 1)), mode="reflect")

    shape = image.shape
    true_scale = [int(round(shape[0] * scale)) / shape[0],
                  int(round(shape[1] * scale)) / shape[1],
                  int(round(shape[2] * scale)) / shape[2]]
    image_resized = cp.empty((int(round(shape[0] * scale)),
                              int(round(shape[1] * scale)),
                              int(round(shape[2] * scale))), dtype=cp.float32)
    ndimage.zoom(image, (scale, scale, scale), output=image_resized, mode="reflect")

    return image_resized, true_scale


def imresize_3d(image, scale=(0.5, 0.5, 0.5)):
    image = ndimage.zoom(image, (1 / scale[0], 1 / scale[1], 1 / scale[2]))

    return image


def farneback_3d(image_1, image_2, iters, num_levels,
                 scale=0.5, kernelsize=9, sigma_k=0.15, filter_type="box", filter_size=5,
                 presmoothing=None, threadsperblock=(8, 8, 8)):
    if filter_type.lower() == "gaussian":
        filter_fn = lambda x: cupyx.scipy.ndimage.gaussian_filter(x, filter_size / 2 * 0.3)
    else:
        filter_fn = lambda x: cupyx.scipy.ndimage.uniform_filter(x, size=filter_size)

    image_1 = cp.asarray(image_1)
    image_2 = cp.asarray(image_2)
    if presmoothing is not None:
        image_1 = cupyx.scipy.ndimage.gaussian_filter(image_1, presmoothing)
        image_2 = cupyx.scipy.ndimage.gaussian_filter(image_2, presmoothing)

    # initialize gaussian pyramid
    gauss_pyramid_1 = {1: image_1}
    gauss_pyramid_2 = {1: image_2}
    true_scale_dict = {}
    for pyr_lvl in range(1, num_levels + 1):
        if pyr_lvl == 1:
            gauss_pyramid_1 = {pyr_lvl: image_1}
            gauss_pyramid_2 = {pyr_lvl: image_2}
        else:
            gauss_pyramid_1[pyr_lvl], true_scale_dict[pyr_lvl] = gaussian_pyramid_3d(gauss_pyramid_1[pyr_lvl - 1],
                                                                                     sigma=1, scale=scale)
            gauss_pyramid_2[pyr_lvl], _ = gaussian_pyramid_3d(gauss_pyramid_2[pyr_lvl - 1], sigma=1, scale=scale)

    if type(iters) != list:
        iters = [iters] * num_levels

    # Pyr code
    for lvl in range(num_levels, 0, -1):
        # print("Currently working on pyramid level: {}".format(lvl))
        lvl_image_1 = gauss_pyramid_1[lvl]
        lvl_image_2 = gauss_pyramid_2[lvl]

        if lvl == num_levels:
            # initialize velocities
            vx = cp.zeros(lvl_image_1.shape, dtype=cp.float32)
            vy = cp.zeros(lvl_image_1.shape, dtype=cp.float32)
            vz = cp.zeros(lvl_image_1.shape, dtype=cp.float32)
        else:
            # check if nan values are present
            vx[cp.isnan(vx)] = 0
            vy[cp.isnan(vy)] = 0
            vz[cp.isnan(vz)] = 0

            vx[cp.abs(error) > 1] = 0
            vy[cp.abs(error) > 1] = 0
            vz[cp.abs(error) > 1] = 0
            del error

            vx = 1 / true_scale_dict[lvl + 1][2] * imresize_3d(vx, scale=true_scale_dict[lvl + 1])
            vy = 1 / true_scale_dict[lvl + 1][1] * imresize_3d(vy, scale=true_scale_dict[lvl + 1])
            vz = 1 / true_scale_dict[lvl + 1][0] * imresize_3d(vz, scale=true_scale_dict[lvl + 1])

        b1_0, b1_1, b1_2, a1_00, a1_01, a1_02, a1_11, a1_12, a1_22 = make_abc_fast(lvl_image_1, kernelsize,
                                                                                   sigma_k=sigma_k)
        b2_0, b2_1, b2_2, a2_00, a2_01, a2_02, a2_11, a2_12, a2_22 = make_abc_fast(lvl_image_2, kernelsize,
                                                                                   sigma_k=sigma_k)

        border = cp.asarray([0.14, 0.14, 0.4472, 0.4472, 0.4472, 1], dtype=cp.float32)
        shape = vx.shape
        h0 = cp.zeros(shape, dtype=cp.float32)
        h1 = cp.zeros(shape, dtype=cp.float32)
        h2 = cp.zeros(shape, dtype=cp.float32)
        g00 = cp.zeros(shape, dtype=cp.float32)
        g01 = cp.zeros(shape, dtype=cp.float32)
        g02 = cp.zeros(shape, dtype=cp.float32)
        g11 = cp.zeros(shape, dtype=cp.float32)
        g12 = cp.zeros(shape, dtype=cp.float32)
        g22 = cp.zeros(shape, dtype=cp.float32)

        for i in range(iters[lvl - 1]):
            blockspergrid_z = math.ceil(shape[0] / threadsperblock[0])
            blockspergrid_y = math.ceil(shape[1] / threadsperblock[1])
            blockspergrid_x = math.ceil(shape[2] / threadsperblock[2])
            blockspergrid = (blockspergrid_z, blockspergrid_y, blockspergrid_x)

            update_matrices[blockspergrid, threadsperblock](b1_0, b1_1, b1_2, a1_00, a1_01, a1_02, a1_11, a1_12, a1_22,
                                                            b2_0, b2_1, b2_2, a2_00, a2_01, a2_02, a2_11, a2_12, a2_22,
                                                            vx, vy, vz, border,
                                                            h0, h1, h2, g00, g01, g02, g11, g12, g22)
            cp.cuda.Stream.null.synchronize()

            h0 = filter_fn(h0)
            h1 = filter_fn(h1)
            h2 = filter_fn(h2)
            g00 = filter_fn(g00)
            g01 = filter_fn(g01)
            g02 = filter_fn(g02)
            g11 = filter_fn(g11)
            g12 = filter_fn(g12)
            g22 = filter_fn(g22)
            cp.cuda.Stream.null.synchronize()

            update_flow[blockspergrid, threadsperblock](h0, h1, h2, g00, g01, g02, g11, g12, g22, vx, vy, vz)
            cp.cuda.Stream.null.synchronize()

            if i == iters[lvl - 1] - 1:
                error = cp.zeros(vx.shape, dtype=cp.float32)
                calculate_error[blockspergrid, threadsperblock](h0, h1, h2, g00, g01, g02, g11, g12, g22, vx, vy, vz, error)

            cp.cuda.Stream.null.synchronize()
    return vx, vy, vz, error


def get_positions(start_point, total_vol, vol, shape, overlap, n):
    q, r = divmod(total_vol[n], vol[n] - overlap[n])
    position = []
    valid_vol = []
    valid_position = []

    count = q + (r != 0)
    for i in range(count):
        if i == 0:
            start = start_point[n] - overlap[n] // 2
            valid_start = 0
        else:
            start = end - overlap[n]
            valid_start = valid_end
        end = start + vol[n]

        _start = max(start, 0)
        start_diff = start - _start
        start_valid = overlap[n] // 2 + start_diff

        _end = min((end, shape[n], start_point[n] + total_vol[n] + overlap[n] // 2))
        valid_end = min((end - overlap[n] // 2 - start_point[n], total_vol[n]))

        end_valid = valid_end - valid_start + start_valid

        position.append((_start, _end))
        valid_position.append((valid_start, valid_end))
        valid_vol.append((start_valid, end_valid))

    return position, valid_position, valid_vol
