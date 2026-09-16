#----------------------------------- CLERK MENU -----------------------------------
def clerk_access():
    try:
        # Reads credentials from 'Clerk_auth.txt'
        with open("Clerk_auth.txt") as clerkCredentials:
            next(clerkCredentials)
            clerkData = {} # Transferring the data from 'Clerk_auth.txt' to a dictionary
            for credential in clerkCredentials:
                parts = credential.strip().split(", ")
                if len(parts) == 2:
                    clerkData.update({parts[0]: parts[1]})
    except FileNotFoundError:
        print("Error: Clerk_auth.txt file not found.")
    
    while True:
        print("\n1. Insert Username")
        print("2. Exit to Main Menu")
        choice = input("Choose an option (1-2): ")

        if choice == "1":
            # Prompt the user for login credentials
            username = input("\nInsert Your Username: ")
            if username in clerkData:
                password = input("Insert Your Password: ")
                if password == clerkData.get(username):
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

def load_showtime_data(movieChoice, file_path = "Showtimes.txt"):
    showTimeData = {}
    movieDates = []

    try:
        with open(file_path) as showTimes:
            next(showTimes)

            for showTime in showTimes:
                # Split line into parts: [showID, title, auditoriumID, date, time]
                parts = showTime.strip().split(", ")

                # Only process if the line matches the selected movie
                if parts[1] == movieChoice:
                    showTimeData[parts[0]] = parts[1:]

                    # Add date if it’s not already in the list
                    if parts[3] not in movieDates:
                        movieDates.append(parts[3])

    except FileNotFoundError:
        print("Error: Showtimes.txt not found.")

    return showTimeData, movieDates

def sort_movie_dates(dates):
    monthMap = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
                "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
                "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    def sort_key(date):
        parts = date.split(" - ")[1].split()
        day = int(parts[0])
        month = monthMap[parts[1]]
        return (month, day)
    dates.sort(key=sort_key)

def sort_movie_times(times):
   
    def sort_key(time):
        parts = time.split()
        clockPart = parts[0]
        period = parts[1]


        timePart = clockPart.split(":")
        hour = int(timePart[0])
        minute = int(timePart[1])

        if period == "PM" and hour != 12:  # 1 PM -> 13, 2 PM -> 14
            hour += 12
        if period == "AM" and hour == 12:  # 12 AM -> 00
            hour = 0

        return (hour, minute)
    times.sort(key=sort_key)

def load_current_movies(file_path = "Movies.txt"):
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
    
    nowShowingTitles = [title for title, data in moviesDict.items() if data[-1].lower() == "now showing"]
    
    if len(nowShowingTitles) > 0:
        header = "Currently Showing"
        maxLengthTitle = max(len(header), max(len(title) for title in nowShowingTitles))

        border = "+" + "-" * (maxLengthTitle + 2) + "+"
        print(border)
        print(f"| {header.ljust(maxLengthTitle)} |")
        print(border)
        for title in nowShowingTitles:
            print(f"| {title.ljust(maxLengthTitle)} |")
        print(border)
    else:
        print("No movies are currently showing.")

    return moviesDict, nowShowingTitles

def identify_next_bookingID(file_path = "Bookings.txt"):
    lastID = 0
    try:
        with open(file_path) as f:
            next(f)
            for line in f:
                if line.strip():
                    bookingID = line.split(", ")[0].strip()
                    num = int(bookingID[1:])
                    if num > lastID:
                        lastID = num
    except FileNotFoundError:
        print("Error: Bookings.txt file not found.")
    return f"B{lastID + 1}"

def identify_next_paymentID(file_path = "Payments.txt"):
    lastID = 0
    try:
        with open(file_path) as f:
            next(f)
            for line in f:
                if line.strip():
                    paymentID = line.split(", ")[0].strip()
                    num = int(paymentID[1:])
                    if num > lastID:
                        lastID = num
    except FileNotFoundError:
        print("Error: Payments.txt file not found.")
    return f"P{lastID + 1}"

def load_auditoriums_seatings(showID, auditoriumID, audi_file_path = "Auditoriums.txt", seats_file_path = "Reserved_seats.txt"):
    auditoriums = {}

    with open(audi_file_path) as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split(", ")  # Split only into ID and Seats
            if parts[0] == auditoriumID:
                AudiID = parts[0]
                seatsRaw = parts[5]
                break

        # Split rows by ";" and seats by space
        seatGrid = [row.strip().split() for row in seatsRaw.split(";")]

        auditoriums[AudiID] = seatGrid

        for seatRow in seatGrid:
            for i in range(len(seatRow)):
                seatRow[i] = 0 # Seating Detail -> 0 = available, 1 = selected, 2 = reserved 
        
        seatMap = {
            "A": 0, "B": 1, "C": 2, "D": 3,
            "E": 4, "F": 5, "G": 6, "H": 7,
            }

        flag = 0
        
        with open(seats_file_path) as reservedSeats:
            next(reservedSeats)
            for reservedSeat in reservedSeats:
                if reservedSeat.split(", ")[0] == showID:
                    flag = 1
                    parts = reservedSeat.split(", ")[1].split()
                    for part in parts:
                        rowNum = seatMap[part[0]]
                        colNum = int(part[1:]) - 1
                        seatGrid[rowNum][colNum] = 2
                    break
                

    return (flag, seatGrid, seatMap)

def render_seats(movieTitle, movieDate, movieTime, movieGenre, movieDuration, movieRating, movieAudi, moviePrice, seats):
    # Show the movie description from the showtime selected
    print("\n─────────────────────────────")
    print("🎬 You Selected:")
    print(f"Movie   : {movieTitle}")
    print(f"Date    : {movieDate}")
    print(f"Time    : {movieTime}")
    print("─────────────────────────────")
    print(f"Genre: {movieGenre}, Duration: {movieDuration}, Rating: {movieRating}, Auditorium: {movieAudi}")
    print(f"Price: {moviePrice}\n")
    
    #Show the seating from the showtime selected
    symbols = {0: "[ ]", 1: "[O]", 2: "[X]"}  
    row_labels = "ABCDEFGH"
                                
    maxSeatCount = max(len(seatRow) for seatRow in seats)
    seatWidth = 4   # "[ ]" + space
    maxScreenWidth = maxSeatCount * seatWidth
    print(("/" + "-" * (maxScreenWidth - 4) + "\\").center(maxScreenWidth))
    print(f"/{'SCREEN'.center(maxScreenWidth-2)}\\")
    print()


    for index, seatRow in enumerate(seats):
        line = row_labels[index] + " " + " ".join(symbols[seat] for seat in seatRow)
        print(line)

def display_booking_summary(payment_id, booking_id, username, status, movie, auditorium, date, time, seats, price_each):
    # Calculate tickets and total price
    tickets = len(seats)
    total_price = tickets * price_each

    # Convert seats list to string
    seats_str = ", ".join(seats)

    lines = [
        f"Payment ID : {payment_id}",
        f"Title: {movie}",
        f"Booking ID : {booking_id}    Status: {status}",
        f"Username   : {username}",
        f"Date : {date}   Time : {time}",
        f"Auditorium : {auditorium}",
        f"Seats : {seats_str}",
        f"Price per seat : RM{price_each:.2f}",
        f"🎟️  Tickets : {tickets}     💵 Total : RM{total_price:.2f}"
    ]

    # Find max width
    max_width = max(len(line) for line in lines)

    # Function to pad each line to same width
    def pad(line):
        return f"| {line.ljust(max_width)} |"

    border = "+" + "-" * (max_width + 2) + "+"
    print(border)
    for line in lines:
        print(pad(line))
        if "Title:" in line or "Username" in line or "Seats" in line:
            print("|" + "-" * (max_width + 2) + "|")
    print(border)

def generate_receipt(payment_id, payment_date, payment_method, booking_id, username, status,
                  movie, auditorium, date, time, seats, price_each, final_price, width = 35):
    
    tickets = len(seats)
    total_price = final_price
    seats_str = ", ".join(seats)

    border = "*" * width
    print(" DSC ".center(width, "*"))

    receipt = [
        f"Payment ID   : {payment_id}",
        f"Payment Date : {payment_date}",
        f"Method       : {payment_method}",
        
        f"\nBooking ID   : {booking_id}",
        f"User         : {username}",
        f"Status       : {status}",

        f"\nMovie        : {movie}",
        f"Audi         : {auditorium}",
        f"Date         : {date}",
        f"Time         : {time}",

        f"\nSeats        : {seats_str}",
        f"Price Each   : RM {price_each:.2f}",
        f"Tickets      : {tickets}",
        f"Total        : RM {total_price:.2f}"
    ]
    for line in receipt:
        print(line)
    print(border)
    print("Enjoy your movie! 🎥 ".center(width))
    print(border)

