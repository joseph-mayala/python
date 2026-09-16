
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
                                        booking.write(line + "\n")
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

ticketing_clerk_menu()