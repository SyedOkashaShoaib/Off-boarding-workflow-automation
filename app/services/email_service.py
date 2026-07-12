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
        recipeants: Sequence[str],
        Subject: str,
        html_body: str, 
        text_body: Optional[str] = None
    ) -> EmailResult: raise NotImplementedError
        

class ConsoleEmailService(EmailService):
    def send_email(
        self, 
        *,
        recipeants: Sequence[str],
        Subject: str,
        html_body: str, 
        text_body: Optional[str] = None
    ) -> EmailResult: 
        recipeants_list = [address.strip() for address in recipeants
                           if address and address.strip()]
        if not recipeants_list: 
            return EmailResult(
                success=False,
                error_message= 'At least one recipient is required.'
            )

        print("\n" + "=" * 70)
        print("EMAIL NOTIFICATION — DEVELOPMENT MODE :)")
        print("=" * 70)
        print(f"To: {', '.join(recipeants_list)}")
        print(f"Subject: {Subject}")
        print("-" * 70)

        if text_body:
            print(text_body)
        else:
            print(html_body)
        print("=" * 70 + "\n")

        return EmailResult(
            success=True,
            provider_message_id="intern@BarretHoggard.com"
        )
    
    def create_email_service(backend_name : str)->EmailService:
        
        normalized_backend_name = backend_name.strip().lower()
        if normalized_backend_name == 'console':
            return ConsoleEmailService
        raise ValueError(
            f"Unsupported email backend : {backend_name}"
        )    
    
    def get_email_service()->EmailService:
        backend_name = current_app.config.get(
            'EMAIL_BACKEND',
            'CONSOLE'
        )

        return create_email_service(backend_name)