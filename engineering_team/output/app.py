import gradio as gr
from mac_center import MACCenter

# Initialize the MAC Center backend
mac = MACCenter()

# Define the UI functions
def register(name, email, password, confirm_password, phone_number, address, gender, occupation, portfolio_str, interests_str):
    try:
        portfolio = eval(portfolio_str)
        interests = [i.strip() for i in interests_str.split(",") if i.strip()]
    except:
        return "Invalid portfolio format. Use a Python dict like: {'initial_deposit': 1000.0, 'current_value': 1200.0, 'holdings': {'Stock A': 10}}"
    
    success = mac.register(name, email, password, confirm_password, phone_number, address, gender, occupation, portfolio, interests)
    return "Registration successful!" if success else "Registration failed. Check inputs (email unique, passwords match, portfolio valid)."

def login(email, password):
    success = mac.login(email, password)
    return "Login successful!" if success else "Login failed. Check email and password."

def logout():
    success = mac.logout()
    return "Logged out." if success else "No user logged in."

def view_profile():
    profile = mac.view_profile()
    if profile is None:
        return "No user logged in."
    return f"Profile:\nName: {profile['name']}\nEmail: {profile['email']}\nPhone: {profile['phone_number']}\nAddress: {profile['address']}\nGender: {profile['gender']}\nOccupation: {profile['occupation']}\nPortfolio: {profile['portfolio']}\nInterests: {profile['interests']}\nEnrolled Clubs: {profile['enrolled_clubs']}\nInterested Clubs: {profile['interested_clubs']}"

def edit_profile(name, phone_number, address, gender, occupation, portfolio_str, interests_str):
    if mac.logged_in_user is None:
        return "No user logged in."
    try:
        portfolio = eval(portfolio_str)
        interests = [i.strip() for i in interests_str.split(",") if i.strip()]
    except:
        return "Invalid portfolio format. Use a Python dict like: {'initial_deposit': 1000.0, 'current_value': 1200.0, 'holdings': {'Stock A': 10}}"
    
    success = mac.edit_profile(name=name, phone_number=phone_number, address=address, gender=gender, occupation=occupation, portfolio=portfolio, interests=interests)
    return "Profile updated!" if success else "Update failed. Check portfolio format."

def delete_account(password):
    success = mac.delete_account(password)
    return "Account deleted." if success else "Deletion failed. Wrong password or no user logged in."

def list_all_clubs():
    clubs = mac.list_all_clubs()
    if clubs is None:
        return "No clubs available."
    return "\n".join([f"{c['club_id']}: {c['name']} - {c['description']}" for c in clubs])

def enroll_club(club_id):
    success = mac.enroll_in_club(club_id)
    return f"Enrolled in club {club_id}!" if success else "Enrollment failed. Invalid club ID or already enrolled."

def deenroll_club(club_id):
    success = mac.deenroll_from_club(club_id)
    return f"Deenrolled from club {club_id}!" if success else "Deenrollment failed. Invalid club ID or not enrolled."

def list_enrolled_clubs():
    clubs = mac.list_enrolled_clubs()
    if clubs is None:
        return "No user logged in."
    if not clubs:
        return "Not enrolled in any clubs."
    return "\n".join([f"{c['club_id']}: {c['name']}" for c in clubs])

def list_not_enrolled_clubs():
    clubs = mac.list_not_enrolled_clubs()
    if clubs is None:
        return "No user logged in."
    if not clubs:
        return "Enrolled in all clubs."
    return "\n".join([f"{c['club_id']}: {c['name']}" for c in clubs])

def add_interest(club_id):
    success = mac.add_interest_in_club(club_id)
    return f"Added interest in club {club_id}!" if success else "Failed. Invalid club ID or already interested."

def remove_interest(club_id):
    success = mac.remove_interest_in_club(club_id)
    return f"Removed interest from club {club_id}!" if success else "Failed. Invalid club ID or not interested."

def list_interested_clubs():
    clubs = mac.list_interested_clubs()
    if clubs is None:
        return "No user logged in."
    if not clubs:
        return "Not interested in any clubs."
    return "\n".join([f"{c['club_id']}: {c['name']}" for c in clubs])

def list_not_interested_clubs():
    clubs = mac.list_not_interested_clubs()
    if clubs is None:
        return "No user logged in."
    if not clubs:
        return "Interested in all clubs."
    return "\n".join([f"{c['club_id']}: {c['name']}" for c in clubs])

def portfolio_summary():
    summary = mac.calculate_portfolio_summary()
    if summary is None:
        return "No user logged in."
    return f"Total Value: {summary['total_value']}\nProfit/Loss: {summary['profit_loss']}"