def select_seats(seats, seatMap, seatQuantity):
    seatsSelected = []
    cnt = 1

    while cnt <= seatQuantity:
        seatChoice = input(f"Seat {cnt}: ").strip().upper()

        # Validate seat format
        if len(seatChoice) < 2 or seatChoice[0] not in seatMap or not seatChoice[1:].isdigit():
            print("Invalid format. Use format like A1, B4, etc.\n")
            continue

        rowNum = seatMap[seatChoice[0]]
        colNum = int(seatChoice[1:]) - 1

        # Validate seat range
        if colNum < 0 or colNum >= len(seats[rowNum]):
            print(f"Invalid seat number. Row {seatChoice[0]} only has {len(seats[rowNum])} seats.\n")
            continue

        # Check seat availability
        if seats[rowNum][colNum] == 2:
            print("That seat is already booked. Choose another.\n")
        elif seats[rowNum][colNum] == 1:
            print("That seat is already selected. Choose another.\n")
        elif seats[rowNum][colNum] == 0:
            seats[rowNum][colNum] = 1
            seatsSelected.append(seatChoice)
            cnt += 1
        else:
            print("Invalid seat. Please select again.")

    return seats, seatsSelected

def clerk_process_payment(username, showTitle, showId, seatsSelected, auditoriumId, showDate, showTime, priceInfo, seatFlag):
    
    # Handles payment and booking confirmation process for a selected movie show.

    while True:
        print("\nHow would you like to Pay?\n")
        print("1. Cash")
        print("2. Debit Card")
        print("3. Credit Card")
        print("4. e-Wallet")

        paymentChoice = input("\nEnter your choice (1-4): ").strip()

        if paymentChoice == "1":
            paymentMethod = "Cash"
        elif paymentChoice == "2":
            paymentMethod = "Debit Card"
        elif paymentChoice == "3":
            paymentMethod = "Credit Card"
        elif paymentChoice == "4":
            paymentMethod = "e-Wallet"
        else:
            print("Invalid choice. Please try again.")
            continue

        print(f"\nSelected payment method: {paymentMethod}")
        input("Waiting for Payment... Press ENTER once payment is completed.\n")

        while True:
            paymentDate = input("Enter the date of payment (DD/MM/YYYY, e.g., 20/09/2025): ").strip()

            # Check overall format (should have 2 slashes)
            if paymentDate.count("/") != 2:
                print("Invalid format. Please use DD/MM/YYYY.\n")
                continue
            
            day, month, year = paymentDate.split("/")

            # Check if all parts are digits and have correct lengths
            if not (day.isdigit() and month.isdigit() and year.isdigit()):
                print("Date must contain only numbers. Please try again.\n")
                continue
            if len(day) != 2 or len(month) != 2 or len(year) != 4:
                print("Invalid format. Please use DD/MM/YYYY.\n")
                continue
            
            day, month, year = int(day), int(month), int(year)
            if not (1 <= month <= 12):
                print("Month must be between 01 and 12.\n")
                continue
            monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if not (1 <= day <= monthDays[month - 1]):
                print(f"Day must be between 01 and {monthDays[month - 1]} for month {month:02d}.\n")
                continue

            break
        print()

        # --- Booking File ---
        bookingId = identify_next_bookingID("Bookings.txt")
        bookingData = [
            bookingId,
            username,
            showId,
            " ".join(seatsSelected),
            "Confirmed"
        ]

        with open("Bookings.txt", "a") as file:
            file.write("\n" + ", ".join(bookingData))

        # --- Payment File ---
        ticketCount = len(seatsSelected)
        priceEach = float(priceInfo[2:])  # removes "RM"
        totalPrice = ticketCount * priceEach

        paymentId = identify_next_paymentID("Payments.txt")
        paymentData = [
            paymentId,
            bookingId,
            f"RM{totalPrice:.2f}",
            paymentMethod,
            paymentDate,
            "Completed"
        ]

        with open("Payments.txt", "a") as file:
            file.write("\n" + ", ".join(paymentData))

        # --- Reserved Seats File ---
        if seatFlag == 0:
            # First booking for this show
            with open("Reserved_seats.txt", "a") as file:
                file.write(f"\n{showId}, {' '.join(seatsSelected)}")

        elif seatFlag == 1:
            # Update existing reserved seats
            with open("Reserved_seats.txt", "r") as file:
                lines = file.readlines()
            seatData = {}
            for line in lines[1:]:  # skip header
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    show, seats = parts
                    seatData.update({show: seats.split(" ")})
            # Append new seats
            seatData[showId].extend(seatsSelected)

            # Rewrite file
            with open("Reserved_seats.txt", "w") as file:
                file.write("ShowID, Reserved Seats\n")
                seatItems = list(seatData.items())
                for i, (show, seats) in enumerate(seatItems):
                    line = f"{show}, {' '.join(seats)}"
                    if i < len(seatItems) - 1:
                        file.write(line + "\n")
                    else:
                        file.write(line)

        # --- Generate Receipt ---
        while True:
            receiptChoice = input("Booking successful! Print receipt? (Y/N): ").strip().lower()
            if receiptChoice == "y":
                print()
                generate_receipt(
                    payment_id=paymentId,
                    payment_date=paymentDate,
                    payment_method=paymentMethod,
                    booking_id=bookingId,
                    username=username,
                    status="CONFIRMED",
                    movie=showTitle,
                    auditorium=auditoriumId,
                    date=showDate,
                    time=showTime,
                    seats=seatsSelected,
                    price_each=priceEach,
                    final_price=totalPrice
                )
                input("Receipt printed successfully. Enjoy your movie! (Press ENTER to continue) ")
                break
            elif receiptChoice == "n":
                print("No receipt will be printed. Redirecting to booking menu...")
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
        break

def cancel_booking(bookingData):
    
    while True:
        userBookingID = input("\nEnter your Booking ID to cancel (e.g., 'B1') or type 'back' to return: ").strip()
        if userBookingID.lower() == "back":
            print()
            break

        if userBookingID not in bookingData:
            print("Booking ID not found. Please check and try again.")
            continue

        specShowID = bookingData[userBookingID][1]
        seatsChosen = bookingData[userBookingID][2].split()

        # Check if booking already cancelled
        if bookingData[userBookingID][-1].lower() == "cancelled":
            print(f"⚠️  Booking ID {userBookingID} has already been cancelled.")
            continue

        # Retrieve Reserved Seat Info
        try:
            with open("Reserved_seats.txt") as reservedSeats:
                next(reservedSeats)  # Skip header
                reservedSeatData = {}
                for reservedSeat in reservedSeats:
                    parts = reservedSeat.strip().split(", ")
                    reservedSeatData[parts[0]] = parts[1]
        except FileNotFoundError:
            print("Error: Reserved_seats.txt file not found.")
            break

        reservedSeatsList = reservedSeatData[specShowID].split()

        # Confirm Cancellation 
        while True:
            print(f"\nYou are about to cancel Booking ID: {userBookingID}.")
            print(f"Reserved seats: {' '.join(seatsChosen)}")
            cancelBooking = input("Are you sure you want to cancel this booking? (Y/N): ").strip().lower()

            if cancelBooking == "y":
                # Remove seats from reserved list
                for seat in seatsChosen:
                    if seat in reservedSeatsList:
                        reservedSeatsList.remove(seat)

                # Update booking status
                bookingData[userBookingID][3] = "Cancelled"

                # Save updated Bookings.txt 
                with open("Bookings.txt", "w") as bookings:
                    bookings.write("BookingID, Username, ShowID, Seats, Status\n")
                    bookingItems = list(bookingData.items())
                    for i, (bookingID, bookingDetails) in enumerate(bookingItems):
                        line = f"{bookingID}, {bookingDetails[0]}, {bookingDetails[1]}, {bookingDetails[2]}, {bookingDetails[3]}"
                        if i < len(bookingItems) - 1:
                            bookings.write(line + "\n")
                        else:
                            bookings.write(line)

                # Save updated Reserved_seats.txt 
                reservedSeatData[specShowID] = ' '.join(reservedSeatsList)
                with open("Reserved_seats.txt", "w") as reservedSeats:
                    reservedSeats.write("ShowID, Reserved Seats\n")
                    reservedSeatsItems = list(reservedSeatData.items())
                    for i, (showID, seats) in enumerate(reservedSeatsItems):
                        if not seats:  # Skip shows with no reserved seats
                            continue
                        line = f"{showID}, {seats}"
                        if i < len(reservedSeatsItems) - 1:
                            reservedSeats.write(line + "\n")
                        else:
                            reservedSeats.write(line)

                print(f"\nBooking ID {userBookingID} successfully cancelled.")
                input("Press ENTER to continue...")
                print()
                return  # Exit confirmation loop

            elif cancelBooking == "n":
                print("Cancellation aborted.\n")
                break

            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

