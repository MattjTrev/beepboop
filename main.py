import tkinter.messagebox as tkmessagebox
import smtplib
import tempfile
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from email.mime.image import MIMEImage

class PotholeReporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PublicWorksPal")

        # City
        self.city_label = tk.Label(root, text="City:")
        self.city_label.pack()

        self.city_entry = tk.Entry(root)
        self.city_entry.pack()

        # Street
        self.street_label = tk.Label(root, text="Street:")
        self.street_label.pack()

        self.street_entry = tk.Entry(root)
        self.street_entry.pack()

        # Zip Code
        self.zip_label = tk.Label(root, text="Zip Code:")
        self.zip_label.pack()

        self.zip_entry = tk.Entry(root)
        self.zip_entry.pack()

        # Description
        self.description_label = tk.Label(root, text="Description:")
        self.description_label.pack()

        self.description_entry = tk.Text(root, height=5, width=40)
        self.description_entry.pack()

        # Severity
        self.severity_label = tk.Label(root, text="Severity:")
        self.severity_label.pack()

        self.severity_slider = tk.Scale(root, from_=1, to=10, orient="horizontal")
        self.severity_slider.pack()

        # Photo
        self.photo_label = tk.Label(root, text="Photo:")
        self.photo_label.pack()

        self.photo_button = tk.Button(root, text="Add Photo", command=self.add_photo)
        self.photo_button.pack()

        # Report Pothole
        self.report_button = tk.Button(root, text="Report problem", command=self.report_pothole)
        self.report_button.pack()

        self.reports = []

    def add_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            self.photo_path = file_path  # Save the file path

            # Create a PhotoImage object to load the image
            self.photo_image = tk.PhotoImage(file=file_path)

            # Resize the image
            image = Image.open(file_path)
            image = image.resize((100, 100))  # Adjust the size as needed
            resized_photo = ImageTk.PhotoImage(image)

            # Set the resized image to the photo_label
            self.photo_label.config(image=resized_photo)
            self.photo_label.photo = resized_photo  # Keep a reference to the image to prevent it from being garbage
    def report_pothole(self):
        city = self.city_entry.get()
        street = self.street_entry.get()
        zip_code = self.zip_entry.get()
        description = self.description_entry.get("1.0", tk.END)
        severity = self.severity_slider.get()

        if city and street and zip_code and description:
            location = f"City: {city}\n Street: {street}\n Zip Code: {zip_code}\n"
            report = f" {location}\nDescription: {description}\nSeverity: {severity}"

            if hasattr(self, 'photo_image'):
                # Report the image path, if available
                report += f"\nPhoto: {self.photo_path}"

            self.reports.append(report)
            self.clear_entries()
            self.show_thank_you_page()
        else:
            # Display an error message if any required field is empty
            tk.messagebox.showerror("Error", "Please fill out all the required fields.")

    def send_email(self, report):
        # Email configuration
        smtp_server = "smtp.office365.com"
        smtp_port = 587
        sender_email = "mattjtrevino@outlook.com"
        sender_password = "Minecraft15$"
        recipient_email = "mattjtrevino@outlook.com"

        # Create a message object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = "Problem Report"

        # Add the report content to the email
        message.attach(MIMEText(report, 'plain'))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

            # Close the SMTP server connection
            server.quit()

            # Display a confirmation message
            tk.messagebox.showinfo("Success", "Report sent successfully via email.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        self.city_entry.delete(0, tk.END)
        self.street_entry.delete(0, tk.END)
        self.zip_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.photo_label.config(image=None)

    def show_thank_you_page(self):
        thank_you_window = tk.Toplevel(self.root)
        thank_you_window.geometry("450x300")  # Adjust the width and height as needed
        thank_you_window.title("Thank You!")

        thank_you_label = tk.Label(thank_you_window,
                                   text="Thank you for your concern! Please provide your email address.")
        thank_you_label.pack()

        email_label = tk.Label(thank_you_window, text="Email:")
        email_label.pack()

        email_entry = tk.Entry(thank_you_window)
        email_entry.pack()

        confirm_email_label = tk.Label(thank_you_window, text="Confirm Email:")
        confirm_email_label.pack()

        confirm_email_entry = tk.Entry(thank_you_window)
        confirm_email_entry.pack()

        submit_button = tk.Button(thank_you_window, text="Submit",
                                  command=lambda: self.submit_follow_up(email_entry.get(), confirm_email_entry.get(),
                                                                        thank_you_window))
        submit_button.pack()

    def submit_follow_up(self, email, confirm_email, window):
        if email == confirm_email:
            email_subject = "Thank you for your report! Problem Report Follow-up"
            email_body = "\n".join(self.reports)
            send_email(email, email_subject, email_body)
            window.destroy()
            self.root.quit()
        else:
            tkmessagebox.showinfo("Emails Mismatch", "Email and Confirm Email must match. Please try again.")


def send_email(to_email, subject, body):
    # Configure your email server and credentials here
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "mattjtrevino@outlook.com"
    smtp_password = "Minecraft15$"

    # Create an SMTP connection
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)

    # Start the TLS connection
    smtp_connection.starttls()

    # Login to your email account
    smtp_connection.login(smtp_username, smtp_password)

    # Create the email message
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send the email
    smtp_connection.sendmail(smtp_username, to_email, message.as_string())

    # Close the SMTP connection
    smtp_connection.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PotholeReporterApp(root)
    root.mainloop()