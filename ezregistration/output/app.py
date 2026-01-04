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
    
    # Create HTML for event grid with numbered buttons
    event_html = "<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;'>"
    for event in events:
        event_html += f"""
        <div style='border: 2px solid #4CAF50; padding: 15px; border-radius: 8px; background: #f9f9f9;'>
            <h3 style='color: #2c3e50; margin-top: 0;'>{event.name}</h3>
            <p><strong>Date:</strong> {event.date}</p>
            <p><strong>Time:</strong> {event.time}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p style='color: #555;'>{event.description[:80]}...</p>
            <p style='color: #888; font-size: 0.9em; margin-top: 10px;'>
                <em>Click "View Event {event.id}" button below to register</em>
            </p>
        </div>
        """
    event_html += "</div>"
    
    # Add user info if logged in
    user_info = ""
    if current_user_id:
        user = backend.users.get(current_user_id)
        if user:
            user_info = f"""
            <div style='background: #e8f5e9; padding: 15px; margin-bottom: 20px; border-radius: 8px; border: 2px solid #4CAF50;'>
                <h3 style='color: #2e7d32; margin-top: 0;'>✓ Logged in as: {user.name}</h3>
                <p style='margin: 5px 0;'><strong>Email:</strong> {user.email}</p>
                <p style='color: #666; margin-bottom: 0;'>Use the buttons below to view your registrations or reports</p>
            </div>
            """
    
    return f"""
    <div style='max-width: 1200px; margin: 0 auto;'>
        <h1 style='color: #1976d2; text-align: center;'>🎉 Event Registration System</h1>
        {user_info}
        <h2 style='color: #424242; border-bottom: 2px solid #1976d2; padding-bottom: 10px;'>Upcoming Events</h2>
        {event_html}
        <div style='margin-top: 30px; padding: 20px; background: #f5f5f5; border-radius: 8px;'>
            <h3 style='color: #424242;'>Quick Actions</h3>
            <p style='color: #666;'>Use the buttons below to navigate:</p>
            <ul style='color: #666;'>
                <li>Click <strong>View Event 1-6</strong> buttons to see event details and register</li>
                <li>Click <strong>My Registrations</strong> to see your registered events</li>
                <li>Click <strong>View Report</strong> to see registration statistics</li>
                <li>Click <strong>Delete Account</strong> to remove your account</li>
            </ul>
        </div>
    </div>
    """

def get_event_page(event_id):
    """Create event details page."""
    event = backend.get_event_by_id(event_id)
    if not event:
        return """
        <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
            <h2 style='color: #d32f2f;'>❌ Event not found</h2>
            <p>The requested event does not exist.</p>
            <p style='color: #666;'>Click the <strong>Home</strong> button to return to the event list.</p>
        </div>
        """
    
    # Check if user is already registered
    already_registered = False
    if current_user_id:
        user = backend.users.get(current_user_id)
        if user and event_id in user.event_ids:
            already_registered = True
    
    registration_form = ""
    if already_registered:
        registration_form = """
        <div style='background: #fff3cd; padding: 20px; border-radius: 8px; border: 2px solid #ffc107; margin-top: 20px;'>
            <h3 style='color: #856404; margin-top: 0;'>✓ You are already registered for this event!</h3>
            <p style='color: #856404; margin-bottom: 0;'>Check "My Registrations" to see all your events.</p>
        </div>
        """
    else:
        registration_form = """
        <div style='background: #e3f2fd; padding: 20px; border-radius: 8px; border: 2px solid #2196F3; margin-top: 20px;'>
            <h3 style='color: #1565c0; margin-top: 0;'>📝 Register for this Event</h3>
            <p style='color: #666;'>Fill in the form below and click the <strong>Register</strong> button at the bottom.</p>
        </div>
        """
    
    return f"""
    <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
        <h1 style='color: #1976d2;'>{event.name}</h1>
        <div style='background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #1976d2;'>
            <p><strong style='color: #424242;'>Description:</strong> {event.description}</p>
            <p><strong style='color: #424242;'>📅 Date:</strong> {event.date}</p>
            <p><strong style='color: #424242;'>🕐 Time:</strong> {event.time}</p>
            <p><strong style='color: #424242;'>📍 Location:</strong> {event.location}</p>
        </div>
        
        {registration_form}
        
        <div style='margin-top: 30px; padding: 15px; background: #fffde7; border-radius: 8px;'>
            <p style='color: #f57f17; margin: 0;'><strong>💡 Tip:</strong> Click the <strong>Home</strong> button below to return to the event list.</p>
        </div>
    </div>
    """