# --- Book Tickets ---
def book_tickets(role = "Clerk", defaultUsername = "Walk-in Customer"):
    
    while True:
        print("\n--- Book Tickets ---\n")

        movieDatas, *_ = load_current_movies() # Display all 'Now Showing' Movies
        if not movieDatas:
            print("⚠️  No movie data found.")
            break
        print("\nSelect an option to continue: ")
        print("1. Book a Ticket")
        print("2. Go Back to Clerk Menu")
        choice = input("\nEnter your choice (1-2): ")
        if choice == "1":
            while True:
                print()
                load_current_movies()
                movieChoice = input("Enter the movie title to book (match spelling exactly): ").strip()
                if movieChoice in movieDatas and movieDatas[movieChoice][-1].lower() == "now showing":
                    showTimeDatas, movieDates = load_showtime_data(movieChoice)
                    if not showTimeDatas:
                        print("⚠️  No showtime data found.")
                        return
                    sort_movie_dates(movieDates)
                    genre, duration, rating, price, *_ = movieDatas[movieChoice]
                    audiID = showTimeDatas[next(iter(showTimeDatas))][1]

                    while True:
                        print(f"\n[ {movieChoice} ]")
                        print(" | ".join(movieDates))
                        print(f"\nGenre: {genre}")
                        print(f"Duration: {duration}")
                        print(f"Rating: {rating}")
                        print(f"Auditorium: {audiID}")
                        print(f"Price: {price}\n")
    
                        dateChoice = input("Enter your preferred date (e.g. 'Wed - 15 Oct'): ").strip()
                        if dateChoice in movieDates:
                            dateTimes = []
                            for showID, data in showTimeDatas.items():
                                if data[-2] == dateChoice:
                                    dateTimes.append(data[-1])
                            sort_movie_times(dateTimes)

                            while True:
                                print(f"\nShowtimes on {dateChoice}:")
                                for time in dateTimes:
                                    print(f"[ {time} ]", end = " ")
                                timeChoice = input("\n\nSelect a time slot (e.g. '1:00 PM'): ").strip()
                                if timeChoice in dateTimes:
                                    for showID, showDesciptions in showTimeDatas.items():
                                        if movieChoice in showDesciptions and dateChoice in showDesciptions and timeChoice in showDesciptions:
                                            specShowID = showID
                                            break

                                    while True:
                                        reservedSeatFlag, audiSeats, seatMap = load_auditoriums_seatings(showID = specShowID, auditoriumID = audiID)
                                        
                                        # Display Current Layout
                                        render_seats(movieTitle = movieChoice, movieDate = dateChoice, movieTime = timeChoice, 
                                                     movieGenre = genre, movieDuration = duration, movieRating = rating, 
                                                     movieAudi = audiID, moviePrice = price, seats = audiSeats)

                                        seatCnt = sum(seat == 0 for row in audiSeats for seat in row)
                                        if seatCnt == 0:
                                                print("No seats left. Please choose another showtime.")
                                                return book_tickets()
                                        try:
                                            seatQty = int(input(("\nInsert the number of seats you want to book: ")))
                                        except ValueError:
                                            print("Invalid Input. Please key in an integer...")
                                            continue
                                        if seatQty <= 0:
                                            print("Please enter a number greater than 0.")
                                            continue
                                        if seatQty <= seatCnt:
                                            print()
                                            # Select seats with the select_seats() function
                                            audiSeats, seatsChosen = select_seats(seats = audiSeats, seatMap = seatMap, seatQuantity = seatQty) 
                                            print()
                                            render_seats(movieTitle = movieChoice, movieDate = dateChoice, movieTime = timeChoice, 
                                                 movieGenre = genre, movieDuration = duration, movieRating = rating, 
                                                 movieAudi = audiID, moviePrice = price, seats = audiSeats)
                                            print("\nHere are all the seats selected, please choose the following to continue:")
                                            while True:
                                                print("\n1. Book Now")
                                                print("2. Change Seatings")
                                                print("3. Cancel Booking")
    
                                                choice = input("\nEnter your choice (1-3): ")
    
                                                if choice == "1":
                                                    print("\nBooking Summary")

                                                    display_booking_summary(
                                                        payment_id = identify_next_paymentID("Payments.txt"),
                                                        booking_id = identify_next_bookingID("Bookings.txt"),
                                                        username = defaultUsername,
                                                        status = "Pending",
                                                        movie = movieChoice,
                                                        auditorium = audiID,
                                                        date = dateChoice,
                                                        time = timeChoice,
                                                        seats = seatsChosen,
                                                        price_each = float(price[2:])
                                                    )
                                                    if role == "Clerk":
                                                        clerk_process_payment(
                                                            username = defaultUsername,
                                                            showTitle = movieChoice,
                                                            showId = specShowID,
                                                            seatsSelected = seatsChosen,
                                                            auditoriumId = audiID,
                                                            showDate = dateChoice,
                                                            showTime = timeChoice,
                                                            priceInfo = price,
                                                            seatFlag = reservedSeatFlag,
                                                        )
                                                    else:
                                                        customer_process_payment(
                                                            username = defaultUsername,
                                                            showTitle = movieChoice,
                                                            showId = specShowID,
                                                            seatsSelected = seatsChosen,
                                                            auditoriumId = audiID,
                                                            showDate = dateChoice,
                                                            showTime = timeChoice,
                                                            priceInfo = price,
                                                            seatFlag = reservedSeatFlag,
                                                        )
                                                    return book_tickets()
    
                                                elif choice == "2":
                                                    break
                                                elif choice == "3":
                                                    print("The booking process has been stopped. Returning to booking menu.")
                                                    return book_tickets()
                                                else:
                                                    print("Invalid choice. Please try again.")
    
                                        else: 
                                            print(f"Sorry there are {seatCnt} seats left")
                                            print("Please select again.")

                                elif timeChoice.lower() in [time.lower() for time in dateTimes]:
                                    print("The time exists but the formatting/capitalization is incorrect.")
                                    print("Please type it exactly as shown, e.g. '1:00 PM'.")
                                else:
                                    print("Invalid showtime. The time you entered is not available.")
    
                        elif dateChoice.lower() in [date.lower() for date in movieDates]:
                            print("The date exists but formatting/capitalization is incorrect.")
                            print("Please type it exactly as shown, e.g. 'Wed - 15 Oct'.")
                        else:
                            print("Invalid date. The date you entered is not available.")
    
                else:
                    print("Booking unavailable for the movie you entered.")
                    if movieChoice in movieDatas and movieDatas[movieChoice][-1].lower() == "comming soon":
                        print("This movie cannot be booked at the moment.")
                    else:
                        print("Kindly verify the title and re-enter it.")

        elif choice == "2":
            return
        else:
            print("Invalid choice. Please try again.\n")

# --- View Seating ---
def view_seating_availability():

    while True:
        print("\n--- View Seats & Showtimes ---\n")

        movieDatas, *_ = load_current_movies()
        if not movieDatas:
            print("⚠️  No movie data found.")
            break
        movieChoice = input("Enter the movie title you want to view (match spelling exactly) or type 'back' to return: ").strip()
        if movieChoice.lower() == "back":
            print()
            break
        if movieChoice in movieDatas and movieDatas[movieChoice][-1].lower() == "now showing":
            showTimeDatas, movieDates = load_showtime_data(movieChoice)
            if not showTimeDatas:
                print("⚠️  No showtime data found.")
                break

            sort_movie_dates(movieDates)
            genre, duration, rating, price, *_ = movieDatas[movieChoice]
            audiID = showTimeDatas[next(iter(showTimeDatas))][1]

            while True:
                print(f"\n[ {movieChoice} ]")
                print(" | ".join(movieDates))
                print(f"\nGenre: {genre}")
                print(f"Duration: {duration}")
                print(f"Rating: {rating}")
                print(f"Auditorium: {audiID}")
                print(f"Price: {price}\n")
    
                dateChoice = input("Select a date (e.g. 'Wed - 15 Oct'): ").strip()
                if dateChoice in movieDates:
                    dateTimes = []
                    for showID, data in showTimeDatas.items():
                        if data[-2] == dateChoice:
                            dateTimes.append(data[-1])
                    sort_movie_times(dateTimes)

                    while True:
                        print(f"\nShowtimes on {dateChoice}:")
                        for time in dateTimes:
                            print(f"[ {time} ]", end = " ")
                        timeChoice = input("\n\nSelect a time (e.g. '1:00 PM'): ").strip()
                        if timeChoice in dateTimes:
                            for showID, showDesciptions in showTimeDatas.items():
                                if movieChoice in showDesciptions and dateChoice in showDesciptions and timeChoice in showDesciptions:
                                    specShowID = showID
                                    break
                            audiSeats= load_auditoriums_seatings(showID = specShowID, auditoriumID = audiID)[1] # Only use the second return value of the function which will be the seating layout

                            render_seats(movieTitle = movieChoice, movieDate = dateChoice, movieTime = timeChoice, 
                                             movieGenre = genre, movieDuration = duration, movieRating = rating, 
                                             movieAudi = audiID, moviePrice = price, seats = audiSeats)
                            while True:
                                print("\nSelect an option to continue: \n")
                                print("1. View Another Showtime")
                                print("2. Go Back to Clerk Menu")
                                choice = input("\nEnter your choice (1-2): ")
                                if choice == "1":
                                    return view_seating_availability()
                                elif choice == "2":
                                    return
                                else:
                                    print("Invalid choice. Please try again.")

                        elif timeChoice.lower() in [time.lower() for time in dateTimes]:
                            print("The time exists but the formatting/capitalization is incorrect.")
                            print("Please type it exactly as shown, e.g. '1:00 PM'.")
                        else:
                            print("Invalid showtime. The time you entered is not available.")

                elif dateChoice.lower() in [date.lower() for date in movieDates]:
                    print("The date exists but formatting/capitalization is incorrect.")
                    print("Please type it exactly as shown, e.g. 'Wed - 15 Oct'.")
                else:
                    print("Invalid date. The date you entered is not available.")

        else:
            print("Invalid movie title or not currently showing. Please try again.")

