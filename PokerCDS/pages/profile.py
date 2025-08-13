#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User profile page for editing own data.
"""

import reflex as rx
import asyncio
from ..components.member_form import MemberForm, MemberFormState
from ..state.auth_state import AuthState


class ProfileState(MemberFormState):
    """State for user profile page."""
    
    async def load_current_user_data(self):
        """Load current user data from auth state."""
        # Get auth state
        auth_state = await self.get_state(AuthState)
        
        # Load user data into form
        user_data = {
            "cpf": "59469390415",  # TODO: Get from auth_state when available
            "name": auth_state.user_name,
            "nickname": auth_state.user_nickname,
            "email": auth_state.user_email,
            "pix_key": "sr.marcelo.campos@gmail.com",  # TODO: Get from database
            "phone": "61984017586",  # TODO: Get from database
            "is_admin": auth_state.is_admin,
            "is_enabled": True,
        }
        
        self.load_member_data(user_data)
        self.is_editing = True
    
    async def handle_submit(self):
        """Handle profile form submission."""
        self.is_loading = True
        self.clear_messages()
        
        try:
            # Validate form
            if not self._validate_form():
                return
            
            # TODO: Implement database update
            # For now, simulate API call
            await asyncio.sleep(1)
            
            # Update auth state with new data
            auth_state = await self.get_state(AuthState)
            user_data = {
                "id": auth_state.user_id,
                "name": self.name,
                "nickname": self.nickname,
                "email": self.email,
                "is_admin": auth_state.is_admin,
            }
            auth_state.login_user(user_data)
            
            self.success_message = "Dados atualizados com sucesso!"
            
        except Exception as e:
            self.error_message = f"Erro ao atualizar dados: {str(e)}"
            
        finally:
            self.is_loading = False
    
    def handle_cancel(self):
        """Handle cancel action."""
        return rx.redirect("/dashboard")


@rx.page(route="/profile", title="PokerCDS - Meu Perfil", on_load=[AuthState.require_auth, ProfileState.load_current_user_data])
def profile_page() -> rx.Component:
    """User profile page."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.hstack(
                    rx.button(
                        rx.icon("arrow-left", size=16, id="profile-back-icon"),
                        "Voltar",
                        variant="outline",
                        on_click=lambda: rx.redirect("/dashboard"),
                        id="profile-back-button",
                    ),
                    rx.heading("Meu Perfil", size="6", id="profile-page-title"),
                    justify="between",
                    align="center",
                    width="100%",
                    id="profile-header-content",
                ),
                max_width="1200px",
                id="profile-header-container",
            ),
            padding="1.5rem 0",
            width="100%",
            id="profile-header",
        ),
        
        # Main content
        rx.container(
            rx.vstack(
                rx.text(
                    "Aqui você pode visualizar e editar seus dados pessoais.",
                    size="3",
                    text_align="center",
                    margin_bottom="2rem",
                    id="profile-description",
                ),
                
                # Profile form
                MemberForm(
                    form_state=ProfileState,
                    title="Meus Dados",
                    show_admin_fields=False,
                    readonly_cpf=True,
                    readonly_nickname=True,
                    on_submit=ProfileState.handle_submit,
                    on_cancel=ProfileState.handle_cancel,
                ),
                
                spacing="4",
                align="center",
                width="100%",
                id="profile-main-content",
            ),
            max_width="1200px",
            padding="2rem",
            id="profile-main-container",
        ),
        
        min_height="100vh",
        id="profile-page",
    )
