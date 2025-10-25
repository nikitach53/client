import math
import datetime
import json

class LoanSimulator:
    """
    Симуляция различных видов кредитов: ипотека, автокредит, персональный.
    Поддержка графика платежей, досрочного погашения и анализа.
    """
    def __init__(self, principal, annual_rate, years, loan_type="mortgage"):
        self.principal = principal
        self.annual_rate = annual_rate
        self.years = years
        self.loan_type = loan_type
        self.schedule = []

    def generate_schedule(self, extra_payment=0):
        rate = self.annual_rate / 12
        n = self.years * 12
        principal = self.principal

        # Аннуитетная схема
        if rate:
            monthly = principal * (rate * math.pow(1 + rate, n)) / (math.pow(1 + rate, n) - 1)
        else:
            monthly = principal / n

        self.schedule = []
        balance = principal

        for i in range(1, n + 1):
            interest = balance * rate
            main = monthly - interest + extra_payment
            balance -= main
            self.schedule.append({
                "month": i,
                "payment": monthly + extra_payment,
                "principal": main,
                "interest": interest,
                "remaining": max(0, balance)
            })
            if balance <= 0:
                break

    def total_payments(self):
        return sum(p["payment"] for p in self.schedule)

    def total_interest_paid(self):
        return sum(p["interest"] for p in self.schedule)

    def export_schedule(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=4)
        print(f"График платежей сохранён в {filename}.")

    def print_summary(self):
        print(f"Тип кредита: {self.loan_type}")
        print(f"Сумма: {self.principal} Ставка: {self.annual_rate*100:.2f}% Срок: {self.years} лет")
        print(f"Всего выплачено: {self.total_payments():,.2f}")
        print(f"Переплата по процентам: {self.total_interest_paid():,.2f}")

if __name__ == "__main__":
    loan = LoanSimulator(3000000, 0.09, 15, "mortgage")
    loan.generate_schedule(extra_payment=2000)
    loan.print_summary()
    loan.export_schedule("loan_schedule.json")
