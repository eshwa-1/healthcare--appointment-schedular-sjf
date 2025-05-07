def get_patient_input():
    patients = []
    n = int(input("Enter number of patients: "))
    for i in range(n):
        print(f"\nEnter details for Patient #{i+1}:")
        name = input("  Name           : ").strip()
        arrival = int(input("  Arrival Time   : "))
        duration = int(input("  Consultation Time (minutes): "))
        patients.append({"name": name, "arrival": arrival, "duration": duration})
    return patients

def schedule_sjf_non_preemptive(patients):
    n = len(patients)
    time = 0
    completed = 0
    scheduled = []
    visited = [False] * n

    while completed < n:
        available = []
        for i in range(n):
            if not visited[i] and patients[i]["arrival"] <= time and patients[i]["name"].lower() != "dd":
                available.append((i, patients[i]["duration"]))

        if not available:
            for i in range(n):
                if not visited[i] and patients[i]["arrival"] <= time:
                    available.append((i, patients[i]["duration"]))
            if not available:
                scheduled.append({"name": "Idle", "start": time, "finish": time + 1})
                time += 1
                continue

        selected_index = min(available, key=lambda x: x[1])[0]
        selected = patients[selected_index]

        start_time = time
        finish_time = start_time + selected["duration"]
        waiting_time = start_time - selected["arrival"]
        turnaround_time = finish_time - selected["arrival"]

        scheduled.append({
            "name": selected["name"],
            "arrival": selected["arrival"],
            "duration": selected["duration"],
            "start": start_time,
            "finish": finish_time,
            "waiting": waiting_time,
            "turnaround": turnaround_time
        })

        visited[selected_index] = True
        completed += 1
        time = finish_time

    return scheduled

def display_table(patients):
    print("\nAppointment Schedule:")
    print("=" * 90)
    print(f"{'Patient Name':<15}{'Arrival':<10}{'Consult':<10}"
          f"{'Start':<10}{'Finish':<10}{'Waiting':<10}{'Turnaround':<10}")
    print("-" * 90)
    for p in patients:
        if p['name'].lower() == "idle":
            print(f"{p['name']:<15}--{'':<45}Idle Time")
        else:
            print(f"{p['name']:<15}{p['arrival']:<10}{p['duration']:<10}"
                  f"{p['start']:<10}{p['finish']:<10}{p['waiting']:<10}{p['turnaround']:<10}")
    print("=" * 90)

def display_gantt_chart(patients):
    print("\nGantt Chart:")
    chart = "|"
    timeline = f"{patients[0]['start']}".ljust(4)
    for p in patients:
        label = p['name']
        chart += f" {label} ".center(6, "-") + "|"
        timeline += f"{str(p['finish']).rjust(6)}"
    print(chart)
    print(timeline)

def display_stairs(patients):
    print("\nPatient Stairs View:")
    for p in patients:
        if p['name'].lower() == "idle":
            print(" " * p['start'] + "Idle Time")
        else:
            line = " " * p['start'] + f"{p['name']} ➜ " + "🧍" * p['duration']
            print(line)

def calculate_statistics(patients):
    real_patients = [p for p in patients if p['name'].lower() != "idle"]
    total_waiting = sum(p["waiting"] for p in real_patients)
    total_turnaround = sum(p["turnaround"] for p in real_patients)
    avg_waiting = total_waiting / len(real_patients)
    avg_turnaround = total_turnaround / len(real_patients)
    return avg_waiting, avg_turnaround, len([p for p in patients if p['name'] == "Idle"])

def check_dd_avoided(patients):
    for i, p in enumerate(patients):
        if p["name"].lower() == "dd" and i > 0:
            return True
    return False

def display_final_report_table(patients, avg_waiting, avg_turnaround, idle_count):
    print("\nFinal Summary Table")
    print("=" * 60)
    print(f"{'Total Patients':<25}: {len([p for p in patients if p['name'].lower() != 'idle'])}")
    print(f"{'Total Idle Periods':<25}: {idle_count}")
    print(f"{'Average Waiting Time':<25}: {avg_waiting:.2f} min")
    print(f"{'Average Turnaround Time':<25}: {avg_turnaround:.2f} min")
    print(f"{'DD Skipped (Delayed)':<25}: {'YES' if check_dd_avoided(patients) else 'NO'}")
    print("=" * 60)

# === Main Execution ===
print("\n==== Healthcare Appointment Scheduler (SJF Non-Preemptive) ====\n")

patients = get_patient_input()
patients.sort(key=lambda x: x["name"].lower())

scheduled_patients = schedule_sjf_non_preemptive(patients)

display_table(scheduled_patients)
display_gantt_chart(scheduled_patients)
display_stairs(scheduled_patients)

avg_wt, avg_tt, idle_count = calculate_statistics(scheduled_patients)
display_final_report_table(scheduled_patients, avg_wt, avg_tt, idle_count)

print("\n✅ Scheduling Complete! Thank you. Stay Healthy! 💙")
