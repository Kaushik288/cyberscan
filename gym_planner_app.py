# Smart Gym Planner - desktop app

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk  # for photos


# ---------- LOGIC FUNCTIONS ----------

def calculate_bmi(height_cm, weight_kg):
    try:
        h_m = height_cm / 100
        if h_m <= 0 or weight_kg <= 0:
            return None
        return weight_kg / (h_m * h_m)
    except Exception:
        return None


def get_bmi_status(bmi):
    if bmi is None:
        return "N/A"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def get_workout_plan(goal, experience, activity):
    plan = {"title": "", "summary": "", "days": []}

    if goal == "fat-loss":
        plan["title"] = "Fat Loss + Strength Plan"
        plan["summary"] = (
            "Focus on calorie burn + preserving muscle. "
            "Start with compound lifts, finish with short but intense cardio."
        )
        plan["days"] = [
            {
                "name": "Day 1 – Full Body + Cardio",
                "items": [
                    "Squats / Leg Press – 3×10–12",
                    "Push-ups or Bench Press – 3×10",
                    "Lat Pulldown / Assisted Pull-ups – 3×10–12",
                    "Plank – 3×30s",
                    "Treadmill walk / incline – 20 mins",
                ],
            },
            {
                "name": "Day 2 – Upper Body + Core",
                "items": [
                    "Dumbbell Shoulder Press – 3×10–12",
                    "One-arm Dumbbell Row – 3×10 each side",
                    "Cable / Machine Chest Fly – 3×12",
                    "Russian twists – 3×16",
                    "Cycling / cross-trainer – 15–20 mins",
                ],
            },
            {
                "name": "Day 3 – Lower Body + HIIT",
                "items": [
                    "Leg Extension – 3×12",
                    "Leg Curl – 3×12",
                    "Walking Lunges – 3×12 steps each leg",
                    "Mountain climbers – 3×30s",
                    "HIIT: 30s fast, 60s slow × 8 rounds",
                ],
            },
        ]
    elif goal == "muscle-gain":
        plan["title"] = "Hypertrophy (Muscle Gain) Plan"
        plan["summary"] = (
            "Progressive overload with enough volume. "
            "Keep form clean, increase weights slowly every week."
        )
        plan["days"] = [
            {
                "name": "Day 1 – Push (Chest + Shoulders + Triceps)",
                "items": [
                    "Bench Press / Machine Press – 4×8–10",
                    "Incline Dumbbell Press – 3×10–12",
                    "Shoulder Press – 3×10",
                    "Lateral Raises – 3×12–15",
                    "Triceps Rope Pushdown – 3×12",
                ],
            },
            {
                "name": "Day 2 – Pull (Back + Biceps)",
                "items": [
                    "Lat Pulldown / Pull-ups – 4×8–10",
                    "Seated Cable Row – 3×10–12",
                    "Face Pulls – 3×15",
                    "Barbell / Dumbbell Curls – 3×10–12",
                    "Hammer Curls – 3×10",
                ],
            },
            {
                "name": "Day 3 – Legs + Core",
                "items": [
                    "Squats / Leg Press – 4×8–10",
                    "Romanian Deadlift – 3×10",
                    "Leg Curls – 3×12",
                    "Calf Raises – 3×15–20",
                    "Plank + Leg Raises – 3 sets each",
                ],
            },
        ]
    else:
        plan["title"] = "General Fitness & Conditioning Plan"
        plan["summary"] = (
            "Balanced strength, mobility and cardio. "
            "Great if you want to stay active, toned and healthy."
        )
        plan["days"] = [
            {
                "name": "Day 1 – Full Body Strength",
                "items": [
                    "Goblet Squat – 3×12",
                    "Dumbbell Bench Press – 3×12",
                    "Seated Row – 3×12",
                    "Plank – 3×30s",
                    "10–15 mins light cardio",
                ],
            },
            {
                "name": "Day 2 – Cardio + Mobility",
                "items": [
                    "30–40 mins brisk walk / cycling",
                    "Dynamic stretches (hips, shoulders, hamstrings)",
                    "Light core work (deadbugs, side plank)",
                ],
            },
            {
                "name": "Day 3 – Mixed Strength",
                "items": [
                    "Deadlift variation (light) – 3×8",
                    "Overhead Press – 3×10",
                    "Lat Pulldown – 3×12",
                    "Bodyweight Lunges – 3×12 each leg",
                    "10 mins cool-down walk + stretching",
                ],
            },
        ]

    if experience == "beginner":
        plan["summary"] += (
            " Since you are a beginner, start with lighter weights, "
            "keep 1–2 reps in reserve and focus on learning technique first."
        )
    elif experience == "advanced":
        plan["summary"] += (
            " As you are advanced, you can add 1–2 extra sets for main lifts "
            "and use variations like drop-sets or supersets."
        )

    if activity == "sedentary" and goal == "fat-loss":
        plan["summary"] += (
            " Because your current activity is low, try to hit a minimum of "
            "8–9k steps per day outside the gym."
        )

    return plan


