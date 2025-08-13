#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login form component for user authentication.
"""

import reflex as rx
import asyncio
from typing import Optional
from ..state.auth_state import AuthState


class LoginState(rx.State):
    """State for login form."""
    
    cpf: str = ""
    password: str = ""
    is_loading: bool = False
    error_message: str = ""
    
    def set_cpf(self, value: str):
        """Set CPF value."""
        self.cpf = value
        
    def set_password(self, value: str):
        """Set password value."""
        self.password = value
    
    def _validate_required_fields(self) -> bool:
        """Validate that required fields are filled."""
        if not self.cpf or not self.password:
            self.error_message = "CPF e senha são obrigatórios"
            return False
        return True
    
    def _validate_cpf_format(self) -> tuple[bool, str]:
        """Validate CPF format and return cleaned CPF."""
        clean_cpf = ''.join(filter(str.isdigit, self.cpf))
        
        if len(clean_cpf) != 11:
            self.error_message = "CPF deve ter 11 dígitos"
            return False, ""
        
        return True, clean_cpf
    
    def _validate_credentials(self, clean_cpf: str) -> dict | None:
        """Validate user credentials and return user data if valid."""
        # Temporary validation (replace with actual database check)
        if clean_cpf == "59469390415" and self.password == "admin123":
            # Return user session data (temporary - replace with database query)
            user_data = {
                "id": 1,
                "name": "Marcelo de Campos",
                "nickname": "That's Poker",
                "email": "sr.marcelo.campos@gmail.com",
                "is_admin": True,
            }
            print("DEBUG: Credentials validated, returning user_data:", user_data)
            return user_data
        
        self.error_message = "CPF ou senha inválidos"
        return None
    
    async def handle_login(self):
        """Handle login form submission."""
        self.is_loading = True
        self.error_message = ""
        
        try:
            # Validate required fields
            if not self._validate_required_fields():
                return
                
            # Validate CPF format
            is_valid_cpf, clean_cpf = self._validate_cpf_format()
            if not is_valid_cpf:
                return
                
            # Simulate authentication delay
            await asyncio.sleep(1)
            
            # Validate credentials
            user_data = self._validate_credentials(clean_cpf)
            if user_data:
                # Get auth state and login user
                print("DEBUG: About to call AuthState.login_user")
                auth_state = await self.get_state(AuthState)
                auth_state.login_user(user_data)
                print("DEBUG: AuthState.login_user called successfully")
                
                # Success - redirect to dashboard
                self.error_message = ""
                return rx.redirect("/dashboard")
            
            return rx.toast.error(self.error_message)
        finally:
            self.is_loading = False


def LoginForm() -> rx.Component:
    """Login form component."""
    return rx.container(
        rx.vstack(
            # Logo/Title
            rx.heading(
                "PokerCDS",
                size="9",
                margin_bottom="2rem",
                text_align="center",
                color="accent.9",
                id="login-form-logo",
            ),
            
            # Subtitle
            rx.text(
                "Sistema de Controle Financeiro para Poker",
                size="4",
                margin_bottom="3rem",
                text_align="center",
                color="gray.11",
                id="login-form-subtitle",
            ),
            
            # Login Form
            rx.card(
                rx.vstack(
                    rx.heading(
                        "Login",
                        size="6",
                        margin_bottom="1.5rem",
                        text_align="center",
                        id="login-form-title",
                    ),
                    
                    # CPF Input
                    rx.vstack(
                        rx.text(
                            "CPF",
                            size="3",
                            font_weight="medium",
                            id="login-form-cpf-label",
                        ),
                        rx.input(
                            placeholder="000.000.000-00",
                            value=LoginState.cpf,
                            on_change=LoginState.set_cpf,
                            size="3",
                            width="100%",
                            max_length=14,
                            id="login-form-cpf-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="login-form-cpf-field",
                    ),
                    
                    # Password Input
                    rx.vstack(
                        rx.text(
                            "Senha",
                            size="3",
                            font_weight="medium",
                            id="login-form-password-label",
                        ),
                        rx.input(
                            placeholder="Digite sua senha",
                            type="password",
                            value=LoginState.password,
                            on_change=LoginState.set_password,
                            on_key_down=lambda key: rx.cond(
                                key == "Enter",
                                LoginState.handle_login(),
                                rx.noop()
                            ),
                            size="3",
                            width="100%",
                            id="login-form-password-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="login-form-password-field",
                    ),
                    
                    # Error Message
                    rx.cond(
                        LoginState.error_message != "",
                        rx.text(
                            LoginState.error_message,
                            color="red.500",
                            size="2",
                            text_align="center",
                            id="login-form-error-message",
                        ),
                    ),
                    
                    # Login Button
                    rx.button(
                        rx.cond(
                            LoginState.is_loading,
                            rx.hstack(
                                rx.spinner(size="1", id="login-form-loading-spinner"),
                                rx.text("Entrando...", id="login-form-loading-text"),
                                spacing="2",
                                id="login-form-loading-content",
                            ),
                            rx.text("Entrar", id="login-form-button-text"),
                        ),
                        on_click=LoginState.handle_login,
                        size="3",
                        width="100%",
                        disabled=LoginState.is_loading,
                        color_scheme="blue",
                        id="login-form-submit-button",
                    ),
                    
                    spacing="4",
                    width="100%",
                    id="login-form-fields",
                ),
                max_width="400px",
                padding="2rem",
                id="login-form-card",
            ),
            
            # Footer Info
            rx.text(
                "Acesso restrito aos membros do grupo de poker",
                size="2",
                color="gray.9",
                text_align="center",
                margin_top="2rem",
                id="login-form-footer",
            ),
            
            spacing="4",
            align="center",
            width="100%",
            min_height="100vh",
            justify="center",
            id="login-form-content",
        ),
        padding="2rem",
        max_width="500px",
        margin="0 auto",
        id="login-form-container",
    )