# --- Modify/Cancel Booking ---
def modify_booking():

    while True:
        print("\n--- Cancel/Modify Booking ---\n")

        print("Select an option to continue: \n")
        print("1. Modify Existing Booking")
        print("2. Cancel Booking")
        print("3. Go Back to Clerk Menu")

        print("\nNote:")
        print("- Customers may only modify the SEATS of an existing booking.")
        print("- Number of seats, movie, date, or time cannot be changed.")
        print("- Cancellations are final and non-refundable.")
        choice = input("\nEnter your choice (1-3): ").strip()

        try:
            # Reads bookings from 'Bookings.txt'
            with open("Bookings.txt") as bookings:
                next(bookings)
                bookingData = {} # Transferring the data from 'Bookings.txt' to a dictionary
                for booking in bookings:
                    parts = booking.strip().split(", ")
                    bookingData.update({parts[0]: parts[1:]}) # -> BookingID: Username, ShowID, Seats, Status
        except FileNotFoundError:
            print("Error: Bookings.txt file not found.")
            continue
        
        if not bookingData:
            print("⚠️  No booking data found.")
            break

        if choice == "1":
            while True:
                userBookingID = input("\nEnter your Booking ID (e.g. 'B1') or type 'back' to return: ").strip()
                if userBookingID.lower() == "back":
                    print()
                    break

                if userBookingID in bookingData:

                    if bookingData[userBookingID][-1].lower() == "cancelled":
                        print(f"⚠️  Booking ID {userBookingID} has already been cancelled. No Modification Allowed")
                        continue

                    # Select the seats previously chosen from the Booking ID
                    seatsChosen = bookingData[userBookingID][2].split()

                    # Retrieve Showtime Info
                    try:
                        with open("Showtimes.txt") as showTimes:
                            next(showTimes)
                            for showTime in showTimes:
                                parts = showTime.strip().split(", ")
                                if parts[0] == bookingData[userBookingID][1]:
                                    specShowID, movieChoice, audiID, dateChoice, timeChoice = parts[:5]
                                    break
                    except FileNotFoundError:
                        print("Error: Showtimes.txt file not found.")
                        break

                    # Retrieve Movie Info
                    try:
                        with open("Movies.txt") as movies:
                            next(movies)
                            for movie in movies:
                                parts = movie.strip().split(", ")
                                if parts[0] == movieChoice:
                                    genre, duration, rating, price = parts[1:5]
                                    break
                    except FileNotFoundError:
                        print("Error: Movies.txt file not found.")
                        break
                    
                    # Retrieve Reserved Seat Info
                    try:
                        with open("Reserved_seats.txt") as reservedSeats:
                            next(reservedSeats)
                            reservedSeatData = {}
                            for reservedSeat in reservedSeats:
                                parts = reservedSeat.strip().split(", ")
                                reservedSeatData.update({parts[0]: parts[1]})
                    except FileNotFoundError:
                        print("Error: Reserved_seats.txt file not found.")
                        break
                    reservedSeatsList = reservedSeatData[specShowID].split() # Insert the list of booked seats of a spesific showtime
                    
                    _, audiSeats, seatMap = load_auditoriums_seatings(showID = specShowID, auditoriumID = audiID)
                    # Free up previously booked seats for re-selection
                    for seat in seatsChosen:
                        rowNum = seatMap[seat[0]]
                        colNum = int(seat[1:]) - 1
                        audiSeats[rowNum][colNum] = 0
                        if seat in reservedSeatsList:
                            reservedSeatsList.remove(seat)
                    # Display Current Layout
                    render_seats(movieTitle = movieChoice, movieDate = dateChoice, movieTime = timeChoice, 
                                 movieGenre = genre, movieDuration = duration, movieRating = rating, 
                                 movieAudi = audiID, moviePrice = price, seats = audiSeats)
                    
                    seatCnt = len(seatsChosen)
                    print(f"\n🎟️  You originally booked {seatCnt} seats.")
                    print("Please select the new seats for this booking.\n")

                    # Select New Seats
                    audiSeats, seatsChosen = select_seats(seats = audiSeats, seatMap = seatMap, seatQuantity = seatCnt) # Select seats with the select_seat() function
                    reservedSeatsList.extend(seatsChosen) # include the new seating to the list of seats
                    print()

                    # Display New Layout
                    print("\nHere is your updated seating arrangement:")
                    render_seats(movieTitle = movieChoice, movieDate = dateChoice, movieTime = timeChoice, 
                         movieGenre = genre, movieDuration = duration, movieRating = rating, 
                         movieAudi = audiID, moviePrice = price, seats = audiSeats)
                    
                    while True:
                        saveSeatChoice = input("\nSave the new seating arrangement? (Y/N): ").strip().lower()
                        if saveSeatChoice == "y":
                            bookingData[userBookingID][2] = ' '.join(seatsChosen) # Change booking seats
                            reservedSeatData[specShowID] = ' '.join(reservedSeatsList) # Change seating in reserved seats

                            with open("Bookings.txt", "w") as bookings: # Save updated bookings file
                                bookings.write("BookingID, Username, ShowID, Seats, Status\n")
                                bookingItems = list(bookingData.items())
                                for i, (bookingID, bookingDetails) in enumerate(bookingItems):
                                    line = f"{bookingID}, {bookingDetails[0]}, {bookingDetails[1]}, {bookingDetails[2]}, {bookingDetails[3]}"
                                    if i < len(bookingItems) - 1:
                                        bookings.write(line + "\n")
                                    else:
                                        bookings.write(line)

                            with open("Reserved_seats.txt", "w") as reservedSeats: # Save updated reserved seats file
                                reservedSeats.write("ShowID, Reserved Seats\n")
                                reservedSeatsItems = list(reservedSeatData.items())
                                for i, (showID, seats) in enumerate(reservedSeatsItems):
                                    line = f"{showID}, {seats}"
                                    if i < len(reservedSeatsItems) - 1:
                                        reservedSeats.write(line + "\n")
                                    else:
                                        reservedSeats.write(line)
                            
                            print("\nBooking successfully updated!")
                            input("Press ENTER to continue...\n")
                            return modify_booking()
                            
                        elif saveSeatChoice == "n":
                            print("\nModification canceled...\n")
                            return modify_booking()
                        else:
                            print("Invalid input. Please enter 'Y' or 'N'.")
                    
                else:
                    print("Booking ID not found. Please check and try again.")

        elif choice == "2":
            cancel_booking(bookingData = bookingData)
            return modify_booking()

        elif choice == "3":
            return
        else:
            print("Invalid choice. Please 1, 2, or 3.\n")

# --- Generate Customer Receipt ---
def generate_customer_receipt():

    while True:
        print("\n--- Generate Customer Receipt ---\n")

        print("Select an option to continue: \n")
        print("1. Generate a Receipt")
        print("2. Go Back to Clerk Menu")
        choice = input("\nEnter your choice (1-2): ").strip()
        if choice == "1":
            try:
                # Reads payment from 'Payments.txt'
                with open("Payments.txt") as payments:
                    next(payments)
                    paymentData = {}
                    for payment in payments:
                        parts = payment.strip().split(", ")
                        paymentData.update({parts[0]: parts[1:]}) # -> PaymentID: BookingID, Total Booking, Payment Method, Payment Date, Status     
            except FileNotFoundError:
                    print("Error: Payments.txt file not found.")
                    continue
            
            if not paymentData:
                print("⚠️  No payment data found.")
                break

            while True:
                userPaymentID = input("\nEnter a Payment ID (e.g. 'P1') or type 'back' to return: ").strip()
                if userPaymentID.lower() == "back":
                    print()
                    break
                if userPaymentID  in paymentData:              
                    # Retrieve Booking Info
                    try:
                        with open("Bookings.txt") as bookings:
                            next(bookings)
                            for booking in bookings:
                                parts = booking.strip().split(", ")
                                if parts[0] == paymentData[userPaymentID][0]:
                                    specUsername = parts[1]
                                    specShowID = parts[2]
                                    seatsSelected = parts[3].split()
                                    break
                    except FileNotFoundError:
                        print("Error: Bookings.txt file not found.")
                        break

                    # Import Showtime Info
                    try:
                        with open("Showtimes.txt") as showTimes:
                            next(showTimes)
                            for showTime in showTimes:
                                parts = showTime.strip().split(", ")
                                if parts[0] == specShowID:
                                    showTitle = parts[1]
                                    audiID = parts[2]
                                    showDate = parts[3]
                                    showTime = parts[4]
                                    break
                    except FileNotFoundError:
                        print("Error: Showtimes.txt file not found.")
                        break

                    # Import Movie Info
                    try:
                        with open("Movies.txt") as movies:
                            next(movies)
                            for movie in movies:
                                parts = movie.strip().split(", ")
                                if parts[0] == showTitle:
                                    price = float(parts[4][2:])
                                    break
                    except FileNotFoundError:
                        print("Error: Movies.txt file not found.")
                        break

                    ticketCount = len(seatsSelected)
                    totalPrice = ticketCount * price

                    print(f"\n🧾 Receipt for Payment ID: {userPaymentID}\n")
                    generate_receipt(
                        payment_id=userPaymentID,
                        payment_date=paymentData[userPaymentID][-2],
                        payment_method=paymentData[userPaymentID][-3],
                        booking_id=paymentData[userPaymentID][0],
                        username=specUsername,
                        status="CONFIRMED",
                        movie=showTitle,
                        auditorium=audiID,
                        date=showDate,
                        time=showTime,
                        seats=seatsSelected,
                        price_each=price,
                        final_price=totalPrice
                    )
                    input("Press ENTER to continue....\n")
                    return generate_customer_receipt()
                
                else:
                    print("Payment ID not found. Please check and try again.")

        elif choice == "2":
            return
        else:
            print("Invalid choice. Please enter 1 or 2.\n")


