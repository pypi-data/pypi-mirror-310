import inspect

from typing import Any, Optional, Callable, List
from pydantic import BaseModel, create_model


def function_to_model(
    func: Callable, exclude_params: List[str] = ["model", "provider"]
) -> BaseModel:
    exclude_params = exclude_params or []
    signature = inspect.signature(func)
    fields = {
        name: (
            param.annotation,
            ...,
        )
        for name, param in signature.parameters.items()
        if name not in exclude_params and not name.startswith("_")
    }

    return create_model(f"{func.__name__.capitalize()}Model", **fields)


def function_to_str(
    func: Callable,
) -> str:
    return str(inspect.signature(func))


def _model_from_function(func: callable) -> BaseModel:
    info = _extract_function_info(func)

    # Prepare a dictionary for model fields
    model_fields = {}

    for param in info["params"]:
        param_name = param["name"]
        param_type = _map_type_string_to_python(
            param["type"]
        )  # Convert string to actual type

        model_fields[param_name] = (
            Optional[param_type],
            None,
        )  # Default to None for optional parameters

    # Create the Pydantic model
    return create_model(info["name"] + "Inputs", **model_fields)


def _map_type_string_to_python(type_str: str):
    mapping = {
        "<class 'str'>": str,
        "<class 'int'>": int,
        "<class 'float'>": float,
        "<class 'bool'>": bool,
        # Add other mappings as needed
    }
    return mapping.get(type_str, Any)  # Default to Any if unknown


def _extract_function_info(func: callable) -> dict:
    name = func.__name__
    docstring = inspect.getdoc(func)
    signature = inspect.signature(func)

    params = []
    for param_name, param in signature.parameters.items():
        if param_name not in ["ai", "model"]:
            param_info = {
                "name": param_name,
                "type": str(param.annotation)
                if param.annotation is not inspect.Parameter.empty
                else None,
                "default": param.default
                if param.default is not inspect.Parameter.empty
                else None,
            }
            params.append(param_info)

    return {"name": name, "doc": docstring, "params": params}
