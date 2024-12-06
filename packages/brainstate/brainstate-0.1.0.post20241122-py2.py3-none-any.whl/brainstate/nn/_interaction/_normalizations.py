# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# -*- coding: utf-8 -*-

from __future__ import annotations

import numbers
from typing import Callable, Union, Sequence, Optional, Any

import jax
import jax.numpy as jnp

from brainstate import environ, init
from brainstate._state import LongTermState, ParamState
from brainstate.nn._module import Module
from brainstate.typing import DTypeLike, ArrayLike, Size, Axes

__all__ = [
    'BatchNorm0d', 'BatchNorm1d', 'BatchNorm2d', 'BatchNorm3d',
]


def _canonicalize_axes(ndim: int, feature_axes: Sequence[int]):
    axes = []
    for axis in feature_axes:
        if axis < 0:
            axis += ndim
        if axis < 0 or axis >= ndim:
            raise ValueError(f'Invalid axis {axis} for {ndim}D input')
        axes.append(axis)
    return tuple(axes)


def _abs_sq(x):
    """Computes the elementwise square of the absolute value |x|^2."""
    if jnp.iscomplexobj(x):
        return jax.lax.square(jax.lax.real(x)) + jax.lax.square(jax.lax.imag(x))
    else:
        return jax.lax.square(x)


def _compute_stats(
    x: ArrayLike,
    axes: Sequence[int],
    dtype: DTypeLike,
    axis_name: Optional[str] = None,
    axis_index_groups: Optional[Sequence[int]] = None,
    use_mean: bool = True,
):
    """Computes mean and variance statistics.

    This implementation takes care of a few important details:
    - Computes in float32 precision for stability in half precision training.
    - mean and variance are computable in a single XLA fusion,
      by using Var = E[|x|^2] - |E[x]|^2 instead of Var = E[|x - E[x]|^2]).
    - Clips negative variances to zero which can happen due to
      roundoff errors. This avoids downstream NaNs.
    - Supports averaging across a parallel axis and subgroups of a parallel axis
      with a single `lax.pmean` call to avoid latency.

    Arguments:
      x: Input array.
      axes: The axes in ``x`` to compute mean and variance statistics for.
      dtype: tp.Optional dtype specifying the minimal precision. Statistics
        are always at least float32 for stability (default: dtype of x).
      axis_name: tp.Optional name for the pmapped axis to compute mean over.
      axis_index_groups: tp.Optional axis indices.
      use_mean: If true, calculate the mean from the input and use it when
        computing the variance. If false, set the mean to zero and compute
        the variance without subtracting the mean.

    Returns:
      A pair ``(mean, val)``.
    """
    if dtype is None:
        dtype = jax.numpy.result_type(x)
    # promote x to at least float32, this avoids half precision computation
    # but preserves double or complex floating points
    dtype = jax.numpy.promote_types(dtype, environ.dftype())
    x = jnp.asarray(x, dtype)

    # Compute mean and mean of squared values.
    mean2 = jnp.mean(_abs_sq(x), axes)
    if use_mean:
        mean = jnp.mean(x, axes)
    else:
        mean = jnp.zeros(mean2.shape, dtype=dtype)

    # If axis_name is provided, we need to average the mean and mean2 across
    if axis_name is not None:
        concatenated_mean = jnp.concatenate([mean, mean2])
        mean, mean2 = jnp.split(
            jax.lax.pmean(
                concatenated_mean,
                axis_name=axis_name,
                axis_index_groups=axis_index_groups,
            ),
            2,
        )

    # mean2 - _abs_sq(mean) is not guaranteed to be non-negative due
    # to floating point round-off errors.
    var = jnp.maximum(0.0, mean2 - _abs_sq(mean))
    return mean, var


def _normalize(
    x: ArrayLike,
    mean: Optional[ArrayLike],
    var: Optional[ArrayLike],
    weights: Optional[ParamState],
    reduction_axes: Sequence[int],
    dtype: DTypeLike,
    epsilon: Union[numbers.Number, jax.Array],
):
    """Normalizes the input of a normalization layer and optionally applies a learned scale and bias.

    Arguments:
      x: The input.
      mean: Mean to use for normalization.
      var: Variance to use for normalization.
      weights: The scale and bias parameters.
      reduction_axes: The axes in ``x`` to reduce.
      dtype: The dtype of the result (default: infer from input and params).
      epsilon: Normalization epsilon.

    Returns:
      The normalized input.
    """
    if mean is not None:
        assert var is not None, 'mean and val must be both None or not None.'
        stats_shape = list(x.shape)
        for axis in reduction_axes:
            stats_shape[axis] = 1
        mean = mean.reshape(stats_shape)
        var = var.reshape(stats_shape)
        y = x - mean
        mul = jax.lax.rsqrt(var + jnp.asarray(epsilon, dtype))
        y = y * mul
        if weights is not None:
            y = _scale_operation(y, weights.value)
    else:
        assert var is None, 'mean and val must be both None or not None.'
        assert weights is None, 'scale and bias are not supported without mean and val'
        y = x
    return jnp.asarray(y, dtype)