# --- TICKETING CLERK MENU ---
def ticketing_clerk_menu():
    print("\n|------ Ticketing Clerk ------|\n")
    print("This section is restricted to authorized cinema staff only.")
    print("Please enter your login credentials.")

    clerkUsername = clerk_access()
    if clerkUsername is None:
        return None
    
    while True:
        print(f"\n\nWelcome {clerkUsername}, what would you like to do?\n")
        print("1. Book Tickets")
        print("2. Cancel/Modify Booking")
        print("3. View Seats & Showtimes")
        print("4. Generate Receipt")
        print("5. Log Out")
        
        choice = input("\nChoose your operation (1-5): ")
        print()

        if choice == "1":
            book_tickets()
        elif choice == "2":
            modify_booking()
        elif choice == "3":
            view_seating_availability()
        elif choice == "4":
            generate_customer_receipt()
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please try again.\n")
#----------------------------------- CLERK MENU -----------------------------------



#----------------------------------- MANAGER MENU -----------------------------------
def manager_login():
    print("\n----Manager Authentication----")

    try:
        with open("Manager_auth.txt", "r") as f:
            manager_file=f.readlines()

    except FileNotFoundError:
        print("Manager_auth.txt not found!")
        return
    
    manager_id = input("Enter Manager ID: ").strip()
    password = input("Enter Password: ").strip()

    ### check the password
    for manager in manager_file:
        column=manager.strip().split(", ")
       
        stored_id = column[0].strip()
        stored_pass = column[2].strip()

        if stored_id==manager_id and stored_pass==password:
            print("Login In Successful\n")
            cinema_manager_menu()
            break
            
        else:
            print("Wrong Password!")

def add_movie():

    ### ask user how many input that needed
    try:
        number_of_input=int(input("\nHow many movie that needed to be added \n1)  1 \n2)  2 \n3)  3\n"))
        if number_of_input==1:
            pass
        elif number_of_input==2:
            pass
        elif number_of_input==3:
            pass
        else:
            print("Invalid value.Please enter number(1-3).Please Try Again!")
            return
    except ValueError:
         print("Invalid value.Please enter number(1-3).Please Try Again!")
         return

    Existing_Movie_Title=[]
    
   
    
    try:
        with open("Movies.txt", "r") as movie_file:
            for movie in movie_file:
                column = [c.strip() for c in movie.split(", ")]
                if len(column)>=5 and column[0].lower() != "Movie Title":
                    Movie_Title=column[0]
                    Existing_Movie_Title.append(Movie_Title) 
                    
    except FileNotFoundError:
        print("Movies.txt not found!")



    movie_added=[]
    ### the details about Movie
    for i in range(number_of_input):
        print(f"----Movie{i+1}----")

        while True:
            Movie_Title=input("Enter Movie Title              :").strip()
            if  not Movie_Title:
                print("Movie Title cannot be empty.Please Try Again!")
                return

            elif Movie_Title in Existing_Movie_Title:
                print("Movie Title exists.Please try another one!")

            else:
                break
            


        while True:
            Genre=input("Enter genre of movie           :").strip()
            if Genre:
                break
            else:
                print("Genre cannot be empty.Please Try Again!")

        
        while True:
            Duration=float(input("Enter the duration of movie    :"))
            if Duration:
                break
            else:
                print("Duration cannot be empty.Please Try Again!")
        
             
        
        while True:
            rating=("U","PG-13","16+","18+")
            print("Available rating=",rating)
            Age_Based_Rating=input("Enter the age rating         :").strip()
            if Age_Based_Rating in rating:
                break
            else:
                print("Age based rating is empty or invalid.Please Try Again!")

        while True:
            status=("Now Showing","Coming Soon")
            print("Available status=",status)
            Status=input("Now Showing/Coming Soon       :").strip().title() 
            if Status in status:
                break
            else:
                print("Status is empty or invalid.Please Try Again!")

        Ticket_Price="RM-"

        movie_added.append(f"\n{Movie_Title}, {Genre}, {Duration}, {Age_Based_Rating}, {Ticket_Price}, {Status}")


    with open("Movies.txt","a")as f:
        for data in movie_added:
            f.write(data)

    print("\nUpdated successfully and saved to file!")
    print("Returning to manager menu...\n")
    return cinema_manager_menu()

def update_movie():
    
    try:
        with open("Movies.txt", "r") as f:
            movie_file = f.readlines()
    except FileNotFoundError:
        print("Movies.txt not found!")
        return

    
    Existing_Movie_Title = []
    for movie in movie_file:
        column = [c.strip() for c in movie.split(",")]
        if len(column) >= 5 and column[0].lower() != "movie title":
            Existing_Movie_Title.append(column[0])

    
    Movie_Title = input("Enter the movie title to update: ").strip()
    if not Movie_Title:
        print("Movie title cannot be empty!")
        return
    if Movie_Title not in Existing_Movie_Title:
        print(f"Movie not found!")
        return

    
    for i, movie in enumerate(movie_file):
        column = [c.strip() for c in movie.split(",")]
        if column[0] == Movie_Title:
            break  

    
    while True:
        try:
            print("\nWhat do you want to update?")
            print("1. Title")
            print("2. Genre")
            print("3. Duration")
            print("4. Age Based Rating")
            print("5. Status")
            print("0. Exit update menu")

            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Invalid number. Try again.")
            continue

        if choice == 0:
            break

        elif choice == 1:
            new_title = input("Enter new title: ").strip()
            if new_title and new_title != column[0]:
                column[0] = new_title
                print("New Title updated.")
            else:
                print("Invalid or same title.Please Try Again!")

        elif choice == 2:
            new_genre = input("Enter new genre: ").strip()
            if new_genre and new_genre != column[1]:
                column[1] = new_genre
                print("New Genre updated.")
            else:
                print("Invalid or same genre.Please Try Again!")

        elif choice == 3:
            new_duration = input("Enter new duration: ").strip()
            if new_duration and new_duration != column[2]:
                column[2] = new_duration
                print("New Duration updated.")
            else:
                print("Invalid or same duration.Please Try Again!")

        elif choice == 4:
            rating = ("U", "PG-13", "16+", "18+")
            print("Available ratings:",rating)
            new_age = input("Enter new age rating: ").strip()
            if new_age in rating and new_age != column[3]:
                column[3] = new_age
                print("New Age rating updated.")
            else:
                print("Invalid or same age rating.Please Try Again!")

        elif choice == 5:
            status=("Now Showing", "Coming Soon")
            print("Available status:",status)
            new_status = input("Enter new status: ").strip()
            if new_status in status and new_status != column[4]:
                column[4] = new_status
                print("New Status updated.")
            else:
                print("Invalid or same status.Please Try Again!")

        else:
            print("Invalid choice.Please Try again.")
            continue

       
        movie_file[i] = ", ".join(column) + "\n"

        
        with open("Movies.txt", "w") as f:
            f.writelines(movie_file)
        print("Movie updated successfully!\n")

    print("Returning to manager menu...\n")
    return cinema_manager_menu()             

def remove_movie():
    try:
        with open("Movies.txt","r")as f:
                movie_file=f.readlines()
        
        new_update=[]
        
        Movie_Title=input("Enter the movie title:\n").strip()
        movie_found=False

        for movie in movie_file:
            column=movie.strip().split(",")
            if column[0]==Movie_Title:
                movie_found=True
                print(column)
            
                x=input("\nAre you sure you want to delete this movie(Y/N): \n")
                if x=="Y":
                    print(f"{Movie_Title},deleted successfully!")
                elif x=="N":
                    print("Cancelled")
                    new_update.append(movie)
                else:
                    print("Invaild input!Please Try Again!")
            
            else:
                new_update.append(movie)

        if not movie_found:
            print("Invalid movie title!")
        else:
            with open("Movie.txt","w")as f:
                f.writelines(new_update)
            print("Updated successfully and saved to file!")  
            return cinema_manager_menu()       
    except FileNotFoundError:
        print("Movies.txt file not found!")
    except Exception as x:
         print(f"Unexpected error: {x}")

def view_movie():
    try:
        with open("Movies.txt","r")as f:
            movie_file=f.readlines()

        for movie in movie_file:
            column=movie.strip().split(", ")
            print(f"MovieTitle     : {column[0]}")
            print(f"Genre          : {column[1]}")
            print(f"Duration       : {column[2]}")
            print(f"Age Rating     : {column[3]}")
            print(f"TicketPrice    : {column[4]}")
            print(f"Status         : {column[5]}")
            print("\n")   

        while True:
            x=input("Enter Y to Exit\n ").strip().upper()
            if x=="Y":
                return cinema_manager_menu()      
                break  
            else:
                print("Invalid Input")

    except FileNotFoundError:
        print("Movies.txt file not found!")    
    except Exception as x:
         print(f"Unexpected error: {x}")   

