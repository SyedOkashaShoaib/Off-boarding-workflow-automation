from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Optional 
from flask import current_app
from dataclasses import dataclass

@dataclass(frozen=True)
class EmailResult:
    success:bool
    provider_message_id : Optional[str] = None 
    error_message: Optional[str] = None


class EmailService(ABC):
    @abstractmethod
    def send_email(
        self, 
        *,
        reciepent: Sequence[str],
        Subject: str,
        html_body: str, 
        text_body: Optional[str] = None
    ) -> EmailResult: raise NotImplementedError
        

