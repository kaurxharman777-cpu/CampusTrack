
import customtkinter as ctk
import json
import os
from datetime import datetime

# ==========================================
# CAMPUS TRACK | CREATIVE EDITION
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_BG = "#0B0D18"
SIDEBAR_BG = "#111426"
PANEL = "#171B30"
CARD = "#1D2340"
CARD_HOVER = "#252C4D"

PURPLE = "#9275FF"
BLUE = "#579BFF"
PINK = "#ED78C8"
CYAN = "#52D6E8"
GREEN = "#51D6A0"
YELLOW = "#F7C66A"
RED = "#FF7185"

WHITE = "#F4F3FF"
MUTED = "#9299B8"
BORDER = "#292F4D"

FILE_NAME = "tasks.json"

# ==========================================
# DATA
# ==========================================

def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


tasks = load_tasks()


def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def is_overdue(task):
    if task.get("completed", False):
        return False

    try:
        due = datetime.strptime(
            task.get("due_date", ""), "%d-%m-%Y"
        ).date()
        return due < datetime.today().date()
    except ValueError:
        return False


def get_status(task):
    if task.get("completed", False):
        return "Completed"
    if is_overdue(task):
        return "Overdue"
    return "Pending"


def get_counts():
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed", False))
    overdue = sum(1 for t in tasks if is_overdue(t))
    pending = total - completed
    return total, pending, completed, overdue


# ==========================================
# APPLICATION WINDOW
# ==========================================

app = ctk.CTk()
app.title("CampusTrack | Your Student Workspace")
app.geometry("1250x800")
app.minsize(1050, 680)
app.configure(fg_color=APP_BG)

current_page = "Dashboard"


# ==========================================
# REUSABLE UI HELPERS
# ==========================================

def label(parent, text, size=13, color=WHITE,
          weight="normal", **kwargs):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=size,
            weight=weight
        ),
        text_color=color,
        **kwargs
    )


def button(parent, text, command, color=PURPLE,
           hover=None, width=120):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=38,
        corner_radius=11,
        fg_color=color,
        hover_color=hover or color,
        text_color=WHITE,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=12,
            weight="bold"
        )
    )


def panel(parent, color=PANEL, radius=18):
    return ctk.CTkFrame(
        parent,
        fg_color=color,
        corner_radius=radius,
        border_width=1,
        border_color=BORDER
    )


# ==========================================
# MAIN LAYOUT
# ==========================================

sidebar = ctk.CTkFrame(
    app,
    width=235,
    corner_radius=0,
    fg_color=SIDEBAR_BG
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

workspace = ctk.CTkFrame(
    app,
    fg_color=APP_BG,
    corner_radius=0
)
workspace.pack(side="left", fill="both", expand=True)

header = ctk.CTkFrame(
    workspace,
    fg_color=APP_BG,
    height=75,
    corner_radius=0
)
header.pack(fill="x", padx=35, pady=(12, 0))
header.pack_propagate(False)

page_area = ctk.CTkFrame(
    workspace,
    fg_color=APP_BG,
    corner_radius=0
)
page_area.pack(fill="both", expand=True, padx=35, pady=(10, 25))


# ==========================================
# SIDEBAR
# ==========================================

logo_area = ctk.CTkFrame(sidebar, fg_color="transparent")
logo_area.pack(fill="x", padx=22, pady=(30, 38))

logo_icon = ctk.CTkFrame(
    logo_area,
    width=42,
    height=42,
    corner_radius=13,
    fg_color=PURPLE
)
logo_icon.pack(side="left")
logo_icon.pack_propagate(False)

label(
    logo_icon, "C", 23, WHITE, "bold"
).place(relx=0.5, rely=0.5, anchor="center")

logo_text = ctk.CTkFrame(logo_area, fg_color="transparent")
logo_text.pack(side="left", padx=11)

label(logo_text, "CampusTrack", 18, WHITE, "bold").pack(anchor="w")
label(logo_text, "STUDENT WORKSPACE", 8, MUTED, "bold").pack(anchor="w")


label(
    sidebar, "WORKSPACE", 9, MUTED, "bold"
).pack(anchor="w", padx=25, pady=(0, 12))


def clear_page():
    for widget in page_area.winfo_children():
        widget.destroy()


def set_header(title, subtitle):
    for widget in header.winfo_children():
        widget.destroy()

    left = ctk.CTkFrame(header, fg_color="transparent")
    left.pack(side="left", anchor="center")

    label(left, title, 20, WHITE, "bold").pack(anchor="w")
    label(left, subtitle, 10, MUTED).pack(anchor="w", pady=(3, 0))

    date_text = datetime.now().strftime("%A, %d %B %Y")
    label(
        header, date_text, 11, MUTED
    ).pack(side="right", anchor="center")


def nav_button(text, page):
    return ctk.CTkButton(
        sidebar,
        text=text,
        command=lambda: show_page(page),
        anchor="w",
        height=45,
        corner_radius=11,
        fg_color="transparent",
        hover_color=CARD_HOVER,
        text_color=WHITE,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=13
        )
    )