def create_showtime():
    try:
        number_of_input=int(input("How many showtime that needed to be create? \n1)  1 \n2)  2 \n3)  3\n"))
        if number_of_input==1:
            pass
        elif number_of_input==2:
            pass
        elif number_of_input==3:
            pass
        else:
            print("Maximun number is 3")
    except ValueError:
         print("Invalid value")

    Existing_showID=[]
    Existing_audi={}
   
    
    try:
        with open("Showtimes.txt", "r") as f:
            for show in f:
                column = [c.strip() for c in show.split(", ")]
                if len(column) >= 5 and column[0].lower() != "showid":
                    showid, title, audi = column[0], column[1], column[2]
                    Existing_showID.append(showid) 
                    Existing_audi[audi] = title
    except FileNotFoundError:
        print("Showtimes.txt not found!")


    showtime_added=[]
    for i in range(number_of_input):
        print(f"           Movie{i+1}         ")

        while True:
            ShowID=input("Enter ShowID (e.g. S1)      :").strip()
            if not ShowID:
                print("Show cannot be empty.Please Try Again!")
            elif not ShowID.startswith("S"):
                print("Invalid ShowID.Please Try Again!")
            elif ShowID in Existing_showID:
                print("ShowID already exists.Please Try Again!")
            else:
                 Existing_showID.append(ShowID)
                 break
            
            
       
       
        while True:
            Movie_Title=input("Enter title of movie          :").strip()
            if Movie_Title:
                break
            else:
                print("Movie title cannot be empty.Please Try Again!")
        
        

        while True:
            Audi = input("Enter Auditorium (e.g. Audi 1): ").strip()
            if not Audi:
                print("Auditorium cannot be empty.")
                continue
            if Audi in Existing_audi and Existing_audi[Audi]!=Movie_Title:
                print(f"{Audi} is already showing '{Existing_audi[Audi]}'. Try another auditorium.")
                continue
            Existing_audi[Audi]=Movie_Title
            break


        while True:
            Date=input("Enter Date (e.g. Mon - 13 Oct): ").strip()
            if Date:
                break
            else:
                print("Date cannot be empty.Please Try Again!")


        while True:
            Time = input("Enter Time (e.g. 1:00 PM): ").strip()
            if Time:
                break
            else:
                print("Time cannot be empty.Please Try Again!")
        
        showtime_added.append(f"{ShowID}, {Movie_Title}, {Audi}, {Date}, {Time}")

    with open("Showtimes.txt","a")as f:
        for data in showtime_added:
            f.write(data+"\n")


    print("Updated successfully and saved to file!")
    print("Returning to manager menu...\n")
    return cinema_manager_menu()

def update_showtime():
    try:
        with open("Showtimes.txt","r")as f:
            show_file=f.readlines()

      

        ShowID=input("Enter the ShowID").strip()
        show_found=False

        for i,show in enumerate(show_file):
            column=show.strip().split(",")
            if column[0]== ShowID:
                show_found=True
                print (show.strip())

                while True:
                    try:
                        print("\nWhat do you want to update?")
                        print("1. ShowID")
                        print("2. Movie_Title")
                        print("3. Auditorium")
                        print("4. Date")
                        print("5. Time")
                        print("0. Exit update menu")

                        choice=int(input("Enter the number to procced"))
                    except ValueError:
                        print("Invalid number.Please Try Again!")

                    if choice ==1:
                        New_ShowID=input("Enter new showID: ").strip()
                        while True:
                            if New_ShowID and New_ShowID !=column[0]:
                                column[0] = New_ShowID
                                print("New ShowID updated")
                                break
                            elif New_ShowID=="":
                                print("New ShowID cannot be empty.Please Try Again!")
                            else:
                                print("New ShowID same with the Old title.Please Try Again!")
                        
                    elif choice ==2:
                        New_Movie_Title=input("Enter new movie title: ").strip()
                        while True:
                            if New_Movie_Title and New_Movie_Title !=column[1]:
                                column[1] = New_Movie_Title
                                print("New movie title updated.")
                                break
                            elif New_Movie_Title=="":
                                print("New movie title cannot be empty.Please Try Again!")
                                
                            else:
                                print("New movie title same with the Old title.Please Try Again!")
                                

                    elif choice ==3:
                        New_Audi=input("Enter new duration: ").strip()
                        while True:
                            if New_Audi and New_Audi !=column[2]:
                                column[2] = New_Audi
                                print("New duration updated.")
                                break
                            elif New_Audi=="":
                                print("New Auditorium cannot be empty.Please Try Again!")
                            else:
                                print("New Auditorium same with the Old Auditorium.Please Try Again!")
                        
                    elif choice ==4:
                        New_Date=input("Enter new date(e.g. Mon - 13 Oct): ").strip()
                        while True:
                            if New_Date and New_Date !=column[3]:
                                column[3] = New_Date
                                print("New date updated.")
                                break
                            elif New_Date=="":
                                print("New date cannot be empty.Please Try Again!")
                            else:
                                print("New date same with the Old date.Please Try Again!")
                    
                    elif choice ==5:
                        New_Time=input("Enter new time (e.g. 1.00 PM): ").strip()
                        while True:
                            if New_Time and New_Time != column[4]:
                                column[4] = New_Time
                                print("New time updated.")
                                break
                            elif New_Time=="":
                                print("New time cannot be empty.Please Try Again!")
                            else:
                                print("New time same with the Old time.Please Try Again!")
    
                    elif choice ==0:
                        print("Exiting update menu.")
                        return cinema_manager_menu()
                        break
                    else:
                        print("Invalid choice.")


                    show_file[i] = ",".join(column) + "\n"
                    with open("Showtimes.txt", "w") as f:
                        f.writelines(show_file)
                    print(f"\n Updated successfully and saved to file!")
                break

        if not show_found:
            print("Invalid movie title!")

    except FileNotFoundError:
        print("Movies.txt file not found!")
    except Exception as x:
        print(f"Unexpected error: {x}")
                          
def remove_showtime():
    try:
        with open("Showtimes.txt","r")as f:
                showtime_file=f.readlines()
        
        new_update=[]
        
        ShowID=input("Enter the ShowID:\n").strip()
        show_found=False

        for show in showtime_file:
            column=show.strip().split(",")
            if column[0]==ShowID:
                show_found=True
                print(column)
            
                x=input("\nAre you sure you want to delete this showtime(Y/N): \n")
                if x=="Y":
                    print(f"{ShowID},deleted successfully!")
                elif x=="N":
                    print("Cancelled")
                    new_update.append(show)
                else:
                    print("Invaild input!Please Try Again!")
            
            else:
                new_update.append(show)

        if not show_found:
            print("Invalid ShowID!")
        else:
            with open("Showtimes.txt","w")as f:
                f.writelines(new_update)
            print("Updated successfully and saved to file!\n")  
            cinema_manager_menu()       
    except FileNotFoundError:
        print("Showtimes.txt file not found!")
    except Exception as x:
         print(f"Unexpected error: {x}")

def view_showtime():
    try:
        with open("Showtimes.txt","r")as f:
            showtime_file=f.readlines()
        

        for show in showtime_file:
            column=show.strip().split(",")
            if column[0].lower() == "showid":  ### skip the header line
                continue


            print(f"ShowID         : {column[0]}")
            print(f"MovieTitle     : {column[1]}")
            print(f"Auditorium     : {column[2]}")
            print(f"Date           : {column[3]}")
            print(f"Time           : {column[4]}")
            print("\n")       

        while True:
            x=input("Enter Y to Exit\n ").strip().upper()
            if x=="Y":
                return cinema_manager_menu()      
                break  
            else:
                print("Invalid Input")

    except FileNotFoundError:
        print("Showtimes.txt file not found!")    
    except Exception as x:
         print(f"Unexpected error: {x}")   

def price_movie():

    print("\n---Ticket Price and Discount Setting---")
    print("1. Set Ticket Price")
    print("2. Set Discount Policy")
    print("3. Return to Manager Menu")

    choice=input("Enter your choice (1-3): ").strip()


    if choice=="1":

        print("---Setting Ticket Price---")

        try:
            with open("Movies.txt","r")as f:
                movie_file=f.readlines()
        
        except FileNotFoundError:
            print("Invaild File!")
            return

        Movie_title=input("Enter a Movie Title to set Price:")
        movie_found=False

 
        for i, movie in enumerate(movie_file):
            column = [c.strip() for c in movie.split(",")]
            if column[0] == Movie_title:
                movie_found = True
                print(f"Current price: {column[4]}")
                while True:
                    set_price = input("Enter Ticket Price (RM): ").strip()
                    if set_price.replace(".", "", 1).isdigit():
                        column[4] = "RM-" + set_price  
                        movie_file[i] = ", ".join(column) + "\n"
                        break
                    else:
                        print("Invalid price. Please Try Again!")
                break

        if not movie_found:
            print(f"Movie '{Movie_title}' not found!")
            return

        
        with open("Movies.txt", "w") as f:
            f.writelines(movie_file)
        print("Ticket Price updated sucessfully!")



    elif choice=="2":
        print("\n---Setting discount---")
        

        try:
             with open("Discount.txt","r")as f:
                 discounts = [line.strip() for line in f.readlines()]
        
        except FileNotFoundError:
            print("Invaild File!")
    
        
        discounts=[]
        existing_ids = [line.split(",")[0].strip() for line in discounts]

        while True:
            DiscountID = input("Enter DiscountID (e.g., D5): ").strip()
            if not DiscountID:
                print("DiscountID cannot be empty.Please Try Again!")
            elif not DiscountID.startswith("D"):
                print("DiscountID must start with 'D'.Please Try Again!")
            elif DiscountID in existing_ids:
                print(f"{DiscountID} already exists.Please Try Again!")
            else:
                break

        while True:
            Discount_Name = input("Enter the Discount Name: ").strip()
            if Discount_Name:
                break
            else:
                print("Discount name cannot be empty.Please Try Again!")

        while True:
            Discount_Rate = input("Enter the Discount Rate (10,20)%: ").strip()
            if Discount_Rate.isdigit() and 0 < int(Discount_Rate) <= 100:
                break
            else:
                print("Invalid discount rate.Please Try Again!")

       
        discounts.append(f"{DiscountID},{Discount_Name},{Discount_Rate}%\n")
        with open("Discount.txt", "w") as f:
            f.writelines(discounts)

        print("Discount policy set successfully!")

    elif choice=="3":
    
    
        print("Existing Ticket Price and Discount Setting....")
        return cinema_manager_menu()
    
    else:
        print("Invalid Chooice.Please Try Again")
        return



    print("Ticket price and discount set successfully!")
    print("Returning to Manager Menu....")

