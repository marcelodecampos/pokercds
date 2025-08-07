#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reusable password change form component.
"""

import reflex as rx
import asyncio
from typing import Optional, Callable
from ..utils.password import verify_password, hash_password


class PasswordFormState(rx.State):
    """Base state for password change operations."""
    
    # Form fields
    current_password: str = ""
    new_password: str = ""
    confirm_password: str = ""
    
    # Form state
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    require_current_password: bool = True
    
    def set_current_password(self, value: str):
        """Set current password value."""
        self.current_password = value
        
    def set_new_password(self, value: str):
        """Set new password value."""
        self.new_password = value
        
    def set_confirm_password(self, value: str):
        """Set confirm password value."""
        self.confirm_password = value
    
    def clear_messages(self):
        """Clear error and success messages."""
        self.error_message = ""
        self.success_message = ""
    
    def clear_form(self):
        """Clear all form fields."""
        self.current_password = ""
        self.new_password = ""
        self.confirm_password = ""
        self.clear_messages()
    
    def _validate_form(self) -> bool:
        """Validate password form fields."""
        self.clear_messages()
        
        # Check if current password is required and provided
        if self.require_current_password and not self.current_password.strip():
            self.error_message = "Senha atual é obrigatória"
            return False
        
        # Check new password
        if not self.new_password.strip():
            self.error_message = "Nova senha é obrigatória"
            return False
        
        # Check password length
        if len(self.new_password) < 6:
            self.error_message = "Nova senha deve ter pelo menos 6 caracteres"
            return False
        
        # Check password confirmation
        if self.new_password != self.confirm_password:
            self.error_message = "Confirmação de senha não confere"
            return False
        
        return True


def PasswordForm(
    form_state: PasswordFormState,
    title: str = "Alterar Senha",
    show_current_password: bool = True,
    on_submit: Optional[Callable] = None,
    on_cancel: Optional[Callable] = None,
) -> rx.Component:
    """
    Reusable password change form component.
    
    Args:
        form_state: The form state instance
        title: Form title
        show_current_password: Whether to show current password field
        on_submit: Submit handler function
        on_cancel: Cancel handler function
    """
    
    form_fields = rx.vstack(
        # Current Password Field (conditional)
        rx.cond(
            show_current_password,
            rx.vstack(
                rx.text("Senha Atual", size="3", font_weight="medium"),
                rx.input(
                    placeholder="Digite sua senha atual",
                    type="password",
                    value=form_state.current_password,
                    on_change=form_state.set_current_password,
                    size="3",
                    width="100%",
                ),
                width="100%",
                spacing="1",
            ),
        ),
        
        # New Password Field
        rx.vstack(
            rx.text("Nova Senha", size="3", font_weight="medium"),
            rx.input(
                placeholder="Digite sua nova senha",
                type="password",
                value=form_state.new_password,
                on_change=form_state.set_new_password,
                size="3",
                width="100%",
            ),
            rx.text(
                "Mínimo de 6 caracteres",
                size="1",
                color="gray.9",
            ),
            width="100%",
            spacing="1",
        ),
        
        # Confirm Password Field
        rx.vstack(
            rx.text("Confirmar Nova Senha", size="3", font_weight="medium"),
            rx.input(
                placeholder="Digite novamente sua nova senha",
                type="password",
                value=form_state.confirm_password,
                on_change=form_state.set_confirm_password,
                size="3",
                width="100%",
            ),
            width="100%",
            spacing="1",
        ),
        
        spacing="4",
        width="100%",
    )
    
    # Messages
    messages = rx.vstack(
        rx.cond(
            form_state.error_message != "",
            rx.text(
                form_state.error_message,
                color="red.500",
                size="2",
            ),
        ),
        rx.cond(
            form_state.success_message != "",
            rx.text(
                form_state.success_message,
                color="green.500",
                size="2",
            ),
        ),
        width="100%",
        spacing="1",
    )
    
    # Buttons
    button_group = rx.hstack(
        rx.cond(
            on_cancel is not None,
            rx.button(
                "Cancelar",
                variant="outline",
                on_click=on_cancel,
                disabled=form_state.is_loading,
            ),
        ),
        rx.button(
            rx.cond(
                form_state.is_loading,
                rx.hstack(
                    rx.spinner(size="1"),
                    rx.text("Alterando..."),
                    spacing="2",
                ),
                rx.text("Alterar Senha"),
            ),
            on_click=on_submit,
            disabled=form_state.is_loading,
        ),
        spacing="3",
        justify="end",
        width="100%",
    )
    
    return rx.card(
        rx.vstack(
            rx.heading(title, size="6", margin_bottom="1.5rem"),
            form_fields,
            messages,
            button_group,
            spacing="4",
            width="100%",
        ),
        padding="2rem",
        width="100%",
        max_width="500px",
    )