nav_button("⌂    Dashboard", "Dashboard").pack(
    fill="x", padx=12, pady=4
)
nav_button("▤    My Assignments", "Assignments").pack(
    fill="x", padx=12, pady=4
)

label(
    sidebar, "ORGANIZE", 9, MUTED, "bold"
).pack(anchor="w", padx=25, pady=(32, 12))

nav_button("✓    Completed", "Completed").pack(
    fill="x", padx=12, pady=4
)

# Sidebar bottom panel
bottom_panel = ctk.CTkFrame(
    sidebar,
    fg_color=CARD,
    corner_radius=15
)
bottom_panel.pack(side="bottom", fill="x", padx=15, pady=20)

label(
    bottom_panel, "YOUR GOALS", 10, CYAN, "bold"
).pack(anchor="w", padx=15, pady=(14, 5))

label(
    bottom_panel,
    "Small steps today.\nBig achievements tomorrow.",
    11, WHITE
).pack(anchor="w", padx=15, pady=(0, 15))


# ==========================================
# TASK CARD
# ==========================================

def create_task_card(parent, task, index):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=15,
        border_width=1,
        border_color=BORDER
    )
    card.pack(fill="x", pady=6)

    top = ctk.CTkFrame(card, fg_color="transparent")
    top.pack(fill="x", padx=17, pady=(13, 5))

    status = get_status(task)

    status_colors = {
        "Completed": GREEN,
        "Pending": YELLOW,
        "Overdue": RED
    }

    label(
        top,
        task.get("task", "Untitled assignment"),
        13,
        WHITE,
        "bold"
    ).pack(side="left")

    label(
        top,
        status.upper(),
        9,
        status_colors[status],
        "bold"
    ).pack(side="right")

    details = ctk.CTkFrame(card, fg_color="transparent")
    details.pack(fill="x", padx=17, pady=(0, 8))

    subject = task.get("subject", "No subject")
    due_date = task.get("due_date", "Not set")

    label(
        details,
        subject + "   •   Due " + due_date,
        10,
        MUTED
    ).pack(side="left")

    actions = ctk.CTkFrame(card, fg_color="transparent")
    actions.pack(fill="x", padx=17, pady=(2, 13))

    if not task.get("completed", False):
        button(
            actions,
            "✓  Complete",
            lambda i=index: complete_task(i),
            color="#246B5B",
            hover="#328C76",
            width=110
        ).pack(side="left", padx=(0, 8))

    button(
        actions,
        "Delete",
        lambda i=index: delete_task(i),
        color="#633344",
        hover="#874253",
        width=75
    ).pack(side="left")


# ==========================================
# DASHBOARD
# ==========================================

def stat_card(parent, title, number, description, accent):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=17,
        border_width=1,
        border_color=BORDER
    )
    card.pack(side="left", fill="both", expand=True, padx=6)

    accent_line = ctk.CTkFrame(
        card,
        fg_color=accent,
        height=4,
        corner_radius=5
    )
    accent_line.pack(fill="x", padx=15, pady=(13, 12))

    label(card, title, 11, MUTED, "bold").pack(
        anchor="w", padx=17
    )

    label(card, str(number), 29, WHITE, "bold").pack(
        anchor="w", padx=17, pady=(5, 0)
    )

    label(card, description, 9, accent).pack(
        anchor="w", padx=17, pady=(3, 16)
    )

    return card


