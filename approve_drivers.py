"""
Admin page to approve or reject pending driver registrations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH


class ApproveDriversPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Approve Driver Registrations")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f5f5f5")

        # Header
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=80)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="👥 Pending Driver Registrations",
            font=("Helvetica", 22, "bold"),
            bg="#DDC01A",
            fg="white"
        ).pack(pady=20)

        # Filter Buttons Frame
        filter_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        filter_frame.pack(fill="x", padx=20)

        tk.Label(
            filter_frame,
            text="View:",
            font=("Helvetica", 12, "bold"),
            bg="#f5f5f5"
        ).pack(side="left", padx=5)

        # Pending Button
        self.pending_button = tk.Button(
            filter_frame,
            text="⏳ Pending (Need Approval)",
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=22,
            relief="raised",
            bd=3,
            command=self.show_pending
        )
        self.pending_button.pack(side="left", padx=5)

        # Approved Button
        self.approved_button = tk.Button(
            filter_frame,
            text="✅ Approved Drivers",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=18,
            relief="flat",
            command=self.show_approved
        )
        self.approved_button.pack(side="left", padx=5)

        # Rejected Button
        self.rejected_button = tk.Button(
            filter_frame,
            text="❌ Rejected Applications",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            relief="flat",
            command=self.show_rejected
        )
        self.rejected_button.pack(side="left", padx=5)

        # Treeview Frame
        tree_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview
        columns = ("ID", "Name", "Email", "Phone", "License", "Vehicle No", "Vehicle Type", "Status", "Registered On")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Configure columns
        self.tree.heading("ID", text="Driver ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("License", text="License Number")
        self.tree.heading("Vehicle No", text="Vehicle Number")
        self.tree.heading("Vehicle Type", text="Vehicle Type")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Registered On", text="Registered On")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Name", width=120, anchor="w")
        self.tree.column("Email", width=150, anchor="w")
        self.tree.column("Phone", width=100, anchor="center")
        self.tree.column("License", width=120, anchor="center")
        self.tree.column("Vehicle No", width=110, anchor="center")
        self.tree.column("Vehicle Type", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Registered On", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Info Label
        self.info_label = tk.Label(
            self.root,
            text="Select a driver and click buttons below to approve or reject",
            bg="#d1ecf1",
            fg="#0c5460",
            font=("Helvetica", 11, "bold"),
            pady=10
        )
        self.info_label.pack(fill="x", padx=20, pady=5)

        # Action Buttons Frame
        action_frame = tk.Frame(self.root, bg="#f5f5f5", pady=15)
        action_frame.pack(fill="x", padx=20)

        # View Details Button
        view_btn = tk.Button(
            action_frame,
            text="👁️ View Full Details",
            bg="#17a2b8",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=18,
            relief="flat",
            command=self.view_driver_details
        )
        view_btn.pack(side="left", padx=10)

        # Approve Button
        approve_btn = tk.Button(
            action_frame,
            text="✅ APPROVE DRIVER",
            bg="#28a745",
            fg="white",
            font=("Helvetica", 13, "bold"),
            width=18,
            relief="flat",
            command=self.approve_driver
        )
        approve_btn.pack(side="left", padx=10)

        # Reject Button
        reject_btn = tk.Button(
            action_frame,
            text="❌ REJECT APPLICATION",
            bg="#dc3545",
            fg="white",
            font=("Helvetica", 13, "bold"),
            width=20,
            relief="flat",
            command=self.reject_driver
        )
        reject_btn.pack(side="left", padx=10)

        # Refresh Button
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Refresh",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.load_pending_drivers
        )
        refresh_btn.pack(side="left", padx=10)

        # Back Button
        back_btn = tk.Button(
            action_frame,
            text="← Back",
            bg="#000000",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.back_to_dashboard
        )
        back_btn.pack(side="right", padx=10)

        # Load pending drivers
        self.current_filter = "pending"
        self.load_pending_drivers()

    def update_button_styles(self, active):
        """Update button styles"""
        buttons = {
            "pending": self.pending_button,
            "approved": self.approved_button,
            "rejected": self.rejected_button
        }
        
        for key, btn in buttons.items():
            if key == active:
                btn.config(bg="#007bff", relief="raised", bd=3, font=("Helvetica", 12, "bold"))
            else:
                btn.config(bg="#6c757d", relief="flat", bd=1, font=("Helvetica", 12))

    def show_pending(self):
        """Show pending drivers"""
        self.current_filter = "pending"
        self.update_button_styles("pending")
        self.load_pending_drivers()

    def show_approved(self):
        """Show approved drivers"""
        self.current_filter = "available"
        self.update_button_styles("approved")
        self.load_drivers_by_status("available")

    def show_rejected(self):
        """Show rejected drivers"""
        self.current_filter = "rejected"
        self.update_button_styles("rejected")
        self.load_drivers_by_status("rejected")

    def load_pending_drivers(self):
        """Load drivers with pending status"""
        self.load_drivers_by_status("pending")

    def load_drivers_by_status(self, status):
        """Load drivers by status"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            query = """
                SELECT driver_id, name, email, phone, license_number, vehicle_number, 
                       vehicle_type, status, created_at
                FROM drivers
                WHERE status = ?
                ORDER BY created_at DESC
            """
            cursor.execute(query, (status,))
            drivers = cursor.fetchall()

            # Clear existing rows
            for item in self.tree.get_children():
                self.tree.delete(item)

            if drivers:
                for driver in drivers:
                    # Format data
                    formatted_driver = list(driver)
                    if driver[8]:  # created_at
                        formatted_driver[8] = driver[8][:10]  # Show only date
                    self.tree.insert("", "end", values=tuple(formatted_driver))
                
                status_text = status.replace("available", "approved").title()
                self.info_label.config(
                    text=f"✅ {len(drivers)} {status_text} driver(s) found. Select one to view details or take action.",
                    bg="#d4edda" if status == "pending" else "#d1ecf1",
                    fg="#155724" if status == "pending" else "#0c5460"
                )
            else:
                status_text = status.replace("available", "approved").title()
                self.info_label.config(
                    text=f"ℹ️ No {status_text} drivers found.",
                    bg="#f8d7da",
                    fg="#721c24"
                )

        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error loading drivers: {err}")
        finally:
            if conn:
                conn.close()

    def get_selected_driver(self):
        """Get selected driver"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a driver first!")
            return None
        
        values = self.tree.item(selected[0])['values']
        return values

    def view_driver_details(self):
        """View full driver details"""
        driver = self.get_selected_driver()
        if not driver:
            return
        
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Driver Details - {driver[1]}")
        details_window.geometry("500x600")
        details_window.configure(bg="#ffffff")

        # Header
        header = tk.Frame(details_window, bg="#17a2b8", height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text=f"👤 Driver Information",
            font=("Helvetica", 18, "bold"),
            bg="#17a2b8",
            fg="white"
        ).pack(pady=15)

        # Details Frame
        details_frame = tk.Frame(details_window, bg="#ffffff", padx=30, pady=20)
        details_frame.pack(fill="both", expand=True)

        def add_field(label, value, row):
            tk.Label(
                details_frame,
                text=label,
                font=("Helvetica", 11, "bold"),
                bg="#ffffff",
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=8)
            
            tk.Label(
                details_frame,
                text=str(value),
                font=("Helvetica", 11),
                bg="#f0f0f0",
                anchor="w",
                relief="solid",
                bd=1,
                padx=10,
                pady=5
            ).grid(row=row, column=1, sticky="ew", pady=8, padx=(10, 0))

        add_field("Driver ID:", driver[0], 0)
        add_field("Full Name:", driver[1], 1)
        add_field("Email Address:", driver[2], 2)
        add_field("Phone Number:", driver[3], 3)
        add_field("License Number:", driver[4], 4)
        add_field("Vehicle Number:", driver[5], 5)
        add_field("Vehicle Type:", driver[6], 6)
        add_field("Current Status:", driver[7].upper(), 7)
        add_field("Registered On:", driver[8], 8)

        details_frame.columnconfigure(1, weight=1)

        # Status indicator
        status_color = {
            "pending": "#ffc107",
            "available": "#28a745",
            "rejected": "#dc3545"
        }.get(driver[7], "#6c757d")

        status_frame = tk.Frame(details_window, bg=status_color, pady=10)
        status_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            status_frame,
            text=f"STATUS: {driver[7].upper()}",
            font=("Helvetica", 14, "bold"),
            bg=status_color,
            fg="white"
        ).pack()

        # Close button
        tk.Button(
            details_window,
            text="Close",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=15,
            command=details_window.destroy
        ).pack(pady=15)

    def approve_driver(self):
        """Approve selected driver"""
        driver = self.get_selected_driver()
        if not driver:
            return
        
        driver_id, name, status = driver[0], driver[1], driver[7]

        if status != "pending":
            messagebox.showwarning(
                "Invalid Action",
                f"Only 'pending' drivers can be approved.\nThis driver's status is: {status}"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Approval",
            f"Approve driver registration?\n\n"
            f"Driver: {name}\n"
            f"ID: {driver_id}\n"
            f"License: {driver[4]}\n"
            f"Vehicle: {driver[5]} ({driver[6]})\n\n"
            f"This driver will be able to login and accept bookings."
        )

        if not confirm:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Update status to 'available' (approved)
            cursor.execute(
                "UPDATE drivers SET status = 'available' WHERE driver_id = ?",
                (driver_id,)
            )
            conn.commit()

            messagebox.showinfo(
                "✅ Driver Approved!",
                f"Driver {name} has been approved successfully!\n\n"
                f"They can now:\n"
                f"• Login to the driver dashboard\n"
                f"• Accept and manage bookings\n"
                f"• Start earning\n\n"
                f"Status changed: PENDING → AVAILABLE"
            )

            self.load_pending_drivers()

        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error approving driver: {err}")
        finally:
            if conn:
                conn.close()

    def reject_driver(self):
        """Reject selected driver"""
        driver = self.get_selected_driver()
        if not driver:
            return
        
        driver_id, name, status = driver[0], driver[1], driver[7]

        if status != "pending":
            messagebox.showwarning(
                "Invalid Action",
                f"Only 'pending' drivers can be rejected.\nThis driver's status is: {status}"
            )
            return

        # Ask for rejection reason
        reason_window = tk.Toplevel(self.root)
        reason_window.title("Rejection Reason")
        reason_window.geometry("400x250")
        reason_window.configure(bg="#ffffff")

        tk.Label(
            reason_window,
            text="Why are you rejecting this application?",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=15)

        reason_text = tk.Text(reason_window, height=6, width=40, font=("Helvetica", 10))
        reason_text.pack(padx=20, pady=10)

        def confirm_rejection():
            reason = reason_text.get("1.0", "end-1c").strip()
            if not reason:
                messagebox.showwarning("Reason Required", "Please provide a reason for rejection.")
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                cursor.execute(
                    "UPDATE drivers SET status = 'rejected' WHERE driver_id = ?",
                    (driver_id,)
                )
                conn.commit()

                messagebox.showinfo(
                    "❌ Application Rejected",
                    f"Driver application for {name} has been rejected.\n\n"
                    f"Reason: {reason}\n\n"
                    f"The driver will not be able to login."
                )

                reason_window.destroy()
                self.load_pending_drivers()

            except sqlite3.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                if conn:
                    conn.close()

        tk.Button(
            reason_window,
            text="Confirm Rejection",
            bg="#dc3545",
            fg="white",
            font=("Helvetica", 11, "bold"),
            command=confirm_rejection
        ).pack(pady=10)

    def back_to_dashboard(self):
        """Close window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ApproveDriversPage(root)
    root.mainloop()