def get_diet_plan(goal, diet_pref, weight):
    base_protein = round(weight * 1.6)
    diet = {"title": "", "summary": "", "meals": [], "extras": []}

    if diet_pref == "veg":
        pref_name = "Vegetarian"
    elif diet_pref == "non-veg":
        pref_name = "Non-Vegetarian"
    else:
        pref_name = "Eggetarian"

    diet["title"] = f"Daily Meal Guidance ({pref_name})"
    diet["summary"] = (
        f"Aim for around {base_protein}g of protein per day. "
        "Keep most of your meals simple, repeatable and easy to cook."
    )

    if diet_pref == "veg":
        diet["meals"] = [
            {
                "name": "Breakfast",
                "items": [
                    "Oats with milk + 1 scoop whey (if available) + nuts",
                    "OR 2–3 besan chillas with curd",
                    "1 fruit (banana / apple)",
                ],
            },
            {
                "name": "Lunch",
                "items": [
                    "2–3 phulkas / 1.5 cup rice",
                    "1.5 cup dal / rajma / chole",
                    "1 cup mixed veg sabzi",
                    "Salad: cucumber, carrot, onion, lemon",
                ],
            },
            {
                "name": "Evening Snack",
                "items": [
                    "Sprouts salad with onion + tomato + lemon",
                    "OR roasted chana + buttermilk",
                ],
            },
            {
                "name": "Dinner",
                "items": [
                    "Paneer bhurji / tofu + 2 phulkas",
                    "Mixed veggie sabzi",
                    "Light salad (avoid heavy fried food at night)",
                ],
            },
        ]
    elif diet_pref == "non-veg":
        diet["meals"] = [
            {
                "name": "Breakfast",
                "items": [
                    "3–4 egg omelette (2 whole + 2 whites) + 2 bread slices",
                    "OR oats with milk + boiled eggs",
                    "1 fruit",
                ],
            },
            {
                "name": "Lunch",
                "items": [
                    "150–180g chicken (grilled / curry) or fish",
                    "2–3 phulkas / 1.5 cup rice",
                    "1 cup sabzi",
                    "Salad bowl",
                ],
            },
            {
                "name": "Evening Snack",
                "items": [
                    "Greek curd / dahi + peanuts / nuts",
                    "OR tuna / chicken sandwich (less mayo)",
                ],
            },
            {
                "name": "Dinner",
                "items": [
                    "Chicken / fish + lots of veggies (stir-fried / grilled)",
                    "1–2 phulkas or small portion of rice",
                    "Avoid sugary drinks and deep fried sides",
                ],
            },
        ]
    else:  # eggetarian
        diet["meals"] = [
            {
                "name": "Breakfast",
                "items": [
                    "Oats with milk + 1–2 boiled eggs",
                    "OR 2–3 egg bhurji + 2 phulkas",
                    "1 fruit",
                ],
            },
            {
                "name": "Lunch",
                "items": [
                    "2–3 phulkas / 1.5 cup rice",
                    "1 cup dal",
                    "2 boiled eggs / egg curry",
                    "Veg sabzi + salad",
                ],
            },
            {
                "name": "Evening Snack",
                "items": [
                    "Sprouts / chana + buttermilk",
                    "OR peanut butter on toast (thin layer)",
                ],
            },
            {
                "name": "Dinner",
                "items": [
                    "Paneer / tofu / egg bhurji",
                    "2 phulkas",
                    "Veg sabzi + salad",
                ],
            },
        ]

    if goal == "fat-loss":
        diet["extras"].extend([
            "Keep sugar low. Avoid daily sweets, soft drinks and heavy fried food.",
            "Use smaller plates, eat slowly and stop when you are ~80% full.",
            "Prioritise protein + veggies in every meal; control oil quantity.",
        ])
    elif goal == "muscle-gain":
        diet["extras"].extend([
            "You may need a small calorie surplus; add extra roti / rice or 1 extra snack if weight is not increasing.",
            "Keep protein high across all meals, not only at night.",
            "If using whey protein, 1–2 scoops per day is enough for most people.",
        ])
    else:
        diet["extras"].extend([
            "Balance: half the plate veggies / salad, quarter protein, quarter carbs.",
            "Stay consistent through the week; small treats are okay but not daily.",
            "Drink water regularly instead of sugary drinks.",
        ])

    return diet


