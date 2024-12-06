from typing import Any, Dict, Optional
import logging
from ipulse_shared_base_ftredge import (
                                        LogLevel,
                                        log_warning)
from ipulse_shared_data_eng_ftredge import Pipelinemon, ContextLog

def handle_operation_exception(
    e: Exception,
    result: Dict[str, Any],
    log_level: LogLevel,
    operation_name: str,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> None:
    """Centralized error handler for GCP operations"""

    error_msg = f"EXCEPTION: {operation_name} failed: {type(e).__name__} - {str(e)}"
    result["status"]["execution_state"] += ">EXCEPTION"
    # Append to error history with separator if previous errors exist
    if result["status"]["exception_or_error_during_operation"]:
        result["status"]["exception_or_error_during_operation"] += "\n" + error_msg
    else:
        result["status"]["exception_or_error_during_operation"] = error_msg

    log_warning(
        msg=f"EXCEPTION occurred. Result Status: {result['status']}",
        logger=logger,
        print_out=print_out
    )
    
    if pipelinemon:
        pipelinemon.add_log(ContextLog(
            level=log_level,
            e=e,
            description=result["status"]
        ))
    
    if raise_e:
        raise e from e