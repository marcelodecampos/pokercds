#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Members management page with full CRUD operations.
"""

import reflex as rx
import asyncio
from typing import List, Optional
from ..components.member_form import MemberForm, MemberFormState
from ..state.auth_state import AuthState


class MembersManagementState(rx.State):
    """State for members management page."""
    
    # Members list
    members: List[dict] = []
    selected_members: List[int] = []
    current_page: int = 1
    total_pages: int = 1
    members_per_page: int = 20
    
    # Modal states
    show_add_modal: bool = False
    show_edit_modal: bool = False
    show_delete_modal: bool = False
    editing_member: Optional[dict] = None
    
    # Loading states
    is_loading: bool = False
    is_deleting: bool = False
    
    # Messages
    error_message: str = ""
    success_message: str = ""
    
    async def load_members(self):
        """Load members from database (paginated)."""
        self.is_loading = True
        self.error_message = ""
        
        try:
            # TODO: Replace with actual database query
            # Simulate API call
            await asyncio.sleep(0.5)
            
            # Mock data for demonstration
            mock_members = [
                {
                    "id": 1,
                    "cpf": "59469390415",
                    "name": "Marcelo de Campos",
                    "nickname": "That's Poker",
                    "email": "sr.marcelo.campos@gmail.com",
                    "pix_key": "sr.marcelo.campos@gmail.com",
                    "phone": "61984017586",
                    "is_admin": True,
                    "is_enabled": True,
                },
                {
                    "id": 2,
                    "cpf": "12345678901",
                    "name": "João Silva",
                    "nickname": "Joãozinho",
                    "email": "joao@exemplo.com",
                    "pix_key": "joao@exemplo.com",
                    "phone": "11999887766",
                    "is_admin": False,
                    "is_enabled": True,
                },
                {
                    "id": 3,
                    "cpf": "98765432100",
                    "name": "Maria Santos",
                    "nickname": "Mari",
                    "email": "maria@exemplo.com",
                    "pix_key": "maria@exemplo.com",
                    "phone": "11888776655",
                    "is_admin": False,
                    "is_enabled": False,
                },
            ]
            
            self.members = mock_members
            self.total_pages = 1  # For now, single page
            
        except Exception as e:
            self.error_message = f"Erro ao carregar membros: {str(e)}"
            
        finally:
            self.is_loading = False
    
    def toggle_member_selection(self, member_id: int):
        """Toggle member selection for bulk operations."""
        if member_id in self.selected_members:
            self.selected_members.remove(member_id)
        else:
            self.selected_members.append(member_id)
    
    def select_all_members(self):
        """Select all visible members."""
        self.selected_members = [member["id"] for member in self.members]
    
    def clear_selection(self):
        """Clear all selections."""
        self.selected_members = []
    
    def toggle_select_all(self):
        """Toggle select all members."""
        if len(self.selected_members) == len(self.members):
            self.clear_selection()
        else:
            self.select_all_members()
    
    def open_add_modal(self):
        """Open add member modal."""
        self.show_add_modal = True
        self.editing_member = None
    
    def close_add_modal(self):
        """Close add member modal."""
        self.show_add_modal = False
    
    def open_edit_modal(self, member: dict):
        """Open edit member modal."""
        self.editing_member = member
        self.show_edit_modal = True
    
    def close_edit_modal(self):
        """Close edit member modal."""
        self.show_edit_modal = False
        self.editing_member = None
    
    def open_delete_modal(self):
        """Open delete confirmation modal."""
        if self.selected_members:
            self.show_delete_modal = True
    
    def close_delete_modal(self):
        """Close delete confirmation modal."""
        self.show_delete_modal = False
    
    async def delete_selected_members(self):
        """Delete selected members."""
        self.is_deleting = True
        self.error_message = ""
        
        try:
            # TODO: Implement actual database deletion
            await asyncio.sleep(1)
            
            # Remove from local list (simulate)
            self.members = [
                member for member in self.members 
                if member["id"] not in self.selected_members
            ]
            
            count = len(self.selected_members)
            self.success_message = f"{count} membro(s) excluído(s) com sucesso!"
            self.selected_members = []
            self.close_delete_modal()
            
        except Exception as e:
            self.error_message = f"Erro ao excluir membros: {str(e)}"
            
        finally:
            self.is_deleting = False
    
    def clear_messages(self):
        """Clear error and success messages."""
        self.error_message = ""
        self.success_message = ""
    
    def open_edit_modal_by_id(self, member_id: int):
        """Open edit modal for specific member by ID."""
        member = next((m for m in self.members if m["id"] == member_id), None)
        if member:
            self.open_edit_modal(member)


class MemberFormModalState(MemberFormState):
    """State for member form in modal."""
    
    async def handle_add_submit(self):
        """Handle add member form submission."""
        self.is_loading = True
        self.clear_messages()
        
        try:
            # Validate form
            if not self._validate_form():
                return
            
            # TODO: Implement database insertion
            await asyncio.sleep(1)
            
            member_data = self.get_form_data()
            print(f"DEBUG: Adding member: {member_data}")
            
            # Get main state and close modal
            main_state = await self.get_state(MembersManagementState)
            main_state.success_message = f"Membro '{self.name}' adicionado com sucesso!"
            main_state.close_add_modal()
            
            # Reload members list
            await main_state.load_members()
            
        except Exception as e:
            self.error_message = f"Erro ao adicionar membro: {str(e)}"
            
        finally:
            self.is_loading = False
    
    async def handle_edit_submit(self):
        """Handle edit member form submission."""
        self.is_loading = True
        self.clear_messages()
        
        try:
            # Validate form
            if not self._validate_form():
                return
            
            # TODO: Implement database update
            await asyncio.sleep(1)
            
            member_data = self.get_form_data()
            print(f"DEBUG: Updating member: {member_data}")
            
            # Get main state and close modal
            main_state = await self.get_state(MembersManagementState)
            main_state.success_message = f"Membro '{self.name}' atualizado com sucesso!"
            main_state.close_edit_modal()
            
            # Reload members list
            await main_state.load_members()
            
        except Exception as e:
            self.error_message = f"Erro ao atualizar membro: {str(e)}"
            
        finally:
            self.is_loading = False


def MembersTable() -> rx.Component:
    """Members table with selection and actions."""
    return rx.card(
        rx.vstack(
            # Table header with actions
            rx.hstack(
                rx.hstack(
                    rx.checkbox(
                        checked=MembersManagementState.selected_members.length() == MembersManagementState.members.length(),
                        on_change=lambda _: MembersManagementState.toggle_select_all(),
                    ),
                    rx.text("Selecionar todos", size="2"),
                    spacing="2",
                    align="center",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("plus", size=16),
                        "Novo Membro",
                        on_click=MembersManagementState.open_add_modal,
                        size="2",
                    ),
                    rx.button(
                        rx.icon("trash-2", size=16),
                        rx.text("Excluir (", MembersManagementState.selected_members.length(), ")"),
                        on_click=MembersManagementState.open_delete_modal,
                        disabled=MembersManagementState.selected_members.length() == 0,
                        color_scheme="red",
                        variant="outline",
                        size="2",
                    ),
                    spacing="2",
                ),
                justify="between",
                width="100%",
                margin_bottom="1rem",
            ),
            
            # Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(""),
                        rx.table.column_header_cell("CPF"),
                        rx.table.column_header_cell("Nome"),
                        rx.table.column_header_cell("Apelido"),
                        rx.table.column_header_cell("E-mail"),
                        rx.table.column_header_cell("Status"),
                        rx.table.column_header_cell("Admin"),
                        rx.table.column_header_cell("Ações"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        MembersManagementState.members,
                        lambda member: rx.table.row(
                            rx.table.cell(
                                rx.checkbox(
                                    checked=MembersManagementState.selected_members.contains(member["id"]),
                                    on_change=lambda _: MembersManagementState.toggle_member_selection(member["id"]),
                                ),
                            ),
                            rx.table.cell(member["cpf"]),
                            rx.table.cell(member["name"]),
                            rx.table.cell(member["nickname"]),
                            rx.table.cell(member["email"]),
                            rx.table.cell(
                                rx.cond(
                                    member["is_enabled"],
                                    rx.badge("Ativo", color_scheme="green"),
                                    rx.badge("Inativo", color_scheme="red"),
                                ),
                            ),
                            rx.table.cell(
                                rx.cond(
                                    member["is_admin"],
                                    rx.badge("Admin", color_scheme="blue"),
                                    rx.text("Membro", size="2"),
                                ),
                            ),
                            rx.table.cell(
                                rx.button(
                                    rx.icon("edit", size=14),
                                    on_click=lambda: MembersManagementState.open_edit_modal_by_id(member["id"]),
                                    variant="ghost",
                                    size="1",
                                ),
                            ),
                        ),
                    ),
                ),
                width="100%",
            ),
            
            width="100%",
        ),
        padding="1.5rem",
    )


def AddMemberModal() -> rx.Component:
    """Modal for adding new member."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Adicionar Novo Membro"),
            MemberForm(
                form_state=MemberFormModalState,
                title="",
                show_admin_fields=True,
                readonly_cpf=False,
                on_submit=MemberFormModalState.handle_add_submit,
                on_cancel=MembersManagementState.close_add_modal,
            ),
            max_width="600px",
        ),
        open=MembersManagementState.show_add_modal,
    )