def get_general_tips(goal):
    tips = [
        "Sleep 7–8 hours every night. Recovery is where the real progress happens.",
        "Water target: roughly 2.5–3.5L per day (more if you sweat a lot).",
        "Warm up 5–10 mins before lifting (light cardio + mobility).",
        "Track your progress: photos, measurements, or notes every 2 weeks.",
    ]
    if goal == "muscle-gain":
        tips.append("Log your lifts and try to add a little weight or reps over time (progressive overload).")
    elif goal == "fat-loss":
        tips.append("Steps matter! Try to keep daily steps high in addition to gym sessions.")
    return tips


# ---------- GUI APP ----------

class GymPlannerApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Gym Planner")
        root.geometry("1100x650")
        root.configure(bg="#101014")

        # ---------- load images (safe if missing) ----------
        self.banner_img = None
        self.side_img = None
        try:
            banner = Image.open("assets/gym_banner.jpg")
            banner = banner.resize((1060, 120))
            self.banner_img = ImageTk.PhotoImage(banner)
        except Exception:
            pass

        try:
            side = Image.open("assets/gym_side.jpg")
            side = side.resize((260, 260))
            self.side_img = ImageTk.PhotoImage(side)
        except Exception:
            pass

        # ---------- styles ----------
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#101014")
        style.configure("TLabel", background="#101014", foreground="#f5f5f5", font=("SF Pro Text", 11))
        style.configure("Header.TLabel", font=("SF Pro Display", 18, "bold"), foreground="#ffffff")
        style.configure("Small.TLabel", font=("SF Pro Text", 9), foreground="#cbd5f5")
        style.configure("Card.TLabelframe",
                        background="#181824",
                        foreground="#e5e7eb",
                        borderwidth=0)
        style.configure("Card.TLabelframe.Label",
                        background="#181824",
                        foreground="#e5e7eb",
                        font=("SF Pro Text", 11, "bold"))
        style.configure("TButton",
                        font=("SF Pro Text", 11, "bold"),
                        padding=6)
        style.map("TButton",
                  background=[("active", "#22c55e")])

        style.configure("TEntry",
                        fieldbackground="#0b0b12",
                        foreground="#f9fafb",
                        bordercolor="#4b5563")
        style.configure("TCombobox",
                        fieldbackground="#0b0b12",
                        background="#0b0b12",
                        foreground="#f9fafb")

        # ---------- main container ----------
        outer = ttk.Frame(root, padding=10)
        outer.pack(fill="both", expand=True)

        # ----- banner -----
        if self.banner_img:
            banner_label = ttk.Label(outer, image=self.banner_img)
            banner_label.pack(fill="x", pady=(0, 10))
        else:
            header_frame = ttk.Frame(outer)
            header_frame.pack(fill="x", pady=(0, 10))
            ttk.Label(header_frame,
                      text="Smart Gym Planner",
                      style="Header.TLabel").pack(side="left")
            ttk.Label(header_frame,
                      text="Personalised workout & diet guide",
                      style="Small.TLabel").pack(side="left", padx=12)

        # ----- content area (left form + right plan) -----
        content = ttk.Frame(outer)
        content.pack(fill="both", expand=True)

        self.left = ttk.Labelframe(content, text="Your Details",
                                   style="Card.TLabelframe", padding=12)
        self.left.pack(side="left", fill="y", padx=(0, 10))

        self.right = ttk.Labelframe(content, text="Your Plan",
                                    style="Card.TLabelframe", padding=12)
        self.right.pack(side="right", fill="both", expand=True)

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        lf = self.left

        ttk.Label(lf, text="Name (optional):").grid(row=0, column=0, sticky="w", pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(lf, textvariable=self.name_var, width=20).grid(row=0, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Age (years):").grid(row=1, column=0, sticky="w", pady=2)
        self.age_var = tk.StringVar()
        ttk.Entry(lf, textvariable=self.age_var, width=10).grid(row=1, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Gender:").grid(row=2, column=0, sticky="w", pady=2)
        self.gender_var = tk.StringVar()
        gender_cb = ttk.Combobox(lf, textvariable=self.gender_var, state="readonly",
                                 values=["Male", "Female", "Other"], width=17)
        gender_cb.grid(row=2, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Height (cm):").grid(row=3, column=0, sticky="w", pady=2)
        self.height_var = tk.StringVar()
        ttk.Entry(lf, textvariable=self.height_var, width=10).grid(row=3, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Weight (kg):").grid(row=4, column=0, sticky="w", pady=2)
        self.weight_var = tk.StringVar()
        ttk.Entry(lf, textvariable=self.weight_var, width=10).grid(row=4, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Goal:").grid(row=5, column=0, sticky="w", pady=2)
        self.goal_var = tk.StringVar()
        goal_cb = ttk.Combobox(
            lf,
            textvariable=self.goal_var,
            state="readonly",
            values=["fat-loss", "muscle-gain", "fitness"],
            width=17,
        )
        goal_cb.grid(row=5, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Activity level:").grid(row=6, column=0, sticky="w", pady=2)
        self.activity_var = tk.StringVar()
        activity_cb = ttk.Combobox(
            lf,
            textvariable=self.activity_var,
            state="readonly",
            values=["sedentary", "light", "moderate", "high"],
            width=17,
        )
        activity_cb.grid(row=6, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Gym experience:").grid(row=7, column=0, sticky="w", pady=2)
        self.experience_var = tk.StringVar()
        exp_cb = ttk.Combobox(
            lf,
            textvariable=self.experience_var,
            state="readonly",
            values=["beginner", "intermediate", "advanced"],
            width=17,
        )
        exp_cb.grid(row=7, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Diet preference:").grid(row=8, column=0, sticky="w", pady=2)
        self.diet_var = tk.StringVar()
        diet_cb = ttk.Combobox(
            lf,
            textvariable=self.diet_var,
            state="readonly",
            values=["veg", "non-veg", "egg"],
            width=17,
        )
        diet_cb.grid(row=8, column=1, pady=2, padx=4, sticky="w")

        ttk.Label(lf, text="Notes / injuries:").grid(row=9, column=0, sticky="nw", pady=2)
        self.notes_var = tk.StringVar()
        ttk.Entry(lf, textvariable=self.notes_var, width=30).grid(row=9, column=1, pady=2, padx=4, sticky="w")

        btn = ttk.Button(lf, text="Generate Plan", command=self.on_generate)
        btn.grid(row=10, column=0, columnspan=2, pady=12, sticky="ew")

        for i in range(11):
            lf.grid_rowconfigure(i, pad=3)

    def build_right_panel(self):
        container = ttk.Frame(self.right)
        container.pack(fill="both", expand=True)

        text_frame = ttk.Frame(container)
        text_frame.pack(side="left", fill="both", expand=True)

        self.output = ScrolledText(
            text_frame,
            wrap="word",
            font=("Menlo", 11),
            bg="#050509",
            fg="#f5f5f5",
            insertbackground="#f5f5f5",
        )
        self.output.pack(fill="both", expand=True, padx=(0, 6))
        self.output.insert("end", "Fill your details on the left and click 'Generate Plan' to see your plan here.")
        self.output.configure(state="disabled")

        if self.side_img:
            side_frame = ttk.Frame(container)
            side_frame.pack(side="right", fill="y")

            img_label = ttk.Label(side_frame, image=self.side_img)
            img_label.pack(pady=(0, 4))

            ttk.Label(
                side_frame,
                text="Stay consistent.\nSmall daily steps → big results.",
                style="Small.TLabel",
                justify="center",
            ).pack()
        else:
            ttk.Label(
                container,
                text="Tip: Add 'assets/gym_side.jpg' to show a motivation photo here.",
                style="Small.TLabel",
                justify="center",
            ).pack(side="right", padx=6)

    def on_generate(self):
        try:
            age = int(self.age_var.get())
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age, height and weight.")
            return

        gender = self.gender_var.get()
        goal = self.goal_var.get()
        activity = self.activity_var.get()
        experience = self.experience_var.get()
        diet_pref = self.diet_var.get()
        name = self.name_var.get().strip()
        notes = self.notes_var.get().strip()

        if not (gender and goal and activity and experience and diet_pref):
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        bmi = calculate_bmi(height, weight)
        bmi_status = get_bmi_status(bmi)

        workout = get_workout_plan(goal, experience, activity)
        diet = get_diet_plan(goal, diet_pref, weight)
        tips = get_general_tips(goal)

        if diet_pref == "veg":
            diet_text = "Vegetarian"
        elif diet_pref == "non-veg":
            diet_text = "Non-Veg"
        else:
            diet_text = "Eggetarian"

        goal_text = {
            "fat-loss": "Fat Loss",
            "muscle-gain": "Muscle Gain",
            "fitness": "Fitness / Toning",
        }.get(goal, goal)

        lines = []
        lines.append("=== SMART GYM PLANNER ===")
        if name:
            lines.append(f"Personalised plan for: {name}")
        lines.append("")

        lines.append("1. OVERVIEW")
        lines.append(f"Age: {age} yrs | Gender: {gender} | Diet: {diet_text}")
        lines.append(f"Height: {height} cm | Weight: {weight} kg")
        if bmi is not None:
            lines.append(f"BMI: {bmi:.1f} ({bmi_status})")
        else:
            lines.append("BMI: N/A")
        lines.append(f"Goal: {goal_text}")
        lines.append(f"Activity: {activity} | Experience: {experience}")
        if notes:
            lines.append(f"Notes: {notes}")
        lines.append("")

        lines.append("2. WORKOUT PLAN")
        lines.append(workout["title"])
        lines.append(workout["summary"])
        lines.append("")
        for day in workout["days"]:
            lines.append(f"- {day['name']}")
            for item in day["items"]:
                lines.append(f"    • {item}")
            lines.append("")
        lines.append("")

        lines.append("3. DAILY MEAL GUIDANCE")
        lines.append(diet["title"])
        lines.append(diet["summary"])
        lines.append("")
        for meal in diet["meals"]:
            lines.append(f"- {meal['name']}:")
            for item in meal["items"]:
                lines.append(f"    • {item}")
            lines.append("")
        lines.append("Extra rules:")
        for ex in diet["extras"]:
            lines.append(f"    • {ex}")
        lines.append("")

        lines.append("4. EXTRA TIPS")
        for t in tips:
            lines.append(f"- {t}")
        lines.append("")
        lines.append("This is a starting point. As your body responds, adjust food quantity and workout intensity.")

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", "\n".join(lines))
        self.output.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = GymPlannerApp(root)
    root.mainloop()
