
def load_upcoming_movies(file_path = "Movies.txt"):
    moviesDict = {}
    try:
        with open(file_path) as f:
            next(f)
            for line in f:
                parts = line.strip().split(", ")
                # Use the movie title as the key, rest of data as value list
                moviesDict.update({parts[0]: parts[1:]})
    except FileNotFoundError:
        print("Error: Movies.txt file not found.")
    
    upcomingTitles = [title for title, data in moviesDict.items() if data[-1].lower() == "coming soon"]
        
    if len(upcomingTitles) > 0:
        header = "Upcoming"
        maxLengthTitle = max(len(header), max(len(title) for title in upcomingTitles))

        border = "+" + "-" * (maxLengthTitle + 2) + "+"
        print(border)
        print(f"| {header.ljust(maxLengthTitle)} |")
        print(border)
        for title in upcomingTitles:
            print(f"| {title.ljust(maxLengthTitle)} |")
        print(border)
    else:
        print("No further movies are currently scheduled.")

    return moviesDict, upcomingTitles

def technician_access():
    try:
        # Reads credentials from 'Technician_auth.txt'
        with open("Technician_auth.txt") as technicianCredentials:
            next(technicianCredentials)
            technicianData = {} # Transferring the data from 'Technician_auth.txt' to a dictionary
            for credential in technicianCredentials:
                parts = credential.strip().split(", ")
                if len(parts) == 2:
                    technicianData.update({parts[0]: parts[1]})
    except FileNotFoundError:
        print("Error: Technician_auth.txt file not found.")
    
    while True:
        print("\n1. Insert Username")
        print("2. Exit to Main Menu")
        choice = input("Choose an option (1-2): ")

        if choice == "1":
            # Prompt the user for login credentials
            username = input("\nInsert Your Username: ")
            if username in technicianData:
                password = input("Insert Your Password: ")
                if password == technicianData.get(username):
                    print("✅ Login Successful")
                    return username
                else:
                    print("❌ Password is incorrect.")
            else:
                print("Username does not exist.")
        elif choice == "2":
            # Go back to main menu
            return None
        else:
            print("Invalid choice. Please try again.")

def load_auditorium(file_path = "Auditoriums.txt"):
    audiDict = {}
    try:
        with open(file_path) as f:
            next(f)
            for line in f:
                parts = line.strip().split(", ")
                audiDict.update({parts[0]: parts[1:]})
    except FileNotFoundError:
        print("Error: Auditoriums.txt file not found.")

    if audiDict:
        header = "Currently Operating"
        maxLengthAudi = max(len(header), max(len(auditorium) for auditorium in audiDict))

        border = "+" + "-" * (maxLengthAudi + 2) + "+"
        print(border)
        print(f"| {header.ljust(maxLengthAudi)} |")
        print(border)
        for auditorium in audiDict:
            print(f"| {auditorium.ljust(maxLengthAudi)} |")
        print(border)
    else:
        print("No auditoriums currently operating.")
    
    return audiDict

def identify_next_issueID(file_path = "Issue_report.txt"):
    lastID = 0
    try:
        with open(file_path) as f:
            next(f)
            for line in f:
                if line.strip():
                    issueID = line.split(", ")[0].strip()
                    num = int(issueID[2:])
                    if num > lastID:
                        lastID = num
    except FileNotFoundError:
        print("Error: Issue_report.txt file not found.")
    return f"IS{lastID + 1}"

# --- View Upcoming Movie Schdules ---
def view_upcoming_screenings():
    print("\n--- Upcoming Screenings ---\n")

    try:
        with open("Movies.txt") as f:
            next(f)
            upcomingMovies = []
            for line in f:
                parts = line.strip().split(", ")
                if parts[-1].lower() == "coming soon":
                    upcomingMovies.append(parts[0])
    except FileNotFoundError:
        print("Error: Movies.txt file not found.")
    if not upcomingMovies:
        print("⚠️  No movie data found.")
    
    showTimeFlag = 0
    try:
        with open("Showtimes.txt") as f:
            next(f)
            for line in f:
                parts = line.strip(). split(", ")
                if parts[1] in upcomingMovies:
                    print(f"Movie: {parts[1]} | Auditorium: {parts[2]} | Date: {parts[3]} | Time: {parts[4]}")
                    showTimeFlag = 1
            print("File loaded successfully.")
    except FileNotFoundError:
        print("Error: Showtimes.txt file not found.")
    if showTimeFlag == 0:
        print("⚠️  No movie data found.")

