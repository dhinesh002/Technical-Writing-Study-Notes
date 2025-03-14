from tempMail2 import TempMail

# Initialize the TempMail object (Ensure you pass all required arguments)
tm = TempMail(login='denis', domain='gnail.pw')
help(TempMail)

# Fetch and print the mailbox
print(tm.get_mailbox())
