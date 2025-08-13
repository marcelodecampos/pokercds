#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reusable member form component for profile editing and member management.
"""

import reflex as rx
from typing import Optional, Callable


class MemberFormState(rx.State):
    """Base state for member form operations."""
    
    # Form fields
    cpf: str = ""
    name: str = ""
    nickname: str = ""
    email: str = ""
    pix_key: str = ""
    phone: str = ""
    is_admin: bool = False
    is_enabled: bool = True
    
    # Form state
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    is_editing: bool = False
    
    def set_cpf(self, value: str):
        """Set CPF value."""
        self.cpf = value
        
    def set_name(self, value: str):
        """Set name value."""
        self.name = value
        
    def set_nickname(self, value: str):
        """Set nickname value."""
        self.nickname = value
        
    def set_email(self, value: str):
        """Set email value."""
        self.email = value
        
    def set_pix_key(self, value: str):
        """Set PIX key value."""
        self.pix_key = value
        
    def set_phone(self, value: str):
        """Set phone value."""
        self.phone = value
        
    def set_is_admin(self, value: bool):
        """Set admin status."""
        self.is_admin = value
        
    def set_is_enabled(self, value: bool):
        """Set enabled status."""
        self.is_enabled = value
    
    def load_member_data(self, member_data: dict):
        """Load member data into form."""
        self.cpf = member_data.get("cpf", "")
        self.name = member_data.get("name", "")
        self.nickname = member_data.get("nickname", "")
        self.email = member_data.get("email", "")
        self.pix_key = member_data.get("pix_key", "")
        self.phone = member_data.get("phone", "")
        self.is_admin = member_data.get("is_admin", False)
        self.is_enabled = member_data.get("is_enabled", True)
    
    def clear_messages(self):
        """Clear error and success messages."""
        self.error_message = ""
        self.success_message = ""
    
    def _validate_form(self) -> bool:
        """Validate form fields."""
        self.clear_messages()
        
        # Required fields validation
        if not self.name.strip():
            self.error_message = "Nome é obrigatório"
            return False
            
        if not self.nickname.strip():
            self.error_message = "Apelido é obrigatório"
            return False
            
        if not self.email.strip():
            self.error_message = "E-mail é obrigatório"
            return False
            
        if not self.pix_key.strip():
            self.error_message = "Chave PIX é obrigatória"
            return False
        
        # CPF validation (only for new members)
        if not self.is_editing and not self.cpf.strip():
            self.error_message = "CPF é obrigatório"
            return False
            
        return True
    
    def get_form_data(self) -> dict:
        """Get form data as dictionary."""
        return {
            "cpf": self.cpf.strip(),
            "name": self.name.strip(),
            "nickname": self.nickname.strip(),
            "email": self.email.strip(),
            "pix_key": self.pix_key.strip(),
            "phone": self.phone.strip(),
            "is_admin": self.is_admin,
            "is_enabled": self.is_enabled,
        }


def MemberForm(
    form_state: MemberFormState,
    title: str = "Dados do Membro",
    show_admin_fields: bool = False,
    readonly_cpf: bool = False,
    readonly_nickname: bool = False,
    on_submit: Optional[Callable] = None,
    on_cancel: Optional[Callable] = None,
) -> rx.Component:
    """
    Reusable member form component.
    
    Args:
        form_state: The form state instance
        title: Form title
        show_admin_fields: Whether to show admin-only fields (is_admin, is_enabled)
        readonly_cpf: Whether CPF field should be readonly
        readonly_nickname: Whether nickname field should be readonly
        on_submit: Submit handler function
        on_cancel: Cancel handler function
    """
    
    form_fields = rx.vstack(
        # CPF Field
        rx.cond(
            readonly_cpf,
            rx.vstack(
                rx.text("CPF", size="3", font_weight="medium"),
                rx.input(
                    value=form_state.cpf,
                    size="3",
                    width="100%",
                    disabled=True,
                ),
                width="100%",
                spacing="1",
            ),
            rx.vstack(
                rx.text("CPF", size="3", font_weight="medium"),
                rx.input(
                    placeholder="000.000.000-00",
                    value=form_state.cpf,
                    on_change=form_state.set_cpf,
                    size="3",
                    width="100%",
                    max_length=14,
                ),
                width="100%",
                spacing="1",
            ),
        ),
        
        # Name Field
        rx.vstack(
            rx.text("Nome Completo", size="3", font_weight="medium"),
            rx.input(
                placeholder="Digite o nome completo",
                value=form_state.name,
                on_change=form_state.set_name,
                size="3",
                width="100%",
                max_length=64,
            ),
            width="100%",
            spacing="1",
        ),
        
        # Nickname Field
        rx.cond(
            readonly_nickname,
            rx.vstack(
                rx.text("Apelido", size="3", font_weight="medium"),
                rx.input(
                    value=form_state.nickname,
                    size="3",
                    width="100%",
                    disabled=True,
                ),
                rx.text(
                    "Apenas administradores podem alterar o apelido",
                    size="1",
                    color="gray.9",
                ),
                width="100%",
                spacing="1",
            ),
            rx.vstack(
                rx.text("Apelido", size="3", font_weight="medium"),
                rx.input(
                    placeholder="Digite o apelido",
                    value=form_state.nickname,
                    on_change=form_state.set_nickname,
                    size="3",
                    width="100%",
                    max_length=48,
                ),
                width="100%",
                spacing="1",
            ),
        ),
        
        # Email Field
        rx.vstack(
            rx.text("E-mail", size="3", font_weight="medium"),
            rx.input(
                placeholder="usuario@exemplo.com",
                type="email",
                value=form_state.email,
                on_change=form_state.set_email,
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
                value=form_state.pix_key,
                on_change=form_state.set_pix_key,
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
                value=form_state.phone,
                on_change=form_state.set_phone,
                size="3",
                width="100%",
                max_length=20,
            ),
            width="100%",
            spacing="1",
        ),
        
        # Admin Fields (conditional)
        rx.cond(
            show_admin_fields,
            rx.vstack(
                rx.divider(),
                rx.text("Permissões", size="4", font_weight="bold"),
                
                # Admin checkbox
                rx.checkbox(
                    "Administrador",
                    checked=form_state.is_admin,
                    on_change=form_state.set_is_admin,
                ),
                
                # Enabled checkbox
                rx.checkbox(
                    "Membro ativo",
                    checked=form_state.is_enabled,
                    on_change=form_state.set_is_enabled,
                ),
                
                width="100%",
                spacing="2",
            ),
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
                    rx.text("Salvando..."),
                    spacing="2",
                ),
                rx.text("Salvar"),
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
        max_width="600px",
    )