# --- View Status of Auditorium Equipments ---
def view_equipment_status():
    print("\n--- Equipment Status ---\n")

    try:
        with open("Auditoriums.txt") as f:
            next(f)
            for line in f:
                parts = line.strip().split(", ")
                print(f"Auditorium: {parts[0]} | Projector: {parts[1]} | Sound: {parts[2]} | AC: {parts[3]} | Status: {parts[4]}")
            print("File loaded successfully.")
    except FileNotFoundError:
        print("Error: Auditoriums.txt file not found.")
                
# --- Modify/Report Issues ---
def modify_issue():
    
    while True:
        print("\n--- Report Technical Issue ---\n")

        print("Select an option to continue: \n")
        print("1. Report New Issue")
        print("2. Update Issue Status")
        print("3. Go Back to Technician Menu")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            while True:
                audiData = load_auditorium()
                audiChoice = input("Select an auditorium (e.g. 'Audi 1') or type 'back' to return: ").strip()
                if audiChoice.lower() == "back":
                    print()
                    break
                if audiChoice in audiData:
                    while True:
                        print(f"Select the faulty equipment in {audiChoice}: \n")
                        print("1. Projector")
                        print("2. Sound System")
                        print("3. Air Conditioner")

                        faultyChoice = input("\nEnter your choice (1-3): ").strip()

                        if faultyChoice == "1":
                            issueType = "Projector"
                            audiData[audiChoice][0] = "FAULT"
                        elif faultyChoice == "2":
                            issueType = "Sound"
                            audiData[audiChoice][1] = "FAULT"
                        elif faultyChoice == "3":
                            issueType = "AC"
                            audiData[audiChoice][2] = "FAULT"
                        else:
                            print("Invalid choice. Please try again.")
                            continue

                        issueDescription = input("Enter description of the issue: ").strip().capitalize()

                        if not issueDescription:
                            print("Description cannot be empty. Try again.")
                            continue

                        # Issue Report File
                        issueId = identify_next_issueID("Issue_report.txt")
                        issueData = [
                            issueId,
                            audiChoice,
                            issueType,
                            issueDescription,
                            "Under Maintenance"
                        ]

                        with open("Issue_report.txt", "a") as f:
                            f.write("\n" + ", ".join(issueData))

                        # Auditoriums File
                        audiData[audiChoice][-2] = "Not Ready"

                        with open("Auditoriums.txt", "w") as f: # Save updated Auditorium file
                            f.write("AuditoriumID, Projector, Sound, AC, Status, Seats\n")
                            audiItems = list(audiData.items())
                            for i, (audiID, audiDetails) in enumerate(audiItems):
                                line = f"{audiID}, {audiDetails[0]}, {audiDetails[1]}, {audiDetails[2]}, {audiDetails[3]}, {audiDetails[4]}"
                                if i < len(audiItems) - 1:
                                    f.write(line + "\n")
                                else:
                                    f.write(line)
                        
                        input("Issue Saved...")
                        return modify_issue()
                
                else:
                    print("Auditorium not found. Please check and try again.")
                    print()

        elif choice == "2":
            while True:
                # Importing Issue_report.txt to a dictionary 'issueReportData'
                try:
                    with open("Issue_report.txt") as f:
                        next(f)
                        reportIssueData = {}
                        lines = f.readlines()
                        if len(lines) == 0:
                            print("No issues have been reported yet.")
                        else:
                            for line in lines:
                                parts = line.strip().split(", ")
                                reportIssueData.update({parts[0]: parts[1:]})
                except FileNotFoundError:
                    print("Error: Issue_report.txt file not found.")
                    break
                
                try:
                    with open("Auditoriums.txt") as f:
                        next(f)
                        audiData = {}
                        lines = f.readlines()
                        if len(lines) == 0:
                            print("Auditorium Data Not Found.")
                        else:
                            for line in lines:
                                parts = line.strip().split(", ")
                                audiData.update({parts[0]: parts[1:]})
                except FileNotFoundError:
                    print("Error: Auditoriums.txt file not found.")
                    break
    
                reportIssueID = input("\nEnter your Issue ID to resolve (e.g., 'IS1') or type 'back' to return: ").strip()
                if reportIssueID.lower() == "back":
                    print()
                    break

                if reportIssueID in reportIssueData:
                    if reportIssueData[reportIssueID][-1].lower() == "resolved":
                        print(f"⚠️  Issue ID {reportIssueID} has already been resolved.")
                        continue

                    while True:
                        resolveChoice = input(f"Are you sure you want to mark Issue: {reportIssueID} as resolved? (Y/N): ").strip().lower()

                        if resolveChoice == "y":
                            # Change the status of the issue to 'Resolved'
                            reportIssueData[reportIssueID][-1] = "Resolved" 
                            
                            # Change the status of the spesific Auditorium equipment to 'OK'
                            specAudiID = reportIssueData[reportIssueID][0]
                            issueType = reportIssueData[reportIssueID][1]
                            if issueType == "Projector":
                                equipmentNNum = 0
                            elif issueType == "Sound":
                                equipmentNNum = 1
                            elif issueType == "AC":
                                equipmentNNum = 2
                            audiData[specAudiID][equipmentNNum] = "OK"

                            # Check if all equipment are 'OK', if yes then the status of the auditorium is "Ready"
                            if audiData[specAudiID][0] == "OK" and audiData[specAudiID][1] == "OK" and audiData[specAudiID][2] == "OK":
                                audiData[specAudiID][3] = "Ready"
                                                   
                            with open("Issue_report.txt", "w") as f: # Save updated Issue file
                                f.write("IssueID, AuditoriumID, IssueType, Description, Status\n")
                                issueItems = list(reportIssueData.items())
                                for i, (issueID, issueDetails) in enumerate(issueItems):
                                    line = f"{issueID}, {issueDetails[0]}, {issueDetails[1]}, {issueDetails[2]}, {issueDetails[3]}"
                                    if i < len(issueItems) - 1:
                                        f.write(line + "\n")
                                    else:
                                        f.write(line)

                            with open("Auditoriums.txt", "w") as f: # Save updated Auditorium file
                                f.write("AuditoriumID, Projector, Sound, AC, Status, Seats\n")
                                audiItems = list(audiData.items())
                                for i, (audiID, audiDetails) in enumerate(audiItems):
                                    line = f"{audiID}, {audiDetails[0]}, {audiDetails[1]}, {audiDetails[2]}, {audiDetails[3]}, {audiDetails[4]}"
                                    if i < len(audiItems) - 1:
                                        f.write(line + "\n")
                                    else:
                                        f.write(line)
                            
                            print(f"\nIssue ID: {reportIssueID} successfully resolved.")
                            input("Press ENTER to continue...")
                            print()
                            return modify_issue()

                        elif resolveChoice == "n":
                            print("Action cancelled. Issue not updated.")
                            return modify_issue()
                        else:
                            print("Invalid input. Please enter 'Y' or 'N'.")
                
                else:
                    print("Issue ID not found. Please check and try again.")

        elif choice == "3":
            return
        else: 
            print("Invalid choice. Please 1, 2, or 3.\n")