def EditMemberModal() -> rx.Component:
    """Modal for editing member."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar Membro"),
            MemberForm(
                form_state=MemberFormModalState,
                title="",
                show_admin_fields=True,
                readonly_cpf=True,
                on_submit=MemberFormModalState.handle_edit_submit,
                on_cancel=MembersManagementState.close_edit_modal,
            ),
            max_width="600px",
        ),
        open=MembersManagementState.show_edit_modal,
    )


def DeleteConfirmationModal() -> rx.Component:
    """Modal for delete confirmation."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Exclusão"),
            rx.vstack(
                rx.text(
                    "Tem certeza que deseja excluir ",
                    MembersManagementState.selected_members.length(),
                    " membro(s) selecionado(s)?",
                    size="3",
                ),
                rx.text(
                    "Esta ação não pode ser desfeita.",
                    size="2",
                    color="red.500",
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="outline",
                        on_click=MembersManagementState.close_delete_modal,
                        disabled=MembersManagementState.is_deleting,
                    ),
                    rx.button(
                        rx.cond(
                            MembersManagementState.is_deleting,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text("Excluindo..."),
                                spacing="2",
                            ),
                            rx.text("Excluir"),
                        ),
                        on_click=MembersManagementState.delete_selected_members,
                        color_scheme="red",
                        disabled=MembersManagementState.is_deleting,
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            max_width="400px",
        ),
        open=MembersManagementState.show_delete_modal,
    )


@rx.page(route="/members", title="PokerCDS - Gerenciar Membros", on_load=[AuthState.require_auth, MembersManagementState.load_members])
def members_management_page() -> rx.Component:
    """Members management page."""
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
                    rx.heading("Gerenciar Membros", size="6"),
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
                # Messages
                rx.cond(
                    MembersManagementState.error_message != "",
                    rx.callout(
                        MembersManagementState.error_message,
                        icon="alert-circle",
                        color_scheme="red",
                    ),
                ),
                rx.cond(
                    MembersManagementState.success_message != "",
                    rx.callout(
                        MembersManagementState.success_message,
                        icon="check-circle",
                        color_scheme="green",
                    ),
                ),
                
                # Loading or table
                rx.cond(
                    MembersManagementState.is_loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3"),
                            rx.text("Carregando membros..."),
                            spacing="3",
                            align="center",
                        ),
                        padding="4rem",
                    ),
                    MembersTable(),
                ),
                
                spacing="4",
                width="100%",
            ),
            max_width="1200px",
            padding="2rem",
        ),
        
        # Modals
        AddMemberModal(),
        EditMemberModal(),
        DeleteConfirmationModal(),
        
        min_height="100vh",
    )