def sumarise_movie():
    
    print("\n---Cinema Summary Report--- \n")

    try:
        with open("movies.txt", "r") as f:
            movie = f.readlines()
            print(f"Total movies listed: {len(movie)-1}")

    except FileNotFoundError:
        print("No movies file found.")

    
    try:
        with open("showtimes.txt", "r") as f:
            showtime = f.readlines()
            print(f" Total showtimes scheduled: {len(showtime)-1}")
            
    except FileNotFoundError:
        print("No showtimes file found.")

    print("\nReturning to Manager Menu...\n")
    return cinema_manager_menu()


# --- MANAGER MENU ---
def cinema_manager_menu():  
       print("----Cinema Manager Menu---- \n1.Add New Movie \n2.Update Movie \n3.Remove Movie \n4.View Current Movie \n5.Create Showtime" \
       " \n6.Update Showtime \n7.Remove Showtime \n8.View Current Showtime \n9.Set Ticket Price And Discount \n10.Summarise \n0.Exit") 

       menu_option=(input("\nChoose a function using its representative number:"))
    
       if menu_option=="1":
          add_movie()
       elif menu_option=="2":
          update_movie()
       elif menu_option=="3":
          remove_movie()
       elif menu_option=="4":
          view_movie()
       elif menu_option=="5":
          create_showtime()
       elif menu_option=="6":
          update_showtime()
       elif menu_option=="7":
          remove_showtime()
       elif menu_option=="8":
          view_showtime()
       elif menu_option=="9":
          price_movie()
       elif menu_option=="10":
           sumarise_movie()
       elif menu_option=="0":
          print("Exiting Manager Menu...")
          return
       else:
            print("Invalid option, try again.")
#----------------------------------- MANAGER MENU -----------------------------------



#----------------------------------- CUSTOMER MENU -----------------------------------
customer_file = 'Customer_auth.txt'

def get_next_customer_id():
    try:
        with open(customer_file, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return "C1001"
        
        last_line = lines[-1].strip()
        if last_line:
            last_id = last_line.split(', ')[0]
            if last_id.startswith('C'):
                num = int(last_id[1:]) + 1
                return f"C{num}"
        return "C1001"
    except FileNotFoundError:
        return "C1001"

def is_email_unique(email):
    try:
        with open(customer_file, 'r') as f:
            for line in f:
                data = line.strip().split(', ')
                if len(data) >= 3 and data[2].lower() == email.lower():
                    return False
        return True
    except FileNotFoundError:
        return True

def validate_input(name, email, password):
    
    if not all([name, email, password]):
        return False, "Error: All fields are required!"
    
    if "@" not in email or "." not in email:
        return False, "Error: Please enter a valid email address!"
        
    
    if not is_email_unique(email):
        return False, "Error: Email already registered!"
    
    
    if len(password) < 4:
        return False, "Error: Password must be at least 4 characters!"
    
    return True, "Valid"

def customer_register():
    print("\n" + "="*40)
    print("        CUSTOMER REGISTRATION")
    print("="*40)
    
    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    
   
    is_valid, message = validate_input(name, email, password)
    if not is_valid:
        print(f" {message}")
        return
    
    
    customer_id = get_next_customer_id()
    
    try:
        with open(customer_file, 'a') as f:
            f.write(f"{customer_id}, {name}, {email}, {password}\n")
        print(f" Registration successful!")
        print(f" Your Customer ID is: {customer_id}")
        print(" Please remember your ID for future logins.")
        
    except Exception as e:
        print(f" Error: Could not save registration data.")
   
def customer_login():
    customer_found = False

    print("\n" + "="*40)
    print("          CUSTOMER LOGIN")
    print("="*40)
    
    customer_id = input("Enter your Customer ID: ").strip().upper()
    password = input("Enter your password: ").strip()

    if not customer_id or not password:
        print("Error: Both Customer ID and password are required!")
        return None
    
    if not customer_id.startswith('C') or not customer_id[1:].isdigit():
        print("Error: Invalid Customer ID format. (Example: C1001, C1002, etc.)")
        return None
        
    
    try:
        customer_found = False
        with open(customer_file, 'r') as f:
            for line in f:
                data = line.strip().split(', ')
                if len(data) >= 4:  
                    if data[0] == customer_id:
                        customer_username = data[1]
                        customer_found = True
                        if data[3] == password:  
                            print(f"Login successful! Welcome back, {data[1]}!")
                            return customer_id, customer_username
                        else:
                            print("Error: Incorrect password.")
                            return None
                        
        
        if not customer_found:
            print("Error: Customer ID not found. Please check your ID or register first.")
        return None
        
    except FileNotFoundError:
        print("Error: Customer database not found. Please register first.")
        return None
    except Exception as e:
        print(f"Error during login: {e}")
    return None

def view_movies():
    print("\n" + "="*40)
    print("          AVAILABLE MOVIES")
    print("="*40)
    
    try:
        with open('Movies.txt', 'r') as f:
            movies = f.readlines()
        
        if not movies:
            print("No movies available at the moment.")
            return
        
        for line in movies:
            data = line.strip().split(',')
            if len(data) >= 4:
                print(f"Movie Title: {data[0]}")
                print(f"Genre: {data[1]}")
                print(f"Duration: {data[2]}")
                print(f"Age rating: {data[3]}")
                print(f"Ticket price: {data[4]}")
                print(f"Status: {data[5]}")
                print("="*60)
    
    except FileNotFoundError:
        print("Error: Movies database not found.")
    except Exception as e:
        print(f"Error while fetching movies: {e}")
        
    input("\nPress Enter to continue...")    

def load_showtimes(filename="Showtimes.txt"):
    showtimes = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) >= 5:
            show_id, title, audi, date, time = parts[0], parts[1], parts[2], parts[3], parts[4]
            showtimes[show_id.upper()] = {
                "title": title,
                "audi": audi,
                "date": date,
                "time": time
            }
    return showtimes

def load_movie_prices(filename="Movies.txt"):
    prices = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) >= 5:
            title = parts[0]
            raw_price = parts[4].upper().replace("RM", "").strip()

            if raw_price == "-" or raw_price == "":
                continue  # Skip movies without valid price

            try:
                price = float(raw_price)
                prices[title] = price
            except ValueError:
                pass
    return prices

def load_discounts(filename="Discount.txt"):
    discounts = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) >= 3:
            disc_id = parts[0]
            name = parts[1]
            rate_str = parts[2].replace("%", "")
            try:
                rate = float(rate_str)
            except:
                rate = 0
            discounts[disc_id] = {"name": name, "rate": rate}
    return discounts

def file_exists(filename):
    try:
        with open(filename, "r"):
            return True
    except FileNotFoundError:
        return False

def view_booking_history(username):
    print("\n" + "=" * 40)
    print("          BOOKING HISTORY")
    print("=" * 40)

    try:
        with open("Bookings.txt", "r") as f:
            lines = f.readlines()

        if len(lines) <= 1:
            print("No bookings found.")
            return

        # Skip header
        header = lines[0].strip().split(", ")
        bookings = [line.strip().split(", ") for line in lines[1:] if line.strip()]

        # Filter by username (case-insensitive match)
        user_bookings = [b for b in bookings if len(b) >= 5 and b[1].lower() == username.lower()]

        if not user_bookings:
            print("No bookings found for this user.")
            return

        showtimes = load_showtimes()  # Assuming this returns a dict like {'S1': {'title': 'Movie A', 'date': '...', 'time': '...'}}

        for booking in user_bookings:
            booking_id, user, show_id, seats, status = booking[:5]

            print(f"\nBooking ID : {booking_id}")
            print(f"Show ID    : {show_id}")

            # Get showtime info if available
            if show_id in showtimes:
                show_info = showtimes[show_id]
                print(f"Movie      : {show_info['title']}")
                print(f"Date       : {show_info['date']}")
                print(f"Time       : {show_info['time']}")
            else:
                print("Movie      : [Show details not found]")

            print(f"Seats      : {seats}")
            print(f"Status     : {status}")
            print("-" * 60)

    except FileNotFoundError:
        print("Bookings.txt not found.")
    except Exception as e:
        print(f"Error while fetching booking history: {e}")

    input("\nPress Enter to continue...")

