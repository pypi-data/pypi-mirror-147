# Copyright 2021, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for working with file systems."""

import os
import random
from typing import Any, Union

import tensorflow as tf

from tensorflow_federated.python.common_libs import py_typecheck


class FileAlreadyExistsError(Exception):
  pass


class _ValueModule(tf.Module):
  """A `tf.Module` wrapping a single value."""

  def __init__(self, value):
    super().__init__()
    self._value = value

  @tf.function(input_signature=())
  def __call__(self):
    return self._value


def read_saved_model(path: Union[str, os.PathLike[str]]) -> Any:
  """Reads a SavedModel from `path`."""
  py_typecheck.check_type(path, (str, os.PathLike))

  if isinstance(path, os.PathLike):
    path = os.fspath(path)
  module = tf.saved_model.load(path)
  return module()


def write_saved_model(value: Any,
                      path: Union[str, os.PathLike[str]],
                      overwrite: bool = False):
  """Writes `value` to `path` using the SavedModel format."""
  py_typecheck.check_type(path, (str, os.PathLike))
  py_typecheck.check_type(overwrite, bool)

  if isinstance(path, os.PathLike):
    path = os.fspath(path)

  # Create a temporary directory.
  temp_path = f'{path}_temp{random.randint(1000, 9999)}'
  if tf.io.gfile.exists(temp_path):
    tf.io.gfile.rmtree(temp_path)
  tf.io.gfile.makedirs(temp_path)

  # Write to the temporary directory.
  module = _ValueModule(value)
  tf.saved_model.save(module, temp_path, signatures={})

  # Rename the temporary directory to the final location atomically.
  if tf.io.gfile.exists(path):
    if not overwrite:
      raise FileAlreadyExistsError(f'File already exists for path: {path}')
    tf.io.gfile.rmtree(path)
  tf.io.gfile.rename(temp_path, path)
