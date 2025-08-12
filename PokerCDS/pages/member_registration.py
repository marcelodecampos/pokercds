#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Member registration page for administrators.
"""

import reflex as rx
import asyncio
from ..components.member_form import MemberForm, MemberFormState
from ..components.password_form import PasswordForm, PasswordFormState
from ..state.auth_state import AuthState

class MemberRegistrationState(MemberFormState):
    """State for member registration page."""
    
    # Password form state
    password: str = ""
    confirm_password: str = ""
    is_editing: bool = False  # This is a new member
    
    def set_password(self, value: str):
        """Set password value."""
        self.password = value
        
    def set_confirm_password_reg(self, value: str):
        """Set confirm password value."""
        self.confirm_password = value
    
    def _validate_passwords(self) -> bool:
        """Validate password fields."""
        if not self.password.strip():
            self.error_message = "Senha é obrigatória"
            return False
        
        if len(self.password) < 6:
            self.error_message = "Senha deve ter pelo menos 6 caracteres"
            return False
        
        if self.password != self.confirm_password:
            self.error_message = "Confirmação de senha não confere"
            return False
        
        return True
    
    def _validate_form(self) -> bool:
        """Override to include password validation."""
        if not super()._validate_form():
            return False
        
        return self._validate_passwords()
    
    async def handle_submit(self):
        """Handle member registration form submission."""
        self.is_loading = True
        self.clear_messages()
        
        try:
            # Check if user is admin
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_admin:
                self.error_message = "Acesso negado. Apenas administradores podem cadastrar membros."
                return
            
            # Validate form
            if not self._validate_form():
                return
            
            # TODO: Implement database insertion
            # For now, simulate API call
            await asyncio.sleep(1)
            
            # Get form data including password
            member_data = self.get_form_data()
            member_data["password"] = self.password
            
            print(f"DEBUG: Registering new member: {member_data}")
            
            self.success_message = f"Membro '{self.name}' cadastrado com sucesso!"
            
            # Clear form for next registration
            await asyncio.sleep(2)
            self._clear_form()
            
        except Exception as e:
            self.error_message = f"Erro ao cadastrar membro: {str(e)}"
            
        finally:
            self.is_loading = False
    
    def _clear_form(self):
        """Clear all form fields."""
        self.cpf = ""
        self.name = ""
        self.nickname = ""
        self.email = ""
        self.pix_key = ""
        self.phone = ""
        self.password = ""
        self.confirm_password = ""
        self.is_admin = False
        self.is_enabled = True
        self.clear_messages()
    
    def handle_cancel(self):
        """Handle cancel action."""
        return rx.redirect("/dashboard")


def MemberRegistrationForm() -> rx.Component:
    """Custom form combining member data and password fields."""
    return rx.card(
        rx.vstack(
            rx.heading("Cadastrar Novo Membro", size="6", margin_bottom="1.5rem"),
            
            # Member basic fields
            rx.vstack(
                # CPF Field
                rx.vstack(
                    rx.text("CPF", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="000.000.000-00",
                        value=MemberRegistrationState.cpf,
                        on_change=MemberRegistrationState.set_cpf,
                        size="3",
                        width="100%",
                        max_length=14,
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                # Name Field
                rx.vstack(
                    rx.text("Nome Completo", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="Digite o nome completo",
                        value=MemberRegistrationState.name,
                        on_change=MemberRegistrationState.set_name,
                        size="3",
                        width="100%",
                        max_length=64,
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                # Nickname Field
                rx.vstack(
                    rx.text("Apelido", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="Digite o apelido",
                        value=MemberRegistrationState.nickname,
                        on_change=MemberRegistrationState.set_nickname,
                        size="3",
                        width="100%",
                        max_length=48,
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                # Email Field
                rx.vstack(
                    rx.text("E-mail", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="usuario@exemplo.com",
                        type="email",
                        value=MemberRegistrationState.email,
                        on_change=MemberRegistrationState.set_email,
                        size="3",
                        width="100%",
                        max_length=255,
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                # PIX Key Field
                rx.vstack(
                    rx.text("Chave PIX", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="Digite a chave PIX",
                        value=MemberRegistrationState.pix_key,
                        on_change=MemberRegistrationState.set_pix_key,
                        size="3",
                        width="100%",
                        max_length=128,
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                # Phone Field
                rx.vstack(
                    rx.text("Telefone", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="(11) 99999-9999",
                        value=MemberRegistrationState.phone,
                        on_change=MemberRegistrationState.set_phone,
                        size="3",
                        width="100%",
                        max_length=20,
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                spacing="3",
                width="100%",
            ),
            
            # Password section
            rx.divider(),
            rx.text("Definir Senha de Acesso", size="4", font_weight="bold"),
            
            rx.vstack(
                # Password Field
                rx.vstack(
                    rx.text("Senha", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="Digite a senha",
                        type="password",
                        value=MemberRegistrationState.password,
                        on_change=MemberRegistrationState.set_password,
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
                    rx.text("Confirmar Senha", size="3", font_weight="medium"),
                    rx.input(
                        placeholder="Digite novamente a senha",
                        type="password",
                        value=MemberRegistrationState.confirm_password,
                        on_change=MemberRegistrationState.set_confirm_password_reg,
                        size="3",
                        width="100%",
                    ),
                    width="100%",
                    spacing="1",
                ),
                
                spacing="3",
                width="100%",
            ),
            
            # Admin permissions section
            rx.divider(),
            rx.text("Permissões", size="4", font_weight="bold"),
            
            rx.vstack(
                rx.checkbox(
                    "Administrador",
                    checked=MemberRegistrationState.is_admin,
                    on_change=MemberRegistrationState.set_is_admin,
                ),
                rx.checkbox(
                    "Membro ativo",
                    checked=MemberRegistrationState.is_enabled,
                    on_change=MemberRegistrationState.set_is_enabled,
                ),
                spacing="2",
                width="100%",
            ),
            
            # Messages
            rx.vstack(
                rx.cond(
                    MemberRegistrationState.error_message != "",
                    rx.text(
                        MemberRegistrationState.error_message,
                        color="red.500",
                        size="2",
                    ),
                ),
                rx.cond(
                    MemberRegistrationState.success_message != "",
                    rx.text(
                        MemberRegistrationState.success_message,
                        color="green.500",
                        size="2",
                    ),
                ),
                width="100%",
                spacing="1",
            ),
            
            # Buttons
            rx.hstack(
                rx.button(
                    "Cancelar",
                    variant="outline",
                    on_click=MemberRegistrationState.handle_cancel,
                    disabled=MemberRegistrationState.is_loading,
                ),
                rx.button(
                    rx.cond(
                        MemberRegistrationState.is_loading,
                        rx.hstack(
                            rx.spinner(size="1"),
                            rx.text("Cadastrando..."),
                            spacing="2",
                        ),
                        rx.text("Cadastrar Membro"),
                    ),
                    on_click=MemberRegistrationState.handle_submit,
                    disabled=MemberRegistrationState.is_loading,
                ),
                spacing="3",
                justify="end",
                width="100%",
            ),
            
            spacing="4",
            width="100%",
        ),
        padding="2rem",
        width="100%",
        max_width="600px",
    )


@rx.page(route="/member-registration", title="PokerCDS - Cadastrar Membro", on_load=AuthState.require_auth)
def member_registration_page() -> rx.Component:
    """Member registration page."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.hstack(
                    rx.button(
                        rx.icon("arrow-left", size=16),
                        "Voltar",
                        variant="outline",
                        on_click=lambda: rx.redirect("/dashboard"),
                    ),
                    rx.heading("Cadastrar Novo Membro", size="6"),
                    justify="between",
                    align="center",
                    width="100%",
                ),
                max_width="1200px",
            ),
            padding="1.5rem 0",
            width="100%",
        ),
        
        # Main content
        rx.container(
            rx.vstack(
                rx.text(
                    "Preencha os dados abaixo para cadastrar um novo membro do grupo de poker.",
                    size="3",
                    text_align="center",
                    margin_bottom="2rem",
                ),
                
                # Registration form
                MemberRegistrationForm(),
                
                spacing="4",
                align="center",
                width="100%",
            ),
            max_width="1200px",
            padding="2rem",
        ),
        
        min_height="100vh",
    )