def get_my_registrations():
    """Display user's registered events."""
    if not current_user_id:
        return """
        <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
            <h2 style='color: #f57c00;'>⚠️ No Active Account</h2>
            <p>Please register for an event first to create your account.</p>
            <p style='color: #666;'>Click the <strong>Home</strong> button to browse events and register.</p>
        </div>
        """
    
    events = backend.get_user_registrations(current_user_id)
    user = backend.users.get(current_user_id)
    
    if not events:
        return f"""
        <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
            <h1 style='color: #1976d2;'>My Event Registrations</h1>
            <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; border: 2px solid #4CAF50; margin-bottom: 20px;'>
                <p style='margin: 0;'><strong>Account:</strong> {user.name} ({user.email})</p>
            </div>
            <div style='background: #fff3cd; padding: 20px; border-radius: 8px; border: 2px solid #ffc107;'>
                <h3 style='color: #856404; margin-top: 0;'>No registrations found</h3>
                <p style='color: #856404; margin-bottom: 0;'>You haven't registered for any events yet. Click <strong>Home</strong> to browse events.</p>
            </div>
        </div>
        """
    
    events_html = ""
    for i, event in enumerate(events, 1):
        events_html += f"""
        <div style='border: 2px solid #4CAF50; padding: 20px; border-radius: 8px; background: #f1f8f4; margin-bottom: 15px;'>
            <h3 style='color: #2e7d32; margin-top: 0;'>✓ {event.name}</h3>
            <p><strong>📅 Date:</strong> {event.date} at {event.time}</p>
            <p><strong>📍 Location:</strong> {event.location}</p>
            <p style='color: #555;'>{event.description}</p>
        </div>
        """
    
    return f"""
    <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
        <h1 style='color: #1976d2;'>My Event Registrations</h1>
        <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; border: 2px solid #4CAF50; margin-bottom: 20px;'>
            <p style='margin: 5px 0;'><strong>Account:</strong> {user.name}</p>
            <p style='margin: 5px 0;'><strong>Email:</strong> {user.email}</p>
            <p style='margin: 5px 0;'><strong>Phone:</strong> {user.phone}</p>
        </div>
        <h2 style='color: #424242;'>Registered Events ({len(events)})</h2>
        {events_html}
        <div style='margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px;'>
            <p style='color: #1565c0; margin: 0;'><strong>💡 Tip:</strong> Click <strong>Home</strong> to view more events or <strong>Delete Account</strong> to remove all registrations.</p>
        </div>
    </div>
    """

