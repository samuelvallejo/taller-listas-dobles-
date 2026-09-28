import tkinter as tk


class BusRouteApp:
    """tkinter frontend for the doubly linked bus route. O(n) redraws."""

    def __init__(self, root, route):
        """Build every widget and draw the first screen. O(n)."""
        self.root = root
        self.route = route
        root.title("Urban Bus Route - Doubly Linked List")
        root.geometry("1000x760")
        root.configure(bg="#f2f2f2")
        self._build_inputs()
        self._build_commands()
        self._build_navigation()
        self._build_canvas()
        self._build_trips()
        self._build_status()
        self.refresh()

    def _build_inputs(self):
        """Create the stop name field and the reference stop field. O(1)."""
        frame = tk.Frame(self.root, bg="#f2f2f2")
        frame.pack(fill="x", padx=10, pady=8)

        label_name = tk.Label(frame, text="Stop name:", bg="#f2f2f2", font="Arial 11")
        label_name.pack(side="left")
        self.name_entry = tk.Entry(frame, width=26, font="Arial 11")
        self.name_entry.pack(side="left", padx=6)

        label_ref = tk.Label(frame, text="Reference stop:", bg="#f2f2f2", font="Arial 11")
        label_ref.pack(side="left", padx=14)
        self.ref_entry = tk.Entry(frame, width=26, font="Arial 11")
        self.ref_entry.pack(side="left", padx=6)

        label_pos = tk.Label(frame, text="Position:", bg="#f2f2f2", font="Arial 11")
        label_pos.pack(side="left", padx=14)
        self.position_entry = tk.Entry(frame, width=6, font="Arial 11")
        self.position_entry.pack(side="left", padx=6)

    def _build_commands(self):
        """Create the buttons that modify and search the route. O(1)."""
        frame = tk.Frame(self.root, bg="#f2f2f2")
        frame.pack(fill="x", padx=10, pady=2)

        self._make_button(frame, "Add First", self.on_add_first)
        self._make_button(frame, "Add Last", self.on_add_last)
        self._make_button(frame, "Add After", self.on_add_after)
        self._make_button(frame, "Add Before", self.on_add_before)
        self._make_button(frame, "Add at Position", self.on_add_at)
        self._make_button(frame, "Remove", self.on_remove)
        self._make_button(frame, "Search", self.on_search)

    def _build_navigation(self):
        """Create the navigation buttons and the stop counter. O(1)."""
        frame = tk.Frame(self.root, bg="#f2f2f2")
        frame.pack(fill="x", padx=10, pady=2)

        self._make_button(frame, "Previous Stop", self.on_previous)
        self._make_button(frame, "Next Stop", self.on_next)
        self._make_button(frame, "Go to Start", self.on_go_start)
        self._make_button(frame, "Go to End", self.on_go_end)

        self.counter_label = tk.Label(frame, text="Stops: 0", bg="#f2f2f2",
                                      font="Arial 12 bold", fg="#b02a2a")
        self.counter_label.pack(side="right", padx=12)

    def _build_canvas(self):
        """Create the canvas that draws the route plus a horizontal bar. O(1)."""
        self.canvas = tk.Canvas(self.root, height=250, bg="white",
                                highlightthickness=1, highlightbackground="#bbbbbb")
        self.canvas.pack(fill="x", padx=10, pady=6)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        bar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        bar.pack(fill="x", padx=10)
        self.canvas.config(xscrollcommand=bar.set)

    def _build_trips(self):
        """Create the text panel that shows both route directions. O(1)."""
        label = tk.Label(self.root, text="Route trips", bg="#f2f2f2",
                         font="Arial 11 bold", anchor="w")
        label.pack(fill="x", padx=10)
        self.trips_text = tk.Text(self.root, height=5, font="Arial 11",
                                  state="disabled", bg="white")
        self.trips_text.pack(fill="both", padx=10, pady=2, expand=True)

    def _build_status(self):
        """Create the status bar at the bottom of the window. O(1)."""
        self.status_label = tk.Label(self.root, text="Status: ready", bg="#dddddd",
                                     font="Arial 10", anchor="w", padx=10)
        self.status_label.pack(fill="x", side="bottom", pady=4)

    def _make_button(self, parent, text, command):
        """Create one button with the shared style. O(1)."""
        button = tk.Button(parent, text=text, command=command, font="Arial 10 bold",
                           bg="#2a6fb0", fg="white", activebackground="#1e5586",
                           activeforeground="white", relief="raised", padx=8, pady=4)
        button.pack(side="left", padx=4, pady=2)
        return button

    def set_status(self, message):
        """Show a message in the status bar. O(1)."""
        self.status_label.config(text="Status: " + message)

    def refresh(self):
        """Redraw the canvas, the trip panel and the stop counter. O(n)."""
        self.redraw()
        self.update_trips()

    def redraw(self):
        """Clear the canvas and walk the list to draw every stop. O(n)."""
        self.canvas.delete("all")
        self.counter_label.config(text="Stops: " + str(self.route.size))
        if self.route.is_empty():
            self.canvas.create_text(420, 120, text="Route is empty",
                                    fill="#888888", font="Arial 14")
            self.canvas.config(scrollregion="0 0 840 250")
            return

        x = 80
        y = 155
        gap = 155
        previous_x = None
        pointer = self.route.head
        while pointer is not None:
            if previous_x is not None:
                self.canvas.create_line(previous_x + 40, y, x - 44, y,
                                        fill="#777777", width=3, arrow="last")
            self._draw_stop(pointer, x, y)
            previous_x = x
            x = x + gap
            pointer = pointer.next
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _draw_stop(self, stop, x, y):
        """Draw one stop circle and highlight the stop where the bus is. O(1)."""
        if stop is self.route.current:
            fill = "#ffb347"
            outline = "#b36b00"
        else:
            fill = "#e1eef7"
            outline = "#2a6fb0"
        self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40,
                                fill=fill, outline=outline, width=3)
        self.canvas.create_text(x, y, text=stop.name, font="Arial 10 bold",
                                fill="#222222", width=72)
        if stop is self.route.current:
            self._draw_bus(x, y)

    def _draw_bus(self, x, y):
        """Draw a small bus above the current stop. O(1)."""
        self.canvas.create_rectangle(x - 36, y - 100, x + 36, y - 64,
                                     fill="#2a6fb0", outline="white", width=2)
        self.canvas.create_text(x, y - 82, text="BUS", fill="white", font="Arial 11 bold")
        self.canvas.create_oval(x - 28, y - 70, x - 14, y - 56, fill="#333333")
        self.canvas.create_oval(x + 14, y - 70, x + 28, y - 56, fill="#333333")

    def update_trips(self):
        """Refresh the forward and backward route text. O(n)."""
        self.trips_text.config(state="normal")
        self.trips_text.delete("1.0", "end")
        self.trips_text.insert("end", "Forward route: " + self.route.forward_text() + "\n")
        self.trips_text.insert("end", "Backward route: " + self.route.backward_text())
        self.trips_text.config(state="disabled")

    def on_mousewheel(self, event):
        """Scroll the route horizontally with the mouse wheel. O(1)."""
        if event.delta != 0:
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def _check_new_name(self, name):
        """Validate a new stop name and report why it was rejected. O(n)."""
        if name == "":
            self.set_status("empty name")
            return False
        if self.route.search(name) is not None:
            self.set_status("duplicate name")
            return False
        return True

    def _check_target(self, reference):
        """Validate the reference stop used by add_after and add_before. O(n)."""
        if self.route.is_empty():
            self.set_status("route is empty")
            return False
        if self.route.search(reference) is None:
            self.set_status("stop not found")
            return False
        return True

    def on_add_first(self):
        """Insert a stop at the start of the route. O(n)."""
        name = self.name_entry.get().strip()
        if not self._check_new_name(name):
            return
        self.route.add_first(name)
        self.name_entry.delete(0, "end")
        self.set_status("Stop added at the start: " + name)
        self.refresh()

    def on_add_last(self):
        """Insert a stop at the end of the route. O(n)."""
        name = self.name_entry.get().strip()
        if not self._check_new_name(name):
            return
        self.route.add_last(name)
        self.name_entry.delete(0, "end")
        self.set_status("Stop added at the end: " + name)
        self.refresh()

    def on_add_after(self):
        """Insert a stop right after the reference stop. O(n)."""
        name = self.name_entry.get().strip()
        reference = self.ref_entry.get().strip()
        if not self._check_new_name(name):
            return
        if not self._check_target(reference):
            return
        self.route.add_after(reference, name)
        self.name_entry.delete(0, "end")
        self.set_status("Stop added after " + reference + ": " + name)
        self.refresh()

    def on_add_before(self):
        """Insert a stop right before the reference stop. O(n)."""
        name = self.name_entry.get().strip()
        reference = self.ref_entry.get().strip()
        if not self._check_new_name(name):
            return
        if not self._check_target(reference):
            return
        self.route.add_before(reference, name)
        self.name_entry.delete(0, "end")
        self.set_status("Stop added before " + reference + ": " + name)
        self.refresh()

    def on_add_at(self):
        """Insert a stop at the 1-based position typed in the position field. O(n)."""
        name = self.name_entry.get().strip()
        position_text = self.position_entry.get().strip()
        if not self._check_new_name(name):
            return
        if not position_text.isdigit():
            self.set_status("invalid position")
            return
        if self.route.add_at(int(position_text), name):
            self.name_entry.delete(0, "end")
            self.position_entry.delete(0, "end")
            self.set_status("Stop added at position " + position_text + ": " + name)
            self.refresh()
            return
        self.set_status("invalid position, use 1 to " + str(self.route.size + 1))

    def on_remove(self):
        """Remove the stop typed in the name field. O(n)."""
        name = self.name_entry.get().strip()
        if name == "":
            self.set_status("empty name")
            return
        if self.route.is_empty():
            self.set_status("route is empty")
            return
        if self.route.search(name) is None:
            self.set_status("stop not found")
            return
        self.route.remove(name)
        self.name_entry.delete(0, "end")
        self.set_status("Stop removed: " + name)
        self.refresh()

    def on_search(self):
        """Find a stop and show its previous and next stop. O(n)."""
        name = self.name_entry.get().strip()
        if name == "":
            self.set_status("empty name")
            return
        if self.route.is_empty():
            self.set_status("route is empty")
            return
        if self.route.search(name) is None:
            self.set_status("stop not found")
            return
        self.set_status("Stop found: " + name + " | " + self.route.neighbors_text(name))

    def on_previous(self):
        """Move the bus to the previous stop. O(1)."""
        if self.route.is_empty():
            self.set_status("route is empty")
            return
        if self.route.move_prev():
            self.set_status("Bus moved to: " + self.route.current.name)
            self.refresh()
            return
        self.set_status("The bus is already at the first stop")

    def on_next(self):
        """Move the bus to the next stop. O(1)."""
        if self.route.is_empty():
            self.set_status("route is empty")
            return
        if self.route.move_next():
            self.set_status("Bus moved to: " + self.route.current.name)
            self.refresh()
            return
        self.set_status("The bus is already at the last stop")

    def on_go_start(self):
        """Move the bus to the first stop. O(1)."""
        if self.route.go_to_head():
            self.set_status("Bus moved to: " + self.route.current.name)
            self.refresh()
            return
        self.set_status("route is empty")

    def on_go_end(self):
        """Move the bus to the last stop. O(1)."""
        if self.route.go_to_tail():
            self.set_status("Bus moved to: " + self.route.current.name)
            self.refresh()
            return
        self.set_status("route is empty")


def run(route):
    """Open the window and start the interface loop. O(1)."""
    root = tk.Tk()
    BusRouteApp(root, route)
    root.mainloop()
