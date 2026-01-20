

# Lab 5: Банковские счета

Account - базовый класс:
- init(holder, balance=0) - создает счет с историей операций
- deposit(amount) - пополнение (>0), фиксирует success/fail
- withdraw(amount) - снятие с проверкой баланса  
- get_balance() - текущий баланс
- get_history() - история операций {type, amount, time, balance_after, status}

CreditAccount наследует Account:
- credit_limit - допускает отрицательный баланс до лимита
- get_available_credit() - баланс + остаток кредита
- withdraw показывает used_credit=True/False

Все операции логируются с datetime.now()

# Тест:
acc = Account("Иван", 1000)
acc.deposit(500) -> success, balance=1500
acc.withdraw(2000) -> fail (недостаточно средств)
