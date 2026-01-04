import gradio as gr
from engineering_team.output.mac_center1 import MACCenter

# Initialize MACCenter instance
mac_center = MACCenter()

# Handle registration
def register(name, email, password, confirm_password, phone, address, gender, occupation, portfolio, interests):
    portfolio_dict = {k.strip(): float(v.strip()) for k, v in (item.split(':') for item in portfolio.split(','))}
    interests_list = [item.strip() for item in interests.split(',')]
    return mac_center.register_member(name, email, password, confirm_password, phone, address, gender, occupation, portfolio_dict, interests_list)

# Handle login
def login(email, password):
    return mac_center.login(email, password)

# Handle logout
def logout():
    return mac_center.logout()

# Show user profile
def view_profile():
    return mac_center.view_profile()

# View all available clubs
def view_clubs():
    return list(mac_center.view_clubs())

# Enroll in a club
def enroll_club(club_name):
    return mac_center.enroll_in_club(club_name)

# Deenroll from a club
def deenroll_club(club_name):
    return mac_center.deenroll_from_club(club_name)

# View clubs enrolled
def view_enrolled_clubs():
    return mac_center.view_enrolled_clubs()

# Calculate portfolio
def calculate_portfolio():
    return mac_center.calculate_portfolio_value()

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# MAC Center Member Management")

    with gr.Tabs():
        with gr.TabItem("Register"):
            reg_name = gr.Text(label="Name")
            reg_email = gr.Text(label="Email")
            reg_password = gr.Text(label="Password", type="password")
            reg_confirm_password = gr.Text(label="Confirm Password", type="password")
            reg_phone = gr.Text(label="Phone Number")
            reg_address = gr.Text(label="Address")
            reg_gender = gr.Text(label="Gender")
            reg_occupation = gr.Text(label="Occupation")
            reg_portfolio = gr.Text(label="Portfolio (e.g. stocks:1000, bonds:500)")
            reg_interests = gr.Text(label="Interests (e.g. AI Club, Book Club)")

            reg_btn = gr.Button("Register")
            reg_output = gr.Textbox(label="Registration Result")

            reg_btn.click(register, inputs=[reg_name, reg_email, reg_password, reg_confirm_password,
                                            reg_phone, reg_address, reg_gender, reg_occupation, 
                                            reg_portfolio, reg_interests], outputs=reg_output)

        with gr.TabItem("Login"):
            login_email = gr.Text(label="Email")
            login_password = gr.Text(label="Password", type="password")
            
            login_btn = gr.Button("Login")
            login_output = gr.Textbox(label="Login Result")
            
            login_btn.click(login, inputs=[login_email, login_password], outputs=login_output)
        
        with gr.TabItem("Profile"):
            profile_btn = gr.Button("View Profile")
            profile_output = gr.Textbox(label="Profile")

            profile_btn.click(view_profile, outputs=profile_output)

        with gr.TabItem("Clubs"):
            clubs_btn = gr.Button("View All Clubs")
            clubs_output = gr.List(label="Clubs")
            clubs_btn.click(view_clubs, outputs=clubs_output)

            enroll_club_input = gr.Text(label="Club to Enroll")
            enroll_club_btn = gr.Button("Enroll in Club")
            enroll_club_output = gr.Textbox(label="Enroll Result")
            enroll_club_btn.click(enroll_club, inputs=[enroll_club_input], outputs=enroll_club_output)

            deenroll_club_input = gr.Text(label="Club to Deenroll")
            deenroll_club_btn = gr.Button("Deenroll from Club")
            deenroll_club_output = gr.Textbox(label="Deenroll Result")
            deenroll_club_btn.click(deenroll_club, inputs=[deenroll_club_input], outputs=deenroll_club_output)

            enrolled_clubs_btn = gr.Button("View Enrolled Clubs")
            enrolled_clubs_output = gr.List(label="Enrolled Clubs")
            enrolled_clubs_btn.click(view_enrolled_clubs, outputs=enrolled_clubs_output)

        with gr.TabItem("Portfolio"):
            portfolio_btn = gr.Button("Calculate Portfolio Value")
            portfolio_output = gr.Textbox(label="Portfolio Value")
            portfolio_btn.click(calculate_portfolio, outputs=portfolio_output)

        with gr.TabItem("Logout"):
            logout_btn = gr.Button("Logout")
            logout_output = gr.Textbox(label="Logout Result")
            logout_btn.click(logout, outputs=logout_output)

if __name__ == "__main__":
    demo.launch()