def get_report_page():
    """Display registration report."""
    report = backend.get_detailed_report()
    
    if not report:
        return """
        <div style='max-width: 1000px; margin: 0 auto; padding: 20px;'>
            <h2 style='color: #f57c00;'>No registration data available</h2>
            <p>No one has registered for any events yet.</p>
            <p style='color: #666;'>Click the <strong>Home</strong> button to return to the event list.</p>
        </div>
        """
    
    # Calculate totals
    total_registrations = sum(item['registrations'] for item in report)
    
    # Create table
    table_html = """
    <table style='width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <thead>
            <tr style='background: #1976d2; color: white;'>
                <th style='padding: 15px; text-align: left; border: 1px solid #ddd;'>Event ID</th>
                <th style='padding: 15px; text-align: left; border: 1px solid #ddd;'>Event Name</th>
                <th style='padding: 15px; text-align: center; border: 1px solid #ddd;'>Registrations</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for item in report:
        bg_color = '#f9f9f9' if item['registrations'] > 0 else '#fff'
        table_html += f"""
        <tr style='background: {bg_color};'>
            <td style='padding: 12px 15px; border: 1px solid #ddd;'>{item['event_id']}</td>
            <td style='padding: 12px 15px; border: 1px solid #ddd;'>{item['event_name']}</td>
            <td style='padding: 12px 15px; text-align: center; border: 1px solid #ddd; font-weight: bold; color: #1976d2;'>{item['registrations']}</td>
        </tr>
        """
    table_html += "</tbody></table>"
    
    return f"""
    <div style='max-width: 1000px; margin: 0 auto; padding: 20px;'>
        <h1 style='color: #1976d2;'>📊 Registration Report</h1>
        <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 2px solid #4CAF50;'>
            <h3 style='color: #2e7d32; margin: 5px 0;'>Summary Statistics</h3>
            <p style='margin: 5px 0;'><strong>Total Events:</strong> {len(report)}</p>
            <p style='margin: 5px 0;'><strong>Total Registrations:</strong> {total_registrations}</p>
            <p style='margin: 5px 0;'><strong>Average Registrations per Event:</strong> {total_registrations / len(report):.1f}</p>
        </div>
        <h2 style='color: #424242;'>Detailed Breakdown</h2>
        {table_html}
        <div style='margin-top: 20px; padding: 15px; background: #fffde7; border-radius: 8px;'>
            <p style='color: #f57f17; margin: 0;'><strong>💡 Tip:</strong> Click <strong>Home</strong> to return to the event list.</p>
        </div>
    </div>
    """

def get_delete_account_page():
    """Page for deleting user account."""
    if not current_user_id:
        return """
        <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
            <h2 style='color: #f57c00;'>No account to delete</h2>
            <p>You don't have an active account.</p>
            <p style='color: #666;'>Click the <strong>Home</strong> button to browse events and register.</p>
        </div>
        """
    
    user = backend.users.get(current_user_id)
    events = backend.get_user_registrations(current_user_id)
    event_count = len(events) if events else 0
    
    return f"""
    <div style='max-width: 800px; margin: 0 auto; padding: 20px;'>
        <h1 style='color: #d32f2f;'>⚠️ Delete Account</h1>
        <div style='background: #ffebee; padding: 20px; border-radius: 8px; border: 2px solid #f44336; margin-bottom: 20px;'>
            <h3 style='color: #c62828; margin-top: 0;'>Warning: This action cannot be undone!</h3>
            <p style='color: #c62828;'><strong>Account Details:</strong></p>
            <ul style='color: #c62828;'>
                <li>Name: {user.name}</li>
                <li>Email: {user.email}</li>
                <li>Phone: {user.phone}</li>
                <li>Registered Events: {event_count}</li>
            </ul>
            <p style='color: #c62828; margin-bottom: 0;'>
                Deleting your account will permanently remove all your event registrations.
                This action cannot be undone.
            </p>
        </div>
        
        <div style='background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <p style='color: #1565c0; margin: 0;'><strong>💡 Tip:</strong> Click the <strong>Confirm Delete</strong> button below to permanently delete your account, or click <strong>Home</strong> to cancel.</p>
        </div>
    </div>
    """

# Gradio functions
def register_user(event_id, name, email, phone):
    """Register user for event."""
    global current_user_id
    
    # Validate inputs
    if not name or not email or not phone:
        return False, "Please fill in all fields"
    
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
    gr.Markdown("# 🎉 Event Registration System")
    gr.Markdown("*A simple system for managing event registrations*")
    
    # Hidden state for current page and event
    current_page = gr.State("home")
    selected_event_id = gr.State(1)
    
    # Main display area
    display_html = gr.HTML(value=get_home_page())
    
    # Navigation buttons - VISIBLE and functional
    gr.Markdown("---")
    gr.Markdown("### Navigation")
    
    with gr.Row():
        nav_home = gr.Button("🏠 Home", variant="primary")
        nav_my_reg = gr.Button("📋 My Registrations")
        nav_report = gr.Button("📊 View Report")
        nav_delete = gr.Button("🗑️ Delete Account", variant="stop")
    
    gr.Markdown("### Event Details")
    with gr.Row():
        nav_event1 = gr.Button("View Event 1")
        nav_event2 = gr.Button("View Event 2")
        nav_event3 = gr.Button("View Event 3")
    with gr.Row():
        nav_event4 = gr.Button("View Event 4")
        nav_event5 = gr.Button("View Event 5")
        nav_event6 = gr.Button("View Event 6")
    
    # Registration form (shown when on event page)
    gr.Markdown("---")
    gr.Markdown("### Registration Form")
    gr.Markdown("*Fill in your details below when viewing an event to register*")
    
    with gr.Row():
        reg_name = gr.Textbox(label="Your Name", placeholder="John Doe")
        reg_email = gr.Textbox(label="Your Email", placeholder="john@example.com")
        reg_phone = gr.Textbox(label="Your Phone", placeholder="+1234567890")
    
    with gr.Row():
        register_btn = gr.Button("✅ Register for Selected Event", variant="primary", size="lg")
        delete_confirm_btn = gr.Button("❌ Confirm Delete Account", variant="stop", size="lg")
    
    # Status message
    status_msg = gr.Textbox(label="Status", interactive=False, visible=True)
    
    # Event handlers for navigation
    def go_home():
        return "home", get_home_page(), ""
    
    def go_event(event_num):
        return f"event-{event_num}", get_event_page(event_num), f"Viewing Event {event_num}"
    
    nav_home.click(go_home, outputs=[current_page, display_html, status_msg])
    nav_event1.click(lambda: go_event(1), outputs=[current_page, display_html, status_msg]).then(lambda: 1, outputs=[selected_event_id])
    nav_event2.click(lambda: go_event(2), outputs=[current_page, display_html, status_msg]).then(lambda: 2, outputs=[selected_event_id])
    nav_event3.click(lambda: go_event(3), outputs=[current_page, display_html, status_msg]).then(lambda: 3, outputs=[selected_event_id])
    nav_event4.click(lambda: go_event(4), outputs=[current_page, display_html, status_msg]).then(lambda: 4, outputs=[selected_event_id])
    nav_event5.click(lambda: go_event(5), outputs=[current_page, display_html, status_msg]).then(lambda: 5, outputs=[selected_event_id])
    nav_event6.click(lambda: go_event(6), outputs=[current_page, display_html, status_msg]).then(lambda: 6, outputs=[selected_event_id])
    nav_my_reg.click(lambda: ("my-registrations", get_my_registrations(), "Viewing your registrations"), outputs=[current_page, display_html, status_msg])
    nav_report.click(lambda: ("report", get_report_page(), "Viewing registration report"), outputs=[current_page, display_html, status_msg])
    nav_delete.click(lambda: ("delete-account", get_delete_account_page(), "Account deletion page"), outputs=[current_page, display_html, status_msg])
    
    # Registration handler
    def handle_registration(event_id, name, email, phone):
        success, message = register_user(event_id, name, email, phone)
        if success:
            return get_home_page(), f"✅ Success: {message}", "", "", ""
        else:
            return get_event_page(event_id), f"❌ Error: {message}", name, email, phone
    
    register_btn.click(
        handle_registration,
        inputs=[selected_event_id, reg_name, reg_email, reg_phone],
        outputs=[display_html, status_msg, reg_name, reg_email, reg_phone]
    )
    
    # Delete account handler
    def handle_delete():
        success, message = delete_user_account()
        if success:
            return get_home_page(), f"✅ {message}"
        else:
            return get_delete_account_page(), f"❌ Error: {message}"
    
    delete_confirm_btn.click(
        handle_delete,
        outputs=[display_html, status_msg]
    )

# For direct execution
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7866, share=True)
