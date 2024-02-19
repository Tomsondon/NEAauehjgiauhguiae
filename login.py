import tkinter
import database
import time
from tkinter import messagebox


class AccountManager:
    def __init__(self, user):
        self.window = tkinter.Tk()
        self.window.title("Account Manager")
        self.window.geometry('300x400')
        self.leaderboard = database.Leaderboard()
        self.user = user

    def displayWidgets(self, *widgets):
        for widget in widgets:
            widget.grid()

    def getUser(self):
        return self.user

    def attemptLogin(self, username, password):
        if self.leaderboard.checkValidLogin(username, password) == 0:
            self.leaderboard.close()
            self.user = username
            messagebox.showinfo("Successful login", f'Successfully logged in as {self.user}')
        elif self.leaderboard.checkValidLogin(username, password) == 1:
            messagebox.showwarning("Unsuccessful login", "Incorrect password")
        elif self.leaderboard.checkValidLogin(username, password) == 2:
            messagebox.showwarning("Unsuccessful login", "User does not exist")

    def createAccount(self, username, password):
        if not username:
            messagebox.showwarning("Issue", "Username is blank")
            return
        try:
            self.leaderboard.addUserToDatabase(username, password)
            self.leaderboard.close()
            self.user = username
            messagebox.showinfo("Successful creation", f'Successfully created account {self.user}')
        except:
            messagebox.showerror("Failure", "Failed to create user profile, profile likely already exists")

    def signOut(self):
        self.user = ""
        messagebox.showinfo("Successful sign out", f'Successfully signed out')

    def deleteAccount(self):
        try:
            self.leaderboard.deleteUser(self.user)
            self.leaderboard.close()
            self.user = ""
            messagebox.showinfo("Successful deletion", f"Successfully deleted account {self.user}")
        except:
            messagebox.showerror("Failure", f"Could not delete {self.user}")

    def signIn(self, *widgets):
        for widget in widgets:
            widget.destroy()
        usernameLabel = tkinter.Label(self.window, text="Username: ")
        username = tkinter.Entry(self.window)
        passwordLabel = tkinter.Label(self.window, text="Password: ")
        password = tkinter.Entry(self.window)
        logInButton = tkinter.Button(self.window, text="Log In",
                                     command=lambda: self.attemptLogin(username.get(), password.get()))
        goBackButton = tkinter.Button(self.window, text="Go back",
                                      command=lambda: self.main(usernameLabel, username, passwordLabel, password,
                                                                logInButton, goBackButton))
        self.displayWidgets(usernameLabel, username, passwordLabel, password, logInButton, goBackButton)

    def signUp(self, *widgets):
        for widget in widgets:
            widget.destroy()
        usernameLabel = tkinter.Label(self.window, text="Username: ")
        username = tkinter.Entry(self.window)
        passwordLabel = tkinter.Label(self.window, text="Password: ")
        password = tkinter.Entry(self.window)
        createAccountButton = tkinter.Button(self.window, text="Create Account",
                                             command=lambda: self.createAccount(username.get(), password.get()))
        goBackButton = tkinter.Button(self.window, text="Go back",
                                      command=lambda: self.main(usernameLabel, username, passwordLabel, password,
                                                                createAccountButton,
                                                                goBackButton))
        self.displayWidgets(usernameLabel, username, passwordLabel, password, createAccountButton, goBackButton)

    def deleteAccountMenu(self, *widgets):
        if self.user != "":
            for widget in widgets:
                widget.destroy()
            confirmationLabel = tkinter.Label(self.window, text="Are you sure you want to delete your account?")
            yesButton = tkinter.Button(self.window, text="Yes",
                                       command=lambda: self.deleteAccount())
            noButton = tkinter.Button(self.window, text="No",
                                      command=lambda: self.main(confirmationLabel, yesButton, noButton))
            self.displayWidgets(confirmationLabel, yesButton, noButton)

    def main(self, *widgets):
        for widget in widgets:
            widget.destroy()
        signInButton = tkinter.Button(self.window, text="Sign in",
                                      command=lambda: self.signIn(signInButton, signUpButton, signOutButton,
                                                                  deleteAccountButton))
        signUpButton = tkinter.Button(self.window, text="Sign up",
                                      command=lambda: self.signUp(signInButton, signUpButton, signOutButton,
                                                                  deleteAccountButton))
        deleteAccountButton = tkinter.Button(self.window, text="Delete account",
                                             command=lambda: self.deleteAccountMenu(signInButton, signUpButton,
                                                                                    signOutButton, deleteAccountButton))
        signOutButton = tkinter.Button(self.window, text="Log out",
                                       command=lambda: self.signOut())
        signInButton.grid(row=1, column=0)
        signUpButton.grid(row=1, column=1)
        signOutButton.grid(row=1, column=2)
        deleteAccountButton.grid(row=1, column=3)
        if self.user:
            accountLabel = tkinter.Label(self.window, text=f"Currently signed in as {self.user}")
            accountLabel.grid(row=0, column=0)

        self.window.mainloop()


def openTab(user):
    accountManager = AccountManager(user)
    accountManager.main()
    return accountManager.getUser()


if __name__ == "__main__":
    openTab("")