def show_dashboard():
    clear_page()
    set_header("Dashboard", "Your productivity at a glance")

    total, pending, completed, overdue = get_counts()

    # Welcome banner
    hero = ctk.CTkFrame(
        page_area,
        fg_color="#28204F",
        corner_radius=20,
        height=165
    )
    hero.pack(fill="x", pady=(5, 20))
    hero.pack_propagate(False)

    hero_left = ctk.CTkFrame(
        hero, fg_color="transparent"
    )
    hero_left.pack(side="left", padx=25, pady=20)

    label(
        hero_left, "MAKE TODAY COUNT ✦",
        10, CYAN, "bold"
    ).pack(anchor="w")

    label(
        hero_left, "Your goals, your pace.",
        23, WHITE, "bold"
    ).pack(anchor="w", pady=(9, 3))

    label(
        hero_left,
        "Stay organized. Keep learning. Get things done.",
        11, "#C3B9F2"
    ).pack(anchor="w", pady=(0, 13))

    button(
        hero_left,
        "+  Add New Task",
        show_add_task,
        color=PURPLE,
        hover="#765AE6",
        width=145
    ).pack(anchor="w")

    # Decorative shapes
    decoration = ctk.CTkFrame(
        hero,
        width=125,
        height=125,
        fg_color="#49368A",
        corner_radius=60
    )
    decoration.pack(side="right", padx=35, pady=15)
    decoration.pack_propagate(False)

    label(
        decoration, "✦", 57, "#D4C9FF", "bold"
    ).place(relx=0.5, rely=0.5, anchor="center")

    # Stats
    label(
        page_area, "YOUR OVERVIEW",
        11, MUTED, "bold"
    ).pack(anchor="w", pady=(2, 10))

    stats = ctk.CTkFrame(page_area, fg_color="transparent")
    stats.pack(fill="x", pady=(0, 20))

    stat_card(stats, "TOTAL TASKS", total, "All assignments", PURPLE)
    stat_card(stats, "PENDING", pending, "Still to be done", YELLOW)
    stat_card(stats, "COMPLETED", completed, "Tasks finished", GREEN)
    stat_card(stats, "OVERDUE", overdue, "Past due date", RED)

    # Progress section
    progress_card = ctk.CTkFrame(
        page_area,
        fg_color=PANEL,
        corner_radius=17,
        border_width=1,
        border_color=BORDER
    )
    progress_card.pack(fill="x", pady=(0, 20))

    progress_top = ctk.CTkFrame(
        progress_card, fg_color="transparent"
    )
    progress_top.pack(fill="x", padx=20, pady=(17, 8))

    label(
        progress_top, "Your progress",
        13, WHITE, "bold"
    ).pack(side="left")

    percent = int((completed / total) * 100) if total else 0

    label(
        progress_top, f"{percent}% completed",
        11, CYAN, "bold"
    ).pack(side="right")

    progress = ctk.CTkProgressBar(
        progress_card,
        height=11,
        corner_radius=8,
        fg_color="#303650",
        progress_color=PURPLE
    )
    progress.pack(fill="x", padx=20, pady=(0, 8))
    progress.set(completed / total if total else 0)

    label(
        progress_card,
        f"You have completed {completed} out of {total} assignments.",
        10, MUTED
    ).pack(anchor="w", padx=20, pady=(0, 17))

    # Recent assignments
    section = ctk.CTkFrame(page_area, fg_color="transparent")
    section.pack(fill="x", pady=(0, 8))

    label(
        section, "Recent assignments",
        15, WHITE, "bold"
    ).pack(side="left")

    button(
        section, "View all →",
        lambda: show_page("Assignments"),
        color=CARD,
        hover=CARD_HOVER,
        width=90
    ).pack(side="right")

    recent = tasks[-3:][::-1]

    if not recent:
        empty = ctk.CTkFrame(
            page_area,
            fg_color=CARD,
            corner_radius=15
        )
        empty.pack(fill="x", pady=10)

        label(
            empty, "Nothing here yet ✦",
            16, WHITE, "bold"
        ).pack(pady=(20, 5))

        label(
            empty,
            "Add your first assignment to get started.",
            11, MUTED
        ).pack(pady=(0, 20))
    else:
        for task in recent:
            create_task_card(page_area, task, tasks.index(task))


# ==========================================
# ADD TASK WINDOW
# ==========================================

