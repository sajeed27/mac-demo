import gradio as gr
from event_registration import EventRegistration
import pandas as pd

# Initialize backend
backend = EventRegistration()

# Global state for current user (simplified for single user demo)
current_user_id = None

def get_home_page():
    """Create the home page with event grid."""
    events = backend.get_all_events()
    
    # Create HTML for event grid
    event_html = "<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;'>"
    for event in events:
        event_html += f"""
        <div style='border: 1px solid #ccc; padding: 15px; border-radius: 8px; cursor: pointer;' 
             onclick='window.location.href="#event-{event.id}"'>
            <h3>{event.name}</h3>
            <p><strong>Date:</strong> {event.date}</p>
            <p><strong>Time:</strong> {event.time}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p>{event.description[:100]}...</p>
        </div>
        """
    event_html += "</div>"
    
    # Add user info if logged in
    user_info = ""
    if current_user_id:
        user = backend.users.get(current_user_id)
        if user:
            user_info = f"""
            <div style='background: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px;'>
                <h4>Logged in as: {user.name} ({user.email})</h4>
                <button onclick='window.location.href="#my-registrations"'>My Registrations</button>
                <button onclick='window.location.href="#report"'>View Report</button>
                <button onclick='window.location.href="#delete-account"'>Delete Account</button>
            </div>
            """
    
    return f"""
    <h1>Event Registration System</h1>
    {user_info}
    <h2>Upcoming Events</h2>
    {event_html}
    <div style='margin-top: 30px;'>
        <h3>Quick Actions</h3>
        <button onclick='window.location.href="#report"'>View Registration Report</button>
        <button onclick='window.location.href="#my-registrations"'>View My Registrations</button>
    </div>
    """

def get_event_page(event_id):
    """Create event details page."""
    event = backend.get_event_by_id(event_id)
    if not event:
        return "<h2>Event not found</h2><p><a href='#'>Back to Home</a></p>"
    
    return f"""
    <h1>{event.name}</h1>
    <div style='background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px;'>
        <p><strong>Description:</strong> {event.description}</p>
        <p><strong>Date:</strong> {event.date}</p>
        <p><strong>Time:</strong> {event.time}</p>
        <p><strong>Location:</strong> {event.location}</p>
    </div>
    
    <h2>Register for this Event</h2>
    <div id='registration-form'>
        <input type='text' id='name' placeholder='Your Name' style='width: 100%; padding: 8px; margin: 5px 0;'><br>
        <input type='email' id='email' placeholder='Your Email' style='width: 100%; padding: 8px; margin: 5px 0;'><br>
        <input type='tel' id='phone' placeholder='Your Phone Number' style='width: 100%; padding: 8px; margin: 5px 0;'><br>
        <button onclick='registerForEvent({event_id})'>Register Now</button>
    </div>
    <div id='registration-result' style='margin-top: 20px;'></div>
    
    <p style='margin-top: 30px;'><a href='#'>← Back to Home</a></p>
    
    <script>
    function registerForEvent(eventId) {{
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        
        // Simple validation
        if (!name || !email || !phone) {{
            document.getElementById('registration-result').innerHTML = 
                "<div style='color: red;'>Please fill all fields</div>";
            return;
        }}
        
        // Call backend via Gradio
        const result = registerUser(eventId, name, email, phone);
        if (result[0]) {{
            document.getElementById('registration-result').innerHTML = 
                "<div style='color: green; font-size: 1.2em;'>✓ You are registered for the event!</div>";
            document.getElementById('registration-form').style.display = 'none';
        }} else {{
            document.getElementById('registration-result').innerHTML = 
                "<div style='color: red;'>Error: " + result[1] + "</div>";
        }}
    }}
    </script>
    """

def get_my_registrations():
    """Display user's registered events."""
    if not current_user_id:
        return "<h2>Please register for an event first</h2><p><a href='#'>Back to Home</a></p>"
    
    events = backend.get_user_registrations(current_user_id)
    if not events:
        return "<h2>No registrations found</h2><p>You haven't registered for any events yet.</p><p><a href='#'>Back to Home</a></p>"
    
    events_html = "<div style='display: grid; gap: 15px;'>"
    for event in events:
        events_html += f"""
        <div style='border: 1px solid #4CAF50; padding: 15px; border-radius: 8px; background: #f0fff0;'>
            <h3>{event.name}</h3>
            <p><strong>Date:</strong> {event.date} at {event.time}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p>{event.description}</p>
        </div>
        """
    events_html += "</div>"
    
    return f"""
    <h1>My Event Registrations</h1>
    {events_html}
    <p style='margin-top: 30px;'><a href='#'>← Back to Home</a></p>
    """

def get_report_page():
    """Display registration report."""
    report = backend.get_detailed_report()
    
    if not report:
        return "<h2>No registration data available</h2><p><a href='#'>Back to Home</a></p>"
    
    # Create table
    table_html = "<table style='width: 100%; border-collapse: collapse;'>"
    table_html += "<tr style='background: #4CAF50; color: white;'><th>Event ID</th><th>Event Name</th><th>Registrations</th></tr>"
    
    for item in report:
        table_html += f"""
        <tr style='border-bottom: 1px solid #ddd;'>
            <td style='padding: 10px;'>{item['event_id']}</td>
            <td style='padding: 10px;'>{item['event_name']}</td>
            <td style='padding: 10px;'>{item['registrations']}</td>
        </tr>
        """
    table_html += "</table>"
    
    return f"""
    <h1>Registration Report</h1>
    <p>Total events: {len(report)}</p>
    {table_html}
    <p style='margin-top: 30px;'><a href='#'>← Back to Home</a></p>
    """

