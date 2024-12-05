
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import (
    equally_sized_accessor as _ods_equally_sized_accessor,
    get_default_loc_context as _ods_get_default_loc_context,
    get_op_result_or_op_results as _get_op_result_or_op_results,
    get_op_result_or_value as _get_op_result_or_value,
    get_op_results_or_values as _get_op_results_or_values,
    segmented_accessor as _ods_segmented_accessor,
)
_ods_ir = _ods_cext.ir

import builtins
from typing import Sequence as _Sequence, Union as _Union


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "fsm"

@_ods_cext.register_operation(_Dialect)
class HWInstanceOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.hw_instance"

  _ODS_REGIONS = (0, True)

  def __init__(self, outputs, name, machine, inputs, clock, reset, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    operands.append(_get_op_result_or_value(clock))
    operands.append(_get_op_result_or_value(reset))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["name"] = (name if (
    isinstance(name, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    attributes["machine"] = (machine if (
    isinstance(machine, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('FlatSymbolRefAttr')) else
      _ods_ir.AttrBuilder.get('FlatSymbolRefAttr')(machine, context=_ods_context))
    results.extend(outputs)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 3 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def clock(self):
    _ods_variadic_group_length = len(self.operation.operands) - 3 + 1
    return self.operation.operands[1 + _ods_variadic_group_length - 1]

  @builtins.property
  def reset(self):
    _ods_variadic_group_length = len(self.operation.operands) - 3 + 1
    return self.operation.operands[2 + _ods_variadic_group_length - 1]

  @builtins.property
  def name(self):
    return self.operation.attributes["name"]

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def machine(self):
    return self.operation.attributes["machine"]

  @machine.setter
  def machine(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["machine"] = value

  @builtins.property
  def outputs(self):
    _ods_variadic_group_length = len(self.operation.results) - 1 + 1
    return self.operation.results[0:0 + _ods_variadic_group_length]

def hw_instance(outputs, name, machine, inputs, clock, reset, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(HWInstanceOp(outputs=outputs, name=name, machine=machine, inputs=inputs, clock=clock, reset=reset, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class InstanceOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.instance"

  _ODS_REGIONS = (0, True)

  def __init__(self, instance, name, machine, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["name"] = (name if (
    isinstance(name, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    attributes["machine"] = (machine if (
    isinstance(machine, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('FlatSymbolRefAttr')) else
      _ods_ir.AttrBuilder.get('FlatSymbolRefAttr')(machine, context=_ods_context))
    results.append(instance)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def name(self):
    return self.operation.attributes["name"]

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def machine(self):
    return self.operation.attributes["machine"]

  @machine.setter
  def machine(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["machine"] = value

  @builtins.property
  def instance(self):
    return self.operation.results[0]

def instance(instance, name, machine, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(InstanceOp(instance=instance, name=name, machine=machine, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class MachineOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.machine"

  _ODS_REGIONS = (1, True)

  def __init__(self, sym_name, initialState, function_type, *, arg_attrs=None, res_attrs=None, argNames=None, resNames=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    isinstance(sym_name, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(sym_name, context=_ods_context))
    attributes["initialState"] = (initialState if (
    isinstance(initialState, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(initialState, context=_ods_context))
    attributes["function_type"] = (function_type if (
    isinstance(function_type, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('anonymous_408')) else
      _ods_ir.AttrBuilder.get('anonymous_408')(function_type, context=_ods_context))
    if arg_attrs is not None: attributes["arg_attrs"] = (arg_attrs if (
        isinstance(arg_attrs, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('DictArrayAttr')) else
          _ods_ir.AttrBuilder.get('DictArrayAttr')(arg_attrs, context=_ods_context))
    if res_attrs is not None: attributes["res_attrs"] = (res_attrs if (
        isinstance(res_attrs, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('DictArrayAttr')) else
          _ods_ir.AttrBuilder.get('DictArrayAttr')(res_attrs, context=_ods_context))
    if argNames is not None: attributes["argNames"] = (argNames if (
        isinstance(argNames, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('StrArrayAttr')) else
          _ods_ir.AttrBuilder.get('StrArrayAttr')(argNames, context=_ods_context))
    if resNames is not None: attributes["resNames"] = (resNames if (
        isinstance(resNames, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('StrArrayAttr')) else
          _ods_ir.AttrBuilder.get('StrArrayAttr')(resNames, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return self.operation.attributes["sym_name"]

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def initialState(self):
    return self.operation.attributes["initialState"]

  @initialState.setter
  def initialState(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["initialState"] = value

  @builtins.property
  def function_type(self):
    return self.operation.attributes["function_type"]

  @function_type.setter
  def function_type(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["function_type"] = value

  @builtins.property
  def arg_attrs(self):
    if "arg_attrs" not in self.operation.attributes:
      return None
    return self.operation.attributes["arg_attrs"]

  @arg_attrs.setter
  def arg_attrs(self, value):
    if value is not None:
      self.operation.attributes["arg_attrs"] = value
    elif "arg_attrs" in self.operation.attributes:
      del self.operation.attributes["arg_attrs"]

  @arg_attrs.deleter
  def arg_attrs(self):
    del self.operation.attributes["arg_attrs"]

  @builtins.property
  def res_attrs(self):
    if "res_attrs" not in self.operation.attributes:
      return None
    return self.operation.attributes["res_attrs"]

  @res_attrs.setter
  def res_attrs(self, value):
    if value is not None:
      self.operation.attributes["res_attrs"] = value
    elif "res_attrs" in self.operation.attributes:
      del self.operation.attributes["res_attrs"]

  @res_attrs.deleter
  def res_attrs(self):
    del self.operation.attributes["res_attrs"]

  @builtins.property
  def argNames(self):
    if "argNames" not in self.operation.attributes:
      return None
    return self.operation.attributes["argNames"]

  @argNames.setter
  def argNames(self, value):
    if value is not None:
      self.operation.attributes["argNames"] = value
    elif "argNames" in self.operation.attributes:
      del self.operation.attributes["argNames"]

  @argNames.deleter
  def argNames(self):
    del self.operation.attributes["argNames"]

  @builtins.property
  def resNames(self):
    if "resNames" not in self.operation.attributes:
      return None
    return self.operation.attributes["resNames"]

  @resNames.setter
  def resNames(self, value):
    if value is not None:
      self.operation.attributes["resNames"] = value
    elif "resNames" in self.operation.attributes:
      del self.operation.attributes["resNames"]

  @resNames.deleter
  def resNames(self):
    del self.operation.attributes["resNames"]

  @builtins.property
  def body(self):
    return self.regions[0]

def machine(sym_name, initial_state, function_type, *, arg_attrs=None, res_attrs=None, arg_names=None, res_names=None, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(MachineOp(sym_name=sym_name, initialState=initial_state, function_type=function_type, arg_attrs=arg_attrs, res_attrs=res_attrs, argNames=arg_names, resNames=res_names, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class OutputOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.output"

  _ODS_REGIONS = (0, True)

  def __init__(self, operands_, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(operands_))
    _ods_context = _ods_get_default_loc_context(loc)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def operands_(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

def output(operands_, *, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(OutputOp(operands_=operands_, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class ReturnOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.return"

  _ODS_REGIONS = (0, True)

  def __init__(self, *, operand=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if operand is not None: operands.append(_get_op_result_or_value(operand))
    _ods_context = _ods_get_default_loc_context(loc)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def operand(self):
    return None if len(self.operation.operands) < 1 else self.operation.operands[0]

def return_(*, operand=None, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(ReturnOp(operand=operand, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class StateOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.state"

  _ODS_REGIONS = (2, True)

  def __init__(self, sym_name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    isinstance(sym_name, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(sym_name, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return self.operation.attributes["sym_name"]

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def output(self):
    return self.regions[0]

  @builtins.property
  def transitions(self):
    return self.regions[1]

def state(sym_name, *, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(StateOp(sym_name=sym_name, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class TransitionOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.transition"

  _ODS_REGIONS = (2, True)

  def __init__(self, nextState, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["nextState"] = (nextState if (
    isinstance(nextState, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('FlatSymbolRefAttr')) else
      _ods_ir.AttrBuilder.get('FlatSymbolRefAttr')(nextState, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def nextState(self):
    return self.operation.attributes["nextState"]

  @nextState.setter
  def nextState(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["nextState"] = value

  @builtins.property
  def guard(self):
    return self.regions[0]

  @builtins.property
  def action(self):
    return self.regions[1]

def transition(next_state, *, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(TransitionOp(nextState=next_state, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class TriggerOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.trigger"

  _ODS_REGIONS = (0, True)

  def __init__(self, outputs, inputs, instance, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    operands.append(_get_op_result_or_value(instance))
    _ods_context = _ods_get_default_loc_context(loc)
    results.extend(outputs)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 2 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def instance(self):
    _ods_variadic_group_length = len(self.operation.operands) - 2 + 1
    return self.operation.operands[1 + _ods_variadic_group_length - 1]

  @builtins.property
  def outputs(self):
    _ods_variadic_group_length = len(self.operation.results) - 1 + 1
    return self.operation.results[0:0 + _ods_variadic_group_length]

def trigger(outputs, inputs, instance, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(TriggerOp(outputs=outputs, inputs=inputs, instance=instance, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class UpdateOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.update"

  _ODS_REGIONS = (0, True)

  def __init__(self, variable, value, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(variable))
    operands.append(_get_op_result_or_value(value))
    _ods_context = _ods_get_default_loc_context(loc)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def variable(self):
    return self.operation.operands[0]

  @builtins.property
  def value(self):
    return self.operation.operands[1]

def update(variable, value, *, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(UpdateOp(variable=variable, value=value, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class VariableOp(_ods_ir.OpView):
  OPERATION_NAME = "fsm.variable"

  _ODS_REGIONS = (0, True)

  def __init__(self, initValue, name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["initValue"] = (initValue if (
    isinstance(initValue, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('AnyAttr')) else
      _ods_ir.AttrBuilder.get('AnyAttr')(initValue, context=_ods_context))
    attributes["name"] = (name if (
    isinstance(name, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    _ods_result_type_source_attr = attributes["initValue"]
    _ods_derived_result_type = (
        _ods_ir.TypeAttr(_ods_result_type_source_attr).value
        if _ods_ir.TypeAttr.isinstance(_ods_result_type_source_attr) else
        _ods_result_type_source_attr.type)
    results.extend([_ods_derived_result_type] * 1)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def initValue(self):
    return self.operation.attributes["initValue"]

  @initValue.setter
  def initValue(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["initValue"] = value

  @builtins.property
  def name(self):
    return self.operation.attributes["name"]

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def result(self):
    return self.operation.results[0]

def variable(init_value, name, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(VariableOp(initValue=init_value, name=name, loc=loc, ip=ip))