def update_profile(customer_id):
    print("\n" + "="*40)
    print("        UPDATE PROFILE")
    print("="*40)

    try:
        with open(customer_file, 'r') as f:
            lines = f.readlines()

        customer_data = None
        for i, line in enumerate(lines):
            data = line.strip().split(', ')
            if len(data) >= 4 and data[0] == customer_id:
                customer_data = data
                customer_index = i
                break

        if not customer_data:
            print("Error: Customer not found.")
            return

        print(f"Current Name: {customer_data[1]}")
        print(f"Current Email: {customer_data[2]}")

        new_name = input("Enter new name (or press Enter to keep current): ").strip()
        new_email = input("Enter new email (or press Enter to keep current): ").strip()
        new_password = input("Enter new password (or press Enter to keep current): ").strip()

        if new_name:
            customer_data[1] = new_name
        if new_email:
            if new_email != customer_data[2] and not is_email_unique(new_email):
                print("Error: Email already registered by another account.")
                return
            if "@" not in new_email or "." not in new_email:
                print("Error: Please enter a valid email address!")
                return
            customer_data[2] = new_email
        if new_password:
            if len(new_password) < 4:
                print("Error: Password must be at least 4 characters!")
                return
            customer_data[3] = new_password

        lines[customer_index] = ", ".join(customer_data) + "\n"

        with open(customer_file, 'w') as f:
            f.writelines(lines)

        print("Profile updated successfully!")

    except FileNotFoundError:
        print("Error: Customer database not found.")
    except Exception as e:
        print(f"Error while updating profile: {e}")

    input("\nPress Enter to continue...")        

def customer_process_payment(username, showTitle, showId, seatsSelected, auditoriumId, showDate, showTime, priceInfo, seatFlag):
    
    # Handles payment and booking confirmation process for a selected movie show.

    while True:
        print("\nHow would you like to Pay?\n")
        print("1. Cash")
        print("2. Debit Card")
        print("3. Credit Card")
        print("4. e-Wallet")

        paymentChoice = input("\nEnter your choice (1-4): ").strip()

        if paymentChoice == "1":
            paymentMethod = "Cash"
        elif paymentChoice == "2":
            paymentMethod = "Debit Card"
        elif paymentChoice == "3":
            paymentMethod = "Credit Card"
        elif paymentChoice == "4":
            paymentMethod = "e-Wallet"
        else:
            print("Invalid choice. Please try again.")
            continue

        print(f"\nSelected payment method: {paymentMethod}")

        # Discount application
        discounts = load_discounts()
        ticketCount = len(seatsSelected)
        priceEach = float(priceInfo[2:])  # removes "RM"
        totalPrice = ticketCount * priceEach

        base_total_price = totalPrice
        final_price = base_total_price
        if discounts:
            print("\n=== Available Discounts ===")
            for disc_id, disc_info in discounts.items():
                print(f"{disc_id}: {disc_info['name']} ({disc_info['rate']}% off)")

            chosen_disc = input("\nEnter Discount ID to apply (or press Enter to skip): ").upper().strip()
            if chosen_disc in discounts:
                disc_rate = discounts[chosen_disc]["rate"]
                discount_amount = base_total_price * (disc_rate / 100)
                final_price = base_total_price - discount_amount
                print(f" {discounts[chosen_disc]['name']} applied! You saved RM {discount_amount:.2f}")
            else:
                print("No discount applied.")
        print(f"\n Final Price: RM {final_price:.2f}")

        input("Waiting for Payment... Press ENTER once payment is completed.\n")

        while True:
            paymentDate = input("Enter the date of payment (DD/MM/YYYY, e.g., 20/09/2025): ").strip()

            # Check overall format (should have 2 slashes)
            if paymentDate.count("/") != 2:
                print("Invalid format. Please use DD/MM/YYYY.\n")
                continue
            
            day, month, year = paymentDate.split("/")

            # Check if all parts are digits and have correct lengths
            if not (day.isdigit() and month.isdigit() and year.isdigit()):
                print("Date must contain only numbers. Please try again.\n")
                continue
            if len(day) != 2 or len(month) != 2 or len(year) != 4:
                print("Invalid format. Please use DD/MM/YYYY.\n")
                continue
            
            day, month, year = int(day), int(month), int(year)
            if not (1 <= month <= 12):
                print("Month must be between 01 and 12.\n")
                continue
            monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if not (1 <= day <= monthDays[month - 1]):
                print(f"Day must be between 01 and {monthDays[month - 1]} for month {month:02d}.\n")
                continue

            break
        print()

        # --- Booking File ---
        bookingId = identify_next_bookingID("Bookings.txt")
        bookingData = [
            bookingId,
            username,
            showId,
            " ".join(seatsSelected),
            "Confirmed"
        ]

        with open("Bookings.txt", "a") as file:
            file.write("\n" + ", ".join(bookingData))

        # --- Payment File ---

        paymentId = identify_next_paymentID("Payments.txt")
        paymentData = [
            paymentId,
            bookingId,
            f"RM{final_price:.2f}",
            paymentMethod,
            paymentDate,
            "Completed"
        ]

        with open("Payments.txt", "a") as file:
            file.write("\n" + ", ".join(paymentData))

        # --- Reserved Seats File ---
        if seatFlag == 0:
            # First booking for this show
            with open("Reserved_seats.txt", "a") as file:
                file.write(f"\n{showId}, {' '.join(seatsSelected)}")

        elif seatFlag == 1:
            # Update existing reserved seats
            with open("Reserved_seats.txt", "r") as file:
                lines = file.readlines()
            seatData = {}
            for line in lines[1:]:  # skip header
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    show, seats = parts
                    seatData.update({show: seats.split(" ")})
            # Append new seats
            seatData[showId].extend(seatsSelected)

            # Rewrite file
            with open("Reserved_seats.txt", "w") as file:
                file.write("ShowID, Reserved Seats\n")
                seatItems = list(seatData.items())
                for i, (show, seats) in enumerate(seatItems):
                    line = f"{show}, {' '.join(seats)}"
                    if i < len(seatItems) - 1:
                        file.write(line + "\n")
                    else:
                        file.write(line)

        # --- Generate Receipt ---
        while True:
            receiptChoice = input("Booking successful! Print receipt? (Y/N): ").strip().lower()
            if receiptChoice == "y":
                print()
                generate_receipt(
                    payment_id=paymentId,
                    payment_date=paymentDate,
                    payment_method=paymentMethod,
                    booking_id=bookingId,
                    username=username,
                    status="CONFIRMED",
                    movie=showTitle,
                    auditorium=auditoriumId,
                    date=showDate,
                    time=showTime,
                    seats=seatsSelected,
                    price_each=priceEach,
                    final_price=final_price
                )
                input("Receipt printed successfully. Enjoy your movie! (Press ENTER to continue) ")
                break
            elif receiptChoice == "n":
                print("No receipt will be printed. Redirecting to booking menu...")
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
        break


# --- CUSTOMER MENU ---
def customer_menu():
    current_customer = None  

    while True:
        print("\n" + "="*50)
        print("    Customer Menu")
        print("="*50)
        
        if current_customer is None:
           
            print("Authentication Required")
            print("1. Register New Account")
            print("2. Login to Your Account")
            print("3. Back to Main Menu")
        else:
           
            print(f"Welcome back, {current_username}!")
            print("3. View Movies")
            print("4. Book Tickets")
            print("5. View Booking History")
            print("6. Update Profile")
            print("7. Logout")
            print("8. Back to Main Menu")
        
        print("="*50)
        choice = input("Please enter your choice: ").strip()
        
        if current_customer is None:
            
            if choice == '1':
                customer_register()
            elif choice == '2':
                current_customer, current_username = customer_login()  
            elif choice == '3':
                print("Returning to main menu...")
                return
            else:
                print("Invalid choice. Please try again.")
        
        else:
            if choice == '3':
                view_movies()
            elif choice == '4':
                book_tickets(role = current_customer, defaultUsername = current_username)
            elif choice == '5':
                view_booking_history(current_username)
            elif choice == '6':
                update_profile(current_customer)
            elif choice == '7':
                print("Logging out...")
                current_customer = None  
            elif choice == '8':
                print("Returning to main menu...")
                return
            else:
                print(" Invalid choice. Please try again.")
#----------------------------------- CUSTOMER MENU -----------------------------------



#----------------------------------- TECHICIAN MENU -----------------------------------
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
#----------------------------------- TECHICIAN MENU -----------------------------------



#----------------------------------- MAIN MENU -----------------------------------
def display_cinema_name():
    # Shows the cinema name in a billboard style
    print("    O=================================O")
    print("\033[1m    |   🌙 DreamSight Cinema (DSC)    | \033[0m")
    print("    O=================================O\n")

def main():
    while True:
        display_cinema_name()
        print("Please select your role to continue:\n")
        print("1. Ticketing Clerk")
        print("2. Cinema Manager")
        print("3. Technician")
        print("4. Customer")
        print("5. Exit")
        
        choice = input("Enter your role (1-5): ")

        if choice == "1":
            ticketing_clerk_menu()
        elif choice == "2":
            manager_login()
            cinema_manager_menu()
        elif choice == "3":
            technician_menu()
        elif choice == "4":
            customer_menu()
        elif choice == "5":
            print("Exiting system... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.\n")
#----------------------------------- MAIN MENU -----------------------------------

main()