# Create the Gradio interface
with gr.Blocks(title="MAC Center Demo") as demo:
    gr.Markdown("# MAC Center Member Management System")
    
    with gr.Tab("Register"):
        name = gr.Textbox(label="Name")
        email = gr.Textbox(label="Email")
        password = gr.Textbox(label="Password", type="password")
        confirm_password = gr.Textbox(label="Confirm Password", type="password")
        phone_number = gr.Textbox(label="Phone Number")
        address = gr.Textbox(label="Address")
        gender = gr.Textbox(label="Gender")
        occupation = gr.Textbox(label="Occupation")
        portfolio = gr.Textbox(label="Portfolio (Python dict)", value="{'initial_deposit': 1000.0, 'current_value': 1200.0, 'holdings': {'Stock A': 10}}")
        interests = gr.Textbox(label="Interests (comma-separated)", value="AI, Finance")
        register_btn = gr.Button("Register")
        register_output = gr.Textbox(label="Output")
        register_btn.click(register, inputs=[name, email, password, confirm_password, phone_number, address, gender, occupation, portfolio, interests], outputs=register_output)
    
    with gr.Tab("Login/Logout"):
        login_email = gr.Textbox(label="Email")
        login_password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        logout_btn = gr.Button("Logout")
        login_output = gr.Textbox(label="Output")
        login_btn.click(login, inputs=[login_email, login_password], outputs=login_output)
        logout_btn.click(logout, outputs=login_output)
    
    with gr.Tab("Profile"):
        view_profile_btn = gr.Button("View Profile")
        profile_output = gr.Textbox(label="Profile", lines=10)
        view_profile_btn.click(view_profile, outputs=profile_output)
        
        gr.Markdown("### Edit Profile")
        edit_name = gr.Textbox(label="Name")
        edit_phone = gr.Textbox(label="Phone Number")
        edit_address = gr.Textbox(label="Address")
        edit_gender = gr.Textbox(label="Gender")
        edit_occupation = gr.Textbox(label="Occupation")
        edit_portfolio = gr.Textbox(label="Portfolio (Python dict)", value="{'initial_deposit': 1000.0, 'current_value': 1200.0, 'holdings': {'Stock A': 10}}")
        edit_interests = gr.Textbox(label="Interests (comma-separated)", value="AI, Finance")
        edit_btn = gr.Button("Update Profile")
        edit_output = gr.Textbox(label="Output")
        edit_btn.click(edit_profile, inputs=[edit_name, edit_phone, edit_address, edit_gender, edit_occupation, edit_portfolio, edit_interests], outputs=edit_output)
        
        gr.Markdown("### Delete Account")
        delete_password = gr.Textbox(label="Password", type="password")
        delete_btn = gr.Button("Delete Account")
        delete_output = gr.Textbox(label="Output")
        delete_btn.click(delete_account, inputs=[delete_password], outputs=delete_output)
    
    with gr.Tab("Clubs"):
        gr.Markdown("### All Clubs")
        list_clubs_btn = gr.Button("List All Clubs")
        clubs_output = gr.Textbox(label="Clubs", lines=10)
        list_clubs_btn.click(list_all_clubs, outputs=clubs_output)
        
        gr.Markdown("### Enroll/Deenroll")
        club_id_enroll = gr.Textbox(label="Club ID (e.g., club_1)")
        enroll_btn = gr.Button("Enroll")
        deenroll_btn = gr.Button("Deenroll")
        enroll_output = gr.Textbox(label="Output")
        enroll_btn.click(enroll_club, inputs=[club_id_enroll], outputs=enroll_output)
        deenroll_btn.click(deenroll_club, inputs=[club_id_enroll], outputs=enroll_output)
        
        gr.Markdown("### Enrolled Clubs")
        enrolled_btn = gr.Button("List Enrolled Clubs")
        enrolled_output = gr.Textbox(label="Enrolled Clubs", lines=5)
        enrolled_btn.click(list_enrolled_clubs, outputs=enrolled_output)
        
        gr.Markdown("### Not Enrolled Clubs")
        not_enrolled_btn = gr.Button("List Not Enrolled Clubs")
        not_enrolled_output = gr.Textbox(label="Not Enrolled Clubs", lines=5)
        not_enrolled_btn.click(list_not_enrolled_clubs, outputs=not_enrolled_output)
        
        gr.Markdown("### Interest Management")
        club_id_interest = gr.Textbox(label="Club ID (e.g., club_1)")
        add_interest_btn = gr.Button("Add Interest")
        remove_interest_btn = gr.Button("Remove Interest")
        interest_output = gr.Textbox(label="Output")
        add_interest_btn.click(add_interest, inputs=[club_id_interest], outputs=interest_output)
        remove_interest_btn.click(remove_interest, inputs=[club_id_interest], outputs=interest_output)
        
        gr.Markdown("### Interested Clubs")
        interested_btn = gr.Button("List Interested Clubs")
        interested_output = gr.Textbox(label="Interested Clubs", lines=5)
        interested_btn.click(list_interested_clubs, outputs=interested_output)
        
        gr.Markdown("### Not Interested Clubs")
        not_interested_btn = gr.Button("List Not Interested Clubs")
        not_interested_output = gr.Textbox(label="Not Interested Clubs", lines=5)
        not_interested_btn.click(list_not_interested_clubs, outputs=not_interested_output)
    
    with gr.Tab("Portfolio"):
        summary_btn = gr.Button("Calculate Portfolio Summary")
        summary_output = gr.Textbox(label="Summary")
        summary_btn.click(portfolio_summary, outputs=summary_output)

# Run the app
if __name__ == "__main__":
    demo.launch()