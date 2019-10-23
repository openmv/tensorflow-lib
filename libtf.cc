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
                                 unsigned int *input_height, unsigned int *input_width, unsigned int *input_channels)
    {
        tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter *error_reporter = &micro_error_reporter;

        const tflite::Model *model = tflite::GetModel(model_data);

        if (model->version() != TFLITE_SCHEMA_VERSION) {
            error_reporter->Report("Model provided is schema version is not equal to supported version!\n");
            return 1;
        }

        tflite::ops::micro::AllOpsResolver resolver;
        tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, tensor_arena_size, error_reporter);

        if (interpreter.AllocateTensors() != kTfLiteOk) {
            error_reporter->Report("AllocateTensors() failed!\n");
            return 1;
        }

        TfLiteTensor *model_input = interpreter.input(0);

        if (model_input->dims->size != 4) {
            error_reporter->Report("Input dimensions should be [n][h][w][c], e.g. 4!\n");
            return 1;
        }

        if (model_input->dims->data[0] != 1) {
            error_reporter->Report("Input dimension [n] should be 1!\n");
            return 1;
        }

        if (model_input->type != kTfLiteUInt8) {
            error_reporter->Report("Input model data type should be 8-bit quantized!\n");
            return 1;
        }

        *input_height = model_input->dims->data[1];
        *input_width = model_input->dims->data[2];
        *input_channels = model_input->dims->data[3];

        return 0;
    }

    int libtf_get_output_data_hwc(const unsigned char *model_data,
                                  unsigned char *tensor_arena, const unsigned int tensor_arena_size,
                                  unsigned int *output_height, unsigned int *output_width, unsigned int *output_channels)
    {
        tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter *error_reporter = &micro_error_reporter;

        const tflite::Model *model = tflite::GetModel(model_data);

        if (model->version() != TFLITE_SCHEMA_VERSION) {
            error_reporter->Report("Model provided is schema version is not equal to supported version!\n");
            return 1;
        }

        tflite::ops::micro::AllOpsResolver resolver;
        tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, tensor_arena_size, error_reporter);

        if (interpreter.AllocateTensors() != kTfLiteOk) {
            error_reporter->Report("AllocateTensors() failed!\n");
            return 1;
        }

        TfLiteTensor *model_output = interpreter.output(0);

        if (model_output->dims->size != 4) {
            error_reporter->Report("Output dimensions should be [n][h][w][c], e.g. 4!\n");
            return 1;
        }

        if (model_output->dims->data[0] != 1) {
            error_reporter->Report("Output dimension [n] should be 1!\n");
            return 1;
        }

        if (model_output->type != kTfLiteUInt8) {
            error_reporter->Report("Output model data type should be 8-bit quantized!\n");
            return 1;
        }

        *output_height = model_output->dims->data[1];
        *output_width = model_output->dims->data[2];
        *output_channels = model_output->dims->data[3];

        return 0;
    }

    int libtf_invoke(const unsigned char *model_data,
                     unsigned char *tensor_arena, const unsigned int tensor_arena_size,
                     libtf_input_data_callback_t input_callback, void *input_callback_data,
                     libtf_output_data_callback_t output_callback, void *output_callback_data)
    {
        tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter *error_reporter = &micro_error_reporter;

        const tflite::Model *model = tflite::GetModel(model_data);

        if (model->version() != TFLITE_SCHEMA_VERSION) {
            error_reporter->Report("Model provided is schema version is not equal to supported version!\n");
            return 1;
        }

        tflite::ops::micro::AllOpsResolver resolver;
        tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, tensor_arena_size, error_reporter);

        if (interpreter.AllocateTensors() != kTfLiteOk) {
            error_reporter->Report("AllocateTensors() failed!\n");
            return 1;
        }

        TfLiteTensor *model_input = interpreter.input(0);

        if (model_input->dims->size != 4) {
            error_reporter->Report("Input dimensions should be [n][h][w][c], e.g. 4!\n");
            return 1;
        }

        if (model_input->dims->data[0] != 1) {
            error_reporter->Report("Input dimension [n] should be 1!\n");
            return 1;
        }

        if (model_input->type != kTfLiteUInt8) {
            error_reporter->Report("Input model data type should be 8-bit quantized!\n");
            return 1;
        }

        input_callback(input_callback_data, model_input->data.uint8,
                       model_input->dims->data[1], model_input->dims->data[2], model_input->dims->data[3]);

        if (interpreter.Invoke() != kTfLiteOk) {
            error_reporter->Report("Invoke() failed!\n");
            return 1;
        }

        TfLiteTensor *model_output = interpreter.output(0);

        if (model_output->dims->size != 4) {
            error_reporter->Report("Output dimensions should be [n][h][w][c], e.g. 4!\n");
            return 1;
        }

        if (model_output->dims->data[0] != 1) {
            error_reporter->Report("Output dimension [n] should be 1!\n");
            return 1;
        }

        if (model_output->type != kTfLiteUInt8) {
            error_reporter->Report("Output model data type should be 8-bit quantized!\n");
            return 1;
        }

        output_callback(output_callback_data, model_output->data.uint8,
                        model_output->dims->data[1], model_output->dims->data[2], model_output->dims->data[3]);

        return 0;
    }
}