def _scale_operation(x, param):
    if 'scale' in param:
        x = x * param['scale']
    if 'bias' in param:
        x = x + param['bias']
    return x


class _BatchNorm(Module):
    __module__ = 'brainstate.nn'
    num_spatial_dims: int

    def __init__(
        self,
        in_size: Size,
        feature_axis: Axes = -1,
        track_running_stats: bool = True,
        epsilon: float = 1e-5,
        momentum: float = 0.99,
        affine: bool = True,
        bias_initializer: Union[ArrayLike, Callable] = init.Constant(0.),
        scale_initializer: Union[ArrayLike, Callable] = init.Constant(1.),
        axis_name: Optional[Union[str, Sequence[str]]] = None,
        axis_index_groups: Optional[Sequence[Sequence[int]]] = None,
        name: Optional[str] = None,
        dtype: Any = None,
    ):
        super().__init__(name=name)

        # parameters
        self.in_size = tuple(in_size)
        self.out_size = tuple(in_size)
        self.affine = affine
        self.bias_initializer = bias_initializer
        self.scale_initializer = scale_initializer
        self.dtype = dtype or environ.dftype()
        self.track_running_stats = track_running_stats
        self.momentum = jnp.asarray(momentum, dtype=self.dtype)
        self.epsilon = jnp.asarray(epsilon, dtype=self.dtype)

        # parameters about axis
        feature_axis = (feature_axis,) if isinstance(feature_axis, int) else feature_axis
        self.feature_axis = _canonicalize_axes(len(in_size), feature_axis)
        self.axis_name = axis_name
        self.axis_index_groups = axis_index_groups

        # variables
        feature_shape = tuple([ax if i in self.feature_axis else 1 for i, ax in enumerate(in_size)])
        if self.track_running_stats:
            self.running_mean = LongTermState(jnp.zeros(feature_shape, dtype=self.dtype))
            self.running_var = LongTermState(jnp.ones(feature_shape, dtype=self.dtype))
        else:
            self.running_mean = None
            self.running_var = None

        # parameters
        if self.affine:
            assert track_running_stats, "Affine parameters are not needed when track_running_stats is False."
            bias = init.param(self.bias_initializer, feature_shape)
            scale = init.param(self.scale_initializer, feature_shape)
            self.weight = ParamState(dict(bias=bias, scale=scale))
        else:
            self.weight = None

    def update(self, x):
        # input shape and batch mode or not
        if x.ndim == self.num_spatial_dims + 2:
            x_shape = x.shape[1:]
            batch = True
        elif x.ndim == self.num_spatial_dims + 1:
            x_shape = x.shape
            batch = False
        else:
            raise ValueError(f"expected {self.num_spatial_dims + 2}D (with batch) or "
                             f"{self.num_spatial_dims + 1}D (without batch) input (got {x.ndim}D input, {x.shape})")
        if self.in_size != x_shape:
            raise ValueError(f"The expected input shape is {self.in_size}, while we got {x_shape}.")

        # reduce the feature axis
        if batch:
            reduction_axes = tuple(i for i in range(x.ndim) if (i - 1) not in self.feature_axis)
        else:
            reduction_axes = tuple(i for i in range(x.ndim) if i not in self.feature_axis)

        # fitting phase
        fit_phase = environ.get('fit', desc='Whether this is a fitting process. Bool.')

        # compute the running mean and variance
        if self.track_running_stats:
            if fit_phase:
                mean, var = _compute_stats(
                    x,
                    reduction_axes,
                    dtype=self.dtype,
                    axis_name=self.axis_name,
                    axis_index_groups=self.axis_index_groups,
                )
                self.running_mean.value = self.momentum * self.running_mean.value + (1 - self.momentum) * mean
                self.running_var.value = self.momentum * self.running_var.value + (1 - self.momentum) * var
            else:
                mean = self.running_mean.value
                var = self.running_var.value
        else:
            mean, var = None, None

        # normalize
        return _normalize(x, mean, var, self.weight, reduction_axes, self.dtype, self.epsilon)


