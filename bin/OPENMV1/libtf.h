/* This file is part of the OpenMV project.
 * Copyright (c) 2013-2019 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
 * This work is licensed under the MIT license, see the file LICENSE for details.
 */

#ifndef __LIBTF_H
#define __LIBTF_H

#ifdef __cplusplus
extern "C" {
#endif

// Call this first to get the shape of the model input.
// Returns 0 on success and 1 on failure.
// Errors are printed to stdout.
int libtf_get_input_data_hwc(const unsigned char *model_data, // TensorFlow Lite binary model.
                             unsigned char *tensor_arena, // As big as you can make it scratch buffer.
                             const unsigned int tensor_arena_size, // Size of the above scratch buffer.
                             unsigned int *input_height, // Height for the model.
                             unsigned int *input_width, // Width for the model.
                             unsigned int *input_channels); // Channels for the model (1 for grayscale8 and 3 for rgb888).

// Call this second to get the shape of the model output.
// Returns 0 on success and 1 on failure.
// Errors are printed to stdout.
int libtf_get_classification_class_scores_size(const unsigned char *model_data, // TensorFlow Lite binary model.
                                               unsigned char *tensor_arena, // As big as you can make it scratch buffer.
                                               const unsigned int tensor_arena_size, // Size of the above scratch buffer.
                                               unsigned int *class_scores_size); // Size of the output (in floats).

// Returns 0 on success and 1 on failure.
// Errors are printed to stdout.
int libtf_run_classification(const unsigned char *model_data, // TensorFlow Lite binary model.
                             unsigned char *tensor_arena, // As big as you can make it scratch buffer.
                             const unsigned int tensor_arena_size, // Size of the above scratch buffer.
                             unsigned char *input_data, // Input byte array (laid out in [height][width][channel] order).
                             const unsigned int input_height, // Height mentioned above.
                             const unsigned int input_width, // Width mentioned above.
                             const unsigned int input_channels, // Channels mentioned above (1 for grayscale8 and 3 for rgb888).
                             float *class_scores, // Classification results array (always sums to 1).
                             const unsigned int class_scores_size); // Size of the above array.

#ifdef __cplusplus
}
#endif

#endif // __LIBTF_H
