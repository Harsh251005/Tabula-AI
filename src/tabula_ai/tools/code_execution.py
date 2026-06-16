# tabula_ai/tools/execute_python.py

from agents import function_tool
import io
import time
import contextlib

# Import any runtime helpers you want the generated code to use
from tabula_ai.runtime.sheets_runtime import runtime_append_rows


# Persistent runtime for the current process
EXECUTION_CONTEXT = {
    "append_rows": runtime_append_rows,
}


@function_tool
def execute_python(code: str) -> dict:
    """
    Executes Python code in a persistent runtime.

    Available runtime functions:
    - append_rows(spreadsheet_id, sheet_name, values)

    Variables created during execution remain available
    for future executions while the process is running.
    """

    print("[TOOL] Executing Python code")

    stdout_buffer = io.StringIO()
    start_time = time.time()

    try:
        with contextlib.redirect_stdout(stdout_buffer):
            exec(code, EXECUTION_CONTEXT)

        return {
            "success": True,
            "stdout": stdout_buffer.getvalue(),
            "execution_time_ms": round(
                (time.time() - start_time) * 1000,
                2
            ),
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": stdout_buffer.getvalue(),
            "error": str(e),
            "execution_time_ms": round(
                (time.time() - start_time) * 1000,
                2
            ),
        }

