# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Add docstrings to Tensor functions"""
from mindspore.common.tensor import Tensor
from mindspore._c_expression import _add_docstr as add_docstr


def attach_docstr(method, docstr):
    add_docstr(getattr(Tensor, method), docstr)


attach_docstr("argmax", r"""argmax(axis=None, keepdims=False) -> Tensor

Return the indices of the maximum values of a tensor across a dimension.

Args:
    axis (Union[int, None], optional): The dimension to reduce. If `axis` is ``None`` , the indices of the maximum value 
        within the flattened input will be returned. The value of `axis` cannot exceed the dimension of `self`. Default: ``None`` .
    keepdims (bool, optional): Whether the output tensor retains the specified
        dimension. Ignored if `dim` is None. Default: ``False`` .

Returns:
    Tensor, indices of the maximum values across a dimension.

Raises:
    TypeError: If `keepdims` is not bool.
    ValueError: If `axis` is out of range.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([[1, 20, 5], [67, 8, 9], [130, 24, 15]]).astype(np.float32))
    >>> output = Tensor.argmax(x, axis=-1) # x.argmax(axis=-1)
    >>> print(output)
    [1 0 0]

.. method:: Tensor.argmax(dim=None, keepdim=False) -> Tensor

Args:
    dim (Union[int, None], optional): The dimension to reduce. If `axis` is ``None`` , the indices of the maximum value 
        within the flattened input will be returned. The value of `axis` cannot exceed the dimension of `self`. Default: ``None`` .
    keepdim (bool, optional): Whether the output tensor retains the specified
          dimension. Ignored if `dim` is None. Default: ``False`` .

Returns:
    Tensor, indices of the maximum values across a dimension.

Raises:
    TypeError: If `keepdim` is not bool.
    ValueError: If `dim` is out of range.

Supported Platforms:
    ``Ascend``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([[1, 20, 5], [67, 8, 9], [130, 24, 15]]).astype(np.float32))
    >>> output = Tensor.argmax(x, dim=-1) # x.argmax(dim=-1)
    >>> print(output)
    [1 0 0]
""")
attach_docstr("ceil", r"""ceil() -> Tensor

Rounds a tensor up to the closest integer element-wise.

.. math::
    out_i = \lceil self_i \rceil = \lfloor self_i \rfloor + 1

Returns:
    Tensor, has the same shape as `self`.

:raise TypeError: If dtype of `self` is not float16, float32, float64 or bfloat16.

    - Ascend: float16, float32, float64 or bfloat16.
    - GPU/CPU: float16, float32, float64.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1.1, 2.5, -1.5]), mindspore.float32)
    >>> output = input.ceil()
    >>> print(output)
    [ 2.  3. -1.]
    >>> input = Tensor(2.1, mindspore.float32)
    >>> output = input.ceil()
    >>> print(output)
    3.0
""")
attach_docstr("clamp", r"""clamp(min=None, max=None) -> Tensor

Clamps tensor values between the specified minimum value and maximum value.

Limits the value of :math:`self` to a range, whose lower limit is `min` and upper limit is `max` .

.. math::

    out_i= \left\{
    \begin{array}{align}
        max & \text{ if } self_i\ge max \\
        self_i & \text{ if } min \lt self_i \lt max \\
        min & \text{ if } self_i \le min \\
    \end{array}\right.

Note:
    - `min` and `max` cannot be None at the same time;
    - When `min` is None and `max` is not None, the elements in Tensor larger than `max` will become `max`;
    - When `min` is not None and `max` is None, the elements in Tensor smaller than `min` will become `min`;
    - If `min` is greater than `max`, the value of all elements in Tensor will be set to `max`;
    - The data type of `self`, `min` and `max` should support implicit type conversion and cannot be bool type.

Args:
    min (Union(Tensor, float, int), optional): The minimum value. Default: ``None`` .
    max (Union(Tensor, float, int), optional): The maximum value. Default: ``None`` .

Returns:
    Tensor, a clipped Tensor.
    The data type and shape are the same as self.

Raises:
    ValueError: If both `min` and `max` are None.
    TypeError: If the type of `self` is not Tensor.
    TypeError: If the type of `min` is not in None, Tensor, float or int.
    TypeError: If the type of `max` is not in None, Tensor, float or int.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> # case 1: the data type of input is Tensor
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> import numpy as np
    >>> min_value = Tensor(5, mindspore.float32)
    >>> max_value = Tensor(20, mindspore.float32)
    >>> input = Tensor(np.array([[1., 25., 5., 7.], [4., 11., 6., 21.]]), mindspore.float32)
    >>> output = input.clamp(min_value, max_value)
    >>> print(output)
    [[ 5. 20.  5.  7.]
     [ 5. 11.  6. 20.]]
    >>> # case 2: the data type of input is number
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> import numpy as np
    >>> min_value = 5
    >>> max_value = 20
    >>> input = Tensor(np.array([[1., 25., 5., 7.], [4., 11., 6., 21.]]), mindspore.float32)
    >>> output = input.clamp(min_value, max_value)
    >>> print(output)
    [[ 5. 20.  5.  7.]
     [ 5. 11.  6. 20.]]
""")
attach_docstr("clip", r"""clip(min=None, max=None) -> Tensor

Alias for :func:`mindspore.Tensor.clamp`.
""")
attach_docstr("clone", r"""clone() -> Tensor

Returns a copy of self.

.. warning::
    This is an experimental API that is subject to change or deletion.

Note:
    This function is differentiable, and gradients will flow back directly from the calculation
    result of the function to the `self`.

Returns:
    Tensor, with the same data, shape and type as `self`.

Supported Platforms:
    ``Ascend``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.ones((3,3)).astype("float32"))
    >>> output = input.clone()
    >>> print(output)
    [[1. 1. 1.]
     [1. 1. 1.]
     [1. 1. 1.]]
""")
attach_docstr("cos", r"""cos() -> Tensor

Computes cosine of self element-wise.

.. math::
    out_i = \cos(self_i)

.. warning::
    Using float64 may cause a problem of missing precision.

Returns:
    Tensor, has the same shape as the `self`. 
    The dtype of output is float32 when dtype of `self` is in
    [bool, int8, uint8, int16, int32, int64]. Otherwise output has the same dtype as the `self`.

:raise TypeError: If `self` is not a Tensor.
:raise TypeError:

    - CPU/GPU: If dtype of `self` is not float16, float32 or float64, complex64, complex128.
    - Ascend: If dtype of `self` is not bool, int8, uint8, int16, int32, int64, float16, float32, float64, complex64, complex128.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([0.24, 0.83, 0.31, 0.09]), mindspore.float32)
    >>> output = input.cos()
    >>> print(output)
    [0.971338 0.6748758 0.95233357 0.9959527]
""")
attach_docstr("div", r"""div(self, value, *, rounding_mode=None) -> Tensor

Divides the first input tensor by the second input tensor in floating-point type element-wise.

.. math::

    out_{i} = input_{i} / other_{i}

Note:
    - When the two inputs have different shapes, they must be able to broadcast to a common shape.
    - The two inputs can not be bool type at the same time,
      [True, Tensor(True, bool\_), Tensor(np.array([True]), bool\_)] are all considered bool type.
    - The two inputs comply with the implicit type conversion rules to make the data types
      consistent.

Args:
    self (Union[Tensor, Number, bool]): The first input is a number or
        a bool or a tensor whose data type is number or bool.
    other (Union[Tensor, Number, bool]): The second input is a number or
        a bool when the first input is a tensor or a tensor whose data type is number or bool.

Keyword Args:
    rounding_mode (str, optional): Type of rounding applied to the result. Default: ``None`` .
        Three types are defined as,

        - None: Default behavior, which is the same as true division in Python or `true_divide` in NumPy.

        - "floor": Rounds the division of the inputs down, which is the same as floor division in Python
          or `floor_divide` in NumPy.

        - "trunc": Rounds the division of the inputs towards zero, which is the same as C-style integer division.

Returns:
    Tensor, the shape is the same as the one after broadcasting,
    and the data type is the one with higher precision or higher digits among the two inputs.

Raises:
    TypeError: If `self` and `other` is not one of the following: Tensor, Number, bool.
    ValueError: If `rounding_mode` value is not None, "floor" or "trunc".

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([1.0, 2.0, 3.0]), mindspore.float32)
    >>> y = Tensor(np.array([4.0, 5.0, 6.0]), mindspore.float32)
    >>> output = x.div(y)
    >>> print(output)
    [0.25 0.4 0.5]
""")
attach_docstr("divide", r"""For details, please refer to :func:'mindspore.Tensor.div'
""")
attach_docstr("eq", r"""eq(other) -> Tensor

Computes the equivalence between two tensors element-wise.

The second argument can be a number or a tensor whose shape is broadcastable with the first argument and vise versa.

.. math::

    out_{i} =\begin{cases}
        & \text{True,    if } input_{i} = other_{i} \\
        & \text{False,   if } input_{i} \ne other_{i}
        \end{cases}

Note:
    - `input` and `other` comply with the implicit type conversion rules to make the data types consistent.
    - The input must be two Tensors, or a Tensor and a Scalar.
    - The shapes of the inputs can be broadcasted to each other.

Args:
    input (Union[Tensor, Number]): The first input is a number or
        a tensor whose data type is number.
    other (Union[Tensor, Number]): The second input is a number or
        a tensor whose data type is number.

Returns:
    Tensor, the shape is the same as the one after broadcasting, and the data type is bool.

Raises:
    TypeError: If neither `input` nor `other` is a Tensor or number.Number.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> # case 1: The shape of two inputs are different
    >>> input = Tensor([1, 2, 3], mindspore.float32)
    >>> output = input.eq(2.0)
    >>> print(output)
    [False True False]
    >>> # case 2: The shape of two inputs are the same
    >>> input = Tensor([1, 2, 3], mindspore.int32)
    >>> other = Tensor([1, 2, 4], mindspore.int32)
    >>> output = input.eq(other)
    >>> print(output)
    [ True  True False]
""")
attach_docstr("erf", r"""erf() -> Tensor

Computes the Gauss error function of `input` element-wise.

.. math::

    erf(x)=\frac{2} {\sqrt{\pi}} \int\limits_0^{x} e^{-t^{2}} dt

Args:
    input (Tensor): The input tensor of Gaussian error function. :math:`x` in the following formula.
        Supported dtypes: 

        - GPU/CPU: float16, float32, float64.
        - Ascend: float16, float32, float64, int64, bool.

Returns:
    Tensor, has the same shape as the `input`. 
    The dtype of output is float32 when dtype of `input` is in
    [bool, int64]. Otherwise output has the same dtype as the `input`.

:raise TypeError: If `input` is not a Tensor.
:raise TypeError:
        * GPU/CPU: If dtype of `input` is not float16, float32, float64.
        * Ascend: If dtype of `input` is not float16, float32, float64, int64, bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([-1, 0, 1, 2, 3]), mindspore.float32)
    >>> output = Tensor.erf(input)
    >>> print(output)
    [-0.8427168   0.          0.8427168   0.99530876  0.99997765]
""")
attach_docstr("exp", r"""exp() -> Tensor

Returns exponential of a tensor element-wise.

.. math::
    out_i = e^{x_i}

Args:
    input (Tensor): The input tensor. :math:`x` in the following formula.

Returns:
    Tensor, has the same shape as the `input`.

Raises:
    TypeError: If `input` is not a Tensor.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([0.0, 1.0, 3.0]), mindspore.float32)
    >>> output = Tensor.exp(input)
    >>> print(output)
    [ 1.        2.7182817 20.085537]
""")
attach_docstr("floor", r"""floor() -> Tensor

Rounds a tensor down to the closest integer element-wise.

.. math::

    out_i = \lfloor self_i \rfloor

Returns:
    Tensor, has the same shape as `self`.

Raises:
    TypeError: If dtype of `input` is not support. Its supported data types are:

        - Ascend: float16, float32, float64, bfloat16, int8, int16, int32, int64, uint8, uint16, uint32, uint64.
        - GPU/CPU: float16, float32, float64.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1.1, 2.5, -1.5]), mindspore.float32)
    >>> output = input.floor(input)
    >>> print(output)
    [ 1.  2. -2.]
""")
attach_docstr("gather", r"""gather(dim, index) -> Tensor

Gather data from a tensor by indices.

.. math::
    output[(i_0, i_1, ..., i_{dim}, i_{dim+1}, ..., i_n)] =
    input[(i_0, i_1, ..., index[(i_0, i_1, ..., i_{dim}, i_{dim+1}, ..., i_n)], i_{dim+1}, ..., i_n)]

.. warning::
    On Ascend, the behavior is unpredictable in the following cases:

    - the value of `index` is not in the range `[-self.shape[dim], self.shape[dim])` in forward;
    - the value of `index` is not in the range `[0, self.shape[dim])` in backward.

Args:
    dim (int): the axis to index along, must be in range `[-self.rank, self.rank)`.
    index (Tensor): The index tensor, with int32 or int64 data type. An valid `index` should be:

        - `index.rank == self.rank`;
        - for `axis != dim`, `index.shape[axis] <= self.shape[axis]`;
        - the value of `index` is in range `[-self.shape[dim], self.shape[dim])`.

Returns:
    Tensor, has the same type as `self` and the same shape as `index`.

Raises:
    ValueError: If the shape of `index` is illegal.
    ValueError: If `dim` is not in `[-self.rank, self.rank)`.
    ValueError: If the value of `index` is out of the valid range.
    TypeError: If the type of `index` is illegal.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([[-0.1, 0.3, 3.6], [0.4, 0.5, -3.2]]), mindspore.float32)
    >>> index = Tensor(np.array([[0, 0], [1, 1]]), mindspore.int32)
    >>> output = input.gather(1, index)
    >>> print(output)
    [[-0.1 -0.1]
     [0.5   0.5]]

.. method:: Tensor.gather(input_indices, axis, batch_dims=0) -> Tensor
    :noindex:

Returns the slice of the input tensor corresponding to the elements of `input_indices` on the specified `axis`.

The following figure shows the calculation process of Gather commonly:

.. image:: ../../images/Gather.png

where params represents the input `input_params`, and indices represents the index to be sliced `input_indices`.

.. note::
    1. The value of input_indices must be in the range of `[0, input_param.shape[axis])`.
       On CPU and GPU, an error is raised if an out of bound indice is found. On Ascend, the results may be
       undefined.
    2. The data type of self cannot be
       `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ on Ascend
       platform currently.

Args:
    input_indices (Tensor): Index tensor to be sliced, the shape of tensor is :math:`(y_1, y_2, ..., y_S)`.
        Specifies the indices of elements of the original Tensor. The data type can be int32 or int64.
    axis (Union(int, Tensor[int])): Specifies the dimension index to gather indices.
        It must be greater than or equal to `batch_dims`.
        When `axis` is a Tensor, the size must be 1.
    batch_dims (int): Specifies the number of batch dimensions. It must be less than or euqal to the rank
        of `input_indices`. Default: ``0`` .

Returns:
    Tensor, the shape of tensor is
    :math:`input\_params.shape[:axis] + input\_indices.shape[batch\_dims:] + input\_params.shape[axis + 1:]`.

Raises:
    TypeError:  If `axis` is not an int or Tensor.
    ValueError: If `axis` is a Tensor and its size is not 1.
    TypeError:  If `self` is not a tensor.
    TypeError:  If `input_indices` is not a tensor of type int.
    RuntimeError: If `input_indices` is out of range `[0, input_param.shape[axis])` on CPU or GPU.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> # case1: input_indices is a Tensor with shape (5, ).
    >>> input_params = Tensor(np.array([1, 2, 3, 4, 5, 6, 7]), mindspore.float32)
    >>> input_indices = Tensor(np.array([0, 2, 4, 2, 6]), mindspore.int32)
    >>> axis = 0
    >>> output = input_params.gather(input_indices=input_indices, axis=axis)
    >>> print(output)
    [1. 3. 5. 3. 7.]
    >>> # case2: input_indices is a Tensor with shape (2, 2). When the input_params has one dimension,
    >>> # the output shape is equal to the input_indices shape.
    >>> input_indices = Tensor(np.array([[0, 2], [2, 6]]), mindspore.int32)
    >>> axis = 0
    >>> output = input_params.gather(input_indices=input_indices, axis=axis)
    >>> print(output)
    [[1. 3.]
     [3. 7.]]
    >>> # case3: input_indices is a Tensor with shape (2, ) and
    >>> # input_params is a Tensor with shape (3, 4) and axis is 0.
    >>> input_params = Tensor(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), mindspore.float32)
    >>> input_indices = Tensor(np.array([0, 2]), mindspore.int32)
    >>> axis = 0
    >>> output = input_params.gather(input_indices=input_indices, axis=axis)
    >>> print(output)
    [[ 1.  2.  3.  4.]
     [ 9. 10. 11. 12.]]
    >>> # case4: input_indices is a Tensor with shape (2, ) and
    >>> # input_params is a Tensor with shape (3, 4) and axis is 1, batch_dims is 1.
    >>> input_params = Tensor(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), mindspore.float32)
    >>> input_indices = Tensor(np.array([0, 2, 1]), mindspore.int32)
    >>> axis = 1
    >>> batch_dims = 1
    >>> output = input_params.gather(input_indices, axis, batch_dims)
    >>> print(output)
    [ 1.  7. 10.]
""")
attach_docstr("greater", r"""greater(other) -> Tensor

Compare the value of the input parameters :math:`self > other` element-wise, and the output result is a bool value.

Refer to :func:`mindspore.ops.gt` for more details.

Args:
    other (Union[Tensor, Number]): It is a Number or a tensor whose data type is
        `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ or
        `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_.

Returns:
    Tensor, the shape is the same as the one after broadcasting, and the data type is bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1, 2, 3]), mindspore.int32)
    >>> other = Tensor(np.array([1, 1, 4]), mindspore.int32)
    >>> output = input.greater(other)
    >>> print(output)
    [False True False]
""")
attach_docstr("gt", r"""gt(other) -> Tensor

For details, please refer to :func:'mindspore.Tensor.greater'.
""")
attach_docstr("index_select", r"""index_select(axis, index) -> Tensor

Generates a new Tensor that accesses the values of `self` along the specified `axis` dimension
using the indices specified in `index`. The new Tensor has the same number of dimensions as `self`,
with the size of the `axis` dimension being equal to the length of `index`, and the size of all other
dimensions will be unchanged from the original `self` Tensor.

.. note::
    The value of index must be in the range of `[0, self.shape[axis])`, the result is undefined out of range.

Args:
    axis (int): The dimension to be indexed.
    index (Tensor): A 1-D Tensor with the indices to access in `self` along the specified axis.

Returns:
    Tensor, has the same dtype as `self` Tensor.

Raises:
    TypeError: If `index` is not a Tensor.
    TypeError: If `axis` is not int number.
    ValueError: If the value of `axis` is out the range of `[-self.ndim, self.ndim - 1]`.
    ValueError: If the dimension of `index` is not equal to 1.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> import numpy as np
    >>> input = Tensor(np.arange(16).astype(np.float32).reshape(2, 2, 4))
    >>> print(input)
    [[[ 0.  1.  2.  3.]
      [ 4.  5.  6.  7.]]
     [[ 8.  9. 10. 11.]
      [12. 13. 14. 15.]]]
    >>> index = Tensor([0,], mindspore.int32)
    >>> y = input.index_select(1, index)
    >>> print(y)
    [[[ 0.  1.  2.  3.]]
     [[ 8.  9. 10. 11.]]]

.. method:: Tensor.index_select(dim, index) -> Tensor

.. note::
    The value of index must be in the range of `[0, self.shape[dim])`, the result is undefined out of range.

Args:
    dim (int): The dimension to be indexed.
    index (Tensor): A 1-D Tensor with the indices to access in `self` along the specified dim.

Returns:
    Tensor, has the same dtype as `self` Tensor.

Raises:
    TypeError: If `index` is not a Tensor.
    TypeError: If `dim` is not int number.
    ValueError: If the value of `dim` is out the range of `[-self.ndim, self.ndim - 1]`.
    ValueError: If the dimension of `index` is not equal to 1.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> import numpy as np
    >>> input = Tensor(np.arange(16).astype(np.float32).reshape(2, 2, 4))
    >>> print(input)
    [[[ 0.  1.  2.  3.]
      [ 4.  5.  6.  7.]]
     [[ 8.  9. 10. 11.]
      [12. 13. 14. 15.]]]
    >>> index = Tensor([0,], mindspore.int32)
    >>> y = input.index_select(1, index)
    >>> print(y)
    [[[ 0.  1.  2.  3.]]
     [[ 8.  9. 10. 11.]]]
""")
attach_docstr("isfinite", r"""isfinite(input) -> Tensor

Determine which elements are finite for each position. If elements are not ``NaN`` , ``-INF`` , ``INF``,
they are finite.

.. math::

    out_i = \begin{cases}
      & \text{ if } x_{i} = \text{Finite},\ \ True \\
      & \text{ if } x_{i} \ne \text{Finite},\ \ False
    \end{cases}

Args:
  x (Tensor): The input tensor.

Returns:
    Tensor, has the same shape of input, and the dtype is bool.

Raises:
    TypeError: If x is not a Tensor.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([np.log(-1), 1, np.log(0)]), mindspore.float32)
    >>> output = Tensor.isfinite(x)
    >>> print(output)
    [False True False]
    >>> x = Tensor(2.1, mindspore.float64)
    >>> output = Tensor.isfinite(x)
    >>> print(output)
    True
""")
attach_docstr("le", r"""le(other) -> Tensor

Computes the boolean value of :math: `self <= other` element-wise.

.. math::

    out_{i} = \begin{cases}
        & \text{True,    if } self_{i}<=other_{i} \\
        & \text{False,   if } self_{i}>other_{i}
        \end{cases}

.. note::
    - Inputs of `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.
    - The `other` must be tensor or scalar. When the `other` is scalar, the scalar could only be a constant.

Args:
    other (Union[Tensor, number.Number, bool]): The `other` should be a number.Number or bool value,
        or a Tensor whose data type is number or bool\_.

Returns:
    Tensor, the shape is the same as the one after broadcasting, and the data type is bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([1, 2, 3]), mindspore.int32)
    >>> y = Tensor(np.array([1, 1, 4]), mindspore.int32)
    >>> output = x.le(y)
    >>> print(output)
    [ True False  True]
""")
attach_docstr("less", r"""less(other) -> Tensor

Computes the boolean value of :math:`self < other` element-wise.

The inputs of `self` and `other` follow implicit type conversion rules to ensure consistent data types.
When the `other` is Scalar, it can only be a constant.

.. math::
    out_{i} =\begin{cases}
        & \text{True,    if } self_{i}<other_{i} \\
        & \text{False,   if } self_{i}>=other_{i}
        \end{cases}

Args:
    other (Union[Tensor, Number, bool]): A number or a bool or a tensor whose data type is number or bool.

Returns:
    Tensor, the shape is the same as the one after broadcasting, and the data type is bool.

Raises:
    TypeError: If `self` and `other` is not one of the following: Tensor, Number, bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1, 2, 3]), mindspore.int32)
    >>> other = Tensor(np.array([1, 1, 4]), mindspore.int32)
    >>> output = input.less(other)
    >>> print(output)
    [False False True]
""")
attach_docstr("less_equal", r"""less_equal(other) -> Tensor

Computes the boolean value of :math:`self <= other` element-wise.

.. math::
    out_{i} =\begin{cases}
        & \text{True,    if } self_{i}<=other_{i} \\
        & \text{False,   if } self_{i}>other_{i}
        \end{cases}

.. note::
    - Inputs of `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.
    - When `other` is scalar, it could only be a constant.

Args:
    other (Union[Tensor, Number, bool]): A Number or a bool or a tensor whose data type is 
        number or bool\_.

Returns:
    Tensor, the shape is the same as the one after broadcasting, and the data type is bool.

Raises:
    TypeError: If neither `self` nor `other` is a Tensor, number.Number or bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([1, 2, 3]), mindspore.int32)
    >>> other = Tensor(np.array([1, 1, 4]), mindspore.int32)
    >>> output = x.less_equal(other)
    >>> print(output)
    [ True False  True]
""")
attach_docstr("log", r"""log() -> Tensor

Returns the natural logarithm of a tensor element-wise.

.. math::
    y_i = \log_e(self_i)

.. warning::
    If the input value of operator Log is within the range (0, 0.01] or [0.95, 1.05], the output accuracy may
    be affacted.

.. note::
    The value of `self` must be greater than 0.

Returns:
    Tensor, has the same shape as the `self`.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([1.0, 2.0, 4.0]), mindspore.float32)
    >>> output = x.log()
    >>> print(output)
    [0.        0.6931472 1.3862944]
""")
attach_docstr("logical_and", r"""logical_and(other) -> Tensor

Computes the "logical AND" of two tensors element-wise.

.. math::
    out_{i} = self_{i} \wedge other_{i}

.. note::
    - Inputs of `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.
    - When the `other` is bool, it could only be a constant.

Inputs:
    - **other** (Union[Tensor, bool]) - A bool or a tensor whose data type can be implicitly converted to bool.

Outputs:
    Tensor, the shape is the same as that of `self` and `other` after broadcasting, and the data type is bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([True, False, True]), mindspore.bool_)
    >>> other = Tensor(np.array([True, True, False]), mindspore.bool_)
    >>> output = x.logical_and(other)
    >>> print(output)
    [ True False False]
    >>> x = Tensor(1, mindspore.bool_)
    >>> other = Tensor(0, mindspore.bool_)
    >>> output = x.logical_and(other)
    >>> print(output)
    False
    >>> x = True
    >>> other = Tensor(0, mindspore.bool_)
    >>> output = x.logical_and(other)
    >>> print(output)
    False
    >>> x = True
    >>> other = Tensor(np.array([True, False]), mindspore.bool_)
    >>> output = x.logical_and(other)
    >>> print(output)
    [True False]
""")
attach_docstr("logical_not", r"""logical_not() -> Tensor

Computes the "logical NOT" of a tensor element-wise.

.. math::
    out_{i} = \neg self_{i}

Outputs:
    Tensor, the shape is the same as the `self`, and the dtype is bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([True, False, True]), mindspore.bool_)
    >>> output = input.logical_not()
    >>> print(output)
    [False  True False]
""")
attach_docstr("logical_or", r"""logical_or(other) -> Tensor

Computes the "logical OR" of two tensors element-wise.

.. math::
    out_{i} = self_{i} \\vee other_{i}

.. note::
    - Inputs of `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.
    - When the `other` is bool, it could only be a constant.

Inputs:
    - **other** (Union[Tensor, bool]) - A bool or a tensor whose data type can be implicitly converted to bool.

Outputs:
    Tensor, the shape is the same as that of `self` and `other` after broadcasting, and the data type is bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([True, False, True]), mindspore.bool_)
    >>> other = Tensor(np.array([True, True, False]), mindspore.bool_)
    >>> output = input.logical_or(other)
    >>> print(output)
    [ True  True  True]
    >>> input = Tensor(1, mindspore.bool_)
    >>> other = Tensor(0, mindspore.bool_)
    >>> output = input.logical_or(other)
    >>> print(output)
    True
    >>> input = True
    >>> other = Tensor(0, mindspore.bool_)
    >>> output = input.logical_or(other)
    >>> print(output)
    True
    >>> input = True
    >>> other = Tensor(np.array([True, False]), mindspore.bool_)
    >>> output = input.logical_or(other)
    >>> print(output)
    [True True]
""")
attach_docstr("lt", r"""lt(other) -> Tensor

For more details, please refer to :func:`mindspore.Tensor.less`.
""")
attach_docstr("masked_fill", r"""masked_fill(mask, value) -> Tensor

Fills elements of Tensor with value where mask is True.
The shapes of this tensor and `mask` need to be the same or broadcastable.

Args:
    mask (Tensor[bool]): The boolean mask.
    value (Union[Number, Tensor]): The value to fill in with, which dtype is the same as this tensor.

Returns:
    Tensor, has the same type and shape as this tensor.

Raises:
    TypeError: If dtype of `mask` is not bool.
    TypeError: If `mask` is not a Tensor.
    ValueError: If the shapes of this tensor and `mask` could not be broadcast.
    TypeError: If dtype of this tensor or `value` is not one of bool, int8, int32, int64, float16, float32, bfloat16.
    TypeError: If dtype of `value` is different from that of this tensor.
    TypeError: If `value` is neither float number nor Tensor.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input_x = Tensor(np.array([1., 2., 3., 4.]), mindspore.float32)
    >>> mask = Tensor(np.array([True, True, False, True]), mindspore.bool_)
    >>> output = Tensor.masked_fill(input_x, mask, 0.5)  #input_x.masked_fill(mask, 0.5)
    >>> print(output)
    [0.5 0.5 3.  0.5]
""")
attach_docstr("masked_select", r"""masked_select(mask) -> Tensor

Returns a new 1-D Tensor which indexes `self` according to the boolean `mask`.
The shapes of `mask` and `self` don't need to match, but they must be broadcastable.

Args:
    mask (Tensor[bool]): The shape of tensor is :math:`(x_1, x_2, ..., x_R)`.

Returns:
    A 1-D Tensor, with the same type as `self`.

Raises:
    TypeError: If `mask` is not a Tensor.
    TypeError: If dtype of `mask` is not bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([1, 2, 3, 4]), mindspore.int64)
    >>> mask = Tensor(np.array([1, 0, 1, 0]), mindspore.bool_)
    >>> output = x.masked_select(mask)
    >>> print(output)
    [1 3]
""")
attach_docstr("matmul", r"""matmul(tensor2) -> Union[Tensor, numbers.Number]

Returns the matrix product of two tensors.

Note:
    Numpy arguments `out`, `casting`, `order`, `subok`, `signature`, and `extobj` are not supported.

    The dtype of `self` and `tensor2` must be same.

    - On Ascend platform, the dims of `self` and `tensor2` must be between 1 and 6.
    - On GPU platform, the supported dtypes of `self` and `tensor2` are ms.float16 and ms.float32.

Args:
    tensor2 (Tensor): Input tensor, scalar not allowed.
        The last dimension of `self` must be the same size as the second last dimension of `tensor2`.
        And the shape of tensor and other could be broadcast.

Returns:
    Tensor or scalar, the matrix product of the inputs. This is a scalar only
    when both `self` and `tensor2` are 1-d vectors.

Raises:
    TypeError: If the dtype of `self` and the dtype of `tensor2` are not the same.
    ValueError: If the last dimension of `self` is not the same size as the
        second-to-last dimension of `tensor2`, or if a scalar value is passed in.
    ValueError: If the shape of `self` and `tensor2` could not broadcast together.
    RuntimeError: On Ascend platforms, the dims of `self` or `tensor2` is less than 1 or greater than 6.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> # case 1 : Reasonable application of broadcast mechanism
    >>> input = Tensor(np.arange(2 * 3 * 4).reshape(2, 3, 4), mindspore.float32)
    >>> other = Tensor(np.arange(4 * 5).reshape(4, 5), mindspore.float32)
    >>> output = input.matmul(other)
    >>> print(output)
    [[[  70.   76.   82.   88.   94.]
      [ 190.  212.  234.  256.  278.]
      [ 310.  348.  386.  424.  462.]]
     [[ 430.  484.  538.  592.  646.]
      [ 550.  620.  690.  760.  830.]
      [ 670.  756.  842.  928. 1014.]]]
    >>> print(output.shape)
    (2, 3, 5)
    >>> # case 2 : the rank of `tensor2` is 1
    >>> input = Tensor(np.ones([1, 2]), mindspore.float32)
    >>> other = Tensor(np.ones([2,]), mindspore.float32)
    >>> output = input.matmul(other)
    >>> print(output)
    [2.]
    >>> print(output.shape)
    (1,)
""")
attach_docstr("max", r"""max(axis=None, keepdims=False, *, initial=None, where=None, return_indices=False) -> tuple(Tensor)

Return the maximum of a tensor or maximum along an axis.

Note:
    When `axis` is ``None``, `keepdims` and subsequent parameters
    have no effect. At the same time, the index is fixed to return 0.

Args:
    axis (Union[None, int, list, tuple of ints], optional): Axis or
        axes along which to operate. By default, flattened input is used. If
        this is a tuple of ints, the maximum is selected over multiple axes,
        instead of a single axis or all the axes as before. Default: ``None`` .
    keepdims (bool, optional):
        If this is set to ``True`` , the axes which are reduced are left in the
        result as dimensions with size one. With this option, the result will
        broadcast correctly against the input array. Default: ``False`` .

Keyword Args:
    initial (scalar, optional):
        The minimum value of an output element. Must be present to allow
        computation on empty slice. Default: ``None`` .
    where (bool Tensor, optional):
        A boolean tensor which is broadcasted to match the dimensions of array,
        and selects elements to include in the reduction. If non-default value
        is passed, initial must also be provided. Default: ``True`` .
    return_indices (bool, optional): Whether to return the index of the maximum value.
        Default: ``False`` . If `axis` is a list or tuple of ints, it must be ``False`` .

Returns:
    Tensor or scalar, maximum of input tensor. If `axis` is ``None`` , the result is a scalar
    value. If `axis` is given, the result is a tensor of dimension ``self.ndim - 1``.

Raises:
    TypeError: If arguments have types not specified above.

See also:
    - :func:`mindspore.Tensor.argmin`: Return the indices of the minimum values along an axis.
    - :func:`mindspore.Tensor.argmax`: Return the indices of the maximum values along an axis.
    - :func:`mindspore.Tensor.min`: Return the minimum of a tensor or minimum along an axis.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> a = Tensor(np.arange(4).reshape((2, 2)).astype('float32'))
    >>> output = a.max()
    >>> print(output)
    3.0
    >>> value, indices = a.max(axis=0, return_indices=True)
    >>> print(value)
    [2. 3.]
    >>> print(indices)
    [1 1]

.. method:: Tensor.max() -> Tensor
    :noindex:

Returns the maximum value of all elements in `self` .

Returns:
    Tensor - Returns the maximum value of each row of `self` .

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([0.0, 0.4, 0.6, 0.7, 0.1]), mindspore.float32)
    >>> output = x.max()
    >>> print(output)
    [0.7]
""")
attach_docstr("maximum", r"""maximum(other) -> Tensor

Computes the maximum of input tensors element-wise.

.. math::
    output_i = \max(tensor_i, other_i)

Note:
    - `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.
    - The `other` can be a tensor or a scalar.
    - When `other` is a tensor,
      dtypes of `self` and `other` cannot be bool at the same time, and the shapes of them could be broadcast.
    - When `other` is a scalar, the scalar could only be a constant.
    - Broadcasting is supported.
    - If one of the elements being compared is a NaN, then that element is returned.

.. warning::
    If all inputs are of scalar int type, the output is a Tensor of type int32 in GRAPH mode 
    and a Tensor of type int64 in PYNATIVE mode.

Args:
    other (Union[Tensor, Number, bool]): The second input is a number or
        a bool or a tensor whose data type is number or bool.

Returns:
    Tensor, the shape is the same as the one after broadcasting,
    and the data type is the one with higher precision or higher digits among `self` and `other`.

Raises:
    TypeError: If `other` is not one of the following: Tensor, Number, bool.
    ValueError: If `self` and `other` are not the same shape.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> # case 1 : same data type
    >>> x = Tensor(np.array([1.0, 5.0, 3.0]), mindspore.float32)
    >>> y = Tensor(np.array([4.0, 2.0, 6.0]), mindspore.float32)
    >>> output = x.maximum(y)
    >>> print(output)
    [4. 5. 6.]
    >>> # case 2 : different data type
    >>> x = Tensor(np.array([1.0, 5.0, 3.0]), mindspore.int32)
    >>> y = Tensor(np.array([4.0, 2.0, 6.0]), mindspore.float32)
    >>> output = x.maximum(y)
    >>> print(output.dtype)
    Float32
""")
attach_docstr("mean", r"""mean(self, axis=None, keep_dims=False, dtype=None) -> Tensor

Reduces all dimension of a tensor by averaging all elements in the dimension, by default.
And reduce a dimension of `self` along the specified `axis`. `keep_dims`
determines whether the dimensions of the output and self are the same.

Note:
    The `axis` with tensor type is only used for compatibility with older versions and is not recommended.

Args:
    self (Tensor[Number]): The self tensor. The dtype of the tensor to be reduced is number.
        :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
    axis (Union[int, tuple(int), list(int), Tensor]): The dimensions to reduce. Default: ``None`` ,
        reduce all dimensions. Only constant value is allowed. Assume the rank of `self` is r,
        and the value range is [-r,r).
    keep_dims (bool): If ``True`` , keep these reduced dimensions and the length is 1.
        If ``False`` , don't keep these dimensions. Default: ``False`` .
    dtype (:class:`mindspore.dtype`): The desired data type of returned Tensor. Default: ``None`` .

Returns:
    Tensor, has the same data type as self tensor.

    - If `axis` is ``None`` , and `keep_dims` is ``False`` ,
      the output is a 0-D tensor representing the product of all elements in the self tensor.
    - If `axis` is int, set as 1, and `keep_dims` is ``False`` ,
      the shape of output is :math:`(x_0, x_2, ..., x_R)`.
    - If `axis` is tuple(int), set as (1, 2), and `keep_dims` is ``False`` ,
      the shape of output is :math:`(x_0, x_3, ..., x_R)`.
    - If `axis` is 1-D Tensor, set as [1, 2], and `keep_dims` is ``False`` ,
      the shape of output is :math:`(x_0, x_3, ..., x_R)`.

Raises:
    TypeError: If `x` is not a Tensor.
    TypeError: If `axis` is not one of the following: int, tuple, list or Tensor.
    TypeError: If `keep_dims` is not a bool.
    ValueError: If `axis` is out of range.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.random.randn(3, 4, 5, 6).astype(np.float32))
    >>> output = Tensor.mean(x, 1, keep_dims=True)
    >>> result = output.shape
    >>> print(result)
    (3, 1, 5, 6)
    >>> # case 1: Reduces a dimension by averaging all elements in the dimension.
    >>> x = Tensor(np.array([[[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]],
    ... [[4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6]],
    ... [[6, 6, 6, 6, 6, 6], [8, 8, 8, 8, 8, 8], [10, 10, 10, 10, 10, 10]]]),
    ... mindspore.float32)
    >>> output = Tensor.mean(x)
    >>> print(output)
    5.0
    >>> print(output.shape)
    ()
    >>> # case 2: Reduces a dimension along the axis 0
    >>> output = Tensor.mean(x, 0, True)
    >>> print(output)
    [[[4. 4. 4. 4. 4. 4.]
      [5. 5. 5. 5. 5. 5.]
      [6. 6. 6. 6. 6. 6.]]]
    >>> # case 3: Reduces a dimension along the axis 1
    >>> output = Tensor.mean(x, 1, True)
    >>> print(output)
    [[[2. 2. 2. 2. 2. 2.]]
     [[5. 5. 5. 5. 5. 5.]]
     [[8. 8. 8. 8. 8. 8.]]]
    >>> # case 4: Reduces a dimension along the axis 2
    >>> output = Tensor.mean(x, 2, True)
    >>> print(output)
    [[[ 2.]
      [ 2.]
      [ 2.]]
     [[ 4.]
      [ 5.]
      [ 6.]]
     [[ 6.]
      [ 8.]
      [10.]]]

.. method:: Tensor.mean(self, axis=None, keep_dims=False) -> Tensor
    :noindex:

Reduces all dimension of a tensor by averaging all elements in the dimension, by default.
And reduce a dimension of `x` along the specified `axis`. `keep_dims`
determines whether the dimensions of the output and self are the same.

Note:
    The `axis` with tensor type is only used for compatibility with older versions and is not recommended.

Args:
    x (Tensor[Number]): The self tensor. The dtype of the tensor to be reduced is number.
      :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
    axis (Union[int, tuple(int), list(int), Tensor]): The dimensions to reduce. Default: ``None`` ,
        reduce all dimensions. Only constant value is allowed. Assume the rank of `x` is r,
        and the value range is [-r,r).
    keep_dims (bool): If true, keep these reduced dimensions and the length is 1.
                      If false, don't keep these dimensions. Default: ``False`` .

Returns:
    Tensor, has the same data type as self tensor.

    - If `axis` is None, and `keep_dims` is False,
      the output is a 0-D tensor representing the product of all elements in the self tensor.
    - If `axis` is int, set as 1, and `keep_dims` is False,
      the shape of output is :math:`(x_0, x_2, ..., x_R)`.
    - If `axis` is tuple(int), set as (1, 2), and `keep_dims` is ``False`` ,
      the shape of output is :math:`(x_0, x_3, ..., x_R)`.

Raises:
    TypeError: If `x` is not a Tensor.
    TypeError: If `axis` is not one of the following: int, tuple, list or Tensor.
    TypeError: If `keep_dims` is not a bool.
    ValueError: If `axis` is out of range.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.random.randn(3, 4, 5, 6).astype(np.float32))
    >>> output = Tensor.mean(x, 1, keep_dims=True)
    >>> result = output.shape
    >>> print(result)
    (3, 1, 5, 6)
    >>> # case 1: Reduces a dimension by averaging all elements in the dimension.
    >>> x = Tensor(np.array([[[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]],
    ... [[4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6]],
    ... [[6, 6, 6, 6, 6, 6], [8, 8, 8, 8, 8, 8], [10, 10, 10, 10, 10, 10]]]),
    ... mindspore.float32)
    >>> output = Tensor.mean(x)
    >>> print(output)
    5.0
    >>> print(output.shape)
    ()
    >>> # case 2: Reduces a dimension along the axis 0
    >>> output = Tensor.mean(x, 0, True)
    >>> print(output)
    [[[4. 4. 4. 4. 4. 4.]
      [5. 5. 5. 5. 5. 5.]
      [6. 6. 6. 6. 6. 6.]]]
    >>> # case 3: Reduces a dimension along the axis 1
    >>> output = Tensor.mean(x, 1, True)
    >>> print(output)
    [[[2. 2. 2. 2. 2. 2.]]
     [[5. 5. 5. 5. 5. 5.]]
     [[8. 8. 8. 8. 8. 8.]]]
    >>> # case 4: Reduces a dimension along the axis 2
    >>> output = Tensor.mean(x, 2, True)
    >>> print(output)
    [[[ 2.]
      [ 2.]
      [ 2.]]
     [[ 4.]
      [ 5.]
      [ 6.]]
     [[ 6.]
      [ 8.]
      [10.]]]
""")
attach_docstr("min", r"""min(input) -> Tensor

Calculates the minimum value of the input tensor.

Also see :func:`mindspore.ops.extend.min`.

.. min(input, axis=None, keepdims=False, *, initial=None, where=True, return_indices=False) -> Tensor, number

Return the minimum of a tensor or minimum along an axis.

Note:
    When `axis` is ``None``, `keepdims` and subsequent parameters
    have no effect. At the same time, the index is fixed to return 0.

Args:
    axis (Union[None, int, list, tuple of ints], optional): An axis or
        axes along which to operate. By default, flattened input is used. If
        `axis` is a tuple of ints, the minimum is selected over multiple axes,
        instead of a single axis or all the axes as before. Default: ``None`` .
    keepdims (bool, optional):
        If ``True`` , the axes which are reduced are left in the
        result as dimensions with size one. With this option, the result will
        broadcast correctly against the input array. Default: ``False`` .

Keyword Args:
    initial (scalar, optional):
        The minimum value of an output element. Must be present to allow
        computation on empty slice. Default: ``None`` .
    where (Tensor[bool], optional):
        A boolean tensor which is broadcasted to match the dimensions of array,
        and selects elements to include in the reduction. If non-default value
        is passed, initial must also be provided. Default: ``True`` .
    return_indices (bool, optional): Whether to return the index of the minimum value. Default: ``False`` .
        If `axis` is a list or tuple of ints, it must be ``False`` .

Returns:
    Tensor or scalar, minimum of input tensor. If `axis` is ``None`` , the result is a scalar
    value. If `axis` is given, the result is a tensor of dimension ``self.ndim - 1``.

Raises:
    TypeError: If arguments have types not specified above.

See also:
    - :func:`mindspore.Tensor.argmin`: Return the indices of the minimum values along an axis.
    - :func:`mindspore.Tensor.argmax`: Return the indices of the maximum values along an axis.
    - :func:`mindspore.Tensor.max`: Return the minimum of a tensor or minimum along an axis.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> a = Tensor(np.arange(4).reshape((2, 2)).astype('float32'))
    >>> output = Tensor.min(a)
    >>> print(output)
    0.0
    >>> output = Tensor.min(a, axis=0)
    >>> print(output)
    [0. 1.]
    >>> output = Tensor.min(a, axis=0, initial=9, where=Tensor([False]))
    >>> print(output)
    [9. 9.]
    >>> output = Tensor.min(a, axis=0, initial=9, where=Tensor([False, True]))
    >>> print(output)
    [9. 1.]
    >>> value, indices = Tensor.min(a, axis=0, return_indices=True)
    >>> print(value)
    [0. 1.]
    >>> print(indices)
    [0 0]
""")
attach_docstr("minimum", r"""minimum(other) -> Tensor

Computes the minimum of input tensors element-wise.

.. math::
    output_i = \min(tensor_i, other_i)

Note:
    - `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.
    - The `other` can be a tensor or a scalar.
    - When `other` is a tensor,
      dtypes of `self` and `other` cannot be bool at the same time, and the shapes of them could be broadcast.
    - When `other` is a scalar, the scalar could only be a constant.
    - Broadcasting is supported.
    - If one of the elements being compared is a NaN, then that element is returned.

Args:
    other (Union[Tensor, Number, bool]): The input is a number or
        a bool or a tensor whose data type is number or bool.

Returns:
    Tensor, the shape is the same as the one after broadcasting,
    and the data type is the one with higher precision or higher digits among `self` and `other`.

Raises:
    TypeError: If `other` is not one of the following: Tensor, Number, bool.
    ValueError: If `self` and `other` are not the same shape after broadcast.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> # case 1 : same data type
    >>> x = Tensor(np.array([1.0, 5.0, 3.0]), mindspore.float32)
    >>> y = Tensor(np.array([4.0, 2.0, 6.0]), mindspore.float32)
    >>> output = x.minimum(y)
    >>> print(output)
    [1. 2. 3.]
    >>> # case 2 : different data type
    >>> x = Tensor(np.array([1.0, 5.0, 3.0]), mindspore.int32)
    >>> y = Tensor(np.array([4.0, 2.0, 6.0]), mindspore.float32)
    >>> output = x.minimum(y)
    >>> print(output.dtype)
    Float32
""")
attach_docstr("mul", r"""mul(other) -> Tensor

Multiplies two tensors element-wise.

.. math::

    out_{i} = tensor_{i} * other_{i}

Note:
    - When `self` and `other` have different shapes,
      they must be able to broadcast to a common shape.
    - `self` and `other` can not be bool type at the same time,
      [True, Tensor(True, bool\_), Tensor(np.array([True]), bool\_)] are all considered bool type.
    - `self` and `other` comply with the implicit type conversion rules to make the data types
      consistent.

Args:
    other (Union[Tensor, number.Number, bool]): `other` is a number.Number or
        a bool or a tensor whose data type is number.Number and bool.

Returns:
    Tensor, the shape is the same as the one after broadcasting,
    and the data type is the one with higher precision or higher digits among `self` and `other` .

Raises:
    TypeError: If `other` is not one of the following: Tensor, number.Number, bool.
    ValueError: If `self` and `other` are not the same shape.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([1.0, 2.0, 3.0]), mindspore.float32)
    >>> y = Tensor(np.array([4.0, 5.0, 6.0]), mindspore.float32)
    >>> output = x.mul(y)
    >>> print(output)
    [ 4. 10. 18.]
""")
attach_docstr("nan_to_num", r"""nan_to_num(nan, posinf, neginf) -> Tensor

Replace the `NaN`, positive infinity and negative infinity values of the `self` with the
specified values in `nan`, `posinf` and `neginf` respectively.

.. warning::
    For Ascend, it is only supported on Atlas A2 Training Series Products.
    This is an experimental API that is subject to change or deletion.

Args:
    nan (number, optional): The replace value of `NaN`. Default: ``None``.
    posinf (number, optional): the value to replace positive infinity values with. Default: ``None``,
        replacing positive infinity with the maximum value supported by the data type of `self`.
    neginf (number, optional): the value to replace negative infinity values with. Default: ``None``,
        replacing negative infinity with the minimum value supported by the data type of `self`.

Returns:
    Tensor, has the same shape and dtype as `self`.

Supported Platforms:
    ``Ascend`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([float('nan'), float('inf'), -float('inf'), 5.0]), mindspore.float32)
    >>> output = input.nan_to_num(1.0, 2.0, 3.0)
    >>> print(output)
    [1.  2.  3.  5.0]
""")
attach_docstr("ne", r"""ne(other) -> Tensor

Computes the non-equivalence of two tensors element-wise.

Note:
    - `self` and `other` comply with the implicit type conversion rules to make the data types 
      consistent.
    - The `other` can be a tensor or a scalar.
    - When `other` is a tensor, the shapes of `self` and `other` could be broadcast.
    - When `other` is a scalar, it could only be a constant.
    - Broadcasting is supported.

.. math::

    out_{i} =\begin{cases}
    & \text{True,    if } tensor_{i} \ne other_{i} \\
    & \text{False,   if } tensor_{i} = other_{i}
    \end{cases}

Args:
    other (Union[Tensor, number.Number, bool]): `other` is a number.Number or
        a bool or a tensor whose data type is number.Number and bool.

Returns:
    Tensor, the shape is the same as the one after broadcasting, and the data type is bool.

Raises:
    TypeError: If `other` is not one of the following: Tensor, Number, bool.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> from mindspore import Tensor
    >>> x = Tensor([1, 2, 3], mindspore.float32)
    >>> output = x.ne(2.0)
    >>> print(output)
    [ True False  True]
    >>>
    >>> x = Tensor([1, 2, 3], mindspore.int32)
    >>> y = Tensor([1, 2, 4], mindspore.int32)
    >>> output = x.ne(y)
    >>> print(output)
    [False False  True]
""")
attach_docstr("neg", r"""neg() -> Tensor

Returns a tensor with negative values of `self` element-wise.

.. math::
    out_{i} = - tensor_{i}

Returns:
    Tensor, has the same shape and dtype as `self`.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1, 2, -1, 2, 0, -3.5]), mindspore.float32)
    >>> output = input.neg()
    >>> print(output)
    [-1.  -2.   1.  -2.   0.   3.5]
""")
attach_docstr("negative", r"""negative() -> Tensor

Alias for :func:`mindspore.Tensor.neg`.
""")
attach_docstr("new_ones", r"""new_ones(size, dtype=None) -> Tensor

Return a tensor of `size` filled with ones.

Args:
    size (Union[int, tuple(int), list(int)]): An int, list or tuple of integers defining the output shape.
    dtype (:class:`mindspore.dtype`, optional): The desired dtype of the output tensor. If None, the returned
        tensor has the same dtype as `self`. Default: ``None``.

Outputs:
    Tensor, the shape and dtype is defined above and filled with ones.

Raises:
    TypeError: If `size` is neither an int nor a tuple/list of int.
    TypeError: If `dtype` is not a MindSpore dtype.
    ValueError: If `size` contains negative values.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> from mindspore import Tensor
    >>> x = Tensor([1, 2, 3, 4], mindspore.int32)
    >>> output = x.new_ones((2, 3))
    >>> print(output)
    [[1 1 1]
     [1 1 1]]
""")
attach_docstr("new_zeros", r"""new_zeros(size, dtype=None) -> Tensor

Return a tensor of `size` filled with zeros.

Args:
    size (Union[int, tuple(int), list(int)]): An int, list or tuple of integers defining the output shape.
    dtype (:class:`mindspore.dtype`, optional): The desired dtype of the output tensor. If None, the returned
        tensor has the same dtype as `self`. Default: ``None``.

Outputs:
    Tensor, the shape and dtype is defined above and filled with zeros.

Raises:
    TypeError: If `size` is neither an int nor a tuple/list of int.
    TypeError: If `dtype` is not a MindSpore dtype.
    ValueError: If `size` contains negative values.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> from mindspore import Tensor
    >>> x = Tensor([1, 2, 3, 4], mindspore.int32)
    >>> output = x.new_zeros((2, 3))
    >>> print(output)
    [[0 0 0]
     [0 0 0]]
""")
attach_docstr("pow", r"""pow(exponent) -> Tensor

Calculates the `exponent` power of each element in `self`.

When `exponent` is a Tensor, the shapes of `self` and `exponent` must be broadcastable.

.. math::

    out_{i} = self_{i} ^{ exponent_{i}}

Args:
    exponent (Union[Tensor, Number]): The second self is a Number or a tensor whose data type is
        `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ or
        `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_.

Returns:
    Tensor, the shape is the same as the one after broadcasting,
    and the data type is the one with higher precision or higher digits among the two inputs.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1.0, 2.0, 4.0]), mindspore.float32)
    >>> exponent = 3.0
    >>> output = input.pow(exponent)
    >>> print(output)
    [ 1.  8. 64.]
    >>>
    >>> input = Tensor(np.array([1.0, 2.0, 4.0]), mindspore.float32)
    >>> exponent = Tensor(np.array([2.0, 4.0, 3.0]), mindspore.float32)
    >>> output = input.pow(exponent)
    >>> print(output)
    [ 1. 16. 64.]
""")
attach_docstr("prod", r"""prod(dim, keepdim, dtype) -> Tensor

Reduces a dimension of a tensor by multiplying all elements in the dimension, by default. And also can
reduce a dimension of `self` along the `dim`. Determine whether the dimensions of the output and self are the
same by controlling `keepdim`.

Args:
    dim (Union[int, tuple(int), list(int), Tensor], optional): The dimensions to reduce. Default: ``None`` , reduce all dimensions.
        Only constant value is allowed. Assume the rank of `self` is r, and the value range is [-r,r).
    keepdim (bool, optional): If ``True`` , keep these reduced dimensions and the length is 1.
        If ``False`` , don't keep these dimensions. Default: ``False`` .
    dtype (:class:`mindspore.dtype`, optional): The desired data type of returned Tensor. Default: ``None`` .

Returns:
    Tensor.

    - If `dim` is ``None`` , and `keepdim` is ``False`` ,
      the output is a 0-D tensor representing the product of all elements in the self tensor.
    - If `dim` is int, set as 1, and `keepdim` is ``False`` ,
      the shape of output is :math:`(self_0, self_2, ..., self_R)`.
    - If `dim` is tuple(int) or list(int), set as (1, 2), and `keepdim` is ``False`` ,
      the shape of output is :math:`(self_0, self_3, ..., self_R)`.
    - If `dim` is 1-D Tensor, set as [1, 2], and `keepdim` is ``False`` ,
      the shape of output is :math:`(self_0, self_3, ..., self_R)`.

Raises:
    TypeError: If `dim` is not one of the following: int, Tuple, list or Tensor.
    TypeError: If `keepdim` is not a bool.
    ValueError: If `dim` is out of range.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.random.randn(3, 4, 5, 6).astype(np.float32))
    >>> output = Tensor.pord(x, 1, True)
    >>> result = output.shape
    >>> print(result)
    (3, 1, 5, 6)
    >>> # case 1: Reduces a dimension by multiplying all elements in the dimension.
    >>> x = Tensor(np.array([[[1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3]],
    ...                      [[4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6]],
    ...                      [[7, 7, 7, 7, 7, 7], [8, 8, 8, 8, 8, 8], [9, 9, 9, 9, 9, 9]]]), mindspore.float32)
    >>> output = Tensor.prod(x)
    >>> print(output)
    2.2833798e+33
    >>> print(output.shape)
    ()
    >>> # case 2: Reduces a dimension along axis 0.
    >>> output = Tensor.prod(x, 0, True)
    >>> print(output)
    [[[ 28.  28.  28.  28.  28.  28.]
      [ 80.  80.  80.  80.  80.  80.]
      [162. 162. 162. 162. 162. 162.]]]
    >>> # case 3: Reduces a dimension along axis 1.
    >>> output = Tensor.prod(x, 1, True)
    >>> print(output)
    [[[  6.   6.   6.   6.   6.   6.]]
     [[120. 120. 120. 120. 120. 120.]]
     [[504. 504. 504. 504. 504. 504.]]]
    >>> # case 4: Reduces a dimension along axis 2.
    >>> output = Tensor.prod(x, 2, True)
    >>> print(output)
    [[[1.00000e+00]
      [6.40000e+01]
      [7.29000e+02]]
     [[4.09600e+03]
      [1.56250e+04]
      [4.66560e+04]]
     [[1.17649e+05]
      [2.62144e+05]
      [5.31441e+05]]]


.. method:: Tensor.prod(axis, keep_dims, dtype)-> Tensor
    :noindex:

For more details, please refer to :func:`mindspore.ops.prod`.
""")
attach_docstr("reciprocal", r"""reciprocal() -> Tensor

Returns reciprocal of a tensor element-wise.

.. math::

    out_{i} =  \frac{1}{self_{i}}

Returns:
    Tensor, has the same shape as the `self`.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1.0, 2.0, 4.0]), mindspore.float32)
    >>> output = input.reciprocal()
    >>> print(output)
    [1.   0.5  0.25]
""")
attach_docstr("remainder", r"""remainder(self, divisor) -> Tensor

Computes the remainder of `self` divided by `other` element-wise. The result has the same sign as the divisor and
its absolute value is less than that of `other`.

Supports broadcasting to a common shape and implicit type promotion.

.. math::

    remainder(input, other) = input - input.div(other, rounding\_mode="floor") * other

Note:
    Complex inputs are not supported. At least one input need to be tensor, but not both are bool tensors.

Args:
    self (Union[Tensor, numbers.Number, bool]): The dividend is a numbers.Number or
        a bool or a tensor whose data type is
        `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ or
        `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_.
    other (Union[Tensor, numbers.Number, bool]): The divisor is a numbers.Number or
        a bool or a tensor whose data type is number or bool\_ when the dividend is a tensor.
        When the dividend is Scalar, the divisor must be a Tensor whose data type is number or bool\_.

Returns:
    Tensor, with dtype promoted and shape broadcasted.

Raises:
    TypeError: If `self` and `other` are not of types: (tensor, tensor), (tensor, number), (tensor, bool),
        (number, tensor) or (bool, tensor).
    ValueError: If `self` and `other` are not broadcastable.

Supported Platforms:
    ``Ascend``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([-4.0, 5.0, 6.0]).astype(np.float32))
    >>> y = Tensor(np.array([3.0, 2.0, 3.0]).astype(np.float64))
    >>> output = x.remainder(y)
    >>> print(output)
    [2.  1.  0.]
""")
attach_docstr("repeat_interleave", r"""repeat_interleave(self, repeats, dim=None, output_size=None) -> Tensor

Repeat elements of a tensor along an axis, like `numpy.repeat`.

.. warning::
    Only support on Atlas A2 training series.

Args:
    self (Tensor): The tensor to repeat values for. Must be of type: float16,
        float32, int8, uint8, int16, int32, or int64.
    repeats (Union[int, tuple, list, Tensor]): The number of times to repeat, must be positive.
    dim (int, optional): The dim along which to repeat, Default: ``None``. if dims is None,
        the self Tensor will be flattened and the output will alse be flattened.
    output_size (int, optional): Total output size for the given axis (e.g. sum of repeats),
        Default: ``None``.

Returns:
    One tensor with values repeated along the specified dim. If self has shape
    :math:`(s1, s2, ..., sn)` and dim is i, the output will have shape :math:`(s1, s2, ...,
    si * repeats, ..., sn)`. The output type will be the same as the type of `self`.

Supported Platforms:
    ``Ascend``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([[0, 1, 2], [3, 4, 5]]), mindspore.int32)
    >>> output = input.repeat_interleave(repeats=2, dim=0)
    >>> print(output)
    [[0 1 2]
     [0 1 2]
     [3 4 5]
     [3 4 5]]
""")
attach_docstr("reshape", r"""reshape(*shape) -> Tensor

Rearranges self Tensor based on the given shape.

The `shape` can only have one -1 at most, in which case it's inferred from the remaining dimensions and
the number of elements in self Tensor.

Args:
    shape (Union[tuple[int], list[int], Tensor[int]]): If `shape` is a tuple or list, its elements should be
        integers, and only constant value is allowed. i.e., :math:`(y_1, y_2, ..., y_S)`. If `shape` is a Tensor,
        data type should be int32 or int64, and only one-dimensional tensor is supported.

Returns:
    Tensor, If the given `shape` does not contain -1, the `shape` of tensor is :math:`(y_1, y_2, ..., y_S)`.
    If the k-th position in the given `shape` is -1, the `shape` of tensor is :math:`(y_1, ..., y_{k-1},
    \frac{\prod_{i=1}^{R}x_{i}}{y_1\times ...\times y_{k-1}\times y_{k+1}\times...\times y_S} , y_{k+1}, ..., y_S)`

Raises:
    ValueError: The given `shape` contains more than one -1.
    ValueError: The given `shape` contains elements less than -1.
    ValueError: For scenarios where the given `shape` does not contain -1, the product of elements of the given
        `shape` is not equal to the product of self tensor's `shape`,
        :math:`\prod_{i=1}^{R}x_{i} \ne \prod_{i=1}^{S}y_{i}`, (Namely, it does not match self tensor's array size).
        And for scenarios where the given `shape` contains -1, the product of elements other than -1 of the given
        `shape` is an aliquant part of the product of self tensor's `shape` :math:`\prod_{i=1}^{R}x_{i}`.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([[-0.1, 0.3, 3.6], [0.4, 0.5, -3.2]]), mindspore.float32)
    >>> output = Tensor.reshape(input, (3, 2))
    >>> print(output)
    [[-0.1  0.3]
     [ 3.6  0.4]
     [ 0.5 -3.2]]
""")
attach_docstr("round", r"""round(decimals) -> Tensor

Returns half to even of a tensor element-wise.

.. math::
    out_i \approx self_i

.. note::
    The self data types supported by the Ascend platform include 
    bfloat16 (Atlas training series products are not supported), float16, float32, float64, int32, and int64.

Args:
    decimals (int, optional) - Number of decimal places to round to (default: ``0``). If decimals is 
    negative, it specifies the number of positions to the left of the decimal point. It supports 
    converting the single-element tensor to an int.

Returns:
    Tensor, has the same shape and type as the `self`.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([0.8, 1.5, 2.3, 2.5, -4.5]), mindspore.float32)
    >>> output = input.round()
    >>> print(output)
    [ 1.  2.  2.  2. -4.]
""")
attach_docstr("rsqrt", r"""rsqrt() -> Tensor

Computes reciprocal of square root of self tensor element-wise.

.. math::

    out_{i} = \frac{1}{\sqrt{self_{i}}}

Returns:
    Tensor, has the same shape and dtype as the `self`.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore as ms
    >>> from mindspore import Tensor
    >>> input = Tensor([-0.0370,  0.2970,  1.5420, -0.9105])
    >>> output = input.rsqrt()
    >>> print(output)
    [       nan 1.8349396  0.8053002        nan]
""")
attach_docstr("sigmoid", r"""sigmoid(self) -> Tensor

Computes Sigmoid of self element-wise. The Sigmoid function is defined as:

.. math::

    \text{sigmoid}(x_i) = \frac{1}{1 + \exp(-x_i)}

where :math:`x_i` is an element of `x`.

Sigmoid Function Graph:

.. image:: ../../images/Sigmoid.png
    :align: center

Args:
    self (Tensor): `self` is :math:`x` in the preceding formula. Tensor of any dimension,
        the data type is float16, float32, float64, complex64 or complex128.

Returns:
    Tensor, with the same type and shape as the self.

Raises:
    TypeError: If dtype of `self` is not float16, float32, float64, complex64 or complex128.
    TypeError: If `self` is not a Tensor.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor, ops
    >>> input = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
    >>> output = ops.sigmoid(input)
    >>> print(output)
    [0.7310586  0.880797   0.95257413 0.98201376 0.9933072 ]
""")
attach_docstr("sort", r"""sort(self, dim=-1, descending=False) -> (Tensor, Tensor)

Sorts the elements of the self tensor along the given dimension in the specified order.

.. warning::
    Currently, the data types of float16, uint8, int8, int16, int32, int64 are well supported.
    If use float32, it may cause loss of accuracy.

Args:
    self(Tensor): The self tensor to sort.
        The shape is :math:`(N,*)` where :math:`*` means, any number of additional dimensions.

Keyword Args:
    dim (int, optional): The dimension to sort along. Default: ``-1``, means the last dimension.
    descending (bool, optional): Controls the sort order. If `descending` is True, the elements
        are sorted in descending order, or else sorted in ascending order. Default: ``False`` .
    stable (bool, optional): Controls the sort order. If stable is True then the sorting routine
        becomes stable, preserving the order of equivalent elements. Default: ``False`` .

Returns:
    - y1, a tensor whose values are the sorted values, with the same shape and data type as self.
    - y2, a tensor that consists of the indices of the elements in the original self tensor.
      Data type is int64.

Raises:
    TypeError: If `dim` is not an int.
    TypeError: If `descending` is not a bool.
    TypeError: If `self` not in float16, float32, uint8, int8, int16, int32, int64, bfloat16
    TypeError: If `stable` is not a bool.
    ValueError: If `dim` is not in range of [-len(self.shape), len(self.shape)).

Supported Platforms:
    ``Ascend``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([[8, 2, 1], [5, 9, 3], [4, 6, 7]]), mindspore.float16)
    >>> output = x.sort()
    >>> # The output below is based on the Ascend platform.
    >>> print(output)
    (Tensor(shape=[3, 3], dtype=Float16, value=
    [[ 1.0000e+00,  2.0000e+00,  8.0000e+00],
    [ 3.0000e+00,  5.0000e+00,  9.0000e+00],
    [ 4.0000e+00,  6.0000e+00,  7.0000e+00]]), Tensor(shape=[3, 3], dtype=Int64, value=
    [[2, 1, 0],
    [2, 0, 1],
    [0, 1, 2]]))

.. method:: Tensor.sort(self, axis=-1, descending=False) -> (Tensor, Tensor)
    :noindex:

Args:
    self(Tensor): The self tensor to sort.
        The shape is :math:`(N,*)` where :math:`*` means, any number of additional dimensions.
    axis (int, optional): The dimension to sort along. Default: ``-1``, means the last dimension.
        The Ascend backend only supports sorting the last dimension.
    descending (bool, optional): Controls the sort order. If `descending` is True, the elements
        are sorted in descending order, or else sorted in ascending order. Default: ``False`` .

.. warning::
    Currently, the data types of float16, uint8, int8, int16, int32, int64 are well supported.
    If use float32, it may cause loss of accuracy.

Returns:

    - y1, a tensor whose values are the sorted values, with the same shape and data type as self.
    - y2, a tensor that consists of the indices of the elements in the original self tensor.
      Data type is int32.

Raises:
    TypeError: If `axis` is not an int.
    TypeError: If `descending` is not a bool.
    TypeError: If dtype of `self` is neither float16, float32, uint8, int8, int16, int32, int64.
    ValueError: If `axis` is not in range of [-len(self.shape), len(self.shape)).

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([[8, 2, 1], [5, 9, 3], [4, 6, 7]]), mindspore.float16)
    >>> output = x.sort(axis=-1)
    >>> # The output below is based on the Ascend platform.
    >>> print(output)
    (Tensor(shape=[3, 3], dtype=Float16, value=
    [[ 1.0000e+00,  2.0000e+00,  8.0000e+00],
    [ 3.0000e+00,  5.0000e+00,  9.0000e+00],
    [ 4.0000e+00,  6.0000e+00,  7.0000e+00]]), Tensor(shape=[3, 3], dtype=Int32, value=
    [[2, 1, 0],
    [2, 0, 1],
    [0, 1, 2]]))
""")
attach_docstr("split", r"""split(self, split_size_or_sections, axis=0) -> Tensor

Splits the Tensor into chunks along the given axis.

Args:
    tensor (Tensor): A Tensor to be divided.
    split_size_or_sections (Union[int, tuple(int), list(int)]):
        If `split_size_or_sections` is an int type, `tensor` will be split into equally sized chunks,
        each chunk with size `split_size_or_sections`. Last chunk will be smaller than `split_size_or_sections`
        if `tensor.shape[axis]` is not divisible by `split_size_or_sections`.
        If `split_size_or_sections` is a list type, then `tensor` will be split into len(split_size_or_sections)
        chunks with sizes `split_size_or_sections` along the given `axis`.
    axis (int): The axis along which to split. Default: ``0`` .

Returns:
    A tuple of sub-tensors.

Raises:
    TypeError: If argument `tensor` is not Tensor.
    TypeError: If argument `axis` is not int.
    ValueError: If argument `axis` is out of range of :[-tensor.ndim, tensor.ndim).
    TypeError: If each element in `split_size_or_sections` is not integer.
    TypeError: If argument `split_size_or_sections` is not int, tuple(int) or list(int).
    ValueError: The sum of `split_size_or_sections` is not equal to x.shape[axis].

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input_x = np.arange(9).astype("float32")
    >>> output = Tensor.split(Tensor(input_x), 3)
    >>> print(output)
    (Tensor(shape=[3], dtype=Float32, value= [ 0.00000000e+00,  1.00000000e+00,  2.00000000e+00]),
     Tensor(shape=[3], dtype=Float32, value= [ 3.00000000e+00,  4.00000000e+00,  5.00000000e+00]),
     Tensor(shape=[3], dtype=Float32, value= [ 6.00000000e+00,  7.00000000e+00,  8.00000000e+00]))
""")
attach_docstr("tanh", r"""tanh() -> Tensor

Computes hyperbolic tangent of input element-wise. The Tanh function is defined as:

.. math::

    tanh(x_i) = \frac{\exp(x_i) - \exp(-x_i)}{\exp(x_i) + \exp(-x_i)} = \frac{\exp(2x_i) - 1}{\exp(2x_i) + 1},

where :math:`x_i` is an element of the input Tensor.

Tanh Activation Function Graph:

.. image:: ../../images/Tanh.png
    :align: center

Args:
    input (Tensor): Input of Tanh.

Returns:
    Tensor, with the same type and shape as the `input`.

Raises:
    TypeError: If `input` is not a Tensor.

Supported Platforms:
    ``Ascend`` ``GPU``  ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
    >>> output = Tensor.tanh(input)
    >>> print(output)
    [0.7615941 0.9640276 0.9950547 0.9993293 0.9999092]
""")
attach_docstr("tile", r"""tile(dims) -> Tensor

Replicates an tensor with given dims times.

Note:
    On Ascend, the number of `dims` should not exceed 8, and currently does not support scenarios
    where more than 4 dimensions are repeated simultaneously.

Args:
    dims (tuple[int]): The parameter that specifies the number of replications,
        the parameter type is tuple, and the data type is int, i.e., :math:`(y_1, y_2, ..., y_S)`.
        Only constant value is allowed.

Returns:
    Tensor, has the same data type as the `self`. Suppose the length of `dims` is `d`,
    the dimension of `self` is `self.dim`, and the shape of `self` is :math:`(x_1, x_2, ..., x_S)`.

    - If `self.dim = d`, then the shape of their corresponding positions can be multiplied, and
      the shape of Outputs is :math:`(x_1*y_1, x_2*y_2, ..., x_S*y_S)`.
    - If `self.dim < d`, prepend 1 to the shape of `self` until their lengths are consistent.
      Such as set the shape of `self` as :math:`(1, ..., x_1, x_2, ..., x_S)`,
      then the shape of their corresponding positions can be multiplied, and the shape of Outputs is
      :math:`(1*y_1, ..., x_R*y_R, x_S*y_S)`.
    - If `self.dim > d`, prepend 1 to `dims` until their lengths are consistent. Such as set the
      `dims` as :math:`(1, ..., y_1, y_2, ..., y_S)`, then the shape of their corresponding positions
      can be multiplied, and the shape of Outputs is :math:`(x_1*1, ..., x_R*y_R, x_S*y_S)`.

Raises:
    TypeError: If `dims` is not a tuple or not all elements are int.
    ValueError: If not all elements of `dims` are greater than or equal to 0.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> input = Tensor(np.array([[1, 2], [3, 4]]), mindspore.float32)
    >>> dims = (2, 3)
    >>> output = input.tile(dims)
    >>> print(output)
    [[1.  2.  1.  2.  1.  2.]
     [3.  4.  3.  4.  3.  4.]
     [1.  2.  1.  2.  1.  2.]
     [3.  4.  3.  4.  3.  4.]]
    >>> dims = (2, 3, 2)
    >>> output = input.tile(dims)
    >>> print(output)
    [[[1. 2. 1. 2.]
      [3. 4. 3. 4.]
      [1. 2. 1. 2.]
      [3. 4. 3. 4.]
      [1. 2. 1. 2.]
      [3. 4. 3. 4.]]
     [[1. 2. 1. 2.]
      [3. 4. 3. 4.]
      [1. 2. 1. 2.]
      [3. 4. 3. 4.]
      [1. 2. 1. 2.]
      [3. 4. 3. 4.]]]


.. method:: Tensor.tile(reps) -> Tensor
    :noindex:

For more details, please refer to :func:`mindspore.ops.tile`.
""")
attach_docstr("to", r"""to(dtype) -> Tensor

    Returns a tensor with the new specified data type.

    Note:
        When converting complex numbers to boolean type, the imaginary part of the complex number is not
        taken into account. As long as the real part is non-zero, it returns True; otherwise, it returns False.

    Args:
        dtype (dtype.Number): The valid data type of the output tensor. Only constant value is allowed.

    Returns:
        Tensor, the data type of the tensor is `dtype`.

    Raises:
        TypeError: If `dtype` is not a Number.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> input_np = np.random.randn(2, 3, 4, 5).astype(np.float32)
        >>> input = Tensor(input_np)
        >>> dtype = mindspore.int32
        >>> output = input.to(dtype)
        >>> print(output.dtype)
        Int32
        >>> print(output.shape)
        (2, 3, 4, 5)
""")
attach_docstr("tril", r"""transpose(input, diagonal=0) -> Tensor

Returns the lower triangle part of `input` (elements that contain the diagonal and below),
and set the other elements to zeros.

Args:
    input (Tensor): A Tensor with shape :math:`(x_1, x_2, ..., x_R)`. The rank must be at least 2.
      Supporting all number types including bool.
    diagonal (int, optional): An optional attribute indicates the diagonal to consider, default: 0,
        indicating the main diagonal.

Returns:
    Tensor, the same shape and data type as the `input`.

Raises:
    TypeError: If `input` is not a Tensor.
    TypeError: If `diagonal` is not an int.
    TypeError: If the type of `input` is neither number nor bool.
    ValueError: If the rank of `input` is less than 2.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [10, 11, 12, 13],
    ...                      [14, 15, 16, 17]]))
    >>> result = Tensor.tril(x)
    >>> print(result)
    [[ 1  0  0  0]
     [ 5  6  0  0]
     [10 11 12  0]
     [14 15 16 17]]
    >>> x = Tensor(np.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [10, 11, 12, 13],
    ...                      [14, 15, 16, 17]]))
    >>> result = Tensor.tril(x, diagonal=1)
    >>> print(result)
    [[ 1  2  0  0]
     [ 5  6  7  0]  
     [10 11 12 13]
     [14 15 16 17]]
    >>> x = Tensor(np.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [10, 11, 12, 13],
    ...                      [14, 15, 16, 17]]))
    >>> result = Tensor.tril(x, diagonal=-1)
    >>> print(result)
    [[ 0  0  0  0]
     [ 5  0  0  0]
     [10 11  0  0]
     [14 15 16  0]]
""")
attach_docstr("triu", r"""triu(diagonal) -> Tensor

Returns the upper triangle part of 'self' (elements that contain the diagonal and below),
and set the other elements to zeros.

.. warning::
    This is an experimental API that is subject to change or deletion.

Args:
    diagonal (int, optional): An optional attribute indicates the diagonal to consider, default: ``0`` ,
        indicating the main diagonal.

Returns:
    Tensor, a tensor has the same shape and data type as `self`.

Raises:
    TypeError: If `diagonal` is not an int.
    ValueError: If the dimension of `self` is less than 2.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [10, 11, 12, 13],
    ...                      [14, 15, 16, 17]]))
    >>> result = x.triu()
    >>> print(result)
    [[ 1  2  3  4]
     [ 0  6  7  8]
     [ 0  0 12 13]
     [ 0  0  0 17]]
    >>> x = Tensor(np.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [10, 11, 12, 13],
    ...                      [14, 15, 16, 17]]))
    >>> result = x.triu(diagonal=1)
    >>> print(result)
    [[ 0  2  3  4]
     [ 0  0  7  8]
     [ 0  0  0 13]
     [ 0  0  0  0]]
    >>> x = Tensor(np.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [10, 11, 12, 13],
    ...                      [14, 15, 16, 17]]))
    >>> result = x.triu(diagonal=-1)
    >>> print(result)
    [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 0 11 12 13]
     [ 0  0 16 17]]
""")
attach_docstr("trunc", r"""Returns a new tensor with the truncated integer values of the elements of the input tensor.

Args:
    input (Tensor): The input tensor.

Returns:
    Tensor, the same shape and data type as the input.

Raises:
    TypeError: If `input` is not a Tensor.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import mindspore
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> x = Tensor(np.array([3.4742, 0.5466, -0.8008, -3.9079]),mindspore.float32)
    >>> output = x.trunc()
    >>> print(output)
    [3. 0. 0. -3.]
""")
attach_docstr("where", r"""where(condition, y) -> Tensor

Selects elements from `self` or `y` based on `condition` and returns a tensor.

.. math::
    output_i = \begin{cases} self_i,\quad &if\ condition_i \\ y_i,\quad &otherwise \end{cases}

Args:
    condition (Tensor[bool]): If True, yield `self`, otherwise yield `y`.
    y (Union[Tensor, Scalar]): When `condition` is False, values to select from.

Returns:
    Tensor, elements are selected from `self` and `y`.

Raises:
    TypeError: If `condition` is not a Tensor.
    ValueError: If `condition`, `self` and `y` can not broadcast to each other.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``

Examples:
    >>> import numpy as np
    >>> from mindspore import Tensor
    >>> from mindspore import dtype as mstype
    >>> a = Tensor(np.arange(4).reshape((2, 2)), mstype.float32)
    >>> b = Tensor(np.ones((2, 2)), mstype.float32)
    >>> condition = a < 3
    >>> output = a.where(condition, b)
    >>> print(output)
    [[0. 1.]
     [2. 1.]]
""")