def show_add_task():
    window = ctk.CTkToplevel(app)
    window.title("Add New Assignment")
    window.geometry("470x550")
    window.resizable(False, False)
    window.configure(fg_color=APP_BG)
    window.transient(app)
    window.grab_set()

    outer = ctk.CTkFrame(
        window,
        fg_color=PANEL,
        corner_radius=20,
        border_width=1,
        border_color=BORDER
    )
    outer.pack(fill="both", expand=True, padx=20, pady=20)

    label(
        outer, "Create a new task ✦",
        23, WHITE, "bold"
    ).pack(anchor="w", padx=25, pady=(25, 5))

    label(
        outer,
        "Add the details of your assignment below.",
        11, MUTED
    ).pack(anchor="w", padx=25, pady=(0, 20))

    def field(title, placeholder):
        label(
            outer, title, 11, WHITE, "bold"
        ).pack(anchor="w", padx=25, pady=(10, 6))

        entry = ctk.CTkEntry(
            outer,
            height=43,
            corner_radius=10,
            fg_color="#101426",
            border_color=BORDER,
            text_color=WHITE,
            placeholder_text=placeholder,
            placeholder_text_color=MUTED
        )
        entry.pack(fill="x", padx=25)
        return entry

    task_entry = field(
        "Assignment name",
        "e.g. Mathematics Assignment 1"
    )

    subject_entry = field(
        "Subject",
        "e.g. Engineering Mathematics"
    )

    date_entry = field(
        "Due date",
        "DD-MM-YYYY"
    )

    def submit():
        name = task_entry.get().strip()
        subject = subject_entry.get().strip()
        due_date = date_entry.get().strip()

        if not name or not subject or not due_date:
            message = "Please fill in all three fields."
            ctk.CTkMessagebox if False else None
            import tkinter.messagebox as msg
            msg.showwarning("Missing details", message, parent=window)
            return

        try:
            datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            import tkinter.messagebox as msg
            msg.showerror(
                "Invalid date",
                "Use DD-MM-YYYY format, for example 15-11-2026.",
                parent=window
            )
            return

        tasks.append({
            "task": name,
            "subject": subject,
            "due_date": due_date,
            "completed": False
        })

        save_tasks()
        window.destroy()
        show_page(current_page)

    button(
        outer,
        "＋   Save Assignment",
        submit,
        color=PURPLE,
        hover="#765AE6",
        width=190
    ).pack(anchor="w", padx=25, pady=25)


# ==========================================
# ASSIGNMENT PAGES
# ==========================================

def show_assignments(completed_only=False):
    clear_page()

    if completed_only:
        title = "Completed Tasks"
        subtitle = "Look at everything you've accomplished."
    else:
        title = "My Assignments"
        subtitle = "Search, manage and complete your academic tasks."

    set_header(title, subtitle)

    top = ctk.CTkFrame(page_area, fg_color="transparent")
    top.pack(fill="x", pady=(5, 15))

    search = ctk.CTkEntry(
        top,
        height=42,
        corner_radius=11,
        fg_color=PANEL,
        border_color=BORDER,
        text_color=WHITE,
        placeholder_text="Search by assignment or subject..."
    )
    search.pack(side="left", fill="x", expand=True, padx=(0, 12))

    button(
        top,
        "+  Add Task",
        show_add_task,
        width=125
    ).pack(side="right")

    task_list = ctk.CTkScrollableFrame(
        page_area,
        fg_color="transparent",
        scrollbar_button_color=CARD_HOVER,
        scrollbar_button_hover_color=PURPLE
    )
    task_list.pack(fill="both", expand=True)

    def render(event=None):
        for widget in task_list.winfo_children():
            widget.destroy()

        query = search.get().lower().strip()
        found = False

        for index, task in enumerate(tasks):
            is_completed = task.get("completed", False)

            if completed_only and not is_completed:
                continue

            if not completed_only and is_completed:
                continue

            searchable = (
                task.get("task", "") + " " +
                task.get("subject", "")
            ).lower()

            if query not in searchable:
                continue

            found = True
            create_task_card(task_list, task, index)

        if not found:
            label(
                task_list,
                "No assignments found.",
                14, MUTED
            ).pack(pady=40)

    search.bind("<KeyRelease>", render)
    render()


# ==========================================
# TASK ACTIONS
# ==========================================

def complete_task(index):
    tasks[index]["completed"] = True
    save_tasks()
    show_page(current_page)


def delete_task(index):
    import tkinter.messagebox as msg

    answer = msg.askyesno(
        "Delete assignment",
        "Are you sure you want to delete this assignment?",
        parent=app
    )

    if answer:
        tasks.pop(index)
        save_tasks()
        show_page(current_page)


# ==========================================
# PAGE NAVIGATION
# ==========================================

def show_page(page):
    global current_page
    current_page = page

    if page == "Dashboard":
        show_dashboard()

    elif page == "Assignments":
        show_assignments(False)

    elif page == "Completed":
        show_assignments(True)


# ==========================================
# START APPLICATION
# ==========================================

show_page("Dashboard")

app.mainloop()
