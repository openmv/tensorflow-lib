/* This file is part of the OpenMV project.
 * Copyright (c) 2013-2019 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
 * This work is licensed under the MIT license, see the file LICENSE for details.
 */

#include "tensorflow/lite/experimental/micro/kernels/all_ops_resolver.h"
#include "tensorflow/lite/experimental/micro/micro_error_reporter.h"
#include "tensorflow/lite/experimental/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"
#include "libtf.h"

extern "C" {
    int libtf_get_input_data_hwc(const unsigned char *model_data,
                                 unsigned char *tensor_arena, const unsigned int tensor_arena_size,
                                 unsigned int *input_height, unsigned int *input_width, unsigned int *input_channels) {
        // Set up logging.
        tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter* error_reporter = &micro_error_reporter;

        // Map the model into a usable data structure. This doesn't involve any
        // copying or parsing, it's a very lightweight operation.
        const tflite::Model* model = ::tflite::GetModel(model_data);
        if (model->version() != TFLITE_SCHEMA_VERSION) {
          error_reporter->Report(
              "Model provided is schema version %d not equal to supported version %d.\n",
              model->version(), TFLITE_SCHEMA_VERSION);
          return 1;
        }

        // This pulls in all the operation implementations we need.
        tflite::ops::micro::AllOpsResolver resolver;

        // Create an area of memory to use for input, output, and intermediate arrays.
        // The size of this will depend on the model you're using, and may need to be
        // determined by experimentation.
        tflite::SimpleTensorAllocator tensor_allocator(tensor_arena, tensor_arena_size);

        // Build an interpreter to run the model with.
        tflite::MicroInterpreter interpreter(model, resolver, &tensor_allocator, error_reporter);

        // Get information about the memory area to use for the model's input.
        TfLiteTensor* model_input = interpreter.input(0);

        if ((model_input->dims->size != 4) ||
            (model_input->dims->data[0] != 1) ||
            (model_input->type != kTfLiteUInt8)) {
          error_reporter->Report("Bad input tensor parameters in model!\n");
          return 1;
        }

        *input_height = model_input->dims->data[1];
        *input_width = model_input->dims->data[2];
        *input_channels = model_input->dims->data[3];

        return 0;
    }

    int libtf_get_classification_class_scores_size(const unsigned char *model_data,
                                                   unsigned char *tensor_arena, const unsigned int tensor_arena_size,
                                                   unsigned int *class_scores_size) {
        // Set up logging.
        tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter* error_reporter = &micro_error_reporter;

        // Map the model into a usable data structure. This doesn't involve any
        // copying or parsing, it's a very lightweight operation.
        const tflite::Model* model = ::tflite::GetModel(model_data);
        if (model->version() != TFLITE_SCHEMA_VERSION) {
          error_reporter->Report(
              "Model provided is schema version %d not equal to supported version %d.\n",
              model->version(), TFLITE_SCHEMA_VERSION);
          return 1;
        }

        // This pulls in all the operation implementations we need.
        tflite::ops::micro::AllOpsResolver resolver;

        // Create an area of memory to use for input, output, and intermediate arrays.
        // The size of this will depend on the model you're using, and may need to be
        // determined by experimentation.
        tflite::SimpleTensorAllocator tensor_allocator(tensor_arena, tensor_arena_size);

        // Build an interpreter to run the model with.
        tflite::MicroInterpreter interpreter(model, resolver, &tensor_allocator, error_reporter);

        // The output from the model is a vector containing the scores for each kind of prediction.
        TfLiteTensor* output = interpreter.output(0);

        if ((output->dims->size != 2) ||
            (output->dims->data[0] != 1) ||
            (output->type != kTfLiteUInt8)) {
          error_reporter->Report("Bad ouput tensor parameters in model!\n");
          return 1;
        }

        *class_scores_size = output->dims->data[1];

        return 0;
    }

    int libtf_run_classification(const unsigned char *model_data,
                                 unsigned char *tensor_arena, const unsigned int tensor_arena_size,
                                 unsigned char *input_data, const unsigned int input_height, const unsigned int input_width, const unsigned int input_channels,
                                 float *class_scores, const unsigned int class_scores_size) {
        // Set up logging.
        tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter* error_reporter = &micro_error_reporter;

        // Map the model into a usable data structure. This doesn't involve any
        // copying or parsing, it's a very lightweight operation.
        const tflite::Model* model = ::tflite::GetModel(model_data);
        if (model->version() != TFLITE_SCHEMA_VERSION) {
          error_reporter->Report(
              "Model provided is schema version %d not equal to supported version %d.\n",
              model->version(), TFLITE_SCHEMA_VERSION);
          return 1;
        }

        // This pulls in all the operation implementations we need.
        tflite::ops::micro::AllOpsResolver resolver;

        // Create an area of memory to use for input, output, and intermediate arrays.
        // The size of this will depend on the model you're using, and may need to be
        // determined by experimentation.
        tflite::SimpleTensorAllocator tensor_allocator(tensor_arena, tensor_arena_size);

        // Build an interpreter to run the model with.
        tflite::MicroInterpreter interpreter(model, resolver, &tensor_allocator, error_reporter);

        // Get information about the memory area to use for the model's input.
        TfLiteTensor* model_input = interpreter.input(0);

        if ((model_input->dims->size != 4) ||
            (model_input->dims->data[0] != 1) ||
            (model_input->dims->data[1] != input_height) ||
            (model_input->dims->data[2] != input_width) ||
            (model_input->dims->data[3] != input_channels) ||
            (model_input->type != kTfLiteUInt8)) {
          error_reporter->Report("Bad input tensor parameters in model!\n");
          return 1;
        }

        // Initialize the feature data.
        model_input->data.uint8 = input_data;

        // Run the model on the input and make sure it succeeds.
        if (interpreter.Invoke() != kTfLiteOk) {
          error_reporter->Report("Invoke failed!\n");
          return 1;
        }

        // The output from the model is a vector containing the scores for each kind of prediction.
        TfLiteTensor* output = interpreter.output(0);

        if ((output->dims->size != 2) ||
            (output->dims->data[0] != 1) ||
            (output->dims->data[1] != class_scores_size)) {
          error_reporter->Report(
              "The results for recognition should contain %d elements, but there are %d in an %d-dimensional shape.\n",
              class_scores_size, output->dims->data[1], output->dims->size);
          return 1;
        }

        if (output->type != kTfLiteUInt8) {
          error_reporter->Report(
              "The results for recognition should be uint8 elements, but are %d.\n",
              output->type);
          return 1;
        }

        int sum = 0;
        for (int i = 0; i < class_scores_size; ++i) {
          sum += output->data.uint8[i];
        }

        for (int i = 0; i < class_scores_size; ++i) {
          class_scores[i] = sum ? (((float) output->data.uint8[i]) / sum) : 0;
        }

        return 0;
    }
}

