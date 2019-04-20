/* This file is part of the OpenMV project.
 * Copyright (c) 2013-2019 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
 * This work is licensed under the MIT license, see the file LICENSE for details.
 */

#ifndef __LIBTF_H
#define __LIBTF_H

#ifdef __cplusplus
extern "C" {
#endif

// Returns 0 on success and 1 on failure.
// Errors are printed to stdout.
int run_classification(const unsigned char *model_data, // TensorFlow Lite binary model.
                       uint8_t *tensor_arena, // As big as you can make it scratch buffer.
                       const int tensor_arena_size, // Size of the above scratch buffer.
                       uint8_t *input_data, // Input byte array (laid out in [height][width][channel] order).
                       const int input_height, // Height mentioned above.
                       const int input_width, // Width mentioned above.
                       const int input_channels, // Channels mentioned above (1 for grayscale8 and 3 for rgb888).
                       float *class_scores, // Classification results array (always sums to 1).
                       const int class_scores_size); // Size of the above array.

#ifdef __cplusplus
}
#endif

#endif // __LIBTF_H