def get_delete_account_page():
    """Page for deleting user account."""
    if not current_user_id:
        return "<h2>No account to delete</h2><p><a href='#'>Back to Home</a></p>"
    
    return f"""
    <h1>Delete Account</h1>
    <div style='background: #fff3cd; padding: 20px; border-radius: 8px; border: 1px solid #ffeaa7;'>
        <h3 style='color: #856404;'>⚠️ Warning</h3>
        <p>This will permanently delete your account and all your event registrations.</p>
        <p>This action cannot be undone.</p>
        <button onclick='deleteAccount()' style='background: #dc3545; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;'>
            Delete My Account
        </button>
        <div id='delete-result' style='margin-top: 15px;'></div>
    </div>
    <p style='margin-top: 30px;'><a href='#'>← Back to Home</a></p>
    
    <script>
    function deleteAccount() {{
        const result = deleteUserAccount();
        if (result[0]) {{
            document.getElementById('delete-result').innerHTML = 
                "<div style='color: green;'>Account deleted successfully. <a href='#'>Return to Home</a></div>";
        }} else {{
            document.getElementById('delete-result').innerHTML = 
                "<div style='color: red;'>Error: " + result[1] + "</div>";
        }}
    }}
    </script>
    """

# Gradio functions
def register_user(event_id, name, email, phone):
    """Register user for event."""
    global current_user_id
    success, message, user_id = backend.register_user_for_event(event_id, name, email, phone)
    if success:
        current_user_id = user_id
    return success, message

def delete_user_account():
    """Delete current user account."""
    global current_user_id
    if current_user_id:
        success, message = backend.delete_user_account(current_user_id)
        if success:
            current_user_id = None
        return success, message
    return False, "No user account found"

def navigate_to(page):
    """Handle page navigation."""
    if page == "home":
        return get_home_page()
    elif page.startswith("event-"):
        event_id = int(page.split("-")[1])
        return get_event_page(event_id)
    elif page == "my-registrations":
        return get_my_registrations()
    elif page == "report":
        return get_report_page()
    elif page == "delete-account":
        return get_delete_account_page()
    return get_home_page()

# Create Gradio interface
with gr.Blocks(title="Event Registration System", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Event Registration System")
    gr.Markdown("A simple prototype for event registration management")
    
    # Hidden state for navigation
    current_page = gr.State("home")
    
    # Main display area
    display_html = gr.HTML(value=get_home_page())
    
    # Navigation buttons (hidden but accessible via JavaScript)
    with gr.Row(visible=False):
        nav_home = gr.Button("Home")
        nav_event1 = gr.Button("Event 1")
        nav_event2 = gr.Button("Event 2")
        nav_event3 = gr.Button("Event 3")
        nav_event4 = gr.Button("Event 4")
        nav_event5 = gr.Button("Event 5")
        nav_event6 = gr.Button("Event 6")
        nav_my_reg = gr.Button("My Registrations")
        nav_report = gr.Button("Report")
        nav_delete = gr.Button("Delete Account")
    
    # Register backend functions for JavaScript calls
    app.load(
        fn=lambda: None,
        inputs=[],
        outputs=[],
        js="""
        function() {
            window.registerUser = function(eventId, name, email, phone) {
                return gradioApp().querySelector('#register-btn').click();
            }
            window.deleteUserAccount = function() {
                return gradioApp().querySelector('#delete-btn').click();
            }
        }
        """
    )
    
    # Hidden buttons for backend calls
    with gr.Row(visible=False):
        register_btn = gr.Button("Register", elem_id="register-btn")
        delete_btn = gr.Button("Delete", elem_id="delete-btn")
    
    # Event handlers for navigation
    nav_home.click(lambda: "home", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_event1.click(lambda: "event-1", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_event2.click(lambda: "event-2", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_event3.click(lambda: "event-3", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_event4.click(lambda: "event-4", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_event5.click(lambda: "event-5", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_event6.click(lambda: "event-6", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_my_reg.click(lambda: "my-registrations", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_report.click(lambda: "report", outputs=current_page).then(navigate_to, current_page, display_html)
    nav_delete.click(lambda: "delete-account", outputs=current_page).then(navigate_to, current_page, display_html)
    
    # Backend function handlers
    register_btn.click(
        register_user,
        inputs=[gr.Number(visible=False, value=1), 
                gr.Textbox(visible=False), 
                gr.Textbox(visible=False), 
                gr.Textbox(visible=False)],
        outputs=[gr.Textbox(visible=False), gr.Textbox(visible=False)]
    ).then(lambda: "home", outputs=current_page).then(navigate_to, current_page, display_html)
    
    delete_btn.click(
        delete_user_account,
        inputs=[],
        outputs=[gr.Textbox(visible=False), gr.Textbox(visible=False)]
    ).then(lambda: "home", outputs=current_page).then(navigate_to, current_page, display_html)

# For direct execution
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7866, share=True)