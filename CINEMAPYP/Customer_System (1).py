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

def save_seats(filename, seats):
    with open(filename, "w") as f:
        for row in seats:
            f.write(",".join(row) + "\n")

def load_seats(show_id, rows=10, cols=12):
    filename = f"{show_id}.txt"
    if not file_exists(filename):
        seats = [["O" for _ in range(cols)] for _ in range(rows)]
        save_seats(filename, seats)
    else:
        with open(filename, "r") as f:
            seats = [line.strip().split(",") for line in f]
    return seats

def display_seats(seats):
    print("\n   " + " ".join(str(i+1).rjust(2) for i in range(len(seats[0]))))
    for r_index, row in enumerate(seats):
        row_letter = chr(65 + r_index)
        print(f"{row_letter}  " + " ".join(s.rjust(2) for s in row))
    print("\nO = Available   X = Booked")

def choose_seat(seats):
    while True:
        seat_input = input("Enter seat (e.g. B3): ").upper().strip()
        if len(seat_input) < 2:
            print("Invalid format. Try again.")
            continue

        row_letter = seat_input[0]
        col_str = seat_input[1:]
        if not col_str.isdigit():
            print("Invalid seat number.")
            continue

        row_index = ord(row_letter) - 65
        col_index = int(col_str) - 1

        if row_index < 0 or row_index >= len(seats) or col_index < 0 or col_index >= len(seats[0]):
            print("Seat out of range.")
            continue

        if seats[row_index][col_index] == "X":
            print("That seat is already booked. Please choose another.")
        else:
            seats[row_index][col_index] = "X"
            print(f"Seat {seat_input} booked successfully!")
            return seat_input

def book_by_showid(customer_id):
    showtimes = load_showtimes()
    movie_prices = load_movie_prices()
    discounts = load_discounts()

    # Show all showtimes
    print("\n=== Available Showtimes ===")
    for show_id, info in showtimes.items():
        print(f"{show_id}: {info['title']} | {info['audi']} | {info['date']} | {info['time']}")

    # Loop until valid ShowID is entered
    while True:
        show_id = input("\nEnter ShowID to book (e.g. S7): ").upper().strip()
        if show_id in showtimes:
            break
        else:
            print("Invalid ShowID. Please try again.")

    info = showtimes[show_id]
    movie_title = info["title"]

    print(f"\n {movie_title}")
    print(f" {info['audi']}")
    print(f" {info['date']} at {info['time']}")

    # Ticket price lookup
    if movie_title in movie_prices:
        base_price = movie_prices[movie_title]
    else:
        print("Could not find price for this movie. Defaulting to RM 15.00")
        base_price = 15.00

    # Seat selection
    seats = load_seats(show_id)
    display_seats(seats)
    chosen_seat = choose_seat(seats)

    # Discount application
    final_price = base_price
    if discounts:
        print("\n=== Available Discounts ===")
        for disc_id, disc_info in discounts.items():
            print(f"{disc_id}: {disc_info['name']} ({disc_info['rate']}% off)")

        chosen_disc = input("\nEnter Discount ID to apply (or press Enter to skip): ").upper().strip()
        if chosen_disc in discounts:
            disc_rate = discounts[chosen_disc]["rate"]
            discount_amount = base_price * (disc_rate / 100)
            final_price = base_price - discount_amount
            print(f" {discounts[chosen_disc]['name']} applied! You saved Money by only spending RM {discount_amount:.2f}")
    print(f"\n Final Price: RM {final_price:.2f}")

    # Payment
    confirm = input("Proceed to payment? (Y/N): ").strip().upper()
    if confirm != "Y":
        # Free seat back
        row_letter = chosen_seat[0]
        col_index = int(chosen_seat[1:]) - 1
        row_index = ord(row_letter) - 65
        seats[row_index][col_index] = "O"
        print("Booking cancelled. Seat released.")
        input("\nPress Enter to return to menu...")
        return

    print("\nProcessing payment...", end="")
    import time
    time.sleep(1.5)
    print("Payment successful!")

    # Save seat file and record booking
    save_seats(f"{show_id}.txt", seats)
    with open("Bookings.txt", "a") as f:
        f.write(f"{customer_id},{show_id},{chosen_seat},RM {final_price:.2f}\n")

    print("\n Booking confirmed!")
    print(f"{movie_title} | {info['date']} {info['time']} | Seat: {chosen_seat}")
    print(f"Amount Paid: RM {final_price:.2f}")
    input("\nPress Enter to return to menu...")

def view_booking_history(customer_id):
    print("\n" + "="*40)
    print("       BOOKING HISTORY")
    print("="*40)

    try:
        with open("Bookings.txt", "r") as f:
            bookings = f.readlines()

        user_bookings = [line.strip().split(",") for line in bookings if line.startswith(customer_id + ",")]

        if not user_bookings:
            print("No bookings found.")
            return

        for booking in user_bookings:
            if len(booking) >= 4:
                show_id = booking[1]
                seat = booking[2]
                price = booking[3]

                showtimes = load_showtimes()
                if show_id in showtimes:
                    info = showtimes[show_id]
                    print(f"ShowID: {show_id}")
                    print(f"Movie: {info['title']}")
                    print(f"Date & Time: {info['date']} at {info['time']}")
                    print(f"Seat: {seat}")
                    print(f"Price Paid: {price}")
                    print("="*60)
                else:
                    print(f"ShowID: {show_id} (Details not found)")
                    print(f"Seat: {seat}")
                    print(f"Price Paid: {price}")
                    print("="*60)

    except FileNotFoundError:
        print("No bookings found.")
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
                book_by_showid(current_customer)
            elif choice == '5':
                view_booking_history(current_customer)
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

customer_menu()
        