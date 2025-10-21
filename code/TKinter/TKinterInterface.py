import tkinter as tk
from tkinter import ttk, messagebox
import requests
from typing import List, Dict, Any

class WorkshopMonitorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Monitor de Flujo del Taller - Sistema de Optimización")
        self.root.geometry("1000x600")
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Monitor de Flujo del Taller", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Frame de controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control
        self.refresh_btn = ttk.Button(controls_frame, text="Actualizar", 
                                     command=self.refresh_data)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.optimize_btn = ttk.Button(controls_frame, text="Optimizar Todo", 
                                      command=self.optimize_all_workflows)
        self.optimize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Etiqueta de estado
        self.status_label = ttk.Label(controls_frame, text="Conectando...")
        self.status_label.pack(side=tk.RIGHT)
        
        # Treeview para tickets
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Cliente', 'Equipo', 'Ubicación', 'Siguiente', 'Tiempo', 'Estado'),
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configurar columnas
        columns = {
            'ID': 80,
            'Cliente': 150,
            'Equipo': 150,
            'Ubicación': 120,
            'Siguiente': 120,
            'Tiempo': 100,
            'Estado': 100
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Frame de detalles
        details_frame = ttk.LabelFrame(main_frame, text="Detalles del Ticket", padding="5")
        details_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Información del ticket seleccionado
        self.details_text = tk.Text(details_frame, height=4, font=('Arial', 9))
        self.details_text.pack(fill=tk.X)
        self.details_text.config(state=tk.DISABLED)
        
        # Botones de acción para ticket seleccionado
        action_frame = ttk.Frame(details_frame)
        action_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.optimize_ticket_btn = ttk.Button(
            action_frame, 
            text="Optimizar Este", 
            command=self.optimize_selected_ticket
        )
        self.optimize_ticket_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.move_ticket_btn = ttk.Button(
            action_frame, 
            text="Mover Siguiente", 
            command=self.move_selected_ticket
        )
        self.move_ticket_btn.pack(side=tk.LEFT)
        
        # Bind selección de treeview
        self.tree.bind('<<TreeviewSelect>>', self.on_ticket_select)
    
    def get_api_url(self, endpoint):
        """Construir URL de la API"""
        return f"http://localhost:5000{endpoint}"
    
    def refresh_data(self):
        """Actualizar datos desde la API"""
        try:
            response = requests.get(self.get_api_url("/tickets/active"), timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.update_tickets_display(data['active_tickets'])
                self.status_label.config(text=f"{data['count']} tickets activos")
            else:
                self.status_label.config(text=" Error al cargar datos")
                
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="No se puede conectar al servidor")
            print(f"Error de conexión: {e}")
    
    def update_tickets_display(self, tickets: List[Dict[str, Any]]):
        """Actualizar el treeview con los tickets"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar tickets
        for ticket in tickets:
            
            self.tree.insert('', tk.END, values=(
                ticket['id'],
                ticket['client_name'],
                ticket.get('unit_equipment_name', 'N/A'),
                ticket.get('recommended_next_step', 'N/A'),
                f"{ticket.get('estimated_process_time', 0)} min",
            ))
    
    
    def on_ticket_select(self, event):
        """Manejar selección de ticket"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            ticket_id = self.tree.item(item, 'values')[0]
            self.show_ticket_details(ticket_id)
    
    def show_ticket_details(self, ticket_id: str):
        """Mostrar detalles del ticket seleccionado"""
        try:
            response = requests.get(self.get_api_url(f"/tickets/{ticket_id}"), timeout=5)
            if response.status_code == 200:
                ticket = response.json()
                
                details_text = f"""
Ticket ID: {ticket['id']}
Título: {ticket['title']}
Descripción: {ticket.get('description', 'N/A')}
Cliente: {ticket['client_name']}
Equipo: {ticket.get('unit_equipment_name', 'N/A')}
Ubicación actual: {ticket.get('current_location', 'N/A')}
Siguiente paso recomendado: {ticket.get('recommended_next_step', 'N/A')}
Tiempo estimado: {ticket.get('estimated_process_time', 0)} minutos
Estado: {ticket.get('state', 'N/A')}
Incidentes: {len(ticket.get('incidents', []))}
                """.strip()
                
                self.details_text.config(state=tk.NORMAL)
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(1.0, details_text)
                self.details_text.config(state=tk.DISABLED)
                
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles: {e}")
    
    def optimize_all_workflows(self):
        """Optimizar el flujo de todos los tickets activos"""
        try:
            response = requests.post(self.get_api_url("/tickets/batch-optimize"), timeout=10)
            if response.status_code == 200:
                result = response.json()
                self.status_label.config(text=f" {result['message']}")
                self.refresh_data()
                messagebox.showinfo("Éxito", result['message'])
            else:
                self.status_label.config(text="Error al optimizar")
                messagebox.showerror("Error", "No se pudieron optimizar los tickets")
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="Error de conexión")
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    
    def optimize_selected_ticket(self):
        """Optimizar el ticket seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un ticket primero")
            return
        
        ticket_id = self.tree.item(selection[0], 'values')[0]
        
        try:
            response = requests.get(
                self.get_api_url(f"/tickets/{ticket_id}/optimal-workflow"), 
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                self.status_label.config(
                    text=f"Ticket {ticket_id} optimizado. Siguiente: {result['recommended_next_step']}"
                )
                self.refresh_data()
                messagebox.showinfo("Éxito", 
                    f"Ticket {ticket_id} optimizado\n"
                    f"Siguiente paso: {result['recommended_next_step']}\n"
                    f"Tiempo estimado: {result['estimated_process_time']} min"
                )
            else:
                self.status_label.config(text="Error al optimizar ticket")
                messagebox.showerror("Error", "No se pudo optimizar el ticket")
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="Error de conexión")
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    
    def move_selected_ticket(self):
        """Mover el ticket seleccionado al siguiente paso"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un ticket primero")
            return
        
        ticket_id = self.tree.item(selection[0], 'values')[0]
        
        try:
            response = requests.post(
                self.get_api_url(f"/tickets/{ticket_id}/move-to-next"), 
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                self.status_label.config(
                    text=f"Ticket {ticket_id} movido a: {result['new_location']}"
                )
                self.refresh_data()
                messagebox.showinfo("Éxito", 
                    f"Ticket {ticket_id} movido\n"
                    f"De: {result['previous_location']}\n"
                    f"A: {result['new_location']}"
                )
            else:
                error_msg = response.json().get('error', 'Error desconocido')
                self.status_label.config(text=f"{error_msg}")
                messagebox.showerror("Error", error_msg)
        except requests.exceptions.RequestException as e:
            self.status_label.config(text="Error de conexión")
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WorkshopMonitorApp()
    app.run()