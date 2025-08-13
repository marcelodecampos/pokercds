#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Change password page for users.
"""

import reflex as rx
import asyncio
from ..components.password_form import PasswordForm, PasswordFormState
from ..state.auth_state import AuthState


class ChangePasswordState(PasswordFormState):
    """State for change password page."""
    
    require_current_password: bool = True
    
    async def handle_submit(self):
        """Handle password change form submission."""
        self.is_loading = True
        self.clear_messages()
        
        try:
            # Validate form
            if not self._validate_form():
                return
            
            # TODO: Verify current password against database
            # For now, simulate verification with hardcoded password
            if self.current_password != "admin123":
                self.error_message = "Senha atual incorreta"
                return
            
            # TODO: Implement database update
            # For now, simulate API call
            await asyncio.sleep(1)
            
            # Clear form and show success
            self.clear_form()
            self.success_message = "Senha alterada com sucesso!"
            
        except Exception as e:
            self.error_message = f"Erro ao alterar senha: {str(e)}"
            
        finally:
            self.is_loading = False
    
    def handle_cancel(self):
        """Handle cancel action."""
        return rx.redirect("/profile")


@rx.page(route="/change-password", title="PokerCDS - Alterar Senha", on_load=AuthState.require_auth)
def change_password_page() -> rx.Component:
    """Change password page."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.hstack(
                    rx.button(
                        rx.icon("arrow-left", size=16, id="change-password-back-icon"),
                        "Voltar",
                        variant="outline",
                        on_click=lambda: rx.redirect("/profile"),
                        id="change-password-back-button",
                    ),
                    rx.heading("Alterar Senha", size="6", id="change-password-page-title"),
                    justify="between",
                    align="center",
                    width="100%",
                    id="change-password-header-content",
                ),
                max_width="1200px",
                id="change-password-header-container",
            ),
            padding="1.5rem 0",
            width="100%",
            id="change-password-header",
        ),
        
        # Main content
        rx.container(
            rx.vstack(
                rx.text(
                    "Para sua segurança, digite sua senha atual e escolha uma nova senha.",
                    size="3",
                    text_align="center",
                    margin_bottom="2rem",
                    id="change-password-description",
                ),
                
                # Password form
                PasswordForm(
                    form_state=ChangePasswordState,
                    title="Alterar Minha Senha",
                    show_current_password=True,
                    on_submit=ChangePasswordState.handle_submit,
                    on_cancel=ChangePasswordState.handle_cancel,
                ),
                
                spacing="4",
                align="center",
                width="100%",
                id="change-password-main-content",
            ),
            max_width="1200px",
            padding="2rem",
            id="change-password-main-container",
        ),
        
        min_height="100vh",
        id="change-password-page",
    )