# --- View Ongoing Issues ---
def view_issues():
    print("\n--- Technical Issues ---\n")

    try:
        with open("Issue_report.txt") as f:
            next(f)
            lines = f.readlines()
            if len(lines) == 0:
                print("No issues have been reported yet.")
            else:
                for line in lines:
                    parts = line.strip().split(", ")
                    if parts[4] == "Under Maintenance":
                        print(f"IssueID: {parts[0]} | Auditorium: {parts[1]} | Issue: {parts[2]} | Description: {parts[3]} | Status: {parts[4]}")
                print("File loaded successfully.")
    except FileNotFoundError:
        print("Error: Issue_report.txt file not found.")


# --- TECHNICIAN MENU ---
def technician_menu():
    print("====================================")
    print("    CINEMA TICKET BOOKING SYSTEM    ")
    print("            Technician              ")
    print("====================================")

    # Login Access for Technician
    technicianUsername = technician_access()
    if technicianUsername is None:
        return None

    while True:
        print("\n=== Technician Menu ===")
        print("1. View Upcoming Screenings")
        print("2. View Equipment Status")
        print("3. Report/Modify Issue")
        print("4. View Technical Issues")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            view_upcoming_screenings()
        elif choice == "2":
            view_equipment_status()
        elif choice == "3":
            modify_issue()
        elif choice == "4":
            view_issues()
        elif choice == "5":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please try again.")
