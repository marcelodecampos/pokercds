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
    
    def delete_single_member(self, member_id: int):
        """Set single member for deletion and open modal."""
        self.selected_members = [member_id]
        self.show_delete_modal = True


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
                        id="members-select-all-checkbox",
                    ),
                    rx.text(
                        "Selecionar todos", 
                        size="2",
                        id="members-select-all-text",
                    ),
                    spacing="2",
                    align="center",
                    id="members-select-all-container",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("plus", size=16, id="members-add-icon"),
                        "Novo Membro",
                        on_click=MembersManagementState.open_add_modal,
                        size="2",
                        id="members-add-button",
                    ),
                    rx.button(
                        rx.icon("trash-2", size=16, id="members-bulk-delete-icon"),
                        rx.text("Excluir (", MembersManagementState.selected_members.length(), ")", id="members-bulk-delete-text"),
                        on_click=MembersManagementState.open_delete_modal,
                        disabled=MembersManagementState.selected_members.length() == 0,
                        color_scheme="red",
                        variant="outline",
                        size="2",
                        id="members-bulk-delete-button",
                    ),
                    spacing="2",
                    id="members-action-buttons",
                ),
                justify="between",
                width="100%",
                margin_bottom="1rem",
                id="members-table-header",
            ),
            
            # Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("", id="members-table-header-checkbox"),
                        rx.table.column_header_cell("Nome", id="members-table-header-name"),
                        rx.table.column_header_cell("Apelido", id="members-table-header-nickname"),
                        rx.table.column_header_cell("Status", id="members-table-header-status"),
                        rx.table.column_header_cell("Admin", id="members-table-header-admin"),
                        rx.table.column_header_cell("Ações", id="members-table-header-actions"),
                        id="members-table-header-row",
                    ),
                    id="members-table-header-section",
                ),
                rx.table.body(
                    rx.foreach(
                        MembersManagementState.members,
                        lambda member: rx.table.row(
                            rx.table.cell(
                                rx.checkbox(
                                    checked=MembersManagementState.selected_members.contains(member["id"]),
                                    on_change=lambda _: MembersManagementState.toggle_member_selection(member["id"]),
                                    id=f"member-checkbox-{member['id']}",
                                ),
                                id=f"member-cell-checkbox-{member['id']}",
                            ),
                            rx.table.cell(
                                member["name"],
                                id=f"member-cell-name-{member['id']}",
                            ),
                            rx.table.cell(
                                member["nickname"],
                                id=f"member-cell-nickname-{member['id']}",
                            ),
                            rx.table.cell(
                                rx.cond(
                                    member["is_enabled"],
                                    rx.badge("Ativo", color_scheme="green", id=f"member-badge-active-{member['id']}"),
                                    rx.badge("Inativo", color_scheme="red", id=f"member-badge-inactive-{member['id']}"),
                                ),
                                id=f"member-cell-status-{member['id']}",
                            ),
                            rx.table.cell(
                                rx.cond(
                                    member["is_admin"],
                                    rx.badge("Admin", color_scheme="blue", id=f"member-badge-admin-{member['id']}"),
                                    rx.text("Membro", size="2", id=f"member-text-regular-{member['id']}"),
                                ),
                                id=f"member-cell-admin-{member['id']}",
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        rx.icon("pencil", size=14, id=f"member-edit-icon-{member['id']}"),
                                        on_click=lambda: MembersManagementState.open_edit_modal_by_id(member["id"]),
                                        variant="ghost",
                                        size="1",
                                        id=f"member-edit-button-{member['id']}",
                                    ),
                                    rx.button(
                                        rx.icon("trash-2", size=14, id=f"member-delete-icon-{member['id']}"),
                                        on_click=lambda: MembersManagementState.delete_single_member(member["id"]),
                                        variant="ghost",
                                        size="1",
                                        color_scheme="red",
                                        id=f"member-delete-button-{member['id']}",
                                    ),
                                    spacing="3",
                                    id=f"member-actions-{member['id']}",
                                ),
                                id=f"member-cell-actions-{member['id']}",
                            ),
                            id=f"member-row-{member['id']}",
                        ),
                    ),
                    id="members-table-body",
                ),
                width="100%",
                id="members-table",
            ),
            
            width="100%",
            id="members-table-container",
        ),
        padding="1.5rem",
        width="100%",
        height="100%",
        id="members-table-card",
    )


