# --- ATM --- #
class ATM:
    def __init__(self, atm_code, cash):
        self.__atm_code = atm_code
        # Cash Input: [100, 500, 1000]
        self.__cash = cash
        self.__total_cash = cash[0] * 100 + cash[1] * 500 + cash[2] * 1000

    def put_card_in(self, card):
        status = str(input("Please insert your card (Y/N): "))
        if status == "y" or status == "Y":
            acc = card.get_bankacc()
            pin_in = str(input("Enter your PIN: "))
            return [acc, pin_in]
        else:
            return False

    def get_total_cash(self):
        return self.__total_cash

    def set_total_cash(self):
        self.__total_cash = self.__cash[0] * 100 + self.__cash[1] * 500 + self.__cash[2] * 1000

    def get_cash(self):
        return self.__cash

    def set_cash(self, new_cash):
        self.__cash = new_cash


# --- ATM Card --- #
class ATMCard:
    def __init__(self, cardno, fname, lname, bankacc, expire):
        self.__cardno = cardno
        self.__fname = fname
        self.__lname = lname
        self.__bankacc = bankacc
        self.__expire = expire

    def get_bankacc(self):
        return self.__bankacc


# --- User --- #
class User:
    def __init__(self, fname, lname, bankacc, pin):
        self.__fname = fname
        self.__lname = lname
        # Bankaccount: [AccountNo, Amount]
        self.__bankacc = bankacc
        self.__pin = pin

    def get_fname(self):
        return self.__fname

    def get_lname(self):
        return self.__lname

    def get_bankacc(self):
        return self.__bankacc

    def set_bankacc(self, set_b):
        self.__bankacc = set_b

    def get_pin(self):
        return self.__pin


# --- BankAccount --- #
class BankAccount:
    def __init__(self, accno, remaining):
        self.__accno = accno
        self.__remaining = remaining
        """
        Transaction Type:   1 = Withdraw
                            2 = Deposit
                            3 = Transfer
        Status:     S = Success
                    U = Unsuccess
        Pattern: [Datetime, Transaction Type, Status]
        """
        self.__transaction = []

    def get_accno(self):
        return self.__accno

    def get_remaining(self):
        return self.__remaining

    def set_remaining(self, re):
        self.__remaining = re

    def get_transaction(self):
        return self.__transaction

    def add_transaction(self, tr):
        self.__transaction.append(tr)