class BatchNorm0d(_BatchNorm):
    r"""1-D batch normalization [1]_.

    The data should be of `(b, l, c)`, where `b` is the batch dimension,
    `l` is the layer dimension, and `c` is the channel dimension.

    %s
    """
    __module__ = 'brainstate.nn'
    num_spatial_dims: int = 0


class BatchNorm1d(_BatchNorm):
    r"""1-D batch normalization [1]_.

    The data should be of `(b, l, c)`, where `b` is the batch dimension,
    `l` is the layer dimension, and `c` is the channel dimension.

    %s
    """
    __module__ = 'brainstate.nn'
    num_spatial_dims: int = 1


class BatchNorm2d(_BatchNorm):
    r"""2-D batch normalization [1]_.

    The data should be of `(b, h, w, c)`, where `b` is the batch dimension,
    `h` is the height dimension, `w` is the width dimension, and `c` is the
    channel dimension.

    %s
    """
    __module__ = 'brainstate.nn'
    num_spatial_dims: int = 2


class BatchNorm3d(_BatchNorm):
    r"""3-D batch normalization [1]_.

    The data should be of `(b, h, w, d, c)`, where `b` is the batch dimension,
    `h` is the height dimension, `w` is the width dimension, `d` is the depth
    dimension, and `c` is the channel dimension.

    %s
    """
    __module__ = 'brainstate.nn'
    num_spatial_dims: int = 3


_bn_doc = r'''

  This layer aims to reduce the internal covariant shift of data. It
  normalizes a batch of data by fixing the mean and variance of inputs
  on each feature (channel). Most commonly, the first axis of the data
  is the batch, and the last is the channel. However, users can specify
  the axes to be normalized.

  .. math::
     y=\frac{x-\mathrm{E}[x]}{\sqrt{\operatorname{Var}[x]+\epsilon}} * \gamma+\beta

  .. note::
      This :attr:`momentum` argument is different from one used in optimizer
      classes and the conventional notion of momentum. Mathematically, the
      update rule for running statistics here is
      :math:`\hat{x}_\text{new} = \text{momentum} \times \hat{x} + (1-\text{momentum}) \times x_t`,
      where :math:`\hat{x}` is the estimated statistic and :math:`x_t` is the
      new observed value.

  Parameters
  ----------
  in_size: sequence of int
    The input shape, without batch size.
  feature_axis: int, tuple, list
    The feature or non-batch axis of the input.
  track_running_stats: bool
    A boolean value that when set to ``True``, this module tracks the running mean and variance, 
    and when set to ``False``, this module does not track such statistics, and initializes 
    statistics buffers ``running_mean`` and ``running_var`` as ``None``. When these buffers are ``None``, 
    this module always uses batch statistics. in both training and eval modes. Default: ``True``.
  momentum: float
    The value used for the ``running_mean`` and ``running_var`` computation. Default: 0.99
  epsilon: float
    A value added to the denominator for numerical stability. Default: 1e-5
  affine: bool
    A boolean value that when set to ``True``, this module has
    learnable affine parameters. Default: ``True``
  bias_initializer: ArrayLike, Callable
    An initializer generating the original translation matrix. If not ``None``, bias (beta) is added. 
    Default: ``init.Constant(0.)``
  scale_initializer: ArrayLike, Callable
    An initializer generating the original scaling matrix. If not ``None``, multiply by scale (gamma).
    Default: ``init.Constant(1.)``
  axis_name: optional, str, sequence of str
    If not ``None``, it should be a string (or sequence of
    strings) representing the axis name(s) over which this module is being
    run within a jax map (e.g. ``jax.pmap`` or ``jax.vmap``). Supplying this
    argument means that batch statistics are calculated across all replicas
    on the named axes.
  axis_index_groups: optional, sequence
    Specifies how devices are grouped. Valid
    only within ``jax.pmap`` collectives.
    Groups of axis indices within that named axis
    representing subsets of devices to reduce over (default: None). For
    example, `[[0, 1], [2, 3]]` would independently batch-normalize over
    the examples on the first two and last two devices. See `jax.lax.psum`
    for more details.

  References
  ----------
  .. [1] Ioffe, Sergey and Christian Szegedy. “Batch Normalization: Accelerating Deep Network Training
         by Reducing Internal Covariate Shift.” ArXiv abs/1502.03167 (2015): n. pag.

'''

BatchNorm1d.__doc__ = BatchNorm1d.__doc__ % _bn_doc
BatchNorm2d.__doc__ = BatchNorm2d.__doc__ % _bn_doc
BatchNorm3d.__doc__ = BatchNorm3d.__doc__ % _bn_doc