def AddMemberModal() -> rx.Component:
    """Modal for adding new member."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Adicionar Novo Membro", id="add-member-modal-title"),
            MemberForm(
                form_state=MemberFormModalState,
                title="",
                show_admin_fields=True,
                readonly_cpf=False,
                on_submit=MemberFormModalState.handle_add_submit,
                on_cancel=MembersManagementState.close_add_modal,
            ),
            max_width="600px",
            id="add-member-modal-content",
        ),
        open=MembersManagementState.show_add_modal,
        id="add-member-modal",
    )


def EditMemberModal() -> rx.Component:
    """Modal for editing member."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar Membro", id="edit-member-modal-title"),
            MemberForm(
                form_state=MemberFormModalState,
                title="",
                show_admin_fields=True,
                readonly_cpf=True,
                readonly_nickname=False,  # Admin pode editar nickname
                on_submit=MemberFormModalState.handle_edit_submit,
                on_cancel=MembersManagementState.close_edit_modal,
            ),
            max_width="600px",
            id="edit-member-modal-content",
        ),
        open=MembersManagementState.show_edit_modal,
        id="edit-member-modal",
    )


def DeleteConfirmationModal() -> rx.Component:
    """Modal for delete confirmation."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Exclusão", id="delete-modal-title"),
            rx.vstack(
                rx.text(
                    "Tem certeza que deseja excluir ",
                    MembersManagementState.selected_members.length(),
                    " membro(s) selecionado(s)?",
                    size="3",
                    id="delete-modal-question",
                ),
                rx.text(
                    "Esta ação não pode ser desfeita.",
                    size="2",
                    color="red.500",
                    id="delete-modal-warning",
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="outline",
                        on_click=MembersManagementState.close_delete_modal,
                        disabled=MembersManagementState.is_deleting,
                        id="delete-modal-cancel-button",
                    ),
                    rx.button(
                        rx.cond(
                            MembersManagementState.is_deleting,
                            rx.hstack(
                                rx.spinner(size="1", id="delete-modal-spinner"),
                                rx.text("Excluindo...", id="delete-modal-loading-text"),
                                spacing="2",
                                id="delete-modal-loading",
                            ),
                            rx.text("Excluir", id="delete-modal-confirm-text"),
                        ),
                        on_click=MembersManagementState.delete_selected_members,
                        color_scheme="red",
                        disabled=MembersManagementState.is_deleting,
                        id="delete-modal-confirm-button",
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    id="delete-modal-buttons",
                ),
                spacing="4",
                width="100%",
                id="delete-modal-content",
            ),
            max_width="400px",
            id="delete-modal-dialog-content",
        ),
        open=MembersManagementState.show_delete_modal,
        id="delete-confirmation-modal",
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
                        rx.icon("arrow-left", size=16, id="members-back-icon"),
                        "Voltar",
                        variant="outline",
                        on_click=lambda: rx.redirect("/dashboard"),
                        id="members-back-button",
                    ),
                    rx.heading("Gerenciar Membros", size="6", id="members-page-title"),
                    justify="between",
                    align="center",
                    width="100%",
                    id="members-header-content",
                ),
                max_width="1200px",
                id="members-header-container",
            ),
            padding="1.5rem 0",
            width="100%",
            id="members-header",
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
                        id="members-error-message",
                    ),
                ),
                rx.cond(
                    MembersManagementState.success_message != "",
                    rx.callout(
                        MembersManagementState.success_message,
                        icon="check-circle",
                        color_scheme="green",
                        id="members-success-message",
                    ),
                ),
                
                # Loading or table
                rx.cond(
                    MembersManagementState.is_loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", id="members-loading-spinner"),
                            rx.text("Carregando membros...", id="members-loading-text"),
                            spacing="3",
                            align="center",
                            id="members-loading-content",
                        ),
                        padding="4rem",
                        id="members-loading-center",
                    ),
                    MembersTable(),
                ),
                
                spacing="4",
                width="100%",
                id="members-main-content",
            ),
            max_width="1200px",
            padding="2rem",
            id="members-main-container",
        ),
        
        # Modals
        AddMemberModal(),
        EditMemberModal(),
        DeleteConfirmationModal(),
        
        min_height="100vh",
        id="members-management-page",
    )