# --- Bank --- #
class Bank:
    def __init__(self, name, bank_code):
        self.__name = name
        self.__bank_code = bank_code
        self.__my_atm = []
        self.__customer = []

    def add_atm(self, atm):
        self.__my_atm.append(atm)

    def get_atm(self):
        return self.__my_atm

    def add_customer(self, customer):
        self.__customer.append(customer)

    def get_customer(self):
        return self.__customer

    def check_vaild(self, will_check):
        if not will_check:
            print("Account Incorrect")
        else:
            for i in self.__customer:
                if i.get_bankacc().get_accno == will_check[0].get_accno:
                    if i.get_pin() == will_check[1]:
                        self.transaction(will_check[0])
                    else:
                        print("Account Incorrect")
                        break

    def transaction(self, acc):
        t = int(
            input("Select transaction:\n1. Withdraw Cash\n2. Deposit Cash\n3. Transfer Money\n4. Check Transaction"
                  "\n5. Check remaining bills\n6. Exit\ntransaction(1,2,3,4,5,6): "))
        if t < 1 or t > 6:
            print("Input Error!")
            self.transaction(acc)
        else:
            if t == 1:
                print("Available balance: " + str(acc.get_remaining()))
                withdraw = int(input("Enter amount to withdraw: "))
                if self.__my_atm[0].get_total_cash() < withdraw:
                    print("Not enough cash !!!")
                    print("Balance: " + str(acc.get_remaining()))
                    self.transaction(acc)
                else:
                    if acc.get_remaining() < withdraw:
                        print("Not enough money in your account!!!")
                        print("Balance: " + str(acc.get_remaining()))
                        self.transaction(acc)
                    else:
                        if withdraw % 100 != 0:
                            print("Invalid Input!!!")
                            print("Balance: " + str(acc.get_remaining()))
                            self.transaction(acc)
                        else:
                            acc.set_remaining(acc.get_remaining() - withdraw)
                            thousand = int(withdraw / 1000)
                            withdraw -= thousand * 1000
                            fhundred = int(withdraw / 500)
                            withdraw -= fhundred * 500
                            hundred = int(withdraw / 100)
                            self.__my_atm[0].set_cash([self.__my_atm[0].get_cash()[0] - thousand,
                                                       self.__my_atm[0].get_cash()[1] - fhundred,
                                                       self.__my_atm[0].get_cash()[2] - hundred])

                            print("Number of 1000 bills: " + str(thousand) + "\nNumber of 500 bills: " + str(fhundred) +
                                  "\nNumber of 100 bills:" + str(hundred) + "\nBalance: " + str(acc.get_remaining()))
                            acc.add_transaction(["25/4/2023", 1, "S"])
                            self.transaction(acc)

            elif t == 2:
                print("Available balance: " + str(acc.get_remaining()))
                depot = int(input("Enter 1000 bills to Deposit: "))
                depofh = int(input("Enter 500 bills to Deposit: "))
                depoh = int(input("Enter 100 bills to Deposit: "))
                depo = depot * 1000 + depofh * 500 + depoh * 100
                acc.set_remaining(acc.get_remaining() + depo)
                self.__my_atm[0].set_cash([self.__my_atm[0].get_cash()[0] + depot,
                                           self.__my_atm[0].get_cash()[1] + depofh,
                                           self.__my_atm[0].get_cash()[2] + depoh])
                acc.add_transaction(["25/4/2023", 3, "S"])
                print("Number of 1000 bills: " + str(depot) + "\nNumber of 500 bills: " + str(depofh) +
                      "\nNumber of 100 bills:" + str(depoh) + "\nBalance: " + str(acc.get_remaining()))
                print("Your deposit has been received")
                self.transaction(acc)
            elif t == 3:
                print("Available balance: " + str(acc.get_remaining()))
                trf = str(input("Enter transfer account number: "))
                dest = None
                for i in self.__customer:
                    if i.get_bankacc().get_accno() == trf:
                        dest = i
                        break
                    else:
                        pass
                if dest == None:
                    print("Don't have account!")
                    self.transaction(acc)
                else:
                    amount_trf = int(input("Enter transfer amount: "))
                    if amount_trf <= acc.get_remaining():
                        dest.get_bankacc().set_remaining(dest.get_bankacc().get_remaining() + amount_trf)
                        print("Transfer Succeeded")
                        print("Destination Remaining: " + str(dest.get_bankacc().get_remaining()))
                        print("Available balance: " + str(acc.get_remaining()))
                        self.transaction(acc)
                    else:
                        print("Not enough money in your account!!!")
                        print("Balance: " + str(acc.get_remaining()))
                        self.transaction(acc)
            elif t == 4:
                for i in acc.get_transaction():
                    print(i)
                self.transaction(acc)
            elif t == 5:
                self.__my_atm[0].set_total_cash()
                print("Remaining 100: " + str(self.__my_atm[0].get_cash()[0]) +
                      "\nRemaining 500: " + str(self.__my_atm[0].get_cash()[1]) +
                      "\nRemaining 1000: " + str(self.__my_atm[0].get_cash()[2]) +
                      "\nTotal: " + str(self.__my_atm[0].get_total_cash()))
                self.transaction(acc)
            elif t == 6:
                print("Thank you for using our service!")


# --- Instance Creation Area --- #
atm = ATM('65010604', [100, 100, 100])
bank_acc_u1 = BankAccount("65010604", 1000)
user = User("Phrit", "Nakgate", bank_acc_u1, "0604")
bank_acc_u2 = BankAccount("65010605", 0)
user2 = User("Nakgate", "Phrit", bank_acc_u2, "0605")
my_card = ATMCard("123456789", user.get_fname(), user.get_lname(), user.get_bankacc(), "25/5/2023")
bank = Bank("Thana Bank", "th001")
bank.add_atm(atm)
bank.add_customer(user)
bank.add_customer(user2)

# --- Testing Area --- #
bank.check_vaild(atm.put_card_in(my_